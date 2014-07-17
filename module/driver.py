#!/usr/bin/python

import re
import argparse

class Driver:
    def __init__(self, *cmd_handlers):
        self.cmd_handlers = {}
        for h in cmd_handlers:
            m = re.match(r'^<function cmd_(\w+)', str(h))
            if m:
                self.cmd_handlers[m.group(1)] = h

    def run(self, parser, *args):
        opt = parser.parse_args()
        print opt
        if opt.cmd in self.cmd_handlers:
            h = self.cmd_handlers[opt.cmd]
            all_args = args + tuple(opt.args)
            h(opt, *all_args)

if __name__ == '__main__':
    def cmd_1(opt, p1):
        print 'cmd_1: ' + str(p1)

    def cmd_2(opt, p1, p2):
        print 'cmd_2: ' + str(p1) + str(p2)

    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')
    parser.add_argument('--', action='store_true', dest='delimit')
    parser.add_argument('args', nargs=argparse.REMAINDER)

    d = Driver(cmd_1, cmd_2)
    ex_args = [5]
    d.run(parser, *ex_args)

