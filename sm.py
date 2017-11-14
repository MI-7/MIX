from utility import *
from logger import *

class MySM:
    def start(self):
        self.state = self.startState
        self.halted = False
    
    def getNextValues(self, state, inp, verbose=False):
        nextState = self.getNextState(state, inp)
        return (nextState, nextState)
    
    def step(self, inp, verbose=False, compact=False):
        (s, o) = self.getNextValues(self.state, inp, verbose)
        self.state = s

        if verbose:
            mixlog(MDEBUG, 'output of sm: ', o)
        
        return o
    
    def transduce(self, inputs, verbose=False, compact=False):
        self.start()

        if verbose:
            mixlog (MDEBUG, 'Start state: ' + str(self.startState) + ' .. inputs: ' + str(inputs))
        
        return [self.step(inp, verbose, compact) for inp in inputs if not self.done(self.state)]
    
    def run(self, n=10, verbose=False):
        return self.transduce([undef]*n, verbose)

    def go(self, verbose=False, compact=False):
        self.start()
        
        while(not self.done(self.state)):
            self.step(undef, verbose, compact)
    
    def resume(self, verbose=False, compact=False):
        self.halted = False
        while(not self.done(self.state)):
            self.step(undef, verbose, compact)

    def done(self, state):
        return False

class Accumulator(MySM):
    startState = 0

    def __init__(self, initialValue):
        self.startState = initialValue

    def getNextValues(self, state, inp, verbose=False):
        return (safeAdd(state, inp), safeAdd(state, inp))


class Delay(MySM):
    def __init__(self, v0=0):
        self.startState = v0

    def getNextValues(self, state, inp, verbose=False):
        if verbose:
            print('Delay..' + ' In: ' + str(inp) + ' Out: ' + str(state) + ' Next State: ' + str(inp))
        return (inp, state)

class Constant(MySM):
    def __init__(self, v):
        self.startState = v

    def getNextValues(self, state, inp, verbose=False):
        if verbose:
            print ('Constant..' + ' In: ' + str(inp) + ' Out: ' + str(self.startState) + ' Next State: ' + str(self.startState))
        return (self.startState, self.startState)

class Average2(MySM):
    startState = 0

    def getNextValues(self, state, inp, verbose=False):
        return (inp, (safeDivide(safeAdd(inp, state), 2.0)))

class SumLastThree(MySM):
    startState = (0, 0)

    def getNextValues(self, state, inp, verbose=False):
        return ((state[1], inp), safeAdd(safeAdd(state[0], state[1]), inp))

class Increment(MySM):
    def __init__(self, incr):
        self.incr = incr
        self.startState = undef

    def getNextValues(self, state, inp, verbose=False):
        if verbose:
            print('Increment..' + ' In: ' + str(inp) + ' Out: ' + str(safeAdd(inp, self.incr)) + ' Next State: ' + str(safeAdd(inp, self.incr)))
        return (safeAdd(inp, self.incr), safeAdd(inp, self.incr))

class Adder(MySM):
    def __init__(self):
        self.startState = undef
    def getNextValues(self, state, inp, verbose=False):
        (i1, i2) = splitValue(inp, 2)
        if verbose:
            print('Adder..' + ' In: ' + str(inp) + ' Out: ' + str(safeAdd(i1, i2)) + ' Next State: ' + str(safeAdd(i1, i2)))
        return (safeAdd(i1, i2), safeAdd(i1, i2))

class Multiplier(MySM):
    def __init__(self):
        self.startState = undef
    def getNextValues(self, state, inp, verbose=False):
        (i1, i2) = splitValue(inp, 2)
        if verbose:
            print('Multiplier..'+ ' In: '+ str(inp), ' Out: '+ str(safeMultiply(i1, i2))+ ' Next State: '+ str(safeMultiply(i1, i2)))
        return (safeMultiply(i1, i2), safeMultiply(i1, i2))

class DoubleDelay(MySM):
    def __init__(self, initialState):
        self.startState = initialState

    def getNextValues(self, state, inp, verbose=False):
        (ppstate, pstate) = splitValue(state, 2)
        if verbose:
            print('Double Delay..'+ ' In: '+ str(inp)+ ' Out: '+ str(ppstate)+ ' Next State: '+ str((pstate, inp)))
        return ((pstate, inp), ppstate)

class TripleDelay(MySM):
    def __init__(self, initialState):
        self.startState = initialState
    def getNextValues(self, state, inp, verbose=False):
        (pppstate, ppstate, pstate) = splitValue(state, 3)
        if verbose:
            print('Triple Delay..'+ ' In: '+ str(inp)+ ' Out: '+str(pppstate)+ ' Next State: '+ str((ppstate, pstate, inp)))
        return ((ppstate, pstate, inp), pppstate)

class Wire(MySM):
    def __init__(self):
        self.startState = undef

    def getNextValues(self, state, inp, verbose=False):
        return (inp, inp)

