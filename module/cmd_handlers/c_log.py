from os import path
from module import util
from module import logutil

def cmd_log(opt, slist):
    s = next(util.next_target(opt, slist))[1]
    logpath = path.join(s.run, 'XJCardPlat/{0}/XJCardPlat.{0}.log'.format(s.target))
    logutil.track(logpath, *opt.args[:2])
    return 0
