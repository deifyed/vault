import os.path
import unittest
from libconman.target import Target

class TestTarget(unittest.TestCase):
    def setUp(self):
        pass

    def test_creation(self):
        name, path = 'file.cfg', '/path/'
        t1 = Target(name, path)

        self.assertEqual(t1.name, name)
        self.assertEqual(t1.path, path)
        self.assertEqual(t1._id, -1)
        self.assertEqual(t1.real_path, os.path.join(path, name))
        self.assertIsNone(t1.vault_path)
