import time
from subprocess import call
from ..config import Config
from .. import util

def cmd_stop(opt, slist):
    t = 'ps ax|awk -v pn={0} -v r=1 \'$0~pn && $0!~/awk/ {{ print "{1}", $1; r=0 }} END {{ exit r }}\''
    for i, s in util.next_target(opt, slist):
        name = Config.target_name(s.target)
        cmd_kill = t.format(name, 'kill -9') + '|sh'
        call(cmd_kill, shell=True)

        cmd_check = t.format(name, '')
        while 0 == call(cmd_check, shell=True):
            time.sleep(0.1)

    if opt.clean_shm:
        call('ipcs -m|awk \'$6 == 0 { print "ipcrm -m", $2 }\'|sh', shell=True)
