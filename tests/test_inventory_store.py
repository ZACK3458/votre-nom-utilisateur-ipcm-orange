import os
import tempfile
import json
import unittest
from app.inventory import store

class TestInventoryStore(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.inv_path = os.path.join(self.tmpdir.name, 'inv.json')
        os.environ['IPCM_INVENTORY_PATH'] = self.inv_path
        # reset cache by reloading module functions if needed

    def tearDown(self):
        self.tmpdir.cleanup()
        os.environ.pop('IPCM_INVENTORY_PATH', None)

    def test_crud(self):
        items = store.load_inventory()
        self.assertEqual(items, [])
        a = store.add_equipment({'name':'R1','type':'Router'})
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
