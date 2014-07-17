from os import path
from subprocess import call
from ..config import Config
from .. import util

def cmd_install(opt, slist):
    num_installation = 0
    update_targets = []
    failed_targets = []
    uptodate_targets = []

    for i, s in util.next_target(opt, slist):
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
