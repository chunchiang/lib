'''dec.py

Prerequisites:
    - This module is tested on Python 2.7.12.
    - decorator needs to be installed.
'''
import logging
import os
import sys
import time

import decorator  # python decorator module
from pexpect.exceptions import TIMEOUT

# Include the project package into the system path to allow import
package_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, package_path)

# Import your package (if any) below
from lib.connection import Connection


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


@decorator.decorator
# WIP, not functioning
def connect(f, *args, **kwargs):
    #with open('{}.log'.format(os.path.basename(__file__).split('.')[0]), 'wb') as log:
        status = False
        try:
            args = [x for x in args]
            kwargs = dict((k, v) for k, v in kwargs.items())
            is_logged_in = False
            conn = Connection(logfile=log, static_logpath='~/logs/{}'.format(os.path.basename(__file__).split('.')[0]))
            print('--- Connecting to {} ---'.format(args[0].ip))
            log.debug('--- Connecting to {} ---'.format(args[0].ip))
            is_logged_in = conn.login(args[0].ip, args[0].username, args[0].password)
            status = f(*args, **kwargs)
        except TIMEOUT:
            if conn.output:
                print('{}'.format(conn.output))
                log.debug('{}'.format(conn.output))
            log.error('*** Timeout occurred for {}!'.format(ip))
        finally:
            time.sleep(1)
            if is_logged_in:
                conn.logout()
            return status
