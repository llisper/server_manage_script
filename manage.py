#!/usr/bin/python

import os
import re
import sys
import time
import tempfile
import subprocess
from os import path
from subprocess import *
#from __future__ import print_function

#configuration
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

#print Config.target_name('GameServer')
#print Config.code_dir('ChannelServer')
#print Config.conf_name('ChannelServer')

# target list
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

    @staticmethod
    def find(slist, target):
        for i in slist:
            if i.target == target:
                return i

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

#for i in server_list:
#    print '----------------------------'
#    print i

# parse command line
def parse_cmdline(slist):
    class Opt: pass
    valid_targets = list(svr.target for svr in slist)
    def targets(i): return sys.argv[i:] or valid_targets
    assert(len(sys.argv) > 1)

    opt = Opt()
    opt.cmd = sys.argv[1]
    assert(opt.cmd in ['list', 'install', 'run', 'debug', 'log', 'compile', 'stop', 'restart'])
    if opt.cmd in ['list', 'install', 'stop']:
        opt.targets = targets(2)
    elif opt.cmd in ['debug', 'log']:
        assert(len(sys.argv) > 2)
        opt.targets = [ sys.argv[2] ]
        opt.cmdline = sys.argv[3:]
    elif opt.cmd == 'compile':
        i = 2
        opt.rebuild = False
        if len(sys.argv) > 2 and sys.argv[2] == 'rebuild':
            i = 3
            opt.rebuild = True
        opt.targets = targets(i)
    elif opt.cmd in ['run', 'restart']:
        opt.interval = 0
        opt.targets = sys.argv[2:]
        if re.match(r'^[0-9.]+$', opt.targets[0]):
            opt.interval = float(opt.targets[0])
            opt.targets = opt.targets[1:]

    assert(len(opt.targets) > 0)
    for t in opt.targets:
        if re.match(r'^\d+$', t):
            assert(int(t) in range(len(slist)))
        else:
            assert(t in valid_targets)

    return opt

#opt = parse_cmdline()
#for attr in dir(opt):
#    if not attr.startswith('_'):
#        print getattr(opt, attr)

# handler functions: compile
def compile(opt, slist):
    num_compile = 0
    succeed_targets = []
    failed_targets = []

    for s in slist:
        if s.target not in opt.targets: continue
        make_stat = 'make TARGET={0} -j8 2>/dev/stdout 1>/dev/null'.format(Config.target_name(s.target))
        if opt.rebuild:
            make_stat = 'make cleanall;' + make_stat

        os.chdir(s.code)
        retcode = call(make_stat, shell=True)
        num_compile = num_compile + 1
        if retcode == 0:
            succeed_targets.append(s.target)
        else:
            failed_targets.append(s.target)

    os.chdir(Config.root)
    print 'number of compile: ' + str(num_compile)
    print 'succeed targets:\n\t' + '\n\t'.join(succeed_targets)
    print 'failed targets:\n\t' + '\n\t'.join(failed_targets)

# handler functions: install
def install(opt, slist):
    num_installation = 0
    update_targets = []
    failed_targets = []
    uptodate_targets = []
    for s in slist:
        if s.target not in opt.targets: continue
        f_compiled = path.join(s.code, Config.target_name(s.target))
        f_current = path.join(s.run, Config.target_name(s.target))
        if path.exists(f_compiled) and (not path.exists(f_current) or path.getctime(f_compiled) > path.getctime(f_current)):
            num_installation = num_installation + 1
            mv_stat = 'mv {0} {1}'.format(f_compiled, f_current)
            if 0 == call(mv_stat, shell=True):
                update_targets.append(s.target)
            else:
                failed_targets.append(s.target)
        else:
            uptodate_targets.append(s.target)

    print 'num of installation: ' + str(num_installation)
    print 'updated targets:\n\t' + '\n\t'.join(update_targets)
    print 'up-to-date targets:\n\t' + '\n\t'.join(uptodate_targets)
    print 'failed targets:\n\t' + '\n\t'.join(failed_targets)

# handler functions: list_proc
def list_proc(opt, slist):
    output_str = '--------------------------------------------------\n'
    for i in range(len(slist)):
        s = slist[i]
        if s.target not in opt.targets: continue
        pstat_script = """
        pid=`ps ax|awk -v pn={0} -v r=1 \'$0~pn && $0!~/awk/ {{ print $1; r=0 }} END {{ exit r }}\'`
        retcode=$?
        if [ ! $retcode -eq 0 ]
        then
            exit $retcode
        fi
        echo $pid
        netstat -natp|awk -v p=$pid '$0 ~ p {{ print $4,$5,$6 }}'
        """.format(Config.target_name(s.target))
        output = None
        active = False
        with tempfile.NamedTemporaryFile() as f:
            f.write(pstat_script)
            f.flush()
            try:
                output = str.splitlines(check_output(['/bin/sh', f.name]))
                active = True
            except subprocess.CalledProcessError:
                pass

        if active:
            output_str += '| {0:<4}[active] {1}/{2}\n|\t'.format(str(i) + '.', s.target, output[0])
            output_str += '\n|\t'.join(output[1:]) + '\n'
        else:
            output_str += '| {0:<4}[inactive] {1}\n'.format(str(i) + '.', s.target)

    output_str += '--------------------------------------------------'
    print output_str

def tail_log(opt, slist):
    for s in slist:
        if s.target == opt.targets[0]:
            logpath = path.join(s.run, 'XJCardPlat/{0}/XJCardPlat.{0}.log'.format(s.target))
            cmd = 'viewlog_xj.sh ' + logpath
            if len(opt.cmdline) > 0:
                cmd += ' \'{0}\''.format(opt.cmdline[0])
            if len(opt.cmdline) > 1:
                cmd += ' ' + opt.cmdline[1]

            try:
                call(cmd, shell=True)
            except KeyboardInterrupt:
                pass
            break

def debug(opt, slist):
    for s in slist:
        if s.target == opt.targets[0]:
            #cmd_pid = 'ps h -C {0} -o "%p"'.format(Config.target_name(s.target))
            cmd_pid = 'ps ax|awk -v pn={0} -v r=1 \'$0~pn && $0!~/awk/ {{ print $1; r=0 }} END {{ exit r }}\'' \
                    .format(Config.target_name(s.target))
            try:
                pid = check_output(cmd_pid, shell=True)
            except subprocess.CalledProcessError:
                print 'unable to fetch pid, probably the process doesn\'t exists'
                break
            cmd_gdb = 'gdb --pid={0} {1}'.format(int(pid), path.join(s.run, Config.target_name(s.target)))
            call(cmd_gdb, shell=True)
            break

def run(opt, slist):
    run_list = []
    already_run_list = []
    for t in opt.targets:
        s = Server.find(slist, t)
        cmd_pid = 'ps ax|awk -v pn={0} -v r=1 \'$0~pn && $0!~/awk/ {{ r=0 }} END {{ exit r }}\'' \
                .format(Config.target_name(s.target))
        try:
            check_call(cmd_pid, shell=True)
            already_run_list.append(s.target)
            continue
        except subprocess.CalledProcessError:
            pass

        cmd_run = './{0} --config={1} 1>/dev/null 2>&1 &' \
                .format(Config.target_name(s.target), s.conf)
        os.chdir(s.run)
        call(cmd_run, shell=True)
        run_list.append(s.target)
        time.sleep(opt.interval)

    print 'run:\n\t' + '\n\t'.join(run_list)
    print 'already running:\n\t' + '\n\t'.join(already_run_list)

def stop(opt, slist):
    for t in opt.targets:
        cmd_kill = 'ps ax|awk -v pn={0} -v r=1 \'$0~pn && $0!~/awk/ {{ print "kill -9", $1; r=0 }} END {{ exit r }}\'|sh'.format(Config.target_name(t))
        call(cmd_kill, shell=True)
        if t == 'IStorageMgr':
            call('ipcs -m|awk \'$6 == 0 { print "ipcrm -m", $2 }\'|sh', shell=True)

def restart(opt, slist):
    stop(opt, slist)
    run(opt, slist)

cmd_handlers = {
        'compile':compile,
        'install':install,
        'list':list_proc,
        'log':tail_log,
        'debug':debug,
        'run':run,
        'stop':stop,
        'restart':restart,
        }

################################################################
opt = parse_cmdline(server_list)
cmd_handlers[opt.cmd](opt, server_list)

