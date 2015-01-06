# Python libs
import os.path

# Custom libs
from libconman.database import getDataCommunicator
from libconman.configuration import config, verbose

class Target():
    def getTarget(iid):
        db = getDataCommunicator()

        verbose('Loading target with id {}'.format(iid))
        data = db.getTarget(iid)

        if data:
            verbose('Found target')
            return Target(data['name'], data['path'], _id=iid)
        
        verbose('Could not find target belonging to id {}'.format(iid))
        return data

    def __init__(self, name, path, _id=-1):
        self.name = name
        self.path = path
        self.real_path = os.path.join(path, name)
        self._vault_path = None
        self._id = _id

        self.db = getDataCommunicator()

    @property
    def vault_path(self):
        if self._id == -1:
            return None
        if not self._vault_path:
            self._vault_path = os.path.join(config['general']['conman_path'],
                    str(self._id))

        return self._vault_path 

    def delete(self):
        '''
            Deletes file from vault and removes database information
        '''
        if not self._id:
            verbose('This target does not have an id')
            return False

        # Removes link from vault directory
        verbose('Removing link from vault directory')
        os.remove(self.vault_path)

        verbose('Removing information from database')
        # Removing information from database
        self.db.removeTarget(self._id) 
        self._id = -1

        return True

    def secure(self):
        '''
            Creates a hard link to the target file in the vault directory
            and saves information about the target file in the database
        '''
        verbose('Saving information about target into conman database')
        self._id = self.db.insertTarget(self.name, self.path)

        verbose('Creating a hard link from {} to {} directory'.format(
            str(self), config['general']['conman_directory']   
        ))
        self.deploy()

    def deploy(self):
        '''
            Creates a link at the original path of this target
        '''
        if not os.path.exists(self.path):
            makedirs(self.path)

        link(self.vault_path, self.real_path)
