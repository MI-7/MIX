from utility import *
from logger import *

input_file = "./blockdevices/in"
output_file = "./blockdevices/out"

def read_from_inputdevice():
    f = open(input_file, 'r')
    inputs = f.read()
    inputs_in_list = inputs.splitlines()
    mixlog (MDEBUG, inputs_in_list)
    f.close()
    
    return [dectobin_withsign(int(i), WORD_WIDTH) for i in inputs_in_list]

def write_into_outputdevice(contents, i):
    f = open(output_file+str(i), 'w')
    for c in contents:
        print(partstodec_withsign(c), file=f)
    f.close()

if __name__ == "__main__":
    write_into_outputdevice(read_from_inputdevice())