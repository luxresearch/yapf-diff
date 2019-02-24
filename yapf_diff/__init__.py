#! /usr/bin/env python
"get generate yapf args from a piped git diff"
import sys
import argparse
import os
import subprocess
from typing import Union, Optional, List
from yapf.yapflib.yapf_api import FormatFile  # auto-detects configuration

cli = argparse.ArgumentParser(description='format only changed lines')
cli.add_argument(
    '-d',
    '--diff',
    action='store_true',
    help='print the yapf args and produced diff')
cli.add_argument(
    '-i', '--inplace', action='store_true', help='modify the changed files')
cli.add_argument(  # ignored; intended for compatibility with yapf
    '--from-git-diff',
    nargs='?',
    action='store',
    help='if used as a flag, this indicates that sdin is from git diff. If used'
    ' as an argument, it indicates a ref against which to call git diff',
    const=True,
    default=True)


def run(cmd):
  command = [i for i in cmd.split(' ') if i]
  result = subprocess.run(command, stdout=subprocess.PIPE).stdout or b''
  return result.decode().strip()


class File(object):

  def __init__(self, name_line: str):
    self.is_py = name_line.strip()[-3:] == '.py'
    self.name = name_line[6:].strip()  # ignoring '+++ b/'
    self.ranges = []

  def format(self,
             verbose: bool = False,
             print_diff: bool = True,
             inplace: bool = True):
    if self.is_py:
      formatted = FormatFile(
          self.name, lines=self.ranges, print_diff=print_diff, inplace=inplace)
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


def parseLine(line) -> Union[None, File, LineRange]:
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


def main(*, verbose: bool = False, diff_args: Optional[List[str]] = []):
  """Short summary.

  Args:
      verbose (bool): Whether to print
      diff_args (Optional[List[str]]): arguments for git diff.

  """
  files = parseUnifiedDiff(
      sys.stdin or run('git diff {}'.format(diff_args.join(' '))).split('\n'))
  for f in files:
    if f.is_py:
      f.format(verbose)


if __name__ == '__main__':
  os.chdir(run('git rev-parse --show-toplevel'))
  program_arguments = cli.parse_args(sys.argv)
  diff_args = (
      program_arguments.from_git_diff
      if type(program_arguments.from_git_diff) is str else [])
  main(verbose=program_arguments.verbose, diff_args=diff_args)
