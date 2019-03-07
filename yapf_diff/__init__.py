#! /usr/bin/env python
"get generate yapf args from a piped git diff"
import sys
import argparse
import os
import subprocess
from yapf.yapflib.yapf_api import FormatFile  # auto-detects configuration
from yapf.yapflib.file_resources import IsPythonFile
from .lib import parseUDiff

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
    metavar='BASE_REF',
    action='store',
    help='if used as a flag, this indicates that stdin is from git diff. If used'
    ' as an argument, it indicates a ref against which to call git diff',
    const=True,
    default=True)  # default ignores absence of the flag


def run(cmd):
  "a polyfill for subprocess.run"
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  process.wait()
  return '\n'.join(i.decode() for i in process.stdout)


def getDiff(base=''):
  """Returns a git diff either from stdin or against a base.

  Args:
      base (str|bool): an optional base for the diff. If True, reads from stdin.

  Returns:
      str: a unified diff or an empty string

  """
  if base is True:
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
  args = cli.parse_args(argv)
  if args.from_git_diff:
    git_root = run('git rev-parse --show-toplevel'.split(' ')).strip()
    os.chdir(git_root)
    diff = getDiff(args.from_git_diff)
    files = parseUDiff(diff, parent=git_root)
    for filename, lines in files.items():
      if IsPythonFile(filename):
        FormatFile(
            filename, lines=lines, in_place=args.in_place, print_diff=args.diff)
  else:
    sys.exit(1)


if __name__ == '__main__':
  main(sys.argv)
