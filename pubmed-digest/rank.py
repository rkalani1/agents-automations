"""Transparent, fully-explainable relevance scoring.

There is deliberately **no machine learning** here. Every point a record earns
is traceable to a line in ``config.yaml`` and recorded in ``record.score_breakdown``
so a human reviewer can audit exactly why a paper ranked where it did.

Score components (all weights config-driven under ``ranking.weights``):

  * title_keyword   -- topic keyword found in the title       (high signal)
  * abstract_keyword-- topic keyword found in the abstract     (lower signal)
  * mesh_match      -- topic MeSH term present on the record
  * boost_term      -- a globally high-value phrase (e.g. "randomized controlled trial")
  * recency         -- exponential decay from the publication date
  * journal_tier    -- flat boost based on the journal's configured tier

Total score = sum of the above. Records whose score meets
``ranking.needs_review_threshold`` are flagged ``needs_review = True``.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from config import get_logger
from models import Record

log = get_logger(__name__)


def _today() -> date:
    return datetime.utcnow().date()


def _parse_iso(d: str) -> date | None:
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _count_keyword_hits(text: str, keywords: list[str]) -> list[str]:
    """Return the list of keywords (case-insensitive substring) found in *text*."""
    if not text or not keywords:
        return []
    lowered = text.lower()
    return [kw for kw in keywords if kw.lower() in lowered]


def _recency_points(pub_date: str, max_points: float, halflife_days: float, today: date) -> float:
    """Exponential decay: full points today, halved every ``halflife_days``.

    Papers with no parseable date earn zero recency points (never invented).
    """
    parsed = _parse_iso(pub_date)
    if parsed is None or halflife_days <= 0:
        return 0.0
    age_days = max((today - parsed).days, 0)
    return round(max_points * (0.5 ** (age_days / halflife_days)), 3)


def _journal_tier_points(journal: str, tiers: dict[str, list[str]]) -> tuple[float, str | None]:
    """Return (points, tier_label) for the journal, matching case-insensitively.

    ``tiers`` maps a numeric point value (as a string key) to a list of journal
    name fragments, e.g. ``{"5": ["N Engl J Med", "Lancet"], "3": [...]}.``
    """
    if not journal:
        return 0.0, None
    jlower = journal.lower()
    best_points = 0.0
    best_label: str | None = None
    for points_str, names in tiers.items():
        for name in names:
            if name.lower() in jlower:
                pts = float(points_str)
                if pts > best_points:
                    best_points = pts
                    best_label = name
    return best_points, best_label


def score_record(record: Record, ranking: dict[str, Any], today: date | None = None) -> Record:
    """Compute and attach a transparent relevance score to *record*.

    Mutates and returns the record (sets ``score``, ``score_breakdown``,
    ``matched_keywords``, ``needs_review``). Pure given the same inputs +
    ``today``, which is injectable for deterministic tests.
    """
    today = today or _today()
    weights = ranking.get("weights", {})
    recency_cfg = ranking.get("recency", {})

    # Topic-level keyword/mesh lists are attached to the record's topic config
    # by the caller via ``record.matched_keywords`` seeding is NOT used here;
    # instead keywords come through the ranking call. We read them off the
    # ranking dict's per-call injected fields.
    keywords: list[str] = ranking.get("_active_keywords", [])
    mesh_targets: list[str] = ranking.get("_active_mesh", [])
    boost_terms: dict[str, float] = ranking.get("boost_terms", {})

    breakdown: dict[str, float] = {}
    matched: list[str] = []

    # --- Title keyword hits ---
    title_hits = _count_keyword_hits(record.title, keywords)
    if title_hits:
        pts = len(title_hits) * float(weights.get("title_keyword", 3.0))
        breakdown["title_keyword"] = round(pts, 3)
        matched.extend(title_hits)

    # --- Abstract keyword hits (don't double-count title hits) ---
    abstract_hits = _count_keyword_hits(record.abstract, keywords)
    abstract_only = [k for k in abstract_hits if k not in title_hits]
    if abstract_only:
        pts = len(abstract_only) * float(weights.get("abstract_keyword", 1.0))
        breakdown["abstract_keyword"] = round(pts, 3)
        matched.extend(abstract_only)

    # --- MeSH term matches ---
    if mesh_targets and record.mesh_terms:
        record_mesh_lower = {m.lower() for m in record.mesh_terms}
        mesh_hits = [m for m in mesh_targets if m.lower() in record_mesh_lower]
        if mesh_hits:
            pts = len(mesh_hits) * float(weights.get("mesh_match", 2.5))
            breakdown["mesh_match"] = round(pts, 3)
            matched.extend(mesh_hits)

    # --- Global boost terms (e.g., study designs) ---
    haystack = f"{record.title}\n{record.abstract}".lower()
    boost_total = 0.0
    for term, weight in boost_terms.items():
        if term.lower() in haystack:
            boost_total += float(weight)
    if boost_total:
        breakdown["boost_term"] = round(boost_total, 3)

    # --- Recency ---
    recency_pts = _recency_points(
        record.date,
        max_points=float(recency_cfg.get("max_points", 6.0)),
        halflife_days=float(recency_cfg.get("halflife_days", 14)),
        today=today,
    )
    if recency_pts:
        breakdown["recency"] = recency_pts

    # --- Journal tier ---
    tier_pts, tier_label = _journal_tier_points(record.journal, ranking.get("journal_tiers", {}))
    if tier_pts:
        breakdown["journal_tier"] = round(tier_pts, 3)

    total = round(sum(breakdown.values()), 3)
    record.score = total
    record.score_breakdown = breakdown
    # Preserve order, drop duplicates.
    record.matched_keywords = list(dict.fromkeys(matched))
    record.needs_review = total >= float(ranking.get("needs_review_threshold", 14.0))
    return record


def rank_records(
    records: list[Record],
    ranking: dict[str, Any],
    topic_keywords: list[str],
    topic_mesh: list[str],
    today: date | None = None,
) -> list[Record]:
    """Score a list of records for one topic and return them sorted high->low.

    The topic's keyword and MeSH lists are injected into a per-call copy of the
    ranking config so ``score_record`` stays a pure function of its arguments.
    """
    call_ranking = dict(ranking)
    call_ranking["_active_keywords"] = topic_keywords
    call_ranking["_active_mesh"] = topic_mesh

    for rec in records:
        score_record(rec, call_ranking, today=today)

    ranked = sorted(records, key=lambda r: r.score, reverse=True)
    log.info(
        "Ranked %d records; %d flagged needs_review",
        len(ranked),
        sum(1 for r in ranked if r.needs_review),
    )
    return ranked
