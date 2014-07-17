import signal
from os import path
from subprocess import call, check_output, CalledProcessError
from .. import util
from ..config import Config

def cmd_debug(opt, slist):
    s = next(util.next_target(opt, slist))[1]
    cmd_pid = 'ps ax|awk -v pn={0} -v r=1 \'$0~"/"pn {{ print $1; r=0 }} END {{ exit r }}\'' \
            .format(Config.target_name(s.target))
    try:
        pid = check_output(cmd_pid, shell=True)
    except subprocess.CalledProcessError:
        print 'unable to fetch pid, probably the process doesn\'t exists'
        return

    cmd_gdb = 'gdb --pid={0} {1}'.format(int(pid), path.join(s.run, Config.target_name(s.target)))
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    call(cmd_gdb, shell=True)
