conman - Config Manager
=====

Convenient way to store all your files(read configs) and folders(read containers containing alot of configs) in one folder for version controll.

How it works?
=====

It creates a hard link of the target file inside ~/.conman and saves the path of the target. This way you can version control or rsync ~/.conman and deploy these files if needed later (after a format or if they accidentaly gets deleted).

Usage
=====

conman --secure file.cfg Creates a link of file.cfg inside ~/.conman
conman --recursive --secure folder Creates a link for the files inside folder and subfolders of folder inside ~/.conman
conman --deploy id Creates a link from ~/.conman/id to where the original file was placed
conman --list Lists all the secured files

Installation
=====

1. git clone https://github.com/deifyed/vault.git
2. cd vault
3. python setup.py sdist
4. pip install dist/conman-*.tar.gz

TODO
=====

It's a pretty basic application and I don't plan on adding much more functionality, but the current TODO is:
* Improve argparsing. Maybe make exclusive groups for secure, deploy and list commands
* Improved formatting for conman -l
