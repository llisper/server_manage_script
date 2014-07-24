import tempfile
from subprocess import check_output, CalledProcessError
from module.config import Config
from module import util
from module import logutil

def cmd_list(opt, slist):
    output_str = '--------------------------------------------------\n'
    act_fmt = '| {0:<4}[' + logutil.hiswap('up', 'green', logutil.default_debug_color) + '] {1}/{2}\n|\t'
    inact_fmt = '| {0:<4}[' + logutil.hiswap('down', 'red', logutil.default_debug_color) + '] {1}\n'
    for i, s in util.next_target(opt, slist):
        pstat_script = """
        pid=`ps ax|awk -v pn={0} -v r=1 \'$0~"[.]/"pn {{ print $1; r=0 }} END {{ exit r }}\'`
        retcode=$?
        if [ ! $retcode -eq 0 ]
        then
            exit $retcode
        fi
        echo $pid
        netstat -natp|awk -v p=$pid '$0 ~ p {{ print $4,$5,$6 }}'
        """.format(Config.target_name(s.target))
        output = None
        active = False
        with tempfile.NamedTemporaryFile() as f:
            f.write(pstat_script)
            f.flush()
            try:
                output = str.splitlines(check_output(['/bin/sh', f.name]))
                active = True
            except CalledProcessError:
                pass

        if active:
            output_str += act_fmt.format(str(i) + '.', logutil.hiswap(s.target, 'green', logutil.default_debug_color), output[0])
            output_str += '\n|\t'.join(output[1:]) + '\n'
        else:
            output_str += inact_fmt.format(str(i) + '.', s.target)

    output_str += '--------------------------------------------------'
    logutil.debug(output_str)
