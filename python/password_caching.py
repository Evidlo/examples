#!/bin/env python2
# Evan Widloski - 2017-07-29
# GPGME password caching
# `~/.gnupg/gpg-agent` must contain `allow-loopback-pinentry`

from io import BytesIO
import gpgme
from getpass import getpass
import os

cache_file = os.path.expanduser('~/.cache/password_cache')

c = gpgme.Context()
default_key = c.keylist().next()

def password_cache():
    if os.path.exists(os.path.expanduser(cache_file)):
        # retrieve password from cache
        outfile = BytesIO()
        with open(cache_file, 'rb') as infile:
            c.decrypt(infile, outfile)
        password = outfile.getvalue().decode('utf8')
        outfile.close()
    else:
        # save password to cache
        password = getpass('Enter password to cache')
        infile = BytesIO(password.encode('utf8'))
        with open(cache_file, 'wb') as outfile:
            c.encrypt([default_key], 0, infile, outfile)
        infile.close()

    return password

print password_cache()

# import subprocess
# import urllib

# gpg_agent = subprocess.Popen(["gpg-connect-agent"], stdin=subprocess.PIPE,
#                              stdout=subprocess.PIPE)
# prompt = urllib.quote('Please enter your password')
# cache_id = 'foobar_app1'
# command = "GET_PASSPHRASE %s X X %s\n" % (cache_id, prompt)
# stdout = gpg_agent.communicate(command)[0]
# if gpg_agent.returncode != 0:
#     raise Exception("gpg-connect-agent exited %r" %
#                     (gpg_agent.returncode,))
# elif not stdout.startswith("OK"):
#     raise Exception("gpg-agent says: %s" % (stdout.rstrip(),))
# else:
#     # You'll get an exception here if we get anything we didn't expect.
#     passphrase = stdout[3:-1].decode("hex")
#     print(passphrase)
