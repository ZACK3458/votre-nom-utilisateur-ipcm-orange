"""
Module d'exemple de test de sauvegarde/restauration IPCM
"""
import unittest
from app.backup import backup_data, restore_data

class TestBackup(unittest.TestCase):
    def test_backup_restore(self):
        try:
            backup_data()
            restore_data()
            result = True
        except Exception:
            result = False
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
