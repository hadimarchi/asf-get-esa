# __init__.py
# Author: Hal DiMarchi
# utils package for esa_downloader script

import subprocess
import logging

log = logging.basicConfig(level=logging.DEBUG,
                          format='%(pathname)s %(asctime)s %(levelname)s %(message)s')


def execute(cmd, log, expected=None, quiet=False):
    log.debug('Running command: ' + cmd)
    rcmd = cmd + ' 2>&1'

    pipe = subprocess.Popen(rcmd, shell=True, stdout=subprocess.PIPE)
    output = pipe.communicate()[0]
    return_val = pipe.returncode
    log.debug('return value was: {}'.format(return_val))
    return output
