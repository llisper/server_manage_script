from os import path
from subprocess import call
from .. import util

def cmd_log(opt, slist, pattern='', color=''):
    s = next(util.next_target(opt, slist))[1]
    logpath = path.join(s.run, 'XJCardPlat/{0}/XJCardPlat.{0}.log'.format(s.target))
    cmd = 'viewlog_xj.sh {0} {1} {2}'.format(logpath, pattern, color)
    try:
        call(cmd, shell=True)
    except KeyboardInterrupt:
        pass
