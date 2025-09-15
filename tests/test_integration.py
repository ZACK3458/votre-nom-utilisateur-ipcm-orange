"""
Module d'exemple de test d'intégration réseau IPCM
"""
import unittest
from app.integration import integrate_with_network

class TestIntegration(unittest.TestCase):
    def test_integrate_with_network(self):
        try:
            integrate_with_network()
            result = True
        except Exception:
            result = False
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
