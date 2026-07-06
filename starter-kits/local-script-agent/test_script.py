import os
import unittest
import tempfile
import pathlib

# Set required environment variables for safe import
os.environ["OPERATOR_APPROVED_TO_RUN"] = "1"
os.environ["OPENAI_API_KEY"] = "sk-dummy"

# Import the script
from script import read_note_files, SANDBOX_DIR

class TestReadNoteFiles(unittest.TestCase):
    def setUp(self):
        # Create a temporary sandbox directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_sandbox = pathlib.Path(self.temp_dir.name)

        # We need to temporarily patch SANDBOX_DIR in the script module
        import script
        self.original_sandbox = script.SANDBOX_DIR
        script.SANDBOX_DIR = self.temp_sandbox

        self.notes_dir = self.temp_sandbox / "notes"
        self.notes_dir.mkdir()

    def tearDown(self):
        import script
        script.SANDBOX_DIR = self.original_sandbox
        self.temp_dir.cleanup()

    def test_read_happy_path(self):
        # Create valid notes
        file1 = self.notes_dir / "note1.txt"
        file1.write_text("Hello World", encoding="utf-8")
        file2 = self.notes_dir / "note2.md"
        file2.write_text("Markdown **bold**", encoding="utf-8")

        notes = [file1, file2]

        combined, warnings = read_note_files(notes)

        self.assertIn("--- note1.txt ---", combined)
        self.assertIn("Hello World", combined)
        self.assertIn("--- note2.md ---", combined)
        self.assertIn("Markdown **bold**", combined)
        self.assertEqual(len(warnings), 0)

    def test_permission_error_outside_sandbox(self):
        # Create a file outside the temporary sandbox
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"Outside data")
            outside_file = pathlib.Path(tf.name)

        try:
            combined, warnings = read_note_files([outside_file])

            self.assertEqual(combined, "")
            self.assertEqual(len(warnings), 1)
            self.assertIn("Attempted to read outside sandbox", warnings[0])
        finally:
            os.unlink(outside_file)

    def test_file_not_found(self):
        # Non-existent file in the sandbox
        non_existent = self.notes_dir / "does_not_exist.txt"

        combined, warnings = read_note_files([non_existent])

        self.assertEqual(combined, "")
        self.assertEqual(len(warnings), 1)
        self.assertIn("Skipped does_not_exist.txt", warnings[0])

    def test_empty_list(self):
        combined, warnings = read_note_files([])
        self.assertEqual(combined, "")
        self.assertEqual(warnings, [])

if __name__ == "__main__":
    unittest.main()
