import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from memorystate import MemoryState
from utility import *
from logger import *
from sm import MySM

class LittleExtractStringSM(MySM):
    def __init__(self):
        self.startState = 'start'
        self.output = ''
    
    def getNextValues(self, state, inp, verbose=False):
        s = state
        if (s == 'start' and inp == "*"):
            self.output = inp
            s = 'end'
        elif (s == 'start' and inp.isalpha()):
            s = 'alpha'
            self.output = self.output + inp
        elif (s == 'alpha' and inp.isalpha()):
            self.output = self.output + inp
        elif (s == 'alpha' and not inp.isalpha()):
            s = 'end'
        
        return (s, self.output)
    
    def done(self, state):
        return state == 'end'

class MixALPreProcessor():
    def __init__(self, mix_code):
        self.mix_code = mix_code
        self.orig = 0
        self.end = 0
        self.symboltable = {}
        self.processed_code = []
        self.processed_code_dict = {}
        
        self.buildsymboltable()
    
    def buildsymboltable(self):
        # 0-7 = symbol name
        # 8-15 = op
        # 16-end = address
        current_line = 0
        orig_line = 0
        for s in self.mix_code:
            loc = ''.join(s[0:7].split())
            op = ''.join(s[8:15].split())
            
            comment_pos = s.find("#")
            addr = ''
            if (comment_pos == -1):
                addr = ''.join(s[16:].split())
            else:
                addr = ''.join(s[16:comment_pos].split())
            
            loc.upper()
            op.upper()
            addr.upper()
            
            mixlog (MDEBUG, loc, op, addr)
            
            if (op == "EQU"):
                self.symboltable[loc] = addr
            elif (op == "ORIG"):
                self.orig = my_int(addr)
                orig_line = current_line
            elif (op == 'END'):
                if (loc != ''):
                    self.symboltable[loc] = current_line - orig_line - 1 + self.orig
                self.end = current_line - orig_line - 1 + self.orig
            else:
                if (loc != ''):# and op == 'STJ'):
                    # MAX STJ EXIT
                    #self.runtime_symboltable[addr] = ''
                    #self.symboltable[loc] = current_line - orig_line - 1 + self.orig
                #elif (loc != '' and op == 'JMP'):
                    # EXIT JMP *, DON'T ADD A SYMBOL, EXIT MUST BE DECIDED IN RUN TIME
                    #pass
                #elif (loc != ''):
                    self.symboltable[loc] = current_line - orig_line - 1 + self.orig
            
            current_line = current_line + 1
        
        mixlog (MDEBUG, 'symbol table:', self.symboltable)
        mixlog (MDEBUG, 'processed code:', self.processed_code)
    
    def preprocessall(self):
        current_line = 0
        orig_line = 0
        for s in self.mix_code:
            loc = ''.join(s[0:7].split())
            op = ''.join(s[8:15].split())
            
            comment_pos = s.find("#")
            addr = ''
            if (comment_pos == -1):
                addr = ''.join(s[16:].split())
            else:
                addr = ''.join(s[16:comment_pos].split())
            
            loc.upper()
            op.upper()
            addr.upper()
            
            mixlog (MDEBUG, loc, op, addr)
            
            if (op == "ORIG"):
                orig_line = current_line
            
            symbol = ''
            if (op != "EQU" and op != "ORIG"):
                sm = LittleExtractStringSM()
                sm.transduce(list(addr), verbose=True)
                symbol = sm.output
                
                if (symbol != '' and symbol != '*'):
                    # EXIT JMP *
                    #if (symbol in self.runtime_symboltable):
                        #pass
                    #else:
                    addr = addr.replace(symbol, str(self.symboltable[symbol]))
                elif (symbol != '' and symbol == '*'):
                    #if (loc != '' and op == 'JMP'):
                        # EXIT JMP *
                        #self.processed_code.append(loc + " " + op + " " + addr)
                        #self.processed_code_dict[current_line - orig_line - 1 + self.orig] = loc + " " + op + " " + addr
                        #current_line = current_line + 1
                        #continue
                    #else:
                        # todo: *,3 and *+3 are different
                    addr = str(eval(addr.replace('*', str(current_line - orig_line - 1 + self.orig))))

                self.processed_code.append(op + " " + addr)
                self.processed_code_dict[current_line - orig_line - 1 + self.orig] = op + " " + addr
            
            current_line = current_line + 1
        
        #mixlog(MDEBUG, "runtime symbol table:", self.runtime_symboltable)
        mixlog (MDEBUG, 'symbol table:', self.symboltable)
        mixlog (MDEBUG, 'processed code:', self.processed_code)
        mixlog (MDEBUG, "processed code dict:", self.processed_code_dict)
    
    def preprocess(self, statement):
        pass

if __name__ == "__main__":
    code_text_in_list = []
    fname = './test_programs/test_program_win.txt'

    f = open(fname, 'r')
    with f:
        code_text_in_list = f.read().splitlines()
        #print(self.code_text_in_list)
    f.close()
    
    mapp = MixALPreProcessor(code_text_in_list, MemoryState())
    mapp.preprocessall()
    
    #sm = LittleExtractStringSM()
    #sm.transduce(list("0,1"), verbose=True)
    #mixlog(MDEBUG, sm.output)