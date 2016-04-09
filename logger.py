import inspect

DEBUG = False
ERROR = False

def debug(message):
    '''
    Prints message in DEBUG mode
    '''
    if DEBUG:
        log(message, "DEBUG: ")

def error(message):
    '''
    Prints message in ERROR mode
    '''
    if ERROR:
        log(message, "ERROR: ")

def log(message, level):
    '''
    Prints message at level mode
    '''
    stack = inspect.stack()
    print(str(level) + str(stack[2][1]) + " - " + str(stack[2][2]) + " - " + str(stack[2][3]) + ": " + str(message))
