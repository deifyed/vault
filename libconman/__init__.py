import libconman.configuration as conf

def verbose(msg):
    if conf.VERBOSE:
        print(msg)
