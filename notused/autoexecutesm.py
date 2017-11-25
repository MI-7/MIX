from mixsm import MixSM
from nextstatementsm import NextStatementSM

from mixinterpreter.sm import MySM
from utility import *


class AutoExecuteSM(MySM):
    def __init__(self, sm_code, sm_executor):
        self.sm_code = sm_code
        self.sm_executor = sm_executor
        self.startState = (sm_code.startState, sm_executor.startState)
    
    def getNextValues(self, state, inp, verbose=False):
        (s1, s2) = splitValue(state, 2)
        (news1, o1) = self.sm_code.getNextValues(s1, inp, verbose)
        code = o1[0]
        (news2, o2) = self.sm_executor.getNextValues(s2, code, verbose)
        return ((news1, news2), o2)
    
    def done(self, state):
        (s1, s2) = state
        return self.sm_code.done(s1)

if __name__ == "__main__":
    sm = AutoExecuteSM(NextStatementSM(["1", "2", "3", "5", "5", "6"], 0), MixSM())
    sm.start()
    sm.go(True)
    
    counter_iv = 256  # Can be from 0 to 3.40e38
    print(str(counter_iv).encode())
    #https://stackoverflow.com/questions/14043886/python-2-3-convert-integer-to-bytes-cleanly#comment45417875_14044431
    