import os
import os.path
import shutil
import subprocess
import unittest

from libconman.database import DataCommunicator

VAULT_PATH = os.path.join(os.getcwd(), 'TEST_VAULT')
DB_PATH = os.path.join(VAULT_PATH, '.condb')
EXTERNAL_PATH = os.path.join(os.getcwd(), 'TEST')

#####
## TODO:
##  * Deploy when folders dont exist

class TestFile:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __str__(self):
        return os.path.join(self.path, self.name)

def execute(args, verbose=False):
    cmd = [os.path.join(os.getcwd(), 'conman'), '-c', VAULT_PATH]
    if verbose: cmd.append('-v')

    cmd += args.split()
    result = subprocess.call(cmd)

def fileInVault(iid):
    return os.path.exists(os.path.join(VAULT_PATH, str(iid)))
def getId(testfile):
    db = DataCommunicator(db_path=DB_PATH)

    sql = 'select _id from items where name=? and path=?;'
    cursor = db.db.execute(sql, (testfile.name, testfile.path))

    try:
        return cursor.fetchone()[0]
    except:
        return None

class TestLevelOne(unittest.TestCase):
    '''
        Tests one directory in 
    '''
    def setUp(self):
        # Create working directories
        os.mkdir(VAULT_PATH)
        os.mkdir(EXTERNAL_PATH)

        # Prepare test files
        self.file1 = TestFile('one.cfg', EXTERNAL_PATH)
        self.file2 = TestFile('two.cfg', EXTERNAL_PATH)

        # Create first level files
        with open(str(self.file1), 'w') as f:
            f.write('one')
        with open(str(self.file2), 'w') as f:
            f.write('two')

    def tearDown(self):
        # Clean up test directories and all contents
        shutil.rmtree(VAULT_PATH)
        shutil.rmtree(EXTERNAL_PATH)

    def test_sync_first_level(self):
        ### Testing sync
        execute('sync ' + str(self.file1))
        
        iid = getId(self.file1)
        # Make sure item is added to database
        self.assertIsNotNone(iid)
        # Make sure item link is added to vault
        self.assertTrue(fileInVault(iid))

        ### Double testing sync
        execute('sync ' + str(self.file2))

        iid = getId(self.file2)
        self.assertIsNotNone(iid)
        self.assertTrue(fileInVault(iid))
    def test_sync_folder(self):
        execute('sync ' + EXTERNAL_PATH)
        
        iid = getId(self.file1)
        iid2 = getId(self.file2)

        self.assertIsNotNone(iid)
        self.assertIsNotNone(iid2)

        self.assertTrue(fileInVault(iid))
        self.assertTrue(fileInVault(iid2))

    def test_remove_first_level(self):
        ### Sync some files to remove
        execute('sync ' + str(self.file1))
        execute('sync ' + str(self.file2))

        ### Remove some synched files
        execute('remove 1')
        execute('remove 2')
        
        ### Making sure db info and vault files are gone
        self.assertFalse(fileInVault(1))
        self.assertFalse(fileInVault(2))
        self.assertIsNone(getId(self.file1))
        self.assertIsNone(getId(self.file2))

    def test_deploy_first_level(self):
        ### Sync some files to deploy
        execute('sync ' + str(self.file1))
        execute('sync ' + str(self.file2))

        ### Remove them from external dir
        os.remove(str(self.file1))
        os.remove(str(self.file2))

        ### Make sure they are gone
        self.assertFalse(os.path.exists(str(self.file1)))
        self.assertFalse(os.path.exists(str(self.file2)))

        ### Deploy them
        execute('deploy 1')
        execute('deploy 2')

        ### Make sure they are back
        self.assertTrue(os.path.exists(str(self.file1)))
        self.assertTrue(os.path.exists(str(self.file2)))

    def test_folderless_deploy(self):
        execute('sync ' + str(self.file1))
        execute('sync ' + str(self.file2))

        shutil.rmtree(EXTERNAL_PATH)

        iid = getId(self.file1)
        execute('deploy ' + str(iid))
        iid = getId(self.file2)
        execute('deploy ' + str(iid))

        self.assertTrue(os.path.exists(str(self.file1)))
        self.assertTrue(os.path.exists(str(self.file2)))

    def test_list_first_level(self):
        pass

class TestLevelTwo(unittest.TestCase):
    def setUp(self):
        ### Create first sub directory
        self.folder1 = os.path.join(EXTERNAL_PATH, 'f1')
        # Create working directories
        os.mkdir(VAULT_PATH)
        os.mkdir(EXTERNAL_PATH)
        os.mkdir(self.folder1)

        # Prepare test files
        self.file1 = TestFile('one.cfg', EXTERNAL_PATH)
        self.file2 = TestFile('two.cfg', EXTERNAL_PATH)
        self.file3 = TestFile('three.cfg', self.folder1)
        self.file4 = TestFile('four.cfg', self.folder1)

        # Create first level files
        with open(str(self.file1), 'w') as f:
            f.write('one')
        with open(str(self.file2), 'w') as f:
            f.write('two')
        with open(str(self.file3), 'w') as f:
            f.write('three')
        with open(str(self.file4), 'w') as f:
            f.write('four')

    def tearDown(self):
        # Clean up test directories and all contents
        shutil.rmtree(VAULT_PATH)
        shutil.rmtree(EXTERNAL_PATH)

    def test_sync_second_level(self):
        ### Testing sync
        execute('sync ' + str(self.file3))
        
        iid = getId(self.file3)
        # Make sure item is added to database
        self.assertIsNotNone(iid)
        # Make sure item link is added to vault
        self.assertTrue(fileInVault(iid))

        ### Double testing sync
        execute('sync ' + str(self.file4))

        iid = getId(self.file4)
        self.assertIsNotNone(iid)
        self.assertTrue(fileInVault(iid))

    def test_sync_folder_second_level(self):
        execute('sync -r ' + EXTERNAL_PATH)

        iid = getId(self.file1)
        self.assertIsNotNone(iid)
        self.assertTrue(fileInVault(iid))

        iid = getId(self.file2)
        self.assertIsNotNone(iid)
        self.assertTrue(fileInVault(iid))

        iid = getId(self.file3)
        self.assertIsNotNone(iid)
        self.assertTrue(fileInVault(iid))

        iid = getId(self.file4)
        self.assertIsNotNone(iid)
        self.assertTrue(fileInVault(iid))

    def test_remove_second_level(self):
        ### Sync some files to remove
        execute('sync ' + str(self.file3))
        execute('sync ' + str(self.file4))

        ### Remove some synched files
        execute('remove 1')
        execute('remove 2')
        
        ### Making sure db info and vault files are gone
        self.assertFalse(fileInVault(3))
        self.assertFalse(fileInVault(4))
        self.assertIsNone(getId(self.file3))
        self.assertIsNone(getId(self.file4))

    def test_deploy_second_level(self):
        ### Sync some files to deploy
        execute('sync ' + str(self.file3))
        execute('sync ' + str(self.file4))

        ### Remove them from external dir
        os.remove(str(self.file3))
        os.remove(str(self.file4))

        ### Make sure they are gone
        self.assertFalse(os.path.exists(str(self.file3)))
        self.assertFalse(os.path.exists(str(self.file4)))

        ### Deploy them
        execute('deploy 1')
        execute('deploy 2')

        ### Make sure they are back
        self.assertTrue(os.path.exists(str(self.file3)))
        self.assertTrue(os.path.exists(str(self.file4)))

    def test_folderless_deploy_second_level(self):
        execute('sync ' + str(self.file3))
        execute('sync ' + str(self.file4))

        shutil.rmtree(EXTERNAL_PATH)

        iid = getId(self.file3)
        execute('deploy ' + str(iid))
        iid = getId(self.file4)
        execute('deploy ' + str(iid))

        self.assertTrue(os.path.exists(str(self.folder1)))
        self.assertTrue(os.path.exists(str(self.file3)))
        self.assertTrue(os.path.exists(str(self.file4)))

class TestLevelThree(unittest.TestCase):
    def setUp(self):
        ### Create first sub directory
        self.folder1 = os.path.join(EXTERNAL_PATH, 'f1')
        self.folder2 = os.path.join(self.folder1, 'f2')
        # Create working directories
        os.mkdir(VAULT_PATH)
        os.mkdir(EXTERNAL_PATH)
        os.mkdir(self.folder1)
        os.mkdir(self.folder2)

        # Prepare test files
        self.file1 = TestFile('one.cfg', EXTERNAL_PATH)
        self.file2 = TestFile('two.cfg', EXTERNAL_PATH)
        self.file3 = TestFile('three.cfg', self.folder1)
        self.file4 = TestFile('four.cfg', self.folder1)
        self.file5 = TestFile('five.cfg', self.folder2)
        self.file6 = TestFile('six.cfg', self.folder2)

        # Create first level files
        with open(str(self.file1), 'w') as f:
            f.write('one')
        with open(str(self.file2), 'w') as f:
            f.write('two')
        with open(str(self.file3), 'w') as f:
            f.write('three')
        with open(str(self.file4), 'w') as f:
            f.write('four')
        with open(str(self.file5), 'w') as f:
            f.write('five')
        with open(str(self.file6), 'w') as f:
            f.write('six')

    def tearDown(self):
        # Clean up test directories and all contents
        shutil.rmtree(VAULT_PATH)
        shutil.rmtree(EXTERNAL_PATH)

    def test_sync_third_level(self):
        ### Testing sync
        execute('sync ' + str(self.file5))
        execute('sync ' + str(self.file6))
        
        iid = getId(self.file5)
        # Make sure item is added to database
        self.assertIsNotNone(iid)
        # Make sure item link is added to vault
        self.assertTrue(fileInVault(iid))

        ### Double testing sync
        execute('sync ' + str(self.file6))

        iid = getId(self.file6)
        self.assertIsNotNone(iid)
        self.assertTrue(fileInVault(iid))

    def test_sync_third_level_folders(self):
        execute('sync -r ' + EXTERNAL_PATH)

        files = [
            self.file1, self.file2, self.file3,
            self.file4, self.file5, self.file6,
        ]

        for f in files:
            iid = getId(f)
            self.assertIsNotNone(iid)
            self.assertTrue(fileInVault(iid))

    def test_remove_third_level(self):
        ### Sync some files to remove
        execute('sync ' + str(self.file5))
        execute('sync ' + str(self.file6))

        ### Remove some synched files
        execute('remove 1')
        execute('remove 2')
        
        ### Making sure db info and vault files are gone
        self.assertFalse(fileInVault(1))
        self.assertFalse(fileInVault(2))
        self.assertIsNone(getId(self.file5))
        self.assertIsNone(getId(self.file6))

    def test_deploy_third_level(self):
        ### Sync some files to deploy
        execute('sync ' + str(self.file5))
        execute('sync ' + str(self.file6))

        ### Remove them from external dir
        os.remove(str(self.file5))
        os.remove(str(self.file6))

        ### Make sure they are gone
        self.assertFalse(os.path.exists(str(self.file5)))
        self.assertFalse(os.path.exists(str(self.file6)))

        ### Deploy them
        execute('deploy 1')
        execute('deploy 2')

        ### Make sure they are back
        self.assertTrue(os.path.exists(str(self.file5)))
        self.assertTrue(os.path.exists(str(self.file6)))

    def test_folderless_deploy_third_level(self):
        execute('sync ' + str(self.file5))
        execute('sync ' + str(self.file6))

        shutil.rmtree(EXTERNAL_PATH)

        iid = getId(self.file5)
        execute('deploy ' + str(iid))
        iid = getId(self.file6)
        execute('deploy ' + str(iid))

        self.assertTrue(os.path.exists(str(self.folder2)))
        self.assertTrue(os.path.exists(str(self.file5)))
        self.assertTrue(os.path.exists(str(self.file6)))
