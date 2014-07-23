#!/usr/bin/python
import sys
import re
import subprocess

colors = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'];
color_base = 30

def hilite(line, color):
    return '\x1b[0;{0}m{1}\x1b[0m'.format(colors.index(color) + color_base, line)

def output_line(line, pattern, color):
    line = line.strip()
    if len(line) == 0:
        return
    if len(pattern) > 0 and (color in colors) and re.search(pattern, line):
        print hilite(line, color)
    else:
        print line

def tail(logfile, pattern = '', color = 'white'):
    p = None
    stream = None
    if logfile == '-':
        stream = sys.stdin
    else:
        p = subprocess.Popen(['tail', '-f', logfile], stdout=subprocess.PIPE)
        stream = p.stdout
    try:
        while True:
            output_line(stream.readline(), pattern, color)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    logfile = sys.argv[1]
    pattern = len(sys.argv) > 2 and sys.argv[2] or ''
    color = len(sys.argv) > 3 and sys.argv[3] or 'white'
    tail(logfile, *sys.argv[2:])
