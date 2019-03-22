import sys
import os
import time
import argparse
import logging
import daemon
from daemon import pidfile
import subprocess
import threading
import errno

debug_p = False

def compile(logf, dir_name, compile_option):
    # This does the "work" of the daemon

    logger = logging.getLogger('compile_daemon')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logf, mode='w')
    fh.setLevel(logging.INFO)

    formatstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formatstr)

    fh.setFormatter(formatter)

    logger.addHandler(fh)

    DIR_INC='DIR_INC=' + dir_name + 'include'
    DIR_SRC='DIR_SRC=' + dir_name + 'src'
    DIR_OBJ='DIR_OBJ=' + dir_name + 'obj'
    DIR_BIN='DIR_BIN=' + dir_name + 'bin'
    COMPILE_OPT='COMPILE_OPT=' + compile_option.replace('_', '-')
    p = subprocess.Popen(['make', DIR_SRC, DIR_INC, DIR_OBJ, DIR_BIN, COMPILE_OPT], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time_limit = 10
    st_time = time.time()
    is_time_exceed = False
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.decode().strip()
        if line:
            logger.info(line)
        if (time.time() - st_time) > time_limit:
            p.kill()
            is_time_exceed = True

    if p.returncode == 0:
        logger.info('compile succeeded')
    else:
        if is_time_exceed:
            logger.error('time limit exceeded, compile failed')
        else:
            logger.error('compile failed')


def start_daemon(pidf, logf, dir_name, compile_option):
    # This launches the daemon in its context
    # XXX pidfile is a context
    with daemon.DaemonContext(
        working_directory='./',
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf),
    ) as context:
        compile(logf, dir_name, compile_option)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="compile daemon in Python")
    parser.add_argument('-p', '--pid-file', default='./compile_daemon.pid')
    parser.add_argument('-l', '--log-file', default='./compile_daemon.log')
    parser.add_argument('-d', '--directory-name', default='./')
    parser.add_argument('-o', '--compile-option', default='')

    args = parser.parse_args()

    start_daemon(pidf=args.pid_file, logf=args.log_file, dir_name=args.directory_name, compile_option=args.compile_option)
