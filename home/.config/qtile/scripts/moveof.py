#!/usr/bin/python3
from libqtile.command import Client
import sys
GROUPS = range(1, 10)

def print_usage():
    print('usage: change_group <1|-1>')
    sys.exit(1)

if len(sys.argv) != 2:
    print_usage()

try:
    shift = int(sys.argv[1])
except ValueError:
    print_usage()

c = Client()
cur_group = int(c.group.info()['name'])
target = cur_group + shift
if target in GROUPS:
    c.group[str(target)].toscreen()
