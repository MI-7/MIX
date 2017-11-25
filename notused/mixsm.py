from memorystate import MemoryState

from mixinterpreter.sm import MySM


class MixSM(MySM):
    def __init__(self):
        self.startState = MemoryState()

    def getNextValues(self, state, inp, verbose=False):
        return (inp, inp)