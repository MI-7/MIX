import sys
from logger import *
from mixinterpreter.memorystate import MemoryState
from mixinterpreter.sm import MySM
from utility import *


class LittleExtractStringSM(MySM):
    def __init__(self):
        self.startState = 'start'
        self.output = ''
        self.allowed_input = ['@', '*', '+', '-', '/', ' ']

    def getNextValues(self, state, inp, verbose=False):
        s = state
        if s == 'start' and (inp.isalpha() or inp.isnumeric() or inp in self.allowed_input):
            s = 'alpha'
            self.output = self.output + inp
        elif s == 'alpha' and (inp.isalpha() or inp.isnumeric() or inp in self.allowed_input):
            self.output = self.output + inp
        else:
            s = 'end'

        return s, self.output

    def done(self, state):
        return state == 'end'


class LittleExtractAllWordsSM(MySM):
    def __init__(self):
        self.startState = 'start'
        self.output = []
        self.word = ''

    def getNextValues(self, state, inp, verbose=False):
        if state == 'start' and (inp.isalpha() or inp.isnumeric()):
            state = 'alpha'
            self.word = self.word + inp
        elif state == 'alpha' and (inp.isalpha() or inp.isnumeric()):
            self.word = self.word + inp
        else:
            state = 'start'
            self.output.append(self.word)
            self.word = ''

        return state, self.output


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
            if comment_pos == -1:
                addr = ''.join(s[16:].split())
            else:
                addr = ''.join(s[16:comment_pos].split())

            loc.upper()
            op.upper()
            addr.upper()

            mixlog(MDEBUG, loc, op, addr)

            if op == "EQU":
                for key in self.symboltable.keys():
                    if key in addr:
                        addr = addr.replace(key, str(self.symboltable[key]))

                # keep the string as is, e.g. X EQU 3:5, this cannot be evaluated.
                # self.symboltable[loc] = int(eval(addr))
                self.symboltable[loc] = addr
            elif op == "ORIG":
                for key in self.symboltable.keys():
                    if key in addr:
                        addr = addr.replace(key, str(self.symboltable[key]))
                self.orig = int(eval(addr))
                orig_line = current_line
            elif op == 'END':
                if loc != '':
                    self.symboltable[loc] = current_line - orig_line - 1 + self.orig
                self.end = current_line - orig_line - 1 + self.orig
            else:
                if loc != '':  # and op == 'STJ'):
                    # MAX STJ EXIT
                    # self.runtime_symboltable[addr] = ''
                    # self.symboltable[loc] = current_line - orig_line - 1 + self.orig
                    # elif (loc != '' and op == 'JMP'):
                    # EXIT JMP *, DON'T ADD A SYMBOL, EXIT MUST BE DECIDED IN RUN TIME
                    # pass
                    # elif (loc != ''):
                    self.symboltable[loc] = current_line - orig_line - 1 + self.orig

            current_line = current_line + 1

        mixlog(MDEBUG, 'symbol table:', self.symboltable)
        mixlog(MDEBUG, 'processed code:', self.processed_code)

    def preprocessall(self):
        current_line = 0
        orig_line = 0
        for s in self.mix_code:
            loc = ''.join(s[0:7].split())
            op = ''.join(s[8:15].split())

            comment_pos = s.find("#")
            addr = ''
            if comment_pos == -1:
                addr = ''.join(s[16:].split())
            else:
                addr = ''.join(s[16:comment_pos].split())

            loc.upper()
            op.upper()
            addr.upper()

            mixlog(MDEBUG, loc, op, addr)

            if op == "ORIG":
                orig_line = current_line

            symbol = ''
            if op != "EQU" and op != "ORIG":
                # deal with address part
                sm = LittleExtractStringSM()
                sm.transduce(list(addr), verbose=True)
                symbol = sm.output

                wordsm = LittleExtractAllWordsSM()
                wordsm.transduce(list(symbol), verbose=True)
                words_in_symbol = wordsm.output
                words_in_symbol.append(wordsm.word)

                for key in self.symboltable.keys():
                    if key in words_in_symbol:
                        symbol = symbol.replace(key, str(self.symboltable[key]))

                if '@' in symbol:
                    symbol = symbol.replace('@', str(current_line - orig_line - 1 + self.orig))

                try:
                    symbol = str(int(eval(symbol)))
                except Exception as err:
                    mixlog(MERROR, 'symbol eval failure', err)
                    sys.exit()

                # deal with i, f part
                comma_pos = addr.find(',')
                left_paren_pos = addr.find('(')
                if_part = ''
                if comma_pos != -1:
                    if_part = addr[comma_pos:]
                    wordsm = LittleExtractAllWordsSM()
                    wordsm.transduce(list(if_part), verbose=True)
                    words_in_symbol = wordsm.output
                    words_in_symbol.append(wordsm.word)

                    for key in self.symboltable.keys():
                        if key in words_in_symbol:
                            if_part = if_part.replace(key, str(self.symboltable[key]))
                elif comma_pos == -1 and left_paren_pos != -1:
                    if_part = addr[left_paren_pos:]
                    wordsm = LittleExtractAllWordsSM()
                    wordsm.transduce(list(if_part), verbose=True)
                    words_in_symbol = wordsm.output
                    words_in_symbol.append(wordsm.word)

                    for key in self.symboltable.keys():
                        if key in words_in_symbol:
                            if_part = if_part.replace(key, str(self.symboltable[key]))

                # if symbol != '' and symbol != '*':
                    # EXIT JMP *
                    # if (symbol in self.runtime_symboltable):
                    # pass
                    # else:
                    # addr = addr.replace(symbol, str(self.symboltable[symbol]))
                # elif symbol != '' and symbol == '*':
                    # if (loc != '' and op == 'JMP'):
                    # EXIT JMP *
                    # self.processed_code.append(loc + " " + op + " " + addr)
                    # self.processed_code_dict[current_line - orig_line - 1 + self.orig] = loc + " " + op + " " + addr
                    # current_line = current_line + 1
                    # continue
                    # else:
                    # todo: *,3 and *+3 are different
                    # addr = str(eval(addr.replace('*', str(current_line - orig_line - 1 + self.orig))))

                self.processed_code.append(op + " " + symbol + if_part)
                self.processed_code_dict[current_line - orig_line - 1 + self.orig] = op + " " + symbol + if_part

            current_line = current_line + 1

        # mixlog(MDEBUG, "runtime symbol table:", self.runtime_symboltable)
        mixlog(MDEBUG, 'symbol table:', self.symboltable)
        mixlog(MDEBUG, 'processed code:', self.processed_code)
        mixlog(MDEBUG, "processed code dict:", self.processed_code_dict)

    def preprocess(self, statement):
        pass


if __name__ == "__main__":
    code_text_in_list = []
    fname = '../test_programs/test_program_testpreprocess.txt'

    f = open(fname, 'r')
    with f:
        code_text_in_list = f.read().splitlines()
        # print(self.code_text_in_list)
    f.close()

    mapp = MixALPreProcessor(code_text_in_list)
    mapp.preprocessall()

    # sm = LittleExtractStringSM()
    # sm.transduce(list("0,1"), verbose=True)
    # mixlog(MDEBUG, sm.output)
