"""The code-flow report must match the code. Fix: python docs/code-flow/tools/codeflow.py build"""

import subprocess
import sys
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "docs/code-flow/tools" / "codeflow.py"


class CodeFlowReportIsCurrent(unittest.TestCase):
    def test_report_matches_code(self):
        run = subprocess.run(
            [sys.executable, str(TOOL), "check"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()
