"Utility function to parse unified diffs"
# modified from `parse_udiff` from parse_udiff in
# https://github.com/PyCQA/pycodestyle/blob/master/pycodestyle.py#L1780
# as such, it is provided under the following license:
#
# Copyright © 2006-2009 Johann C. Rocholl <johann@rocholl.net>
# Copyright © 2009-2014 Florent Xicluna <florent.xicluna@gmail.com>
# Copyright © 2014-2018 Ian Lee <IanLee1521@gmail.com>
#
# Licensed under the terms of the Expat License
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import os
HUNK_REGEX = re.compile(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@.*$')


def parseUDiff(diff, parent='.'):
    """Return a dictionary of lines modified post after the diff."""
    # For each file of the diff, the entry key is the filename,
    # and the value is a set of row numbers to consider.
    rv = {}
    path = nrows = None
    for line in diff.splitlines():
        if nrows:
            if line[:1] != '-':
                nrows -= 1
            continue
        if line[:3] == '@@ ':
            hunk_match = HUNK_REGEX.match(line)
            (row, nrows) = [int(g or '1') for g in hunk_match.groups()]
            rv[path].append((row, row + nrows))
        elif line[:3] == '+++':
            path = line[4:].split('\t', 1)[0]
            # Git diff will use (i)ndex, (w)ork tree, (c)ommit and
            # (o)bject instead of a/b/c/d as prefixes for patches
            if path[:2] in ('b/', 'w/', 'i/'):
                path = path[2:]
            rv[path] = []

    return {
        os.path.join(parent, filepath): rows
        for (filepath, rows) in rv.items()
        if rows
    }
