"""
Module d'exemple de test de reporting IPCM
"""
import unittest
from app.reporting import export_inventory_to_excel

class TestReporting(unittest.TestCase):
    def test_export_excel(self):
        # Test fictif, à adapter avec des données réelles
        try:
            export_inventory_to_excel('test_inventory.xlsx')
            result = True
        except Exception:
            result = False
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
