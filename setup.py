from distutils.core import setup

long_description = '''
It creates a hard link of the target file inside ~/.conman and saves the path of
the target. This way you can version control or rsync ~/.conman and deploy these
files if needed later (after a format or if they accidentaly gets deleted).'''

info = {
    'name':'conman',
    'version':'1.0.0b1',
    'description':'Securing files into one folder for easy backup',
    'long_description':long_description,
    'url':'https://github.com/deifyed/vault',
    'author':'Julius Pedersen',
    'author_email':'deifyed+conman@gmail.com',
    'license':'GNU GPLv3',
    'packages':['libconman',],
    'scripts':['conman'],
    'keywords':'backup',
}

setup(**info)
