#! /usr/bin/env python
"get generate yapf args from a piped git diff"
import sys
import argparse
import os
import subprocess
from typing import Union, Optional, List
from yapf.yapflib.yapf_api import FormatFile # auto-detects configuration

cli = argparse.ArgumentParser(description='format only changed lines')
cli.add_argument(
    '--verbose',
    '-v',
    action='store_true',
    help='print the yapf args and produced diff'
)
cli.add_argument(
    '--dry-run', action='store_true', help='don\'t modify the changed files'
)
cli.add_argument('rest', nargs='*', help='positional parameters for `git diff`')


def run(cmd):
    return (
        subprocess.run(
            [i for i in cmd.split(' ') if i], stdout=subprocess.PIPE
        ).stdout or b''
    ).decode().strip()


class File(object):

    def __init__(self, name_line: str):
        self.is_py = name_line.strip()[-3:] == '.py'
        self.name = name_line[6:].strip()
        self.ranges = []

    def format(self, verbose: bool = False, dry_run: bool = False):
        if self.is_py:
            formatted = FormatFile(
                self.name,
                lines=self.ranges,
                print_diff=True,
                inplace=(not dry_run)
            )
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


def parse_line(line: str) -> Union[None, File, LineRange]:
    if line[0:6] == '+++ b/': # it's a filename
        return File(line)
    elif line[0:3] == '@@ ': # it's a range
        return LineRange(line)


def parse_git_diff(diff):
    files = []
    for line in diff:
        parsed = parse_line(line)
        if type(parsed) is File:
            files.append(parsed)
        elif type(parsed) is LineRange:
            files[-1].ranges.append(tuple(parsed))
    return files


def main(*, verbose: bool = False, diff_args: Optional[List[str]] = []):
    files = parse_git_diff(
        sys.stdin or run('git diff {}'.format(diff_args.join(' '))).split('\n')
    )
    for f in files:
        if f.is_py:
            f.format(verbose)


if __name__ == '__main__':
    os.chdir(run('git rev-parse --show-toplevel'))
    program_arguments = cli.parse_args(sys.argv)
    main(
        verbose=program_arguments.verbose,
        diff_args=(
            program_arguments.diff_args
            if 'diff_args' in program_arguments else []
        )
    )

