#! /usr/bin/env python
"get generate yapf args from a piped git diff"
import sys
import argparse
import os
import subprocess
import json
from typing import (
    List,
    Iterable,
    # IO,
    Union,
)
from yapf.yapflib.yapf_api import (FormatFile)
from yapf.yapflib.file_resources import (IsPythonFile, GetDefaultStyleForDir)
from yapf.yapflib.style import (CreateStyleFromConfig)
from .lib import parseUDiff

__version__ = '0.0.1'

cli = argparse.ArgumentParser(description='format only changed lines')
cli.add_argument(
    '-d',
    '--diff',
    action='store_true',
    help='print the yapf args and produced diff')
cli.add_argument(
    '--debug', action='store_true', help='print the style yapf is picking up')
cli.add_argument(
    '-i', '--in-place', action='store_true', help='modify the changed files')
cli.add_argument(
    '--from-git-diff',
    nargs='?',
    metavar='BASE_REF',
    action='store',
    help='if used as a flag, this indicates that stdin is from git diff. If'
    ' used as an argument, it indicates a ref against which to call git diff',
    const=True,
    default=True)  # default ignores absence of the flag


def run(cmd: List[str]) -> str:
  "a polyfill for subprocess.run"
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  process.wait()
  return '\n'.join(
      i.decode() if type(i) is bytes else str(i) for i in process.stdout)


def getDiff(base: Union[str, bool] = '') -> Iterable[str]:
  """Returns a git diff either from stdin or against a base.

  Args:
      base (str|bool): an optional base for the diff. If True, reads from stdin.

  Returns:
      str: a unified diff or an empty string
  """
  if type(base) is bool and base is True:
    if not sys.stdin.isatty():
      return (line.rstrip('\n').rstrip('\r') for line in sys.stdin.readlines())
  elif type(base) is str:
    cmd = ['git', 'diff']
    if base:
      cmd += [str(base)]
    return run(cmd)
  return []


def main(argv: List[str]) -> int:
  """Short summary.

  Args:
      verbose (bool): Whether to print
      diff_args (Optional[List[str]]): arguments for git diff.

  """
  args = cli.parse_args(argv[1:])
  if args.debug:

    class SetEncoder(json.JSONEncoder):

      def default(self, obj):
        if isinstance(obj, set):
          return [*obj]
          return json.JSONEncoder.default(self, obj)

    def debug(dirname, cfg, style):
      print(
          json.dumps(
              {
                  'dirname': dirname,
                  'cfg_file': cfg,
                  'style': style,
              },
              indent=2,
              sort_keys=True,
              cls=SetEncoder))
  else:

    def debug(*args):
      pass

  if args.from_git_diff:  # should always be true
    git_root = run('git rev-parse --show-toplevel'.split(' ')).strip()
    os.chdir(git_root)
    diff = getDiff(args.from_git_diff)
    changes = parseUDiff(diff, parent=git_root)
    dir_cache = {}
    if args.debug:
      cwd = os.getcwd()
      cfg = GetDefaultStyleForDir(cwd)
      debug(cwd, cfg, CreateStyleFromConfig(cfg))
      print('\n\n')
    for filename, lines in changes.items():
      if IsPythonFile(filename):
        dirname = os.path.dirname(filename)
        style = dir_cache.get(dirname)
        if style is None:
          cfg = GetDefaultStyleForDir(dirname)
          style = CreateStyleFromConfig(cfg)
          debug(dirname, cfg, style)
          dir_cache[dirname] = style
        results = FormatFile(
            filename,
            lines=lines,
            in_place=args.in_place,
            print_diff=args.diff,
            style_config=style)
        if args.diff:
          sys.stdout.write(str(results[0]) or '')
    return 1 if bool(changes) and bool(args.diff) else 0
  else:
    return 1


def run_main() -> None:
  sys.exit(main(sys.argv))


if __name__ == '__main__':
  run_main()
