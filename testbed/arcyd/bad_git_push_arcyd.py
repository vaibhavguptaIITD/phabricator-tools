#!/usr/bin/env python
# encoding: utf-8

import os
import random
import sys

# The code base currently depends on version 2.7 of Python, any earlier
# than that and it won't have the requisite argparse feaures.  Any later
# than that (3.x) and there are breaking changes in the syntax.
#
# Prevent nasty runtime surprises by enforcing version 2.7 as early as
# possible.
#
# The version check itself will not work prior to Python version 2.0,
# that's when sys.version_info was introduced.
#
if sys.version_info[:2] != (2, 7):
    sys.stderr.write("You need python 2.7 to run this script\n")
    exit(1)

# append our module dirs to sys.path, which is the list of paths to search
# for modules this is so we can import our libraries directly
# N.B. this magic is only really passable up-front in the entrypoint module
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BASE_DIR = os.path.dirname(PARENT_DIR)
sys.path.append(os.path.join(BASE_DIR, "py", "abd"))
sys.path.append(os.path.join(BASE_DIR, "py", "phl"))

# This is a temprary fix for locationg plugins while not using "."
# notation python packages.
sys.path.append(os.path.join(BASE_DIR, "testbed", "plugins"))

import phlsys_git

import abdcmd_arcyd

if __name__ == "__main__":

    #
    # monkey-patch the base-level git clone to be unreliable
    #

    old_call = getattr(phlsys_git.GitClone, 'call')

    def unreliable_call(self, *args, **kwargs):
        if args and args[0] == 'push':
            if random.choice([True, False]):
                raise Exception('bad_git_push_arcyd.py: random git push fail')
        return old_call(self, *args, **kwargs)

    setattr(phlsys_git.GitClone, 'call', unreliable_call)

    # run arcyd as usual
    sys.exit(abdcmd_arcyd.main())


#------------------------------------------------------------------------------
# Copyright (C) 2012 Bloomberg L.P.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#------------------------------- END-OF-FILE ----------------------------------
