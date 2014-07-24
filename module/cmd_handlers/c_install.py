from os import path
from subprocess import call
from module.config import Config
from module import util
from module import logutil

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

    logutil.debug('num of installation: ' + str(num_installation))
    logutil.debug('updated targets:\n\t' + '\n\t'.join(update_targets))
    logutil.debug('up-to-date targets:\n\t' + '\n\t'.join(uptodate_targets))
    logutil.debug('failed targets:\n\t' + '\n\t'.join(failed_targets))
