from os import path
from subprocess import call
from module import util

def cmd_log(opt, slist):
    s = next(util.next_target(opt, slist))[1]
    logpath = path.join(s.run, 'XJCardPlat/{0}/XJCardPlat.{0}.log'.format(s.target))
    pattern = len(opt.args) > 0 and opt.args[0] or ''
    color = len(opt.args) > 1 and opt.args[1] or ''
    cmd = 'viewlog_xj.sh {0} {1} {2}'.format(logpath, pattern, color)
    try:
        call(cmd, shell=True)
    except KeyboardInterrupt:
        pass
