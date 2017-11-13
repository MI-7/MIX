from sm import MySM
from memorystate import MemoryState

class MixSM(MySM):
    def __init__(self):
        self.startState = MemoryState()

    def getNextValues(self, state, inp, verbose=False):
        return (inp, inp)