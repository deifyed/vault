from libconman.configuration import Configuration 

config = Configuration()

def verbose(msg):
    if config.VERBOSE:
        print(msg)
