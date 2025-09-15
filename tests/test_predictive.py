"""
Module d'exemple de test d'analyse prédictive IPCM
"""
import unittest
from app.predictive import predict_capacity

class TestPredictive(unittest.TestCase):
    def test_predict_capacity(self):
        # Test fictif, à adapter avec des données réelles
        result = predict_capacity([])
        self.assertTrue(result is None)

if __name__ == '__main__':
    unittest.main()
