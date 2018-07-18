import site
import subprocess
import sys

def run_cmd(cmd, allow_error=False):
    '''Runs a command in bash.'''
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/bin/bash")
    stdout, stderr = proc.communicate()
    ret_code = proc.returncode

    if not stderr or allow_error is True:
        # remove the trailing newline, it's messing with regexes
        return stdout[:-1]
    else:
        print ("Command %s failed. returncode is %d\nstdout: %s\nstderr: %s" %
               (cmd, proc.returncode, stdout, stderr))
        sys.exit(-1)


def add_python_packages(package_path):
    '''Add the custom python packages path.'''
    # Get python command path in case there are several versions installed
    # Reference: https://stackoverflow.com/questions/2589711/find-full-path-of-the-python-interpreter
    local_pythonpath = run_cmd('{0} -m site --user-site'.format(sys.executable))

    # Add custom package path
    # Reference: https://stackoverflow.com/a/12311321
    run_cmd('mkdir -p {0}'.format(local_pythonpath))
    run_cmd('echo {0} > {1}/package.pth'.format(package_path, local_pythonpath))

    # Reload the sys.path to make the packages available
    # Reference: https://stackoverflow.com/questions/25384922/how-to-refresh-sys-path
    reload(site)
