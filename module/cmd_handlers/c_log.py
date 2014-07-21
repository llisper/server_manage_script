from os import path
from subprocess import call
from module import util

colors = {
        'black' :r'\\e[0;30m',
        'red'   :r'\\e[0;31m',
        'green' :r'\\e[0;32m',
        'yellow':r'\\e[0;33m',
        'blue'  :r'\\e[0;34m',
        'purple':r'\\e[0;35m',
        'cyan'  :r'\\e[0;36m',
        'white' :r'\\e[0;37m',
        }

def cmd_log(opt, slist):
    s = next(util.next_target(opt, slist))[1]
    logpath = path.join(s.run, 'XJCardPlat/{0}/XJCardPlat.{0}.log'.format(s.target))
    pattern = len(opt.args) > 0 and opt.args[0] or ''
    color = ''
    if (len(opt.args) > 1 and opt.args[1] in colors):
        color = colors[opt.args[1]]

    script = """
    tail -f {0}|awk '
    !/^$/ {{
        if ($0 ~ /{1}/)
            system("echo -e \\"{2}" $0 "\\\\e[0m\\"")
        else
            print $0
    }}' """.format(logpath, pattern, color)

    #print script
    try:
        call(script, shell=True)
    except KeyboardInterrupt:
        pass
