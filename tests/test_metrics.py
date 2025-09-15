import json
import unittest
from app import app

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_metrics_ok(self):
        resp = self.client.get('/metrics')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data.get('status'), 'ok')
        self.assertIn('service', data)
        self.assertIn('version', data)
        self.assertIn('uptime_s', data)
        self.assertIn('routes_count', data)

if __name__ == '__main__':
    unittest.main()
