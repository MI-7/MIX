from sm import MySM
from utility import *
from mixstatement import *

# return (sym, AA, I, F, op, C)
class MixToMachineCodeTranslatorSM(MySM):
    # OP ADDRESS, I(F)
    # LDA 2000, 2(0:3)
    # LDA 2000, 2(1:3)
    # LDA 2000(1:3)
    # LDA 2000
    # LDA -2000, 4
    
    def __init__(self):
        self.op = ""
        self.c = 0
        self.i = "0"
        self.l = "0"
        self.r = str(WORD_WIDTH)
        self.sym = "+"
        self.aa = ""
        
        self.startState = "op"
        self.output = None
    
    def getNextValues(self, state, inp, verbose=False):
        s = state
        if (s == "op" and inp.isalpha()):
            self.op = self.op + inp
        elif (s == "op" and inp.isnumeric()):
            self.op = self.op + inp
        elif (s == "op" and inp.isspace()):
            s = "addr"
            if (self.op in statementdict):
                self.c = statementdict[self.op]
        elif (s == "addr" and inp == "-"):
            self.sym = "-"
            self.aa = self.aa + inp
        elif (s == "addr" and inp.isnumeric()):
            self.aa = self.aa + inp
        # For STJ EXIT
        elif (s == 'addr' and inp.isalpha()):
            self.aa = self.aa + inp
        elif (s == "addr" and inp == ","):
            s = "i"
        elif (s == "addr" and inp == "("):
            s = "L"
        elif (s == "i" and inp.isnumeric()):
            if (self.i == "0"):
                self.i = inp
            else:
                self.i = self.i + inp
        elif (s == "i" and inp == "("):
            s = "L"
        elif (s == "L" and inp.isnumeric()):
            self.l = self.l + inp
        elif (s == "L" and inp == ":"):
            s = "R"
        elif (s == "R" and inp.isnumeric()):
            # if we have some input for R, then we abandon the default "5"
            if (self.r != ''):
                self.r = inp
            else:
                self.r = self.r + inp
        elif (s == "R" and inp == ")"):
            s = "end"
        
        self.output = (self.sym, self.aa, my_int(self.i), LPLUSR(my_int(self.l), my_int(self.r)), self.op, self.c)
        #print(self.output) 
        return (s, (self.sym, self.aa, my_int(self.i), LPLUSR(my_int(self.l), my_int(self.r)), self.op, self.c))

def testStatementParts():
    sm = MixToMachineCodeTranslatorSM()
    sm.transduce([x for x in "LDA 2000,2 (0:3)"], False)
    print (sm.output)
    
    sm = MixToMachineCodeTranslatorSM()
    sm.transduce([x for x in "LDA 2000,2 (1:3)"], False)
    print (sm.output)
    
    sm = MixToMachineCodeTranslatorSM()
    sm.transduce([x for x in "LDA 2000(1:3)"], False)
    print (sm.output)
    
    sm = MixToMachineCodeTranslatorSM()
    sm.transduce([x for x in "LDA 2000"], False)
    print (sm.output)
    
    sm = MixToMachineCodeTranslatorSM()
    sm.transduce([x for x in "LDA -2000, 4"], False)
    print (sm.output)
    
    sm = MixToMachineCodeTranslatorSM()
    sm.transduce([x for x in "LD3 2000,2 (0:3)"], False)
    print (sm.output)
    
    sm = MixToMachineCodeTranslatorSM()
    sm.transduce([x for x in "LD2 2000,2 (1:3)"], False)
    print (sm.output)
    
    sm = MixToMachineCodeTranslatorSM()
    sm.transduce([x for x in "LD1 2000(1:3)"], False)
    print (sm.output)
    
    sm = MixToMachineCodeTranslatorSM()
    sm.transduce([x for x in "LD2 2000"], False)
    print (sm.output)
    
    sm = MixToMachineCodeTranslatorSM()
    sm.transduce([x for x in "LD3 -2000, 4"], False)
    print (sm.output)
    
# LDA 2000, 2(0:3)
# LDA 2000, 2(1:3)
# LDA 2000(1:3)
# LDA 2000
# LDA -2000, 4
if __name__ == "__main__":
    testStatementParts()