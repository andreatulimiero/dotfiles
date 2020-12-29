#!/usr/bin/python3
from os import (path,
                listdir)
import re
from argparse import ArgumentParser
from io import TextIOWrapper
from enum import Enum
from typing import List
from socket import gethostname

HOSTNAME = gethostname()
IGNORE = {'.git', '.gitignore', 'prepare.py', 'plugged', '__pycache__'}
PREPARING_REGEX = r">\s*\[(?P<comment_start>[^0-9A-Za-z]+)@(?P<comment_end>[^0-9A-Za-z]+)(?P<hostname>[0-9A-Za-z]+)\]"
prep_regex = re.compile(PREPARING_REGEX)

class Action(Enum):
    COMMENT = 1
    UNCOMMENT = 2
    NONE = 3

    def get_from_args(args):
        if args.comment:
            return Action.COMMENT
        elif args.decomment:
            return Action.UNCOMMENT
        else:
            return Action.NONE

def log_change(line: str, esc: str = '') -> None:
    print(esc, ' ',  line.strip())

def log_decommented(line: str) -> None:
    log_change(line, '[\x1b[33m+\x1b[0m]')

def log_commented(line: str) -> None:
    log_change(line, '[\x1b[31m-\x1b[0m]')

def is_commented(line: str,
                 comment_start: str,
                 comment_end: str) -> bool:
    return line.startswith(comment_start) and (line.endswith(comment_end) or comment_end == '_')

def line_content(line: str,
                 comment_start: str,
                 comment_end: str) -> str:
    line = line.replace(comment_start, '', 1)
    if comment_end != '_':
        line = line[::-1].replace(comment_end[::-1], '', 1)[::-1]
    return line

def comment_line(line: str,
                 comment_start: str,
                 comment_end: str,
                 tag: str) -> str:
    if is_commented(line, comment_start, comment_end):
        return line
    content = line
    log_commented(content)
    return f'{comment_start}{content}{comment_end if comment_end != "_" else ""}'

def decomment_line(line: str,
                   comment_start: str,
                   comment_end: str,
                   tag: str) -> str:
    if not is_commented(line, comment_start, comment_end):
        return line
    content = line_content(line, comment_start, comment_end)
    log_decommented(content)
    return content

def inspect_file(f: TextIOWrapper,
                 action: Action) -> List[str]:
    lines = []
    for line in f:
        match = prep_regex.search(line)
        if match:
            hostname: str = match.group('hostname')
            comment_start: str = match.group('comment_start')
            comment_end: str = match.group('comment_end')
            assert hostname and comment_start and comment_end
            tag: str = line[match.start():match.end()]
            # Prioritize un-/comment actions over default preparing
            if action == Action.COMMENT:
                action_func = comment_line
            elif action == Action.UNCOMMENT:
                action_func = decomment_line
            elif hostname == HOSTNAME:
                action_func = decomment_line
            else:
                action_func = comment_line
            line = action_func(line, comment_start, comment_end, tag)
        lines.append(line)
    return lines

def inspect_dir(dirname: str,
                action: Action,
                follow_sym: bool = False) -> None:
    for fname in listdir(dirname):
        if fname in IGNORE:
            continue
        fpath: str = path.join(dirname, fname)
        if path.islink(fpath) and not follow_sym:
                continue
        if path.isdir(fpath):
            inspect_dir(fpath, action)
            continue
        try:
            with open(fpath, 'r+') as f:
                lines: List[str] = inspect_file(f, action)
            # TODO: Create backup file in case write fails
            with open(fpath, 'w+') as f:
                for line in lines:
                    f.write(line)
        except UnicodeDecodeError:
            # Error reading the file, just ignore it
            pass

def main() -> None:
    parser = ArgumentParser(description='Prepare configuration files for '
                                        'multiple devices usage')
    parser.add_argument('-C', '--dir', action='store', default='.',
                        help='chdir to DIR before looking for files')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--comment', action='store_true',
                       help='comment all preparable code')
    group.add_argument('-d', '--decomment', action='store_true',
                       help='uncomment all preparable code')
    parser.add_argument('--follow-sym', action='store_true',
                        help='follow symlink folders')
    args = parser.parse_args()
    inspect_dir(args.dir,
                action=Action.get_from_args(args),
                follow_sym=args.follow_sym)

if __name__ == '__main__':
    main()
