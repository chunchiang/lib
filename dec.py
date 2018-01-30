'''dec.py
'''
import logging
import time
import decorator  # python decorator module

# Import your package (if any) below


log = logging.getLogger(__name__)


def whoami():
    '''Return the current def name.'''
    import sys
    return sys._getframe(1).f_code.co_name


@decorator.decorator
def time_elapsed(f, *args, **kwargs):
    '''Timer decorator for time elapsed counter.

    Preserving signatures of decorated functions
    Reference: http://stackoverflow.com/questions/147816/preserving-signatures-of-decorated-functions
    '''
    log.debug('>>> {}.'.format(f.__name__))
    args = [x for x in args]
    kwargs = dict((k, v) for k, v in kwargs.items())
    start_time = time.time()
    status = f(*args, **kwargs)
    timer = time.time() - start_time

    log.debug('<<< {} finished in {:.2f} seconds.'.format(f.__name__, timer))
    return status


@decorator.decorator
def state_machine(f, *args, **kwargs):
    args = [x for x in args]
    kwargs = dict((k, v) for k, v in kwargs.items())
    status = f(*args, **kwargs)
    return status
