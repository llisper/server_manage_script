import os
import time
from subprocess import call, check_call, CalledProcessError
from .. import util
from ..config import Config

def cmd_run(opt, slist):
    run_list = []
    already_run_list = []
    for i, s in util.next_target(opt, slist):
        cmd_pid = 'ps ax|awk -v pn={0} -v r=1 \'$0~"[.]/"pn {{ r=0 }} END {{ exit r }}\'' \
                .format(Config.target_name(s.target))
        try:
            check_call(cmd_pid, shell=True)
            already_run_list.append(s.target)
            continue
        except CalledProcessError:
            pass

        cmd_run = './{0} --config={1} 1>/dev/null 2>&1 &' \
                .format(Config.target_name(s.target), s.conf)
        os.chdir(s.run)
        call(cmd_run, shell=True)
        run_list.append(s.target)
        time.sleep(opt.interval)

    print 'run:\n\t' + '\n\t'.join(run_list)
    print 'already running:\n\t' + '\n\t'.join(already_run_list)
