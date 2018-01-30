'''all_loggers.py
'''
import logging

# Import your package (if any) below
import dec


log = logging.getLogger(__name__)


@dec.time_elapsed
def addHandlerToAllLoggers(handler):
    '''Add handler to all loggers in the logging module.
    
    This function will add a handler to all the logger in the logging module.
    It is useful when trying to log using the same handle across modules that
    are unrelated (ie.  Modules are in different hierarchy from one another).
    '''
    # Add self first, in case logging is needed
    logging.Logger.manager.loggerDict[__name__].addHandler(handler)
    
    for logger_name, logger in logging.Logger.manager.loggerDict.iteritems():
        try:
            logger.addHandler(handler)
        except AttributeError as e:
            pass

@dec.time_elapsed
def setLevelToAllLoggers(level):
    '''Set level to all loggers in the logging module.
    
    This function will set the level to all the logger in the logging module.
    It is useful when trying to log using the same handle across modules that
    are unrelated (ie.  Modules are in different hierarchy from one another).
    '''
    for logger_name, logger in logging.Logger.manager.loggerDict.iteritems():
        try:
            logger.setLevel(level)
        except AttributeError as e:
            pass
            