'''decorator_func.py

Prerequisites:
    - This module is compatible with python 2.7+ and python 3.7+.
'''
import logging
import os
import sys
import time
# from pathlib import Path

log = logging.getLogger(__name__)


def time_elapsed(f):
    '''Timer decorator for time elapsed counter.

    Preserving signatures of decorated functions
    Reference: http://stackoverflow.com/questions/147816/preserving-signatures-of-decorated-functions
    '''
    def wrapper(*args, **kwargs):
        log.debug('>>> {}'.format(f.__name__))
        args = [x for x in args]
        kwargs = dict((k, v) for k, v in kwargs.items())
        start_time = time.time()
        status = f(*args, **kwargs)
        timer = time.time() - start_time

        log.debug('<<< {} finished in {:.2f} seconds'.format(f.__name__, timer))
        return status
    return wrapper


def state_machine(f, *args, **kwargs):
    args = [x for x in args]
    kwargs = dict((k, v) for k, v in kwargs.items())
    status = f(*args, **kwargs)
    return status


# Not working
# def lock(f):
    # '''Lock decorator creates a lock file to ensure only one instance is 
    # running at any given time.'''
    # # TODO: Maybe choose a static path to create the lock file, such as the directory this module is in.
    # def wrapper(*args, **kwargs):
        # # Check if a lock file exist
        # lock_file = Path('{}.lock'.format(f.__name__))
        # if lock_file.is_file():
            # print('Another update process already started.')
            # return None

        # # Create a lock file to indicate an instance is already running
        # lock_file.touch()

        # try:
            # args = [x for x in args]
            # kwargs = dict((k, v) for k, v in kwargs.items())
            # status = f(*args, **kwargs)
        # finally:
            # # Remove the lock file
            # lock_file.unlink()
        # return status
    # return wrapper


