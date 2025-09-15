"""
Module d'exemple de test unitaire IPCM
"""
import unittest
from app.inventory.models import Equipment, EquipmentType, NetworkDomain, SupportStatus

class TestEquipment(unittest.TestCase):
    def test_create_equipment(self):
        eq = Equipment(name='Test', type=EquipmentType.ROUTER)
        self.assertEqual(eq.name, 'Test')
        self.assertEqual(eq.type, EquipmentType.ROUTER)

    def test_create_equipment_with_string(self):
        eq = Equipment(name='Test', type='routeur')
        self.assertEqual(eq.name, 'Test')
        self.assertEqual(eq.type, EquipmentType.ROUTER)
        
    def test_equipment_to_dict(self):
        eq = Equipment(
            name='Test Router',
            type=EquipmentType.ROUTER,
            domain=NetworkDomain.BACKBONE,
            support_status=SupportStatus.ACTIVE
        )
        data = eq.to_dict()
        self.assertEqual(data['name'], 'Test Router')
        self.assertEqual(data['type'], 'routeur')
        self.assertEqual(data['domain'], 'Backbone')
        self.assertEqual(data['support_status'], 'active')
        
    def test_equipment_from_dict(self):
        data = {
            'name': 'Test Router',
            'type': 'routeur',
            'domain': 'Backbone',
            'support_status': 'active'
        }
        eq = Equipment.from_dict(data)
        self.assertEqual(eq.name, 'Test Router')
        self.assertEqual(eq.type, EquipmentType.ROUTER)
        self.assertEqual(eq.domain, NetworkDomain.BACKBONE)
        self.assertEqual(eq.support_status, SupportStatus.ACTIVE)

if __name__ == '__main__':
    unittest.main()
