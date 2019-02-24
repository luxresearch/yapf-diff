#! /usr/bin/env python
"get generate yapf args from a piped git diff"
import sys
import argparse
import os
import subprocess
from yapf.yapflib.yapf_api import FormatFile  # auto-detects configuration

cli = argparse.ArgumentParser(description='format only changed lines')
cli.add_argument(
    '-d',
    '--diff',
    action='store_true',
    help='print the yapf args and produced diff')
cli.add_argument(
    '-i', '--in-place', action='store_true', help='modify the changed files')
cli.add_argument(
    '--from-git-diff',
    nargs='?',
    action='store',
    help='if used as a flag, this indicates that sdin is from git diff. If used'
    ' as an argument, it indicates a ref against which to call git diff',
    const=True,
    default=True)  # default ignores absence of the flag


class File(object):

  def __init__(self, name_line):
    self.is_py = name_line.strip()[-3:] == '.py'
    self.name = name_line[6:].strip()  # ignoring '+++ b/'
    self.ranges = []

  def format(self, verbose=False, print_diff=True, in_place=True):
    if self.is_py:
      formatted = FormatFile(
          self.name,
          lines=self.ranges,
          print_diff=print_diff,
          in_place=in_place)
      if verbose:
        print(formatted[0])


class LineRange(list):

  def __init__(self, diff_range: str):
    end_range = diff_range.split('+')[1].split('@@')[0].strip().split(',')
    if len(end_range) not in [1, 2]:
      raise IndexError('unexpected range: {}'.format(diff_range))

    self.start = int(end_range[0])
    self.end = self.start + (int(end_range[1]) if len(end_range) == 2 else 1)
    super().__init__([self.start, self.end])


def run(cmd):
  "a polyfill for subprocess.run"
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE, check=True)
  process.wait()
  return '\n'.join(i.decode() for i in process.stdout)


def parseLine(line):
  """Parse a line from a combined diff as a file, chunk range, or ignored.
  See https://git-scm.com/docs/git-diff#_combined_diff_format for details on
  combined diffs.

  Args:
      line (str): a line from a combined diff.

  Returns:
      a File, a LineRange, or None.

  """
  if line[0:6] == '+++ b/':  # it's a filename
    return File(line)
  elif line[0:3] == '@@ ':  # it's a range
    return LineRange(line)


def parseUnifiedDiff(diff):
  """Gather the files and their post-image modified lines from a combined diff.

  Args:
      diff (str): A combined diff output by `git diff`. See
        https://git-scm.com/docs/git-diff#_combined_diff_format

  Returns:
      A list of `File`s.

  """
  files = []
  for line in diff:
    parsed = parseLine(line)
    if type(parsed) is File:
      files.append(parsed)
    elif type(parsed) is LineRange:
      files[-1].ranges.append(tuple(parsed))
  return files


def getDiff(base=''):
  """Returns a git diff either from stdin or against a base.

  Args:
      base (str|bool): an optional base for the diff. If True, reads from stdin.

  Returns:
      str: a unified diff or an empty string

  """
  if type(base) is bool and base:
    return sys.stdin
  elif type(base) is str:
    cmd = ['git', 'diff']
    if base:
      cmd += [base]
    return run(cmd)


def main(argv):
  """Short summary.

  Args:
      verbose (bool): Whether to print
      diff_args (Optional[List[str]]): arguments for git diff.

  """
  args = cli.parse(argv)
  if args.from_git_diff:
    os.chdir(run('git rev-parse --show-toplevel'.split()).strip())
    diff = getDiff(args.from_git_diff)
    files = parseUnifiedDiff(diff)
    for f in files:
      if f.is_py:
        f.format(verbose=(not args.inplace), print_diff=args.diff)
  else:
    sys.exit(1)


if __name__ == '__main__':
  main(sys.argv)
