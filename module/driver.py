#!/usr/bin/python

import re
import sys
import argparse

def opt_args(opt):
    opt.args = hasattr(opt, 'args') and opt.args or []
    if len(opt.args) > 0 and opt.args[0] == '--':
        opt.args = opt.args[1:]

class Driver:
    def __init__(self, *cmd_handlers):
        self.cmd_handlers = {}
        for h in cmd_handlers:
            m = re.match(r'^<function cmd_(\w+)', str(h))
            if m:
                self.cmd_handlers[m.group(1)] = h

    def run(self, parser, *args):
        opt = parser.parse_args()
        cmd = sys.argv[1]
        opt_args(opt)

        print cmd, opt
        if cmd in self.cmd_handlers:
            h = self.cmd_handlers[cmd]
            h(opt, *args)

