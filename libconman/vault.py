'''
    The core of conman. Connects all the different parts of conman.
    Author: Julius Pedersen <deifyed+conman@gmail.com>
'''
# Python libs
import os.path

# Custom libs
from libconman import configuration as conf, verbose
from libconman.database import getDataCommunicator
from libconman.target import Target

class Vault():
    def __init__(self):
        self.VAULT_DIR = conf.CONMAN_PATH 

        # Creates the vault directory if it doesn't exist
        if not os.path.isdir(self.VAULT_DIR):
            os.mkdir(self.VAULT_DIR)

        self.db = getDataCommunicator()

    def _fetchFilesFromFolder(self, target, recursive):
        '''
            Fetches files from the target directory, and - if recursive
            mode is on, all subdirectories.

            Returns a list of all found files
        '''
        directory_items = os.walk(target)

        # If recursive is false, fetch only the first tuple
        if not recursive:
            directory_items = [next(directory_items)]

        targets = []
        for dir_name, folders, files in directory_items:
            for f in files:
                targets.append(os.path.join(dir_name, f))

        return targets

    def secure(self, targets, recursive):
        '''
            Saves information about each target file and/or folder and
            creates a hard link from the file(s) to the vault directory
        '''
        for target in targets:
            if os.path.isfile(target):
                path, name = os.path.split(os.path.realpath(target))

                target = Target(name, path)
                target.secure()
            else:
                targets += self._fetchFilesFromFolder(target, recursive)

    def remove(self, iid):
        '''
            Deletes file from vault and removes database information
        '''
        target = Target.getTarget(iid)

        return target.delete()

    def deploy(self, iid):
        '''
            Links an item from the vault to the original path
        '''
        for index in iid:
            target = Target.getTarget(index)

            if target:
                verbose('Deploying id {} from {} to {} with the name {}'
                        .format(index, target.vault_path, target.path, target.name))
                target.deploy()

        verbose('Deploy complete')

    def deployAll(self):
        '''
            Deploys all the items from the vault. Useful after a format
        '''
        targets = [Target.getTarget(iid) for iid, n, p in self.db.listTargets()]

        for target in targets:
            target.deploy()

        verbose('Deploy all complete')

    def listTargets(self):
        '''
            Returns a list of 3-tuples containing the data of all the secured
            targets. (id, name, path)
        '''
        return self.db.listTargets()
