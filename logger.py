import inspect

def debug(message):
    stack = inspect.stack()
    print("DEBUG: " + str(stack[0][1]) + " - " + str(stack[0][2]) + " - " + str(stack[0][3]) + ": " + str(message))

