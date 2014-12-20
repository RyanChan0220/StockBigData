__author__ = 'Ryan'

import time
from functools import wraps


def decorator_run_time(func):
    @wraps(func)
    def wraper(*args, **kwds):
        print "Timer running..."
        time_start = time.time()
        ret = func(*args, **kwds)
        time_end = time.time()
        print "#%s FINISHED# total run out time is: %s" % (func.func_name, str(time_end - time_start))
        return ret
    return wraper