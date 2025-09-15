"""
Module d'exemple de test unitaire IPCM
"""
import unittest
from app.inventory.models import Equipment

class TestEquipment(unittest.TestCase):
    def test_create_equipment(self):
        eq = Equipment(name='Test', type='router')
        self.assertEqual(eq.name, 'Test')
        self.assertEqual(eq.type, 'router')

if __name__ == '__main__':
    unittest.main()
