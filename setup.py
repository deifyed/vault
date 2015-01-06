from distutils.core import setup

long_description = '''
It creates a hard link of the target file inside ~/.sault and saves the path of
the target. This way you can version control or rsync ~/.sault and deploy these
files if needed later (after a format or if they accidentaly gets deleted).'''

info = {
    'name':'sault',
    'version':'1.0.0b1',
    'description':'Securing files into one folder for easy backup',
    'long_description':long_description,
    'url':'https://github.com/deifyed/vault',
    'author':'Julius Pedersen',
    'author_email':'deifyed+sault@gmail.com',
    'license':'GNU GPLv3',
    'packages':['libsault',],
    'scripts':['sault'],
    'keywords':'backup',
}

setup(**info)
