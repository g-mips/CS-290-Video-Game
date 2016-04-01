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
    pygame.VIDEOEXPOSE:     "VIDEOEXPOSE"
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
    "VIDEOEXPOSE":     []
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
    if event in handlers:
        logger.debug(event)
        handlers[event].append(handler)

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
