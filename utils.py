import os
import time
import re
import random
import hashlib


_sha1_re = re.compile(r'^[a-f0-9]{40}$')


def _urandom():
    if hasattr(os, 'urandom'):
        return os.urandom(30)
    return random.random()


def generate_key(salt=None):
    return hashlib.sha1(bytes('%s%s%s' % (salt, time.time(), _urandom()), 'ascii')).hexdigest()


def validate_sha1(value):
    return _sha1_re.match(value) is not None

