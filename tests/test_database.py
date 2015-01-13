# Python libs
import os
import unittest

# Custom libs
from libconman.database import DataCommunicator

PATH = 'testdb'

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = DataCommunicator(db_path=PATH)

        self.entry1 = {
            'id': 1,
            'name': 'file1.cfg',
            'path': '/path1/',
        }

        self.entry2 = {
            'id': 2,
            'name': 'file2.cfg',
            'path': '/path2/',
        }

    def test_insert(self):
        _id = self.db.insertTarget(self.entry1['name'], self.entry1['path'])
        self.assertEqual(_id, self.entry1['id'])

        _id = self.db.insertTarget(self.entry2['name'], self.entry2['path'])
        self.assertEqual(_id, self.entry2['id'])

        # Should not work. Entry1 is already in the database
        _id = self.db.insertTarget(self.entry1['name'], self.entry1['path'])
        self.assertIsNone(_id)

    def test_select(self):
        # Insert data for testing
        _id = self.db.insertTarget(self.entry1['name'], self.entry1['path'])
        _id = self.db.insertTarget(self.entry2['name'], self.entry2['path'])

        target1 = self.db.getTarget(self.entry1['id'])
        self.assertEqual(target1['name'], self.entry1['name'])
        self.assertEqual(target1['path'], self.entry1['path'])

        target2 = self.db.getTarget(self.entry2['id'])
        self.assertEqual(target2['name'], self.entry2['name'])
        self.assertEqual(target2['path'], self.entry2['path'])

        # Should return None. Grabbing value which isnt there
        target3 = self.db.getTarget(3)
        self.assertIsNone(target3)

    def test_delete(self):
        _id = self.db.insertTarget(self.entry1['name'], self.entry1['path'])
        _id = self.db.insertTarget(self.entry2['name'], self.entry2['path'])

        modified = self.db.removeTarget(self.entry1['id'])
        self.assertTrue(modified)

        modified = self.db.removeTarget(self.entry2['id'])
        self.assertTrue(modified)

        modified = self.db.removeTarget(3)
        self.assertFalse(modified)

    def tearDown(self):
        os.remove(PATH)
