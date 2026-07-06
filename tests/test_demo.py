#!/usr/bin/env python3
"""Smoke test for the -stra ecosystem demo. Skips if a sibling platform repo is absent."""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
_MISSING = [r for r in ("Routestra", "Clearstra", "Certstra", "Attestra")
            if not os.path.isdir(os.path.join(HERE, "..", r))]


@unittest.skipIf(_MISSING, f"sibling platform repos absent: {_MISSING}")
class TestEcosystemDemo(unittest.TestCase):
    def setUp(self):
        import demo
        self.r = demo.run_demo()

    def test_four_stages(self):
        names = [s[0].split(" ")[0] for s in self.r["steps"]]
        self.assertEqual(names, ["route", "clear", "certify", "attest"])

    def test_ecosystem_verdict_valid(self):
        self.assertEqual(self.r["ecosystem_verdict"], "valid")

    def test_attestation_issued(self):
        self.assertIsNotNone(self.r["attestation"])
        self.assertEqual(self.r["attestation"]["grade"], "full")

    def test_severity_alignment(self):
        import demo
        self.assertEqual(demo._sev("compliant"), demo._sev("valid"))
        self.assertEqual(demo._sev("certifiable"), demo._sev("valid"))
        self.assertEqual(demo._sev("blocked"), demo._sev("breach"))


if __name__ == "__main__":
    unittest.main()
