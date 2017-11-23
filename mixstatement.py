statementdict ={
                'NOP'       : 0,
                'ADD'       : 1,
                'SUB'       : 2,
                'MUL'       : 3,
                'DIV'       : 4,
                'HLT'       : 5,
                'MOVE'      : 7,
                'LDA'       : 8,
                'LD1'       : 9,     # LDi
                'LD2'       : 10,    # LDi
                'LD3'       : 11,    # LDi
                'LD4'       : 12,
                'LD5'       : 13,
                'LD6'       : 14,
                'LDX'       : 15,
                'LDAN'      : 16,
                'LD1N'      : 17,    # LDiN
                'LD2N'      : 18,    # LDiN
                'LD3N'      : 19,    # LDiN
                'LD4N'      : 20,    # LDiN
                'LD5N'      : 21,    # LDiN
                'LD6N'      : 22,    # LDiN
                'LDXN'      : 23,
                'STA'       : 24,
                'ST1'       : 25,
                'ST2'       : 26,
                'ST3'       : 27,
                'ST4'       : 28,
                'ST5'       : 29,
                'ST6'       : 30,
                'STX'       : 31,
                'STJ'       : 32,
                'STZ'       : 33,
                'JMP'       : 100,
                'JOV'       : 102,
                'JNOV'      : 103,
                'JE'        : 105,
                'JGE'       : 107,
                'JXZ'       : 117,
                'J3Z'       : 130,
                'J1P'       : 134,
                'J2P'       : 135,
                'J3P'       : 136,
                'J4P'       : 137,
                'J5P'       : 138,
                'J6P'       : 139,
                'J6NP'      : 157,
                'ENTA'      : 48,
                'ENT1'      : 49,
                'ENT2'      : 50,
                'ENT3'      : 51,
                'ENT4'      : 52,
                'ENT5'      : 53,
                'ENT6'      : 54,
                'ENTX'      : 55,
                'ENNA'      : 56,
                'ENNX'      : 57,
                'ENN1'      : 58,
                'ENN2'      : 59,
                'ENN3'      : 60,
                'ENN4'      : 61,
                'ENN5'      : 62,
                'ENN6'      : 63,
                'INCA'      : 64,
                'INCX'      : 65,
                'INC1'      : 66,
                'INC2'      : 67,
                'INC3'      : 68,
                'INC4'      : 69,
                'INC5'      : 70,
                'INC6'      : 71,
                'DECA'      : 72,
                'DECX'      : 73,
                'DEC1'      : 74,
                'DEC2'      : 75,
                'DEC3'      : 76,
                'DEC4'      : 77,
                'DEC5'      : 78,
                'DEC6'      : 79,
                'CMPA'      : 80,
                'CMPX'      : 81,
                'CMP1'      : 82,
                'CMP2'      : 83,
                'CMP3'      : 84,
                'CMP4'      : 85,
                'CMP5'      : 86,
                'CMP6'      : 87,
                'NUM'       : 200,
                'CHAR'      : 201,
                'SLA'       : 300,
                'SRA'       : 301,
                'SLAX'      : 302,
                'SRAX'      : 303,
                'SLC'       : 304,
                'SRC'       : 305,
                }

statementprofilingdict =   {
                            'NOP'       : 1,
                            'ADD'       : 2,
                            'SUB'       : 2,
                            'MUL'       : 10,
                            'DIV'       : 12,
                            'HLT'       : 1,
                            'LDA'       : 2,
                            'LD1'       : 2,    # LDi
                            'LD2'       : 2,    # LDi
                            'LD3'       : 2,    # LDi
                            'LD4'       : 2,
                            'LD5'       : 2,
                            'LD6'       : 2,
                            'LDX'       : 2,
                            'LDAN'      : 2,
                            'LD1N'      : 2,    # LDiN
                            'LD2N'      : 2,    # LDiN
                            'LD3N'      : 2,    # LDiN
                            'LD4N'      : 2,    # LDiN
                            'LD5N'      : 2,    # LDiN
                            'LD6N'      : 2,    # LDiN
                            'LDXN'      : 2,
                            'STA'       : 2,
                            'ST1'       : 2,
                            'ST2'       : 2,
                            'ST3'       : 2,
                            'ST4'       : 2,
                            'ST5'       : 2,
                            'ST6'       : 2,
                            'STX'       : 2,
                            'STJ'       : 2,
                            'STZ'       : 2,
                            'JMP'       : 1,
                            'JOV'       : 1,
                            'JNOV'      : 1,
                            'JE'        : 1,
                            'JGE'       : 1,
                            'JXZ'       : 1,
                            'J3Z'       : 1,
                            'J1P'       : 1,
                            'J2P'       : 1,
                            'J3P'       : 1,
                            'J4P'       : 1,
                            'J5P'       : 1,
                            'J6P'       : 1,
                            'J6NP'      : 1,
                            'ENTA'      : 1,
                            'ENT1'      : 1,
                            'ENT2'      : 1,
                            'ENT3'      : 1,
                            'ENT4'      : 1,
                            'ENT5'      : 1,
                            'ENT6'      : 1,
                            'ENTX'      : 1,
                            'ENNA'      : 1,
                            'ENNX'      : 1,
                            'ENN1'      : 1,
                            'ENN2'      : 1,
                            'ENN3'      : 1,
                            'ENN4'      : 1,
                            'ENN5'      : 1,
                            'ENN6'      : 1,
                            'INCA'      : 1,
                            'INCX'      : 1,
                            'INC1'      : 1,
                            'INC2'      : 1,
                            'INC3'      : 1,
                            'INC4'      : 1,
                            'INC5'      : 1,
                            'INC6'      : 1,
                            'DECA'      : 1,
                            'DECX'      : 1,
                            'DEC1'      : 1,
                            'DEC2'      : 1,
                            'DEC3'      : 1,
                            'DEC4'      : 1,
                            'DEC5'      : 1,
                            'DEC6'      : 1,
                            'CMPA'      : 1,
                            'CMP1'      : 1,
                            'CMP2'      : 1,
                            'CMP3'      : 1,
                            'CMP4'      : 1,
                            'CMP5'      : 1,
                            'CMP6'      : 1,
                            'MOVE'      : 1,  # 1 + 2 * each word moved
                            'NUM'       : 10,
                            'CHAR'      : 10,
                            'CMPX'      : 1,
                            'CMP1'      : 1,
                            'CMP2'      : 1,
                            'CMP3'      : 1,
                            'CMP4'      : 1,
                            'CMP5'      : 1,
                            'CMP6'      : 1,
                            'SLA'       : 1,
                            'SRA'       : 1,
                            'SLAX'      : 1,
                            'SRAX'      : 1,
                            'SLC'       : 1,
                            'SRC'       : 1,
                            }

OP_NOP=0
OP_ADD=1
OP_SUB=2
OP_MUL=3
OP_DIV=4
OP_HLT=5
OP_MOVE=7
OP_LDA=8
OP_LD1=9
OP_LD2=10
OP_LD3=11
OP_LD4=12
OP_LD5=13
OP_LD6=14
OP_LDX=15
OP_LDAN=16
OP_LD1N=17
OP_LD2N=18
OP_LD3N=19
OP_LD4N=20
OP_LD5N=21
OP_LD6N=22
OP_LDXN=23
OP_STA=24
OP_ST1=25
OP_ST2=26
OP_ST3=27
OP_ST4=28
OP_ST5=29
OP_ST6=30
OP_STX=31
OP_STJ=32
OP_STZ=33
OP_JMP=100
OP_JOV=102
OP_JNOV=103
OP_JE=105
OP_JGE=107
OP_JXZ=117
OP_J1Z=128
OP_J2Z=129
OP_J3Z=130
OP_J4Z=131
OP_J5Z=132
OP_J6Z=133
OP_J1P=134
OP_J2P=135
OP_J3P=136
OP_J4P=137
OP_J5P=138
OP_J6P=139
OP_J6NP=157
OP_ENTA=48
OP_ENT1=49
OP_ENT2=50
OP_ENT3=51
OP_ENT4=52
OP_ENT5=53
OP_ENT6=54
OP_ENTX=55
OP_ENNA=56
OP_ENNX=57
OP_ENN1=58
OP_ENN2=59
OP_ENN3=60
OP_ENN4=61
OP_ENN5=62
OP_ENN6=63
OP_INCA=64
OP_INCX=65
OP_INC1=66
OP_INC2=67
OP_INC3=68
OP_INC4=69
OP_INC5=70
OP_INC6=71
OP_DECA=72
OP_DECX=73
OP_DEC1=74
OP_DEC2=75
OP_DEC3=76
OP_DEC4=77
OP_DEC5=78
OP_DEC6=79
OP_CMPA=80
OP_CMPX=81
OP_CMP1=82
OP_CMP2=83
OP_CMP3=84
OP_CMP4=85
OP_CMP5=86
OP_CMP6=87
OP_NUM=200
OP_CHAR=201

OP_SLA=300
OP_SRA=301
OP_SLAX=302
OP_SRAX=303
OP_SLC=304
OP_SRC=305