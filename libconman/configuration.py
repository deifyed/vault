'''
    Initializes configuration settings
    Author: Julius Pedersen <deifyed+conman@gmail.com>
'''
import configparser
import os.path

### Creating the config parser
__CONFIG = configparser.ConfigParser()
# Get user settings
__CONFIG.read([
    os.path.expanduser('~/.config/conman'),
])

### General settings
# Conman root directory
CONMAN_PATH = __CONFIG.get('general', 'conman_directory',
        fallback=os.path.expanduser('~/.conman'))
# Verbose setting
VERBOSE = __CONFIG.get('general', 'verbose',
        fallback=False)

### Database settings
DATABASE_PATH = __CONFIG.get('database', 'path',
        fallback=os.path.join(CONMAN_PATH, '.condb'))
