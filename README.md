# MIX
For how to use, read mixexecutor.py, __main__ section.
Required packages: PyQt5 and numpy to run the UI; Nothing required for others.  SIP will be installed automatically while installing pyqt.
  298  sudo pip3.6 install PyQt5
  302  sudo pip3.6 install numpy

https://www.riverbankcomputing.com/software/pyqt/intro
PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt application framework and runs on all platforms supported by Qt including Windows, OS X, Linux, iOS and Android. PyQt5 supports Qt v5. PyQt4 supports Qt v4 and will build against Qt v5. The bindings are implemented as a set of Python modules and contain over 1,000 classes.

The Qt Company no longer supports Qt v4. PyQt5 and Qt v5 are strongly recommended for all new development.

PyQt is dual licensed on all supported platforms under the GNU GPL v3 and the Riverbank Commercial License. Unlike Qt, PyQt is not available under the LGPL. You can purchase the commercial version of PyQt here. More information about licensing can be found in the License FAQ.

PyQt does not include a copy of Qt. You must obtain a correctly licensed copy of Qt yourself. However, binary wheels of the GPL version of PyQt5 are provided and these include a copy of the LGPL version of Qt.

Mix Registers:
rA: Accumulator (full word, five bytes and a sign).
rX: Extension (full word, five bytes and a sign).
rI1, rI2, rI3, rI4, rI5, rI6: Index registers (two bytes and a sign).
rJ: Jump address (two bytes, always positive).

Memory: 0 ~ 3999 Units

Memory / Instruction Format:
¡À Address (2 bytes plus a sign) Index (1 byte)   modiFication (1 byte)    OPeration (1 byte)

LDA ADDR,i(0:5)         rA := memory[ADDR + rIi];
LDX ADDR,i(0:5)         rX := memory[ADDR + rIi];
LD? ADDR,i(0:5)         rI? := memory[ADDR + rIi];
LDAN ADDR,i(0:5)        rA := - memory[ADDR + rIi];
LDXN ADDR,i(0:5)        rX := - memory[ADDR + rIi];
LD?N ADDR,i(0:5)        rI? := - memory[ADDR + rIi];

STA ADDR,i(0:5)         memory[ADDR + rIi] := rA;
STX ADDR,i(0:5)         memory[ADDR + rIi] := rX;
ST? ADDR,i(0:5)         memory[ADDR + rIi] := rI?;
STJ ADDR,i(0:5)         memory[ADDR + rIi] := rJ;
STZ ADDR,i(0:5)         memory[ADDR + rIi] := 0;

ADD ADDR,i(0:5)         rA := rA + memory[ADDR + rIi];
SUB ADDR,i(0:5)         rA := rA - memory[ADDR + rIi];
MUL ADDR,i(0:5)         (rA,rX) := rA * memory[ADDR + rIi];
DIV ADDR,i(0:5)         rA := int( (rA,rX) / memory[ADDR + rIi] );
                        rX := (rA,rX) % memory[ADDR + rIi];

ENTA ADDR,i             rA := ADDR + rIi;
ENTX ADDR,i             rX := ADDR + rIi;
ENT? ADDR,i             rI? := ADDR + rIi;
ENNA ADDR,i             rA := - ADDR - rIi;
ENNX ADDR,i             rX := - ADDR - rIi;
ENN? ADDR,i             rI? := - ADDR - rIi;

INCA ADDR,i             rA := rA + ADDR + rIi;
INCX ADDR,i             rX := rX + ADDR + rIi;
INC? ADDR,i             rI? := rI? + ADDR + rIi;
DECA ADDR,i             rA := rA - ADDR - rIi;
DECX ADDR,i             rX := rX - ADDR - rIi;
DEC? ADDR,i             rI? := rI? - ADDR - rIi;

CMPA ADDR,i(0:5)        compare rA with memory[ADDR + rIi];
CMPX ADDR,i(0:5)        compare rX with memory[ADDR + rIi];
CMP? ADDR,i(0:5)        compare rI? with memory[ADDR + rIi];
JMP ADDR,i              rJ := address of next instruction;
                        goto ADDR + rIi;

JSJ ADDR,i              goto ADDR + rIi;

JOV ADDR,i              if (overflow) then  
                            overflow := false;
                            goto ADDR + rIi;

JNOV ADDR,i             if (no overflow) then 
                            goto ADDR + rIi;
                        else
                            overflow := false;

JL, JE, JG ADDR,i       if (less, equal, greater) then goto ADDR + rIi;
JGE, JNE, JLE ADDR,i    if (no less, unequal, no greater) then goto ADDR + rIi;    
                        
JAN/JAZ/JAP ADDR,i      if (rA<0 or rA==0 or rA>0) then goto ADDR + rIi;
JANN/JANZ/JANP ADDR,i   if (rA>=0 or rA!=0 or rA<=0) then goto ADDR + rIi;


JXN/JXZ/JXP ADDR,i      if (rX<0 or rX==0 or rX>0) then goto ADDR + rIi;
JXNN/JXNZ/JXNP ADDR,i   if (rX>=0 or rX!=0 or rX<=0) then goto ADDR + rIi;


J?N/J?Z/J?P ADDR,i      if (rI?<0 or rI?==0 or rI?>0) then goto ADDR + rIi;
J?NN/J?NZ/J?NP ADDR,i   if (rI?>=0 or rI?!=0 or rI?<=0) then goto ADDR + rIi;


MOVE ADDR,i(F)          for (n = 0; n < F; n++, rI1++)
                            memory[rI1] := memory[ADDR+rIi+n];

SLA/SRA ADDR,i          shift rA to the left/right by ADDR+rIi bytes
SLAX/SRAX ADDR,i        shift (rA,rX) to the left/right by ADDR+rIi bytes
SLC/SRC ADDR,i          rotate (rA,rX) to the left/right by ADDR+rIi bytes  

NOP                     do nothing;
HLT                     halt execution;

IN ADDR,i(F)            read in one block from input unit F
                        into memory[ADDR + rIi] onwards;

OUT ADDR,i(F)           output one block to unit F
                        from memory[ADDR + rIi] onwards;

IOC ADDR,i(F)           send control instruction to i/o unit F;
JRED ADDR,i(F)          if (i/o unit F is ready) then goto ADDR + rIi;
JBUS ADDR,i(F)          if (i/o unit F is busy) then goto ADDR + rIi;
NUM                     rA := numerical value of characters in (rA,rX);
CHAR                    (rA,rX) := character codes representing value of rA;
