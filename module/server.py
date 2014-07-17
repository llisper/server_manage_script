#!/usr/bin/python

from os import path
from config import Config

class Server:
    def __init__(self, target, code=None, conf=None, run=None):
        self.target = target
        self.code = code or path.join(Config.code_comm, target)
        self.conf = conf or Config.conf_name(target)
        self.run = run or Config.run

    def __str__(self):
        return  self.target +'\n' + \
                self.code + '\n' + \
                self.run + '\n' + \
                self.conf

if __name__ == '__main__':
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
    for i in server_list:
        print i
        print '-' * 80
