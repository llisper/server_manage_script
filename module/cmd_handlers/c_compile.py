import os
from subprocess import call
from module.config import Config
from module import util
from module import logutil

def cmd_compile(opt, slist):
    num_compile = 0
    succeed_targets = []
    failed_targets = []

    for i, s in util.next_target(opt, slist):
        make_stat = 'make TARGET={0} -j8 2>/dev/stdout 1>/dev/null'.format(Config.target_name(s.target))
        if opt.rebuild:
            make_stat = 'make cleanall 2>/dev/stdout 1>/dev/null && ' + make_stat

        os.chdir(s.code)
        logutil.debug('compiling ' + s.target + ': ' + make_stat, 'yellow')
        retcode = call(make_stat, shell=True)
        num_compile = num_compile + 1
        if retcode == 0:
            succeed_targets.append(s.target)
        else:
            failed_targets.append(s.target)

    os.chdir(Config.root)
    logutil.debug('number of compile: ' + str(num_compile))
    logutil.debug('succeed targets:\n\t' + '\n\t'.join(succeed_targets))
    logutil.debug('failed targets:\n\t' + '\n\t'.join(failed_targets))
