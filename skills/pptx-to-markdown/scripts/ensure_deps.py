"""Ensure required dependencies are installed."""
from __future__ import annotations

import subprocess
import sys

REQUIRED_PACKAGES = {
    "pptx": "python-pptx",
}


def ensure_dependencies() -> None:
    """Check and install missing dependencies."""
    missing: list[str] = []
    for import_name, pip_name in REQUIRED_PACKAGES.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pip_name)

    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *missing],
            stdout=subprocess.DEVNULL,
        )
        print("Dependencies installed successfully.")


if __name__ == "__main__":
    ensure_dependencies()
