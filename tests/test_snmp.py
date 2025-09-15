"""
Module d'exemple de test SNMP IPCM
"""
import unittest
from app.snmp.collector import collect_interface_data

class TestSNMP(unittest.TestCase):
    def test_snmp_collect(self):
        # Test fictif, à adapter avec un vrai équipement
        result = collect_interface_data('127.0.0.1', 'public', '1.3.6.1.2.1.1.1.0')
        self.assertTrue(result is None or isinstance(result, dict))

if __name__ == '__main__':
    unittest.main()
