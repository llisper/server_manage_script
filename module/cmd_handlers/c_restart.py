import time
import c_stop
import c_run

def cmd_restart(opt, slist):
    c_stop.cmd_stop(opt, slist)
    time.sleep(1.0)
    return c_run.cmd_run(opt, slist)
