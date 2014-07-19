import tempfile
from subprocess import check_output, CalledProcessError
from module.config import Config
from module import util

def cmd_list(opt, slist):
    output_str = '--------------------------------------------------\n'
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
            output_str += '| {0:<4}[active] {1}/{2}\n|\t'.format(str(i) + '.', s.target, output[0])
            output_str += '\n|\t'.join(output[1:]) + '\n'
        else:
            output_str += '| {0:<4}[inactive] {1}\n'.format(str(i) + '.', s.target)

    output_str += '--------------------------------------------------'
    print output_str
