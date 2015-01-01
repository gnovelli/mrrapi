# -*- coding: utf-8 -*-
""" This module will interface with the MiningRigRentals.com API in an attempt to give you easy access to their api.
"""

import hmac
import hashlib
import time
import urllib
import urllib2
import json
import sys
import ConfigParser
import os
from optparse import OptionParser
from inspect import currentframe

debug = False
__author__ = 'jcwoltz'
__version__ = '0.3.5a1'

def getmrrconfig():
    mkey = None
    msecret = None

    config = ConfigParser.ConfigParser()
    for loc in os.curdir, os.path.expanduser("~"), os.path.expanduser("~/.mrrapi"), os.path.expanduser("~/mrrapi"):
        try:
            with open(os.path.join(loc,"mrrapi.cfg")) as source:
                config.readfp(source)
                if debug:
                    print "DEBUG: Using %s for config file" % (str(source.name))
        except IOError:
            pass

    mkey = config.get('MRRAPIKeys','key')
    msecret = config.get('MRRAPIKeys','secret')

    if mkey is not None and msecret is not None:
        return mkey, msecret
    else:
        print "ERROR: Could not find mrrapi.cfg"
        sys.exit(10)
        return str(0), str(0)

def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])
