# Python libs
import os.path

# Custom libs
from libconman.configuration import config, verbose
from libconman.database import getDataCommunicator
from libconman.target import Target

class Vault():
    def __init__(self):
        self.VAULT_DIR = config['general']['conman_directory']

        # Creates the vault directory if it doesn't exist
        if not os.path.isdir(self.VAULT_DIR):
            os.mkdir(self.VAULT_DIR)

        self.db = getDataCommunicator()

    def _secureFolder(self, target, recursive):
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
            Saves information about a target file or a folder and proceedes to:
            moves target to the vault directory and
            links the target in the vault to the original path
        '''
        for target in targets:
            if os.path.isfile(target):
                path, name = os.path.split(target)

                target = Target(name, path)
                target.save()
                target.secure()
            else:
                targets += self._secureFolder(target, recursive)

    def remove(self, iid):
        '''
            Deletes file from vault and removes database information
        '''
        target = Target.getTarget(iid)

        target.delete()

    def deploy(self, iid):
        '''
            Links an item from the vault to the original path
        '''
        for index in iid:
            target = self.db.getTarget(index)

            if target:
                origin = os.path.join(self.VAULT_DIR, str(index))

                verbose('Deploying id {} from {} to {} with the name {}'
                        .format(index, origin, target['path'], target['name']))
                self._deploy(index, target['path'], target['name'])

        verbose('Deploy complete')

    def deployAll(self):
        '''
            Deploys all the items from the vault
        '''
        targets = [Target.getTarget(iid) for i, n, p in self.db.listTargets()]

        for target in targets:
            target.deploy()

        verbose('Deploy all complete')

    def listTargets(self):
        '''
            Returns a list of 3-tuples containing the data of all the secured
            targets. (id, name, path)
        '''
        return self.db.listTargets()
