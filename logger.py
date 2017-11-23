import datetime
import inspect

MDEBUG = 2
MINFO = 1
MERROR = 0
MIX_LOG_LEVEL = MINFO

LOG_FILE = './log.log'
f_logger = open(LOG_FILE, 'a')

# 0-7, level
# 8 - 15, time
# 16 - end, message
def mixlog(level, *message):
    header = ''
    if (level <= MIX_LOG_LEVEL):
        ts = str(datetime.datetime.now())
        if (level == MERROR):
            header = 'error   ' + ts + '    '
        elif (level == MINFO):
            header = 'info    ' + ts + '    '
        elif (level == MDEBUG):
            header = 'debug   ' + ts + '    '
        
        curframe = inspect.currentframe()
        caller = inspect.getouterframes(curframe, 2)
        callername = caller[1][3]
        header = header + callername.ljust(15) + '    '
        
        print(header, message, file=f_logger)
        f_logger.flush()

if __name__ == "__main__":
    mixlog(MDEBUG, "test")
    mixlog(MDEBUG, "hi there", )
    mixlog(MINFO ,"server started")
    mixlog(MERROR, "serious trouble")