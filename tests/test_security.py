"""
Module d'exemple de test de sécurité IPCM
"""
import unittest
from app.security import User

class TestSecurity(unittest.TestCase):
    def test_create_user(self):
        user = User(username='admin', password='secret', role='admin')
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.role, 'admin')

if __name__ == '__main__':
    unittest.main()
