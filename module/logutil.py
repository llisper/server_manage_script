#!/usr/bin/python
import sys
import re
import subprocess

colors = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white'];
color_base = 30

def hilite(line, color):
    return '\x1b[0;{0}m{1}\x1b[0m'.format(colors.index(color) + color_base, line)

def color_line(line, pattern, color):
    if len(pattern) > 0 and (color in colors) and re.search(pattern, line):
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

if __name__ == '__main__':
    logfile = sys.argv[1]
    track(logfile, *sys.argv[2:])
    #tail(logfile, *sys.argv[2:])
