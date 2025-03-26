#!/usr/bin/env python3

import os
import subprocess

fd_in, fd_out = os.pipe()
output = subprocess.check_output(
    f"/home/evan/resources/examples/python/fd_share/child.py {fd_in} {fd_out}",
    shell=True
)
