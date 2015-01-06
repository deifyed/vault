# Python libs
import os.path
import sqlite3

# Custom libs
from libconman.configuration import config

__DATA_COMMUNICATOR = None

class DataCommunicator():
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.TABLE_ITEMS = 'items'

        sql = None

        if not os.path.isfile(config['database']['path']):
            sql = '''create table if not exists {} (
                _id integer primary key autoincrement,
                name varchar(254),
                path varchar(254),
                UNIQUE(name, path)
            );'''.format(self.TABLE_ITEMS)

        self.db = sqlite3.connect(config['database']['path'])

        if sql:
            self.db.execute(sql)

    def getTarget(self, iid):
        '''
            Returns a dictionary containing information about a certain target
        '''
        #_verbose('Fetching information about target {} from database'.format(iid)
        sql = 'select name, path from {} where _id=?'.format(self.TABLE_ITEMS)
        data = self.db.execute(sql, (iid,)).fetchone()

        if data:
            return {'name': data[0], 'path': data[1]}

        return None

    def insertTarget(self, name, path):
        '''
            Inserts a new target into the vault database
            Returns the id of the created target
        '''
        sql = 'insert into {}(name, path) values (?,?);'.format(self.TABLE_ITEMS)

        try:
            _id = self.db.execute(sql, (name, path)).lastrowid
            self.db.commit()

            return _id
        except sqlite3.IntegrityError:
            return None

    def removeTarget(self, iid):
        '''
            Removes target information from vault database
        '''
        sql = 'delete from {} where _id=?'.format(self.TABLE_ITEMS)
        self.db.execute(sql, (iid,))
        self.db.commit()

    def listTargets(self):
        '''
            Returns a list of all the items secured in the vault
        '''
        sql = 'select * from {}'.format(self.TABLE_ITEMS)
        cursor = self.db.execute(sql)

        return [(iid, name, path) for iid, name, path in cursor]

def getDataCommunicator():
    global __DATA_COMMUNICATOR

    if not __DATA_COMMUNICATOR:
        __DATA_COMMUNICATOR = DataCommunicator()

    return __DATA_COMMUNICATOR
