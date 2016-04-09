import sys
import pygame

import logger

bindings = {
    pygame.QUIT:            "QUIT",
    pygame.ACTIVEEVENT:     "ACTIVEEVENT",
    pygame.KEYDOWN:         "KEYDOWN",
    pygame.KEYUP:           "KEYUP",
    pygame.MOUSEMOTION:     "MOUSEMOTION",
    pygame.MOUSEBUTTONUP:   "MOUSEBUTTONUP",
    pygame.MOUSEBUTTONDOWN: "MOUSEBUTTONDOWN",
    pygame.VIDEORESIZE:     "VIDEORESIZE",
    pygame.VIDEOEXPOSE:     "VIDEOEXPOSE",
    pygame.USEREVENT:       "USEREVENT"
}

handlers = {
    "QUIT":            [],
    "ACTIVEEVENT":     [],
    "KEYDOWN":         [],
    "KEYUP":           [],
    "MOUSEMOTION":     [],
    "MOUSEBUTTONUP":   [],
    "MOUSEBUTTONDOWN": [],
    "VIDEORESIZE":     [],
    "VIDEOEXPOSE":     [],
    "USEREVENT":       []
}

def register(event, handler):
    '''
    This registers a new handler rather than the default handler

    PARAMETERS:
        event - The event that will be register
        handler - The function that is registered to event

    RETURN
        NONE
    '''
    if event in handlers and handler not in handlers[event]:
        logger.debug(event)
        handlers[event].append(handler)
    else:
        logger.error("Either event -- " + str(event) + " -- is not in handlers or handler -- " +
                     str(handler) + " -- is in handlers[event]")

def remove(event, handler):
    '''
    Remove the handler found in the event, event.
    '''
    if event in handlers and handler in handlers[event]:
        logger.debug(event)
        handlers[event].remove(handler)
    else:
        logger.error("Either event -- " + str(event) + " -- is not in handlers or handler -- " +
                     str(handler) + " -- is not in handlers[event]")

def remove_all():
    '''
    Removes all the handlers
    '''
    for event in handlers:
        handlers[event] = []

def handle_events():
    '''
    This is called to handle any events that are happening currently

    PARAMETERS:
        NONE

    RETURN:
        NONE
    '''
    for event in pygame.event.get():
        if event.type in bindings:
            for handler in handlers[bindings[event.type]]:
                logger.debug(event)
                handler(event)
