undef = 'undefined'
WORD_WIDTH = 5
BYTE_WIDTH = 6
MAX_BYTE_HOLDING = 2 ** BYTE_WIDTH - 1
MAX_NUMBER = 2 ** (BYTE_WIDTH * WORD_WIDTH) - 1

# 2000 -> [31][16]
def dectobin(num, width, byte_width = BYTE_WIDTH):
    s = bin(num)[2:].zfill(width * byte_width)
    return [int(s[i * byte_width:(i+1) * byte_width], 2) for i in range(0, width)]

# 111111111000000000 -> 0000000000 (get the right part)
def dectobin_right(num, width, byte_width = BYTE_WIDTH):
    s = bin(num)[2:].zfill(width * byte_width)
    s = s[-1 * width * byte_width:]
    
    return [int(s[(i) * byte_width:(i+1) * byte_width], 2) for i in range(0, width)]

def dectobin_withsign(num, width, byte_width = BYTE_WIDTH):
    s = bin(abs(num))[2:].zfill(width * byte_width)
    if (num >= 0):
        return ['+'] + [int(s[i * byte_width:(i+1) * byte_width], 2) for i in range(0, width)]
    else:
        return ['-'] + [int(s[i * byte_width:(i+1) * byte_width], 2) for i in range(0, width)]

# [32, 16] => +2000
def partstodec(s, byte_width = BYTE_WIDTH):
    return int(''.join([bin(n)[2:].zfill(byte_width) for n in s]), 2)

def partstodec_withsign(s):
    r = partstodec(s[1:])
    if (s[0] == '-'):
        r = r * -1
    return r

def negsign(s):
    if (s=='-'):
        return '+'
    else:
        return '-'

def LPLUSR(L, R):
    return 8*L + R

def LRFROMF(F):
    L = int(F / 8)
    R = F - L * 8
    return (L, R)

def my_int(str):
    if str == "":
        return 0
    else:
        return int(str)

def isUndef(v):
    if v == undef:
        return True
    else:
        return False

def splitValue(v, n):
    if isUndef(v):
        return (undef,) * n
    else:
        return v

def safeAdd(i1, i2):
    if isUndef(i1) or isUndef(i2):
        return undef
    else:
        return i1 + i2

def safeMultiply(i1, i2):
    if isUndef(i1) or isUndef(i2):
        return undef
    else:
        return i1 * i2

def safeDivide(i1, i2):
    if isUndef(i1) or isUndef(i2):
        return undef
    else:
        return i1 / i2

def safeSubtract(i1, i2):
    if isUndef(i1) or isUndef(i2):
        return undef
    else:
        return i1 - i2

if __name__ == "__main__":
    print(dectobin(12977699, 5))
    print(dectobin_right(68702699520, 5))
    print(dectobin_withsign(-12933883, 5))
    print(partstodec([1,2,3,4,5,6,7,8,9,10]))
    print(LPLUSR(12, 3))