"""
Module d'exemple de test de conformité IPCM
"""
import unittest
from app.compliance import check_compliance

class TestCompliance(unittest.TestCase):
    def test_check_compliance(self):
        try:
            check_compliance()
            result = True
        except Exception:
            result = False
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
