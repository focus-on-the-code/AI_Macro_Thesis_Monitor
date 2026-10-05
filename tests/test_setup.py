import unittest
from monitor.__main__ import hello


class SetupTest(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "AI / Macro Thesis Monitor: Phase 0 setup ready")
