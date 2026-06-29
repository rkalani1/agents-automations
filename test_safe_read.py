import os
import sys
import pathlib

os.environ["OPERATOR_APPROVED_TO_RUN"] = "1"
os.environ["OPENAI_API_KEY"] = "dummy"

# Mock SANDBOX_DIR
sys.path.insert(0, str(pathlib.Path("./starter-kits/local-script-agent").resolve()))
from script import safe_read, SANDBOX_DIR

def test_safe_read_vulnerability():
    # Attempt to read a sibling directory like `sandbox2`
    # E.g., if SANDBOX_DIR is /path/to/sandbox
    # An attacker could try to read /path/to/sandbox2/secret.txt

    # In our case we create a dummy file in a dummy sibling dir
    sibling_dir = SANDBOX_DIR.parent / (SANDBOX_DIR.name + "2")
    sibling_dir.mkdir(exist_ok=True)
    secret_file = sibling_dir / "secret.txt"
    secret_file.write_text("this is secret")

    try:
        content = safe_read(secret_file)
        print("VULNERABILITY STILL EXISTS! Read content:", content)
        sys.exit(1)
    except PermissionError:
        print("Vulnerability fixed: PermissionError raised as expected when accessing sibling dir.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        secret_file.unlink(missing_ok=True)
        try:
            sibling_dir.rmdir()
        except:
            pass

if __name__ == "__main__":
    test_safe_read_vulnerability()
