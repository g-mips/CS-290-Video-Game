import inspect

DEBUG = True

def debug(message):
    if DEBUG:
        log(message, "DEBUG: ")

def error(message):
    log(message, "ERROR: ")

def log(message, level):
    stack = inspect.stack()
    print(str(level) + str(stack[2][1]) + " - " + str(stack[2][2]) + " - " + str(stack[2][3]) + ": " + str(message))
