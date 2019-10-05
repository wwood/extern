import subprocess
import logging
import os
import multiprocessing

from .multi_runner import MultiRunner

def run(command, stdin=None):
    '''
    Run a subprocess.check_output() with the given command with
    'bash -c command'
    returning the stdout. If the command fails (i.e. has a non-zero exitstatus),
    raise a ExternCalledProcessError that includes the $stderr as part of
    the error message

    Parameters
    ----------
    command: str
        command to run
    stdin: str or None
        stdin to be provided to the process, to subprocess.communicate.

    Returns
    -------
    Standard output of the run command

    Exceptions
    ----------
    extern.ExternCalledProcessError including stdout and stderr of the run
    command should it return with non-zero exit status.
    '''
    logging.debug("Running extern cmd: %s" % command)

    process = subprocess.run(
        ["bash",'-o','pipefail',"-c", command],
        input=stdin.encode() if isinstance(stdin, str) else stdin,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout = process.stdout.decode('UTF-8')
    if process.returncode != 0:
        raise ExternCalledProcessError(process, command)
    return stdout

def run_many(commands,
             num_threads=multiprocessing.cpu_count(),
             progress_stream=None,
             stdin=None):
    '''
    Run a list of programs with multiprocessing

    Parameters
    ----------
    commands: list of str
        a list of string command lines to be run
    num_threads: int
        number of programs to run simultaneously
    progress_stream: a writeable file handle / stream
        write progress to this stream e.g. to write to STDOUT use sys.stdout
    stdin: list of str
        An array of strings to provide as STDIN to each process, or None. The
        length of the list must be the same length as the length of the
        commands.

    Returns
    -------
    A list of standard outputs as per run() in the same order as the commands
    provided.

    Exceptions
    ----------
    extern.ExternalCalledProcessError as per run() when the first command
    returns a non-zero exit status.
    '''
    runner = MultiRunner(num_threads)
    return runner.run(commands, progress_stream=progress_stream,
                      stdin=stdin)

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
    def __init__(self, completed_process, command):
        self.command = command
        self.returncode = completed_process.returncode
        self.stderr = completed_process.stderr
        self.stdout = completed_process.stdout
        self.completed_process = completed_process

    def __str__(self):
        return "Command %s returned non-zero exit status %i.\n"\
            "STDERR was: %sSTDOUT was: %s" % (self.command,
                                                self.returncode,
                                                self.stderr,
                                                self.stdout)
