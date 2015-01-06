from os import (
        link,
        rename as mv,
        replace,
        makedirs,
)

import os.path

# Custom imports
from libconman.configuration import config
from libconman.database import DataCommunicator

class Vault():
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.VAULT_DIR = config['general']['conman_directory']

        # Creates the vault directory if it doesn't exist
        if not os.path.isdir(self.VAULT_DIR):
            os.mkdir(self.VAULT_DIR)

        self.db = DataCommunicator()

    def _verbose(self, msg):
        ''' Prints msg if verbose flag is set to True '''
        if self.verbose:
            print(msg)

    def _deploy(self, iid, path, name):
        ''' Creates a link at path with name from the vault file iid '''
        realpath = os.path.join(path, name)
        vaultpath = os.path.join(self.VAULT_DIR, str(iid))

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
                self._secureFile(target)
            else:
                self._secureFolder(target, recursive)

    def _secureFolder(self, target, recursive):
        if recursive:
            directory_items = os.walk(target)
        else:
            items = []
            for item in os.listdir(target):
                if os.path.isfile(os.path.join(target, item)):
                    items.append(item)

            directory_items = [(target, [], items)]

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
        _id = self.db.insertTarget(name, path) 

        if not _id:
            self._verbose('{} is already secured'.format(target))
            return

        # Create a link in the vault
        self._verbose('Linking target from origin to vault')
        link(target, os.path.join(self.VAULT_DIR, str(_id)))

        self._verbose('Securing finished')

    def remove(self, iid):
        '''
            Deletes file from vault and removes database information
        '''
        vault_file = os.path.join(self.VAULT_DIR, str(iid))

        # Removes the link from the vault
        os.remove(vault_file)

        self._verbose('Removing target information from database')
        self.db.removeTarget(iid)

        self._verbose('Remove complete')

    def deploy(self, iid):
        '''
            Links an item from the vault to the original path
        '''
        for index in iid:
            target = self.db.getTarget(index)

            if target:
                origin = os.path.join(self.VAULT_DIR, str(index))

                self._verbose('Deploying id {} from {} to {} with the name {}'
                        .format(index, origin, target['path'], target['name']))
                self._deploy(index, target['path'], target['name'])

        self._verbose('Deploy complete')

    def deployAll(self):
        '''
            Deploys all the items from the vault
        '''
        items = [i for i, n, p in self.db.listTargets()]

        self.deploy(items)

        self._verbose('Deploy all complete')

    def listTargets(self):
        '''
            Returns a list of 3-tuples containing the data of all the secured
            targets. (id, name, path)
        '''
        return self.db.listTargets()
