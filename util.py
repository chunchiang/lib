'''This module provides generic util functions that can be reused.'''
import datetime
import json
import logging, logging.handlers
import os
import site
import subprocess
import sys
if sys.version_info[0] >= 3:
    # Python 3 need to import reload from importlib
    # Reference: https://stackoverflow.com/questions/10142764/nameerror-name-reload-is-not-defined/10142772
    from importlib import reload


def add_python_packages(package_path):
    '''Add the custom python packages path.'''
    # Get python command path in case there are several versions installed
    # Reference: https://stackoverflow.com/questions/2589711/find-full-path-of-the-python-interpreter
    local_pythonpath = run_cmd('{0} -m site --user-site'.format(sys.executable))

    # Add custom package path
    # Reference: https://stackoverflow.com/a/12311321
    run_cmd('mkdir -p {0}'.format(local_pythonpath))
    run_cmd('echo {0} > {1}/packages.pth'.format(package_path, local_pythonpath))

    # Reload the sys.path to make the packages available
    # Reference: https://stackoverflow.com/questions/25384922/how-to-refresh-sys-path
    reload(site)


def log_to_console(level=logging.WARNING):
    '''Output logging information to console.'''

    # Create logger
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)  # The logger level should always be lower than handler level

    # Create formatter
    formatter = logging.Formatter('%(asctime)s %(name)-8s %(threadName)-10s %(levelname)-8s %(message)s')

    # Create file handler, add formatter, and set level
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    log.addHandler(console_handler)


def log_to_email(level=logging.ERROR):
    '''Output and send logging information to email.
    
    Generally an email is sent for error or critical level messages, to inform
    supporting personnel of errors that can prevent program from working
    properly.
    '''

    # Create logger
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)  # The logger level should always be lower than handler level

    # Create formatter
    formatter = logging.Formatter('%(asctime)s %(name)-8s %(threadName)-10s %(levelname)-8s %(message)s')

    # Create file handler, add formatter, and set level
    email_handler = logging.SMTPHandler()
    email_handler.setFormatter(formatter)
    email_handler.setLevel(level)
    log.addHandler(email_handler)


def log_to_file(log_dir='logs', log_filename='', mode='a', maxBytes=0, backupCount=0, level=logging.DEBUG):
    '''Output logging information to a file.'''

    # Create log directory to store all logs for current UUT
    if log_dir:
        if log_dir.startswith('~'):
            log_dir = os.path.expanduser(log_dir)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, 0o755)  # Equivalent to mkdir -p
        if not log_dir.endswith('/'):
            log_dir = '{}/'.format(log_dir)

    # Create log filename
    if not log_filename:
        log_filename = datetime.datetime.now().isoformat().replace(':', '').replace('-', '').replace('.', '')
    log_file = '{}{}.log'.format(log_dir, log_filename)

    # Create logger
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)  # The logger level should always be lower than handler level

    # Create formatter
    formatter = logging.Formatter('%(asctime)s %(name)-8s %(threadName)-10s %(levelname)-8s %(message)s')

    # Create file handler, add formatter, and set level
    # Use Rotating File Handler to organize log files 
    # Reference: https://docs.python.org/3.1/library/logging.html#logging.handlers.RotatingFileHandler
    file_handler = logging.handlers.RotatingFileHandler(log_file, mode=mode, maxBytes=maxBytes, backupCount=backupCount)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    log.addHandler(file_handler)


def whoami():
    '''Return the current def name.'''
    return sys._getframe(1).f_code.co_name


def read_json(json_file, object_pairs_hook=None):
    '''Read json file provided into python dictionary.'''
    if json_file.startswith('~'):
        json_file = os.path.expanduser(json_file)
    try:
        with open(json_file, 'r') as f:
            data = json.load(f, object_pairs_hook=object_pairs_hook)
    except IOError:
        data = None
    return data


def write_json(data, json_file):
    '''Write json file provided into python dictionary.'''
    if json_file.startswith('~'):
        json_file = os.path.expanduser(json_file)
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)


def run_cmd(cmd, allow_error=False):
    '''Runs a command in bash.'''
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/bin/bash")
    stdout, stderr = proc.communicate()
    ret_code = proc.returncode

    if not stderr or allow_error is True:
        # remove the trailing newline, it's messing with regexes
        return stdout[:-1]
    else:
        print('Command {} failed. returncode is {}\nstdout: {}\nstderr: {}'.format(cmd, proc.returncode, stdout, stderr))
        sys.exit(-1)
