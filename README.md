vault
=====

Convenient way to store all your files(read configs) and folders(read containers containing alot of configs) in one folder for version controll.

How it works?
=====

It creates a hard link of the target file inside ~/.vault and saves the path of the target. This way you can version control or rsync ~/.vault and deploy these files if needed later (after a format or if they accidentaly gets deleted).

Usage
=====

vault --secure file.cfg Creates a link of file.cfg inside ~/.vault
vault --recursive --secure folder Creates a link for the files inside folder and subfolders of folder inside ~/.vault 
vault --deploy id Creates a link from ~/.vault/id to where the original file was placed
vault --list Lists all the secured files

Installation
=====

1. git clone https://github.com/deifyed/vault.git
2. cd vault
3. python setup.py sdist
4. pip install dist/vault-*.tar.gz

TODO
=====

It's a pretty basic application and I don't plan on adding much more functionality, but the current TODO is:
* Improve argparsing. Maybe make exclusive groups for secure, deploy and list commands
