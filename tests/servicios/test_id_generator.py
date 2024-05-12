import unittest
from servicios.id_generator import gen_id


class TestIdGenerator(unittest.TestCase):
    def test_id_gen(self):
        ids = set()
        for i in range (1000):
            new_id = gen_id()
            self.assertTrue(new_id not in ids)
            ids.add(new_id)
