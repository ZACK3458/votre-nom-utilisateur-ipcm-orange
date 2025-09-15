import os
import tempfile
import json
import unittest
from app.inventory import store

class TestInventoryStore(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.inv_path = os.path.join(self.tmpdir.name, 'inv.json')
        # Set environment variable before importing store module
        os.environ['IPCM_INVENTORY_PATH'] = self.inv_path
        # Update the module's path
        store.INVENTORY_PATH = self.inv_path
        
        # Create empty inventory file
        with open(self.inv_path, 'w') as f:
            json.dump([], f)

    def tearDown(self):
        self.tmpdir.cleanup()
        os.environ.pop('IPCM_INVENTORY_PATH', None)

    def test_crud(self):
        items = store.load_inventory()
        self.assertEqual(items, [])
        a = store.add_equipment({'name':'R1','type':'routeur'})  # Use 'routeur' which is valid
        self.assertTrue(a['id'] >= 1)
        ok = store.update_equipment(a['id'], {'brand':'Cisco'})
        self.assertTrue(ok)
        items = store.load_inventory()
        self.assertEqual(items[0]['brand'], 'Cisco')
        ok = store.delete_equipment(a['id'])
        self.assertTrue(ok)
        self.assertEqual(store.load_inventory(), [])

if __name__ == '__main__':
    unittest.main()
