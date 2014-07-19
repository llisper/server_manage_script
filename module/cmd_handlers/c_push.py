import sys
from subprocess import call

svr_map = { 'fr' : 10013, 'syt': 10014, 'rs' : 21705, 'rst': 21706, 'rls': 21707, 'gs': 39997 }

def cmd_push(opt, slist):
    if opt.service_name == 'print':
        print 'server port mapping:'
        for i in svr_map:
            print '{0} -> {1}'.format(i, svr_map[i])
        return

    if svr_map.has_key(opt.service_name):
        cmd = '/usr/local/taf/bin/tafadminclient --ipport=10.1.152.64:{0} --command="{1}"' \
                .format(svr_map[opt.service_name], ' '.join(opt.args))
        call(cmd, shell=True)
