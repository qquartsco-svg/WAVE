from __future__ import annotations
import subprocess, sys
from pathlib import Path

def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    run([sys.executable, "scripts/verify_package_identity.py"], root)
    run([sys.executable, "scripts/verify_signature.py"], root)
    run([sys.executable, "-m", "pytest", "-q", "tests"], root)
    print("OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
