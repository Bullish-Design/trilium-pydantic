#!/usr/bin/env python3
"""Run tests using UV's testing framework."""
# /// script
# dependencies = [
#   "pytest>=7.0.0",
#   "pytest-cov>=4.0.0",
#   "pydantic>=2.5.0",
#   "httpx>=0.25.0",
#   "python-dotenv>=1.0.0",
#   "structlog>=23.0.0",
#   "rich>=13.0.0",
# ]
# ///

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run pytest with UV."""
    # Add src to Python path
    src_path = Path(__file__).parent / "src"
    
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        f"--pythonpath={src_path}",
    ]
    
    # Add coverage if requested
    if "--cov" in sys.argv:
        cmd.extend([
            "--cov=src/trilium_pydantic",
            "--cov-report=term-missing",
        ])
    
    # Add integration tests if configured
    if "--integration" in sys.argv:
        cmd.append("-m")
        cmd.append("integration")
    
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    sys.exit(run_tests())
