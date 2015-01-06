from os import (
        link,
        rename as mv,
        replace,
        makedirs,
)

import os.path
import sqlite3

VAULT_DIR = os.path.expanduser('~') + '/.sault/'
DB_PATH = VAULT_DIR + '.saultdb'

# Tables
TABLE_ITEMS = 'items'

class Vault():
    def __init__(self, verbose=False):
        self.verbose = verbose

        # Creates the vault directory if it doesn't exist
        if not os.path.isdir(VAULT_DIR):
            os.mkdir(VAULT_DIR)

        self.db = self._getDatabase()

    def _verbose(self, msg):
        ''' Prints msg if verbose flag is set to True '''
        if self.verbose:
            print(msg)

    def _getDatabase(self):
        '''
            Returns a sqlite3 database object.
            Creates new and initializes if file didn't exist
        '''
        sql = None

        if not os.path.isfile(DB_PATH):
            sql = '''create table if not exists {} (
                _id integer primary key autoincrement,
                name varchar(254),
                path varchar(254),
                UNIQUE(name, path)
            );'''.format(TABLE_ITEMS)
        
        db = sqlite3.connect(DB_PATH)

        if sql:
            db.execute(sql)

        return db

    def _getTarget(self, iid):
        ''' Returns a dictionary containing information about a certain target '''
        self._verbose('Fetching information about target {} from database'.format(iid))
        sql = '''select name, path from {} where _id=?'''.format(TABLE_ITEMS)
        name, path = self.db.execute(sql, (iid,)).fetchone()

        return {'name':name, 'path':path}

    def _deploy(self, iid, path, name):
        ''' Creates a link at path with name from the vault file iid '''
        realpath = os.path.join(path, name)
        vaultpath = VAULT_DIR + str(iid)

        if not os.path.exists(path):
            makedirs(path)

        link(vaultpath, realpath)

    def secure(self, targets, recursive):
        '''
            Saves information about a target file or a folder and proceedes to:
            moves target to the vault directory and
            links the target in the vault to the original path
        '''
        for target in targets:
            if os.path.isfile(target):
                self._secureFile(self, target)
            else:
                self._secureFolder(target, recursive)

    def _secureFolder(self, target, recursive):
        if recursive:
            directory_items = os.walk(target)
        else:
            directory_items = [target, [], os.listdir(target)]

        for dir_name, folders, files in directory_items:
            for f in files:
                self._secureFile(os.path.join(dir_name, f))


    def _secureFile(self, target):
        # Get path information
        target = os.path.realpath(target)
        # Extract and seperate path and name of target
        path, name = os.path.split(target)

        # Save information about the target into the database
        self._verbose('Entering target {} into database'.format(target))
        sql = '''insert into {}(name, path) values (?,?);'''.format(TABLE_ITEMS)
        try:
            _id = self.db.execute(sql, (name, path)).lastrowid
            self.db.commit()
            self._verbose('Database commit successful')
        except sqlite3.IntegrityError:
            self._verbose('{} is already secured'.format(target))

        if not _id:
            return

        # Create a link in the vault
        self._verbose('Linking target from vault to origin')
        link(target, os.path.join(VAULT_DIR, str(_id)))

        self._verbose('Securing finished')

    def remove(self, iid):
        '''
            Deletes file from vault and removes database information
        '''
        target = self._getTarget(iid)
        vault_file = VAULT_DIR + str(iid)

        # Removes the link from the vault
        os.remove(vault_file)

        self._verbose('Removing target information from database')
        sql = '''delete from {} where _id=?'''.format(TABLE_ITEMS)
        self.db.execute(sql, (iid,))
        self.db.commit()

        self._verbose('Remove complete')

    def deploy(self, iid):
        '''
            Links an item from the vault to the original path
        '''
        for index in iid:
            target = self._getTarget(index)
            origin = VAULT_DIR + str(index)

            self._verbose('Deploying id {} from {} to {} with the name {}'
                    .format(index, origin, target['path'], target['name']))
            self._deploy(index, target['path'], target['name'])

        self._verbose('Deploy complete')
    def deployAll(self):
        '''
            Deploys all the items from the vault
        '''
        items = self.list()

        for iid, name, path in items:
            self.deploy(iid)

        self._verbose('Deploy all complete')

    def list(self):
        '''
            Returns a list of all the items secured in the vault
        '''
        sql = 'select * from {}'.format(TABLE_ITEMS)
        cursor = self.db.execute(sql)

        return [(iid, name, path) for iid, name, path in cursor]
