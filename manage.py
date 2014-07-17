#!/usr/bin/python

import argparse
from os import path
from module.config import Config
from module.server import Server
from module.cmd_handlers import Driver

# declare servers
server_list = [
        Server('GameServer', path.join(Config.code, 'Server/GameServer')),
        Server('IStorageMgr', path.join(Config.code_comm, 'GameStorage'), Config.conf_name('storage')),
        Server('ChannelServer', path.join(Config.code_comm, 'Channel/channel')),
        Server('XGMsgServer'),
        Server('LoginChannel', path.join(Config.code_comm, 'Channel/channel')),
        Server('GUIDServer'),
        Server('OnlineServer'),
        Server('ProxyServer'),
        Server('LoginServer'),
        Server('OuterProxyServer'),
        Server('FragmentRobberyServer'),
        Server('SytPvpServer'),
        Server('RankDataServer', path.join(Config.code_comm, 'RankServer2')),
        Server('RankListServer'),
        ]

# build parser
cmd_list = ['list', 'debug', 'log', 'compile', 'install', 'run', 'stop', 'restart']
target_names = list(s.target for s in server_list)
target_indexes = range(len(server_list))

parser = argparse.ArgumentParser()
parser.add_argument('cmd', help='select a command from: ' + ','.join(cmd_list), \
                    choices=cmd_list, metavar="cmd")
parser.add_argument('-r', '--rebuild', help='rebuild flag, use with \'compile\' command', \
                    action='store_true')
parser.add_argument('-v', '--interval', help='wait \'interval\' sec before apply command on next target, \
                    use with \'run,restart\' commands', type=float, \
                    default=0.0)
parser.add_argument('-t', '--targets', help='specify targets by name', \
                    choices=target_names, metavar="", nargs='*', \
                    default=[])
parser.add_argument('-i', '--target_indexes', help='specify targets by index', \
                    choices=target_indexes, type=int, metavar="", nargs='*', \
                    default=[])
parser.add_argument('-c', '--clean_shm', help='clean share memory, use with \'stop\' command', \
                    action='store_true')
parser.add_argument('--args', help='the rest args will be passed on to command handler', \
                    nargs='*', default=[])

#opt = parser.parse_args()
#print opt

# run
Driver.run(parser, *[server_list])
