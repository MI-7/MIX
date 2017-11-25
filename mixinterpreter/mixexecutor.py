from mixinterpreter.memorystate import *
from mixinterpreter.mixalpreprocessor import *
from mixinterpreter.mixaltomachinecode import *

from mixinterpreter.blockdevice import *
from mixinterpreter.sm import MySM


# execute single line of code
class MixExecutor(MySM):
    def __init__(self, processed_code_dict, orig, end, memory):
        self.processed_code_dict = processed_code_dict
        self.orig = orig
        self.end = end
        self.startState = orig
        self.memory = memory
        self.current_op = ''
        self.profilingresult = {}
        self.halted = False
    
    def getNextValues(self, state, inp, verbose = False):
        mixlog(MDEBUG, "before executing..."+self.processed_code_dict[state], str(self.memory), self.memory.getMemory(1999))
        nexts = self.execute(state)
        mixlog(MDEBUG, "after executing..."+self.processed_code_dict[state], str(self.memory), self.memory.getMemory(1999))
        return (nexts, nexts)
    
    def done(self, state):
        ended = (state == self.end)
        halted = self.halted
        
        if (ended or halted):
            if (ended):
                mixlog(MDEBUG, "profiling result..."+str(self.profilingresult))
            return True
        else:
            return False
    
    def execute(self, current_line):
        #sm = MixToMachineCodeTranslatorSM()
        #sm.transduce([x for x in statement], False)
        (sym, aa1, aa2, i, f, c) = self.memory.getMemory(current_line)
        aa = partstodec_withsign([sym, aa1, aa2])
        next_statement = current_line + 1
        
        # for move instruction profiling, counts how many words have been moved.
        op_moved = 0
        
        op = ''
        for op_key in statementdict.keys():
            if statementdict[op_key] == c:
                op = op_key
                break
        
        #LDA
        if (c == OP_LDA):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            if (f == WORD_WIDTH):
                self.memory.saveA(m)
            else:
                a = self.memory.getA()
                (L, R) = LRFROMF(f)
                
                m_seg = None
                if (L == 0):
                    a[0] = m[0]
                    if (L==R):
                        return #done
                    else:
                        m_seg = m[L+1: R+1]
                else:
                    m_seg = m[L:R+1]
                
                for x in range(6-len(m_seg), 6):
                    a[x] = m_seg[x-6+len(m_seg)]
                self.memory.saveA(a)

        if (c == OP_LDAN):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            if (f == WORD_WIDTH):
                self.memory.saveA(m)
            else:
                a = self.memory.getA()
                (L, R) = LRFROMF(f)
                
                m_seg = None
                if (L == 0):
                    a[0] = negsign(m[0])
                    if (L==R):
                        return #done
                    else:
                        m_seg = m[L+1: R+1]
                else:
                    m_seg = m[L:R+1]
                
                for x in range(6-len(m_seg), 6):
                    if x == 0:
                        a[x] = negsign(m_seg[x-6+len(m_seg)])
                    else:
                        a[x] = m_seg[x-6+len(m_seg)]
                self.memory.saveA(a)

        if (c == OP_LDX):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            if (f == WORD_WIDTH):
                self.memory.saveX(m)
            else:
                x = self.memory.getX()
                (L, R) = LRFROMF(f)
                
                m_seg = None
                if (L == 0):
                    x[0] = m[0]
                    if (L==R):
                        return #done
                    else:
                        m_seg = m[L+1: R+1]
                else:
                    m_seg = m[L:R+1]
                
                for t in range(6-len(m_seg), 6):
                    x[t] = m_seg[t-6+len(m_seg)]
                self.memory.saveX(x)

        if (c == OP_LDXN):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            if (f == WORD_WIDTH):
                self.memory.saveX(m)
            else:
                x = self.memory.getX()
                (L, R) = LRFROMF(f)
                
                m_seg = None
                if (L == 0):
                    x[0] = negsign(m[0])
                    if (L==R):
                        return #done
                    else:
                        m_seg = m[L+1: R+1]
                else:
                    m_seg = m[L:R+1]
                
                for t in range(6-len(m_seg), 6):
                    if (t ==0):
                        x[t] = negsign(m_seg[t-6+len(m_seg)])
                    else:
                        x[t] = m_seg[t-6+len(m_seg)]
                self.memory.saveX(x)
                
        if (c == OP_LD1 or c == OP_LD2 or c == OP_LD3 or c == OP_LD4 or c == OP_LD5 or c == OP_LD6):
            j = c - OP_LD1 + 1
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            getattr(self.memory, 'savei'+str(j))([m[0]]+m[L: R+1])

        if (c == OP_LD1N or c == OP_LD2N or c == OP_LD3N or c == OP_LD4N or c == OP_LD5N or c == OP_LD6N):
            j = c - OP_LD1N + 1
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            getattr(self.memory, 'savei'+str(j))([negsign(m[0])]+m[L: R+1])
        
        if (c == OP_STA):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = self.memory.getA()
            if (f == WORD_WIDTH):
                self.memory.setMemory(aa, a)
            else:
                m = self.memory.getMemory(aa)
                (L, R) = LRFROMF(f)
                
                a_seg = None
                if (L == 0):
                    m[0] = a[0]
                    if (L==R):
                        return #done
                    else:
                        a_seg = a[6-(R-L): 6]
                else:
                    a_seg = a[6-(R-L+1):6]
                if (L == 0):
                    L=L+1
                for t in range(L, R+1):
                    m[t] = a_seg[t-L]
                self.memory.setMemory(aa, m)

        if (c == OP_STX):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            x = self.memory.getX()
            if (f == WORD_WIDTH):
                self.memory.setMemory(aa, x[:])
            else:
                m = self.memory.getMemory(aa)
                (L, R) = LRFROMF(f)
                
                x_seg = None
                if (L == 0):
                    m[0] = x[0]
                    if (L==R):
                        return #done
                    else:
                        x_seg = x[6-(R-L): 6]
                else:
                    x_seg = x[6-(R-L+1):6]
                if (L == 0):
                    L=L+1
                for t in range(L, R+1):
                    m[t] = x_seg[t-L]
                self.memory.setMemory(aa, m)
        
        if (c == OP_ST1 or c == OP_ST2 or c == OP_ST3 or c == OP_ST4 or c == OP_ST5 or c == OP_ST6):
            k = c - OP_ST1 + 1
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            i_content = getattr(self.memory, 'geti'+str(k))();
            m = self.memory.getMemory(aa)
            m[0]=i_content[0]
            m[1:4] = [0] * 3
            m[4:6] = i_content[1:3]
            self.memory.setMemory(aa, m)
        
        if (c == OP_STJ):
            #if (aa.isalpha()):
                # for STJ / JMP
                #j = partstodec_withsign(self.memory.getj());
                #self.runtime_symboltable[aa] = j
            #else:
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            j = self.memory.getj();
            m = self.memory.getMemory(aa)
            m[0]=j[0]
            m[1:3] = j[1:3]
            self.memory.setMemory(aa, m)
        
        if (c == OP_STZ):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            x = ['+', 0, 0, 0, 0, 0]
            if (f == WORD_WIDTH):
                self.memory.setMemory(aa, x)
            else:
                m = self.memory.getMemory(aa)
                (L, R) = LRFROMF(f)
                
                x_seg = None
                if (L == 0):
                    m[0] = x[0]
                    if (L==R):
                        return #done
                    else:
                        x_seg = x[6-(R-L): 6]
                else:
                    x_seg = x[6-(R-L+1):6]
                if (L == 0):
                    L=L+1
                for t in range(L, R+1):
                    m[t] = x_seg[t-L]
                self.memory.setMemory(aa, m)
        
        if (c == OP_ADD):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            m = self.memory.getMemory(aa)
            a = self.memory.getA()
            
            (L, R) = LRFROMF(f)
            if (L == 0):
                L = L + 1
            
            m_seg = m[L:R+1]
            
            m_part = partstodec(m_seg)
            a_part = partstodec(a[1:])
            if (a[0] == '-'):
                a_part = a_part * -1
            
            if (m[0] == '-'):
                m_part = m_part * -1
            
            result = a_part + m_part
            if (result > MAX_NUMBER):
                self.memory.setoverload();
                result = result - MAX_NUMBER

            if (result < -1 * MAX_NUMBER):
                self.memory.setoverload();
                result = result + MAX_NUMBER
            
            self.memory.saveA([a[0]] + dectobin(result, WORD_WIDTH))
        
        if (c == OP_SUB):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            m = self.memory.getMemory(aa)
            a = self.memory.getA()
            (L, R) = LRFROMF(f)
            if (L == 0):
                L = L + 1
            m_seg = m[L:R+1]
            
            m_part = partstodec(m_seg)
            a_part = partstodec(a[1:])
            if (a[0] == '-'):
                a_part = a_part * -1
            
            if (m[0] == '-'):
                m_part = m_part * -1
                
            result = a_part - m_part
            if (result > MAX_NUMBER):
                self.memory.setoverload();
                result = result - MAX_NUMBER

            if (result < -1 * MAX_NUMBER):
                self.memory.setoverload();
                result = result + MAX_NUMBER
            
            self.memory.saveA([a[0]] + dectobin(result, WORD_WIDTH))
        
        if (c == OP_MUL):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            m = self.memory.getMemory(aa)
            a = self.memory.getA()
            (L, R) = LRFROMF(f)
            if (L == 0):
                L = L + 1
            m_seg = m[L:R+1]
            sign = '+'
            
            m_part = partstodec(m_seg)
            a_part = partstodec(a[1:])
            
            result = a_part * m_part
            if (a[0] != m[0]):
                sign = '-'
            
            resultinlist = dectobin(result, WORD_WIDTH*2)
            #print (result, resultinlist)
            
            self.memory.saveA([sign] + resultinlist[0:WORD_WIDTH])
            self.memory.saveX([sign] + resultinlist[WORD_WIDTH:WORD_WIDTH*2])

        if (c == OP_DIV):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            m = self.memory.getMemory(aa)
            a = self.memory.getA()
            x = self.memory.getX()
            (L, R) = LRFROMF(f)
            if (L == 0):
                L = L + 1
            m_seg = m[L:R+1]
            asign = '+'
            xsign = '+'
            
            m_part = partstodec(m_seg)
            ax_part = partstodec(a[1:]+x[1:])
            
            result = int(ax_part / m_part)
            remain = ax_part % m_part
            if (a[0] != m[0]):
                asign = '-'
            
            xsign = a[0]
            
            self.memory.saveA([asign] + dectobin(result, WORD_WIDTH))
            self.memory.saveX([xsign] + dectobin(remain, WORD_WIDTH))
        
        if (c == OP_HLT):
            pass
        
        if (c == OP_ENTA):
            addri = None
            if (i != 0):
                addri = getattr(self.memory, 'geti'+str(i))()
                aa = aa + partstodec_withsign(addri)
            
            if (aa >= 0):
                self.memory.saveA(['+']+dectobin(abs(aa), WORD_WIDTH))
            else:
                self.memory.saveA(['-']+dectobin(abs(aa), WORD_WIDTH))

        if (c == OP_ENTX):
            addri = None
            if (i != 0):
                addri = getattr(self.memory, 'geti'+str(i))()
                aa = aa + partstodec_withsign(addri)
            
            if (aa >= 0):
                self.memory.saveX(['+']+dectobin(abs(aa), WORD_WIDTH))
            else:
                self.memory.saveX(['-']+dectobin(abs(aa), WORD_WIDTH))

        if (c == OP_ENT1 or c == OP_ENT2 or c == OP_ENT3 or c == OP_ENT4 or c == OP_ENT5 or c == OP_ENT6):
            j = c - OP_ENT1 + 1
            getattr(self.memory, 'savei'+str(j))(dectobin_withsign(aa+partstodec_withsign(getattr(self.memory, 'geti'+str(i))()), 2))
        
        if (c == OP_ENNA):
            addri = None
            if (i != 0):
                addri = getattr(self.memory, 'geti'+str(i))()
                aa = (-1 * aa) - partstodec_withsign(addri)
            
            if (aa >= 0):
                self.memory.saveA(['+']+dectobin(abs(aa), WORD_WIDTH))
            else:
                self.memory.saveA(['-']+dectobin(abs(aa), WORD_WIDTH))
        
        if (c == OP_ENNX):
            addri = None
            if (i != 0):
                addri = getattr(self.memory, 'geti'+str(i))()
                aa = (-1 * aa) - partstodec_withsign(addri)
            
            if (aa >= 0):
                self.memory.saveX(['+']+dectobin(abs(aa), WORD_WIDTH))
            else:
                self.memory.saveX(['-']+dectobin(abs(aa), WORD_WIDTH))

        if (c == OP_ENN1 or c == OP_ENN2 or c == OP_ENN3 or c == OP_ENN4 or c == OP_ENN5 or c == OP_ENN6):
            j = c - OP_ENN1 + 1
            getattr(self.memory, 'savei'+str(j))(dectobin_withsign(-1 * (aa+partstodec_withsign(getattr(self.memory, 'geti'+str(i))())), 2))

        if (c == OP_INCA):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = partstodec_withsign(self.memory.getA())
            self.memory.saveA(dectobin_withsign(a + aa, WORD_WIDTH))
            # todo: overload processing
        
        if (c == OP_INCX):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = partstodec_withsign(self.memory.getX())
            self.memory.saveX(dectobin_withsign(a + aa, WORD_WIDTH))
            # todo: overload processing

        if (c == OP_INC1 or c == OP_INC2 or c == OP_INC3 or c == OP_INC4 or c == OP_INC5 or c == OP_INC6):
            j = c - OP_INC1 + 1
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = partstodec_withsign(getattr(self.memory, 'geti'+str(j))())
            getattr(self.memory, 'savei' + str(j))(dectobin_withsign(a + aa, 2))
            # todo: overload processing
        
        if (c == OP_DECA):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = partstodec_withsign(self.memory.getA())
            self.memory.saveA(dectobin_withsign(a - aa, WORD_WIDTH))
            # todo: overload processing

        if (c == OP_DECX):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = partstodec_withsign(self.memory.getX())
            self.memory.saveX(dectobin_withsign(a - aa, WORD_WIDTH))
            # todo: overload processing

        if (c == OP_DEC1 or c == OP_DEC2 or c == OP_DEC3 or c == OP_DEC4 or c == OP_DEC5 or c == OP_DEC6):
            j = c - OP_DEC1 + 1
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = partstodec_withsign(getattr(self.memory, 'geti'+str(j))())
            getattr(self.memory, 'savei' + str(j))(dectobin_withsign(a - aa, 2))
            # todo: overload processing

        # aa == "JMP" for STJ / JMP *
        if (c == OP_JMP): #or aa == "JMP"):
            if (c == OP_JMP):
                self.memory.savej(dectobin_withsign(next_statement, 2))
                m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
                next_statement = aa + m_shift
            # for JMP * back to subroutine caller
            #if (aa == "JMP"):
                #self.memory.savej(dectobin_withsign(next_statement, 2))
                #loc = statement.split()[0]
                #addr = self.runtime_symboltable[loc]
                #next_statement = addr
        
        if (c == OP_JOV):
            if (self.memory.isoverloaded()):
                self.memory.clearoverload()
                m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
                next_statement = aa + m_shift
        
        if (c == OP_JNOV):
            if (self.memory.isoverloaded()):
                self.memory.clearoverload()
            else:
                m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
                next_statement = aa + m_shift
        
        if (c == OP_JE):
            indi = self.memory.getcomparisonindicator()
            if (indi == COMP_EQAL):
                next_statement = aa + partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
        
        if (c == OP_JGE):
            indi = self.memory.getcomparisonindicator()
            if (indi == COMP_GRET or indi == COMP_EQAL):
                next_statement = aa + partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
        
        if (c == OP_JXZ):
            x = partstodec_withsign(self.memory.getX())
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            if (x == 0):
                next_statement = aa + m_shift
        
        if (c >= OP_J1Z and c <= OP_J6Z):
            j = c - OP_J1Z + 1
            rj = partstodec_withsign(getattr(self.memory, 'geti'+str(j))())
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            if (rj == 0):
                next_statement = aa + m_shift
        
        if (c == OP_J1P or c == OP_J2P or c == OP_J3P or c == OP_J4P or c == OP_J5P or c == OP_J6P):
            j = c - OP_J1P + 1
            ri = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            rx = partstodec_withsign(getattr(self.memory, 'geti'+str(j))())
            if (rx > 0):
                next_statement = aa + ri
        
        if (c == OP_CMPA):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa + m_shift
            m = self.memory.getMemory(aa)
            a = self.memory.getA()
            (L, R) = LRFROMF(f)
            
            a_cmp = 0
            m_cmp = 0
            if (L == 0):
                m_sign = m[0]
                a_sign = a[0]
                
                m_seg = m[L+1:R+1]
                a_seg = a[L+1:R+1]
                
                a_cmp = partstodec_withsign([a_sign]+a_seg)
                m_cmp = partstodec_withsign([m_sign]+m_seg)
            else:
                m_seg = m[L:R+1]
                a_seg = a[L:R+1]
                
                a_cmp = partstodec(a_seg)
                m_cmp = partstodec(m_seg)

            if (a_cmp > m_cmp):
                self.memory.setcomparisonindicator(COMP_GRET)
            elif(a_cmp == m_cmp):
                self.memory.setcomparisonindicator(COMP_EQAL)
            else:
                self.memory.setcomparisonindicator(COMP_LESS)

        if (c == OP_CMPX):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa + m_shift
            m = self.memory.getMemory(aa)
            x = self.memory.getX()
            (L, R) = LRFROMF(f)
            
            x_cmp = 0
            m_cmp = 0
            if (L == 0):
                m_sign = m[0]
                x_sign = x[0]
                
                m_seg = m[L+1:R+1]
                x_seg = x[L+1:R+1]
                
                x_cmp = partstodec_withsign([x_sign]+x_seg)
                m_cmp = partstodec_withsign([m_sign]+m_seg)
            else:
                m_seg = m[L:R+1]
                x_seg = x[L:R+1]
                
                x_cmp = partstodec(x_seg)
                m_cmp = partstodec(m_seg)

            if (x_cmp > m_cmp):
                self.memory.setcomparisonindicator(COMP_GRET)
            elif(x_cmp == m_cmp):
                self.memory.setcomparisonindicator(COMP_EQAL)
            else:
                self.memory.setcomparisonindicator(COMP_LESS)

        if (c >= OP_CMP1 and c <= OP_CMP6):
            j = c - OP_CMP1 + 1
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa + m_shift
            m = self.memory.getMemory(aa)
            
            m_cmp = partstodec_withsign([m[0]] + m[4:6])
            rj = partstodec_withsign(getattr(self.memory, 'geti'+str(j))())
            
            if (rj > m_cmp):
                self.memory.setcomparisonindicator(COMP_GRET)
            elif(rj == m_cmp):
                self.memory.setcomparisonindicator(COMP_EQAL)
            else:
                self.memory.setcomparisonindicator(COMP_LESS)

        if (c == OP_MOVE):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            i1 = partstodec_withsign(getattr(self.memory, 'geti'+str(1))())
            for j in range(0, f):
                op_moved = op_moved + 1
                self.memory.setMemory(i1, self.memory.getMemory(aa + m_shift + j)[:])

        # nop is not implemented, all the instructions that cannot be recognized is passed
        
        # ord('9')=57; chr(57)='9'
        if (c == OP_NUM):
            a = self.memory.getA()
            x = self.memory.getX()
            self.memory.saveA([a[0]] + dectobin(int(''.join([chr(n) for n in a[1:]+x[1:]])), WORD_WIDTH))
            mixlog(MDEBUG, "op=num..a=", self.memory.getA())
        
        # ord('9')=57; chr(57)='9'
        if (c == OP_CHAR):
            a = self.memory.getA()
            x = self.memory.getX()
            a_num = str(partstodec_withsign(a)).rjust(10, '0')
            mixlog(MDEBUG, "op=char..a_num=..", a_num)
            
            self.memory.saveA([a[0]] + [ord(n) for n in a_num[0:WORD_WIDTH]])
            self.memory.saveX([x[0]] + [ord(n) for n in a_num[WORD_WIDTH:WORD_WIDTH*2]])
            
            mixlog(MDEBUG, "op=char..a=", self.memory.getA())
            mixlog(MDEBUG, "op=char..x=", self.memory.getX())
        
        if (c == OP_SLA):
            a = self.memory.getA()
            a_num = partstodec(a[1:])
            mixlog(MDEBUG, "op=sla..a_num=", bin(abs(a_num))[2:].zfill(WORD_WIDTH * BYTE_WIDTH), "aa=", aa)
            a_num = a_num << aa * BYTE_WIDTH
            mixlog(MDEBUG, "op=after sla..a_num=", bin(abs(a_num))[2:].zfill(WORD_WIDTH * BYTE_WIDTH))
            self.memory.saveA([a[0]] + dectobin_right(a_num, WORD_WIDTH))
        
        if (c == OP_SRA):
            a = self.memory.getA()
            a_num = partstodec(a[1:])
            mixlog(MDEBUG, "op=sra..a_num=", bin(abs(a_num))[2:].zfill(WORD_WIDTH * BYTE_WIDTH), "aa=", aa)
            a_num = a_num >> aa * BYTE_WIDTH
            mixlog(MDEBUG, "op=after sra..a_num=", bin(abs(a_num))[2:].zfill(WORD_WIDTH * BYTE_WIDTH))
            self.memory.saveA([a[0]] + dectobin_right(a_num, WORD_WIDTH))

        if (c == OP_SLAX):
            a = self.memory.getA()
            x = self.memory.getX()
            #ax_num = partstodec(a[1:] + x[1:]) << aa * BYTE_WIDTH
            #ax_num = rotatearrayleft_n(a[1:] + x[1:], aa % (2 * WORD_WIDTH))
            ax_num = shiftarrayleft_n(a[1:] + x[1:], aa)
            
            #ax_list = dectobin(ax_num, 2 * WORD_WIDTH)
            self.memory.saveA([a[0]] + ax_num[0:WORD_WIDTH])
            self.memory.saveX([x[0]] + ax_num[WORD_WIDTH:])
        
        if (c == OP_SRAX):
            a = self.memory.getA()
            x = self.memory.getX()
            ax_num = partstodec(a[1:] + x[1:]) >> aa * BYTE_WIDTH
            
            ax_list = dectobin_right(ax_num, 2 * WORD_WIDTH)
            self.memory.saveA([a[0]] + ax_list[0:WORD_WIDTH])
            self.memory.saveX([x[0]] + ax_list[WORD_WIDTH:])
        
        if (c == OP_SLC):
            pass
        
        if (c == OP_SRC):
            pass
        
        if (c == OP_NOP):
            pass

        if (c == OP_IN):
            d_con = read_from_inputdevice()
            aa_tmp = aa
            
            for d in d_con:
                self.memory.setMemory(aa_tmp, d)
                aa_tmp = aa_tmp + 1
        
        if (c == OP_OUT):
            write_into_outputdevice(self.memory.getMemorySegment(aa, f), i)

        # generate profiling result
        if (op in statementprofilingdict):
            t = statementprofilingdict[op]
            if (current_line in self.profilingresult):
                (stmt, times, unit, total) = self.profilingresult[current_line]
                if (c == OP_MOVE):
                    unit = op_moved * 2 + 1
                self.profilingresult[current_line] = (stmt, times+1, unit, total+unit)
            else:
                unit = statementprofilingdict[op]
                if (c == OP_MOVE):
                    unit = op_moved * 2 + 1
                self.profilingresult[current_line] = (self.processed_code_dict[current_line], 1, unit, unit)

        return next_statement

def testWithAFile(fname = './test_programs/exercise_1.3.22.txt'):
    code_text_in_list = []
    ms = MemoryState()
    #ms.setMemory(2000, ['+'] + dectobin(200, 5))
    #ms.savei1(['+'] + dectobin(1, 2))
    #ms.savej(['+'] + dectobin(2222, 2))
    #ms.saveA(['-'] + dectobin(1, 5))
    #ms.saveX(['-'] + dectobin(2, 5))

    f = open(fname, 'r')
    with f:
        code_text_in_list = f.read().splitlines()
        #print(self.code_text_in_list)
    f.close()
    
    mapp = MixALPreProcessor(code_text_in_list, ms)
    mapp.preprocessall()
    processed_code = mapp.processed_code
    processed_code_dict = mapp.processed_code_dict
    orig = mapp.orig
    end = mapp.end
    
    mixlog(MDEBUG, "finished preprocessing")
    ms.setMemory(1200, ['+', 1, 2, 3, 4, 5])
    ms.setMemory(1201, ['+', 6, 7, 8, 9, 10])
    
    # load everything into memory
    for line in processed_code_dict.keys():
        sm = MixToMachineCodeTranslatorSM()
        sm.transduce([x for x in processed_code_dict[line]], False)
        (sym, aa, i, f, op, c) = sm.output
        aa = dectobin(my_int(aa), 2)
        ms.setMemory(line, [sym] + aa + [i, f, c])

    me = MixExecutor(processed_code_dict, orig, end, ms)
    me.go(True)
    mixlog(MDEBUG, "finished executing")
    #for n in range (3000, 3050):
        #print("M:", ms.getMemory(n))
    print("M:", ms.getMemory(2000))
    print("A:", ms.getA())
    print("A:", printchars(ms.getA()[1:]))
    print("X:", ms.getX())
    print("X:", printchars(ms.getX()[1:]))
    print("i1", ms.geti1())
    print("i2", ms.geti2())
    print("i3", ms.geti3())
    print("i4", ms.geti4())
    print("i5", ms.geti5())
    print("i6", ms.geti6())
    print("cmp", ms.getcomparisonindicator())

def test_char_and_shift(fname):
    code_text_in_list = []
    ms = MemoryState()

    f = open(fname, 'r')
    with f:
        code_text_in_list = f.read().splitlines()
        #print(self.code_text_in_list)
    f.close()
    
    mapp = MixALPreProcessor(code_text_in_list, ms)
    mapp.preprocessall()
    processed_code = mapp.processed_code
    processed_code_dict = mapp.processed_code_dict
    orig = mapp.orig
    end = mapp.end
    
    mixlog(MDEBUG, "finished preprocessing")
    ms.setMemory(1200, ['+', 48, 97, 98, 99, 100])
    ms.setMemory(1201, ['+', 101, 102, 103, 104, 105])
    
    # load everything into memory
    for line in processed_code_dict.keys():
        sm = MixToMachineCodeTranslatorSM()
        sm.transduce([x for x in processed_code_dict[line]], False)
        (sym, aa, i, f, op, c) = sm.output
        aa = dectobin(my_int(aa), 2)
        ms.setMemory(line, [sym] + aa + [i, f, c])

    me = MixExecutor(processed_code_dict, orig, end, ms)
    me.go(True)
    mixlog(MDEBUG, "finished executing")
    #for n in range (3000, 3050):
        #print("M:", ms.getMemory(n))
    print("M:", ms.getMemory(2000))
    print("M 1200:", printchars(ms.getMemory(1200)[1:]))
    print("M 1201:", printchars(ms.getMemory(1201)[1:]))
    print("A:", ms.getA())
    print("A:", printchars(ms.getA()[1:]))
    print("X:", ms.getX())
    print("X:", printchars(ms.getX()[1:]))
    print("i1", ms.geti1())
    print("i2", ms.geti2())
    print("i3", ms.geti3())
    print("i4", ms.geti4())
    print("i5", ms.geti5())
    print("i6", ms.geti6())
    print("cmp", ms.getcomparisonindicator())

def test_prime(fname):
    code_text_in_list = []
    ms = MemoryState()
    
    f = open(fname, 'r')
    with f:
        code_text_in_list = f.read().splitlines()
        #print(self.code_text_in_list)
    f.close()
        
    mapp = MixALPreProcessor(code_text_in_list)
    mapp.preprocessall()
    processed_code = mapp.processed_code
    processed_code_dict = mapp.processed_code_dict
    orig = mapp.orig
    end = mapp.end
    
    mixlog(MINFO, "finished preprocessing")

    # load everything into memory
    for line in processed_code_dict.keys():
        sm = MixToMachineCodeTranslatorSM()
        sm.transduce([x for x in processed_code_dict[line]], False)
        (sym, aa, i, f, op, c) = sm.output
        aa = dectobin(my_int(aa), 2)
        ms.setMemory(line, [sym] + aa + [i, f, c])

    me = MixExecutor(processed_code_dict, orig, end, ms)
    me.go(False)
    mixlog(MINFO, "finished executing")

    print("A:", ms.getA())
    print("X:", ms.getX())
    print("i1", ms.geti1())
    print("i2", ms.geti2())
    print("i3", ms.geti3())
    print("i4", ms.geti4())
    print("i5", ms.geti5())
    print("i6", ms.geti6())
    print("cmp", ms.getcomparisonindicator())

def testGetMaxNum():
    code_text_in_list = []
    ms = MemoryState()
    
    f = open('./test_programs/test_program_win.txt', 'r')
    with f:
        code_text_in_list = f.read().splitlines()
        #print(self.code_text_in_list)
    f.close()

    mapp = MixALPreProcessor(code_text_in_list)
    mapp.preprocessall()
    processed_code = mapp.processed_code
    processed_code_dict = mapp.processed_code_dict
    orig = mapp.orig
    end = mapp.end
    
    mixlog(MINFO, "finished preprocessing")

    # load everything into memory
    for line in processed_code_dict.keys():
        sm = MixToMachineCodeTranslatorSM()
        sm.transduce([x for x in processed_code_dict[line]], False)
        (sym, aa, i, f, op, c) = sm.output
        aa = dectobin(my_int(aa), 2)
        ms.setMemory(line, [sym] + aa + [i, f, c])

    me = MixExecutor(processed_code_dict, orig, end, ms)
    me.go(False)
    mixlog(MINFO, "finished executing")
    print("A:", ms.getA())
    print("X:", ms.getX())
    print("i1", ms.geti1())
    print("i2", ms.geti2())
    print("i3", ms.geti3())
    print("i4", ms.geti4())
    print("i5", ms.geti5())
    print("i6", ms.geti6())
    print("cmp", ms.getcomparisonindicator())

def testExecutor():
    #testWithAFile(fname = './test_programs/test_program_char.txt')
    #test_char_and_shift('./test_programs/exercise_1.3.24.txt')
    test_prime('./test_programs/test_program_prime.txt')
    #testGetMaxNum()

# LDA 2000, 2(0:3)
# LDA 2000, 2(1:3)
# LDA 2000(1:3)
# LDA 2000
# LDA -2000, 4
if __name__ == "__main__":
    #testStatementParts()
    testExecutor()