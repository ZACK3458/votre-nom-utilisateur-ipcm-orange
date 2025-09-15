"""
Module d'exemple de test du dashboard IPCM
"""
import unittest
from app.dashboard.routes import dashboard

class TestDashboard(unittest.TestCase):
    def test_dashboard_route(self):
        # Test fictif, à adapter avec le client Flask
        self.assertTrue(callable(dashboard))

if __name__ == '__main__':
    unittest.main()
