from datetime import datetime, timezone
import unittest
import sys
from loader.split_loader import read_all_splits
import os
sys.path.append("../../..")



class TestSPlitLoader(unittest.TestCase):
    def test_read_splits(self):
        ruta_ejemplo_fichero_splits = os.path.join(os.path.dirname(__file__),'..', 'data', 'test_splits','split.json')

        splits = read_all_splits(ruta_ejemplo_fichero_splits)
        self.assertEqual("ISIN1_2023_12",splits[0].id, "Id should match expectated value")
        self.assertEqual("ISIN1",splits[0].isin, "isin should expectated value")
        dt = datetime.strptime("2023-12-18T10:20:26.000Z", "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        self.assertEqual(dt, splits[0].fecha, "dates should match")
        self.assertEqual(1,splits[0].numOriginal, "numOriginal should expectated value")
        self.assertEqual(10,splits[0].numDestino, "numDestino should expectated value")