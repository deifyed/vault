'''
    Initializes configuration settings
    Author: Julius Pedersen <deifyed+conman@gmail.com>
'''
import configparser
import os.path

class Configuration:
    class __Configuration:
        def __init__(self):
            config = configparser.ConfigParser()
            config.read(os.path.expanduser('~/.config/conman/conman.cfg'))

            self.CONMAN_PATH = config.get('general', 'conman_directory',
                    fallback=os.path.expanduser('~/.conman'))
            self.VERBOSE = config.get('general', 'verbose',
                    fallback=False)

    instance = None

    def __init__(self):
        if not Configuration.instance:
            Configuration.instance = Configuration.__Configuration()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
