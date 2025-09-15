import unittest
from app import app

class TestInventoryExports(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_export_csv(self):
        resp = self.client.get('/inventory/export.csv')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('text/csv', resp.mimetype)

    def test_export_xlsx(self):
        resp = self.client.get('/inventory/export.xlsx')
        # could be 200 if openpyxl installed, or 503 if not
        self.assertIn(resp.status_code, (200, 503))

if __name__ == '__main__':
    unittest.main()
