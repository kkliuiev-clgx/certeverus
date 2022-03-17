import logging
import inspect 

a = 179

def logr(a):
    logging.basicConfig(level=logging.DEBUG)
    logging.warning('Watch out!')  # will print a message to the console
    # logging.info(f'I told you so {a} at {inspect.getframeinfo(inspect.currentframe()).function}:{inspect.getframeinfo(inspect.currentframe()).lineno}')  # will not print anything
    return

logr(a)