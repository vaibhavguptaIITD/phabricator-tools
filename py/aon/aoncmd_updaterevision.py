"""Update an existing revision in differential.

Note:

    When updating an existing revision, you should submit a diff versus
    the original file. Otherwise the display in Differential may not be as you
    expect.

    e.g.

    You have 3 versions of your README file:
        README_original.txt
        README_update_1.txt
        README_update_2.txt

    You would like to create a review of these two updates in sequence,
    the correct way to do it is this:

    1. create the review with this diff:
       $ diff -u README_original.txt README_update_1.txt

    2. update the review with this diff:
       $ diff -u README_original.txt README_update_2.txt

Usage examples:

    update revision 99 by piping in a diff:
    $ diff -u file1 file2 | arcyon update-revision 99 fixes -f -
    99

    update revision 99 from diff 2:
    $ arcyon update-revision 99 'fix review issues' -d 2
    99

"""
# =============================================================================
# CONTENTS
# -----------------------------------------------------------------------------
# aoncmd_updaterevision
#
# Public Functions:
#   getFromfilePrefixChars
#   setupParser
#   process
#
# -----------------------------------------------------------------------------
# (this contents block is generated, edits will be lost)
# =============================================================================

from __future__ import absolute_import

import argparse

import phlsys_makeconduit


def getFromfilePrefixChars():
    return ""


def setupParser(parser):
    diffsrc_group = parser.add_argument_group(
        'Diff arguments',
        'Mutually exclusive, one is required')
    diffsrc = diffsrc_group.add_mutually_exclusive_group(required=True)
    output_group = parser.add_argument_group(
        'Output format arguments',
        'Mutually exclusive, defaults to "--format-summary"')
    output = output_group.add_mutually_exclusive_group()

    diffsrc.add_argument(
        '--diff-id',
        metavar='INT',
        help='the id of the diff to create the file from, this could be '
             'the output from a "arcyon raw-diff" call',
        type=int)
    diffsrc.add_argument(
        '--raw-diff-file',
        '-f',
        help='the file to read the diff from, use \'-\' for stdin',
        metavar='FILE',
        type=argparse.FileType('r'))

    parser.add_argument(
        'revision_id',
        help='the id of the revision to update, e.g. the output from a '
             'previous "arcyon create-revision" command',
        type=str)

    parser.add_argument(
        'message',
        help='a short description of the update, this appears on the review '
             'page',
        type=str)

    output.add_argument(
        '--format-summary',
        action='store_true',
        help='will print a human-readable summary of the result.')
    output.add_argument(
        '--format-id',
        action='store_true',
        help='will print just the id of the revision, for scripting.')
    output.add_argument(
        '--format-url',
        action='store_true',
        help='will print just the url of the revision, for scripting.')

    phlsys_makeconduit.add_argparse_arguments(parser)


def process(args):
    conduit = phlsys_makeconduit.make_conduit(args.uri, args.user, args.cert)

    # create a new diff if we need to
    if args.diff_id:
        diff_id = args.diff_id
    else:
        d = {'diff': args.raw_diff_file.read()}
        diff_id = conduit.call("differential.createrawdiff", d)["id"]

    fields = {}

    d = {
        'id': args.revision_id,
        'diffid': diff_id,
        'fields': fields,
        'message': args.message
    }

    result = conduit.call("differential.updaterevision", d)

    if args.format_id:
        print result["revisionid"]
    elif args.format_url:
        print result["uri"]
    else:  # args.format_summary:
        print (
            "Updated revision '{rev_id}', you can view it at this URL:\n"
            "  {url}"
        ).format(
            rev_id=result["revisionid"],
            url=result["uri"])


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
