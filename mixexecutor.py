from memorystate import *
from mixaltomachinecode import *
from mixalpreprocessor import *
from sm import MySM

# execute single line of code
class MixExecutor(MySM):
    def __init__(self, mix_code_dict, runtime_symboltable, orig, end, memory):
        self.mix_code_dict = mix_code_dict
        self.runtime_symboltable = runtime_symboltable
        self.orig = orig
        self.end = end
        self.startState = orig
        self.memory = memory
        self.current_op = ''
        self.profilingresult = {}
    
    def getNextValues(self, state, inp, verbose = False):
        statement = self.mix_code_dict[state]
        mixlog(MDEBUG, "before executing..."+statement, str(self.memory))
        s = self.execute(statement, state)
        mixlog(MDEBUG, "after executing..."+statement, str(self.memory))
        mixlog(MDEBUG, "runtime symbols..."+str(self.runtime_symboltable))
        return (s, s)
    
    def done(self, state):
        d = (state == self.end)
        if (d):
            mixlog(MDEBUG, "profiling result..."+str(self.profilingresult))
            return True
        else:
            return False
    
    def execute(self, statement, current_line):
        sm = MixToMachineCodeTranslatorSM()
        sm.transduce([x for x in statement], False)
        (sym, aa, i, f, op, c) = sm.output
        next_statement = current_line + 1
        
        aa_sign = '+'
        if (aa.startswith('-')):
            aa_sign = '-'
        
        # for JMP / STJ
        if (not aa.isalpha()):
            aa = my_int(aa)
        
        #LDA
        if (c == OP_LDA):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            if (f == 5):
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
            if (f == 5):
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
            if (f == 5):
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
            if (f == 5):
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
                
        if (c == OP_LD1):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei1([m[0]]+m[L: R+1])
        
        if (c == OP_LD2):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei2([m[0]]+m[L: R+1])
        
        if (c == OP_LD3):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei3([m[0]]+m[L: R+1])

        if (c == OP_LD4):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            self.memory.savei4([m[0]]+m[L: R+1])

        if (c == OP_LD5):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei5([m[0]]+m[L: R+1])

        if (c == OP_LD6):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei6([m[0]]+m[L: R+1])

        if (c == OP_LD1N):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei1([negsign(m[0])]+m[L: R+1])
        
        if (c == OP_LD2N):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei2([negsign(m[0])]+m[L: R+1])
        
        if (c == OP_LD3N):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei3([negsign(m[0])]+m[L: R+1])

        if (c == OP_LD4N):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei4([negsign(m[0])]+m[L: R+1])

        if (c == OP_LD5N):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei5([negsign(m[0])]+m[L: R+1])

        if (c == OP_LD6N):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            m = self.memory.getMemory(aa+m_shift)
            (L, R) = LRFROMF(f)
            self.memory.savei6([negsign(m[0])]+m[L: R+1])
        
        if (c == OP_STA):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = self.memory.getA()
            if (f == 5):
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
            if (f == 5):
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
            if (aa.isalpha()):
                # for STJ / JMP
                j = partstodec_withsign(self.memory.getj());
                self.runtime_symboltable[aa] = j
            else:
                m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
                aa = aa+m_shift
                j = self.memory.getj();
                m = self.memory.getMemory(aa)
                m[0]=j[0]
                m[1:4] = [0] * 3
                m[4:6] = j[1:3]
                self.memory.setMemory(aa, m)
        
        if (c == OP_STZ):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            x = ['+', 0, 0, 0, 0, 0]
            if (f == 5):
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
            if (L == 0):
                L = L + 1
            (L, R) = LRFROMF(f)
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
            
            self.memory.saveA([a[0]] + dectobin(result, 5))
        
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
            
            self.memory.saveA([a[0]] + dectobin(result, 5))
        
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
            
            resultinlist = dectobin(result, 10)
            #print (result, resultinlist)
            
            self.memory.saveA([sign] + resultinlist[0:5])
            self.memory.saveX([sign] + resultinlist[5:10])

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
            
            self.memory.saveA([asign] + dectobin(result, 5))
            self.memory.saveX([xsign] + dectobin(remain, 5))
        
        if (c == OP_ENTA):
            addri = None
            if (i != 0):
                addri = getattr(self.memory, 'geti'+str(i))()
                aa = aa + partstodec_withsign(addri)
            
            if (aa >= 0):
                self.memory.saveA(['+']+dectobin(abs(aa), 5))
            else:
                self.memory.saveA(['-']+dectobin(abs(aa), 5))

        if (c == OP_ENTX):
            addri = None
            if (i != 0):
                addri = getattr(self.memory, 'geti'+str(i))()
                aa = aa + partstodec_withsign(addri)
            
            if (aa >= 0):
                self.memory.saveX(['+']+dectobin(abs(aa), 5))
            else:
                self.memory.saveX(['-']+dectobin(abs(aa), 5))

        if (c == OP_ENT1 or c == OP_ENT2 or c == OP_ENT3 or c == OP_ENT4 or c == OP_ENT5 or c == OP_ENT6):
            j = c - OP_ENT1 + 1
            getattr(self.memory, 'savei'+str(j))(dectobin_withsign(aa+partstodec_withsign(getattr(self.memory, 'geti'+str(i))()), 2))
        
        if (c == OP_ENNA):
            addri = None
            if (i != 0):
                addri = getattr(self.memory, 'geti'+str(i))()
                aa = (-1 * aa) - partstodec_withsign(addri)
            
            if (aa >= 0):
                self.memory.saveA(['+']+dectobin(abs(aa), 5))
            else:
                self.memory.saveA(['-']+dectobin(abs(aa), 5))
        
        if (c == OP_ENNX):
            addri = None
            if (i != 0):
                addri = getattr(self.memory, 'geti'+str(i))()
                aa = (-1 * aa) - partstodec_withsign(addri)
            
            if (aa >= 0):
                self.memory.saveX(['+']+dectobin(abs(aa), 5))
            else:
                self.memory.saveX(['-']+dectobin(abs(aa), 5))

        if (c == OP_ENN1 or c == OP_ENN2 or c == OP_ENN3 or c == OP_ENN4 or c == OP_ENN5 or c == OP_ENN6):
            j = c - OP_ENN1 + 1
            getattr(self.memory, 'savei'+str(j))(dectobin_withsign(-1 * (aa+partstodec_withsign(getattr(self.memory, 'geti'+str(i))())), 2))

        if (c == OP_INCA):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = partstodec_withsign(self.memory.getA())
            self.memory.saveA(dectobin_withsign(a + aa, 5))
            # todo: overload processing
        
        if (c == OP_INCX):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = partstodec_withsign(self.memory.getX())
            self.memory.saveX(dectobin_withsign(a + aa, 5))
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
            self.memory.saveA(dectobin_withsign(a - aa, 5))
            # todo: overload processing

        if (c == OP_DECX):
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = partstodec_withsign(self.memory.getX())
            self.memory.saveX(dectobin_withsign(a - aa, 5))
            # todo: overload processing

        if (c == OP_DEC1 or c == OP_DEC2 or c == OP_DEC3 or c == OP_DEC4 or c == OP_DEC5 or c == OP_DEC6):
            j = c - OP_DEC1 + 1
            m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
            aa = aa+m_shift
            a = partstodec_withsign(getattr(self.memory, 'geti'+str(j))())
            getattr(self.memory, 'savei' + str(j))(dectobin_withsign(a - aa, 2))
            # todo: overload processing

        # aa == "JMP" for STJ / JMP *
        if (c == OP_JMP or aa == "JMP"):
            if (c == OP_JMP):
                self.memory.savej(dectobin_withsign(next_statement, 2))
                m_shift = partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
                next_statement = aa + m_shift
            # for JMP * back to subroutine caller
            if (aa == "JMP"):
                self.memory.savej(dectobin_withsign(next_statement, 2))
                loc = statement.split()[0]
                addr = self.runtime_symboltable[loc]
                next_statement = addr
        
        if (c == OP_JGE):
            indi = self.memory.getcomparisonindicator()
            if (indi == COMP_GRET or indi == COMP_EQAL):
                next_statement = aa + partstodec_withsign(getattr(self.memory, 'geti'+str(i))())
        
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

        # generate profiling result
        if (op in statementprofilingdict):
            t = statementprofilingdict[op]
            if (current_line in self.profilingresult):
                (stmt, times, unit, total) = self.profilingresult[current_line]
                self.profilingresult[current_line] = (stmt, times+1, unit, total+unit)
            else:
                self.profilingresult[current_line] = (statement, 1, statementprofilingdict[op], statementprofilingdict[op])

        return next_statement

def testExecutor():
    code_text_in_list = []
    processed_code = []
    ms = MemoryState()
    #ms.setMemory(2000, ['+'] + dectobin(200, 5))
    #ms.savei1(['+'] + dectobin(1, 2))
    #ms.savej(['+'] + dectobin(2222, 2))
    #ms.saveA(['-'] + dectobin(1, 5))
    #ms.saveX(['-'] + dectobin(2, 5))
    fname = './test_program_win.txt'

    f = open(fname, 'r')
    with f:
        code_text_in_list = f.read().splitlines()
        #print(self.code_text_in_list)
    f.close()
    
    mapp = MixALPreProcessor(code_text_in_list, ms)
    mapp.preprocessall()
    processed_code_dict = mapp.processed_code_dict
    orig = mapp.orig
    end = mapp.end
    runtime_symboltable = mapp.runtime_symboltable
    
    mixlog(MDEBUG, "finished preprocessing")
    
    me = MixExecutor(processed_code_dict, runtime_symboltable, orig, end, ms)
    me.go(True)
    mixlog(MDEBUG, "finished executing")
    print("M:", ms.getMemory(3000))
    print("A:", ms.getA())
    print("X:", ms.getX())
    print("i1", ms.geti1())
    print("i2", ms.geti2())
    print("i3", ms.geti3())
    print("i4", ms.geti4())
    print("i5", ms.geti5())
    print("i6", ms.geti6())
    print("cmp", ms.getcomparisonindicator())

# LDA 2000, 2(0:3)
# LDA 2000, 2(1:3)
# LDA 2000(1:3)
# LDA 2000
# LDA -2000, 4
if __name__ == "__main__":
    #testStatementParts()
    testExecutor()