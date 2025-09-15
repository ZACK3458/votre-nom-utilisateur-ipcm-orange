"""
Module d'exemple de test d'alertes IPCM
"""
import unittest
from app.alerts import send_alert

class TestAlerts(unittest.TestCase):
    def test_send_alert(self):
        try:
            send_alert('Test alerte', 'warning')
            result = True
        except Exception:
            result = False
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
