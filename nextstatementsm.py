from sm import MySM
from utility import *

class NextStatementSM(MySM):
    def __init__(self, textinlist, current_line):
        self.startState = (textinlist, current_line)

    def isJumper(self, line):
        return False

    def getNextValues(self, state, inp, verbose=False):
        (textinlist, current_line) = state
        
        if (not self.isJumper(textinlist[current_line])):
            return ((textinlist, current_line + 1), (textinlist[current_line], current_line + 1))
        else:
            pass
    
    def done(self, state):
        (textinlist, current_line) = state
        return len(textinlist) == current_line
        

if __name__ == '__main__':
    sm = NextStatementSM(["1", "2", "3", "5", "5", "6"], 0)
    sm.start()
    print(sm.step(undef))
    #sm.go(True)
