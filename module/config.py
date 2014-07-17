#!/usr/bin/python

import os
from os import path

class Config:
    root = os.getcwd()
    code = path.join(root, 'Server')
    run = path.join(root, 'Run')
    suffix = 'simple'
    code_comm = path.join(code, 'XJCommonServer')

    @staticmethod
    def target_name(t):
        return t + '_' + Config.suffix

    @staticmethod
    def code_dir(t):
        return path.join(Config.code_comm, t)

    @staticmethod
    def conf_name(t):
        return t + '.conf'

if __name__ == '__main__':
    print Config.target_name('GameServer')
    print Config.code_dir('ChannelServer')
    print Config.conf_name('ChannelServer')

