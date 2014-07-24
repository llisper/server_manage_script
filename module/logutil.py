#!/usr/bin/python
import sys
import re
import subprocess

__colors = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'];
__color_base = 30

def __cindex(color):
    return __colors.index(color) + __color_base

def hilite(line, color):
    if (color in __colors):
        return '\x1b[0;{0}m{1}\x1b[0m'.format(__cindex(color), line)
    else:
        return line

def hiswap(line, color, origin):
    if (color in __colors) and (origin in __colors):
        return '\x1b[0;{0}m{1}\x1b[0;{2}m' \
                .format(__cindex(color), line, __cindex(origin))
    else:
        return line

def color_line(line, pattern, color):
    if len(pattern) > 0 and re.search(pattern, line):
        return True, hilite(line, color)
    else:
        return False, line

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
            line = stream.readline().strip()
            if len(line) == 0: continue
            print color_line(line, pattern, color)[1]
    except KeyboardInterrupt:
        pass

def track(logfile, *args):
    p = None
    stream = None
    if logfile == '-':
        stream = sys.stdin
    else:
        p = subprocess.Popen(['tail', '-f', logfile], stdout=subprocess.PIPE)
        stream = p.stdout
    try:
        while True:
            line = stream.readline().strip()
            if len(line) == 0: continue
            for i in range(len(args) / 2):
                pattern = args[i * 2]
                color = args[i * 2 + 1]
                ret, line = color_line(line, pattern, color)
                if ret: break
            print line
    except KeyboardInterrupt:
        pass

default_debug_color = 'white'
def debug(log, color = default_debug_color):
    print hilite(log, color)

if __name__ == '__main__':
    logfile = sys.argv[1]
    track(logfile, *sys.argv[2:])
    #tail(logfile, *sys.argv[2:])
