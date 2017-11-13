import os

COMP_LESS='L'
COMP_EQAL='E'
COMP_GRET='G'

class MemoryState:
    def __init__(self, memory_space = 4000, tape_space = 21):
        self.a1 = 0
        self.a2 = 0
        self.a3 = 0
        self.a4 = 0
        self.a5 = 0
        self.asym = '+'
        
        self.x1 = 0
        self.x2 = 0
        self.x3 = 0
        self.x4 = 0
        self.x5 = 0
        self.xsym = '+'
        
        self.i14 = 0
        self.i15 = 0
        self.i1sym = '+'
        
        self.i24 = 0
        self.i25 = 0
        self.i2sym = '+'
        
        self.i34 = 0
        self.i35 = 0
        self.i3sym = '+'
        
        self.i44 = 0
        self.i45 = 0
        self.i4sym = '+'
        
        self.i54 = 0
        self.i55 = 0
        self.i5sym = '+'
        
        self.i64 = 0
        self.i65 = 0
        self.i6sym = '+'
        
        self.j4 = 0
        self.j5 = 0
        self.jsym = '+'
        
        self.overload_switch = 0       # 1=overload / 0=not-overload
        self.comparison_indicator = '' # L / E / G

        self.memory = [['+', 0, 0, 0, 0, 0]] * memory_space
        self.tape = [0] * tape_space

    def __str__(self):
        result = "a=[" + self.asym + " , " + str(self.a1) + " , " \
                + str(self.a2) + " , " + str(self.a3) + " , " \
                + str(self.a4) + " , " + str(self.a5) + "]\n"
        
        result = result + "x=[" + self.xsym + " , " + str(self.x1) + " , " \
                + str(self.x2) + " , " + str(self.x3) + " , " \
                + str(self.x4) + " , " + str(self.x5) + "]\n"

        result = result + "i1=[" + self.i1sym + " , " + str(self.i14) + " , " \
                + str(self.i15) + "]\n"

        result = result + "i2=[" + self.i2sym + " , " + str(self.i24) + " , " \
                + str(self.i25) + "]\n"

        result = result + "i3=[" + self.i3sym + " , " + str(self.i34) + " , " \
                + str(self.i35) + "]\n"

        result = result + "i4=[" + self.i4sym + " , " + str(self.i44) + " , " \
                + str(self.i45) + "]\n"

        result = result + "i5=[" + self.i5sym + " , " + str(self.i54) + " , " \
                + str(self.i55) + "]\n"

        result = result + "i6=[" + self.i6sym + " , " + str(self.i64) + " , " \
                + str(self.i65) + "]\n"
        
        result = result + "j=[" + self.jsym + " , " + str(self.j4) + " , " \
                + str(self.j5) + "]\n"
        
        result = result + "comp = " + self.comparison_indicator + "\n"
        
        return result

    def getMemory(self, addr):
        return self.memory[addr]
    
    def setMemory(self, addr, word):
        self.memory[addr] = word
    
    def getA(self):
        return [self.asym, self.a1, self.a2, self.a3, self.a4, self.a5]
    
    def saveA(self, word):
        [self.asym, self.a1, self.a2, self.a3, self.a4, self.a5] = word
    
    def getX(self):
        return [self.xsym, self.x1, self.x2, self.x3, self.x4, self.x5]
    
    def saveX(self, word):
        [self.xsym, self.x1, self.x2, self.x3, self.x4, self.x5] = word
    
    # fake register, always 0
    def geti0(self):
        return ['+', 0, 0]
    
    def geti1(self):
        return [self.i1sym, self.i14, self.i15]
    
    def savei1(self, word):
        [self.i1sym, self.i14, self.i15] = word
    
    def geti2(self):
        return [self.i2sym, self.i24, self.i25]
    
    def savei2(self, word):
        [self.i2sym, self.i24, self.i25] = word
    
    def geti3(self):
        return [self.i3sym, self.i34, self.i35]
    
    def savei3(self, word):
        [self.i3sym, self.i34, self.i35] = word

    def geti4(self):
        return [self.i4sym, self.i44, self.i45]
    
    def savei4(self, word):
        [self.i4sym, self.i44, self.i45] = word

    def geti5(self):
        return [self.i5sym, self.i54, self.i55]
    
    def savei5(self, word):
        [self.i5sym, self.i54, self.i55] = word

    def geti6(self):
        return [self.i6sym, self.i64, self.i65]
    
    def savei6(self, word):
        [self.i6sym, self.i64, self.i65] = word

    def getj(self):
        return [self.jsym, self.j4, self.j5]
    
    def savej(self, word):
        [self.jsym, self.j4, self.j5] = word
    
    def setoverload(self):
        self.overload_switch = 1
    
    def clearoverload(self):
        self.overload_switch = 0
    
    def setcomparisonindicator(self, indi):
        self.comparison_indicator = indi
    
    def getcomparisonindicator(self):
        return self.comparison_indicator

if __name__ == "__main__":
    ms = MemoryState()
    #print (ms.memory)
    print (str(ms))