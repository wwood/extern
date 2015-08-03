import subprocess
import logging
import os


def run(command):
    '''
    Run a subprocess.check_output() with the given command with 
    'bash -c command'
    returning the stdout. If the command fails (ie has a non-zero exitstatus),
    raise a CommandeerCalledProcessError that includes the $stderr as part of
    the error message
    
    Parameters
    ----------
    command: str
        command to run
    '''
    logging.debug("Running commandeer cmd: %s" % command)

    process = subprocess.Popen(["bash","-c", command],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
        
    if process.returncode != 0:
        raise ExternCalledProcessError(command,
                                   process.returncode,
                                   stderr,
                                   stdout)
    return stdout

def which(program):
    '''
    Determine where a particular executable exists and return this, or None
    if the command was not found.
    
    Parameters
    ----------
    program: str
        program name
    
    Credits to BamM and http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python'''
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


class ExternCalledProcessError(subprocess.CalledProcessError):
    def __init__(self, command, returncode, stderr, stdout):
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout
        
    def __str__(self):
        return "Command %s returned non-zero exit status %i.\n"\
            "STDERR was: %sSTDOUT was: %s" % (self.command,
                                                self.returncode,
                                                self.stderr,
                                                self.stdout)