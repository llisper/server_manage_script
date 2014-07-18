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

# sub command
cmd_list = ['list', 'debug', 'log', 'compile', 'install', 'run', 'stop', 'restart', 'push']
targets = list(s.target for s in server_list) + list(str(i) for i in range(len(server_list)))

# compile [-r,--rebuild] [-i,-inverse] [-t,--targets ...]
# install [-i,-inverse] [-t,--targets ...]
# list [-i,-inverse] [-t,--targets ...]
# debug [-t,--targets ...]
# log [-t,--targets ...] -- [args...]
# run [-v,interval val] [-i,-inverse] [-t,--targets ...]
# stop [-i,-inverse] [-t,--targets ...]
# restart [-v,interval val] [-i,-inverse] [-t,--targets ...]
# push svr_name -- [args...]
parser = argparse.ArgumentParser()
sub_parser = parser.add_subparsers(help="type 'subcmd help' to get help text")
sub_cmd = {}
for cmd in cmd_list:
    sub_cmd[cmd] = sub_parser.add_parser(cmd)

for cmd in ['list', 'debug', 'log', 'compile', 'install', 'run', 'stop', 'restart']:
    sub_cmd[cmd].add_argument('-t', '--targets', help='specify targets by name or index', \
                              choices=targets, metavar="", nargs='*', \
                              default=[])

for cmd in ['list', 'compile', 'install', 'run', 'stop', 'restart']:
    sub_cmd[cmd].add_argument('-i', '--inverse', help='inverse selection flag', \
                              action='store_true')

for cmd in ['run', 'restart']:
    sub_cmd[cmd].add_argument('-v', '--interval', help='wait \'interval\' sec before apply command on next target', \
                              type=float, default=0.0)

for cmd in ['stop', 'restart']:
    sub_cmd[cmd].add_argument('-c', '--clean_shm', help='clean share memory flag', \
                              action='store_true')

sub_cmd['compile'].add_argument('-r', '--rebuild', help='rebuild flag', \
                                action='store_true')

sub_cmd['push'].add_argument('service_name')

for cmd in ['log', 'push']:
    sub_cmd[cmd].add_argument('args', nargs=argparse.REMAINDER, default=[])

# run
Driver.run(parser, *[server_list])
