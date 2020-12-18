import sys

class assembler:
    COMP_TABLE = {
        '0':    '101010',
        '1':    '111111',
        '-1':   '111010',
        'D':    '001100',
        'A':    '110000',
        '!D':   '001101',
        '!A':   '110001',
        '-D':   '001111',
        '-A':   '110011',
        'D+1':  '011111',
        'A+1':  '110111',
        'D-1':  '001110',
        'A-1':  '110010',
        'D+A':  '000010',
        'D-A':  '010011',
        'A-D':  '000111',
        'D&A':  '000000',
        'D|A':  '010101',
    }

    DEST_TABLE = {
        '':     '000',
        'M':    '001',
        'D':    '010',
        'MD':   '011',
        'A':    '100',
        'AM':   '101',
        'AD':   '110',
        'AMD':  '111',
    }

    JUMP_TABLE = {
        '':     '000',
        'JGT':  '001',
        'JEQ':  '010',
        'JGE':  '011',
        'JLT':  '100',
        'JNE':  '101',
        'JLE':  '110',
        'JMP':  '111',
    }

    def __init__(self):
        self.label_table = {
            'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,
            'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15, 
            'SCREEN': 16384, 'KBD': 24576,
            'SP': 0, 'LCL': 1, 'ARG': 2,
            'THIS': 3, 'THAT': 4
        }
        self.custom_label_index = 16

    def remove_whitespace(self, s: str):
        whitespaces = [' ', '\t', '\n', '\r']
        s = s.strip()
        t = ''
        for c in s:
            if not c in whitespaces: 
                t += c

        return t

    def convert_binary_15(self, n: int):
        s = bin(n)[2:]
        while len(s) < 15:
            s = '0' + s
        return s

    def preprocess(self, line: str):
        comment_position = line.find('//')
        if comment_position >= 0:
            line = line[0:comment_position]

        line = self.remove_whitespace(line)
        return line

    def get_label_value(self, label: str):
        if not label in self.label_table:
            self.label_table[label] = self.custom_label_index
            self.custom_label_index += 1

        return self.label_table[label]

    def assemble_a_type(self, instruction: str):
        try:                
            value = int(instruction[1:])
        except ValueError:
            value = self.get_label_value(instruction[1:])

        value = self.convert_binary_15(value)
        return '0' + value

    def assemble_c_type(self, instruction: str):
        machine_code = '111'

        dest = ''
        comp = instruction
        jump = ''
        if comp.find(';') >= 0:
            comp, jump = comp.split(';')
        if comp.find('=') >= 0:
            dest, comp = comp.split('=')

        if comp.find('M') >= 0:
            machine_code += '1'
            comp = comp.replace('M', 'A')
        else:
            machine_code += '0'

        machine_code += self.COMP_TABLE[comp]
        machine_code += self.DEST_TABLE[dest]
        machine_code += self.JUMP_TABLE[jump]
        
        return machine_code

    def assemble_label_declaration(self, instruction: str):
        label = instruction[1:-1]
        value = self.get_label_value(label)
        instruction = '@' + str(value)
        return self.assemble_a_type(instruction)

    def assemble(self, source_code: str):
        preprocessed_source_code = []
        for line in source_code.split('\n'):
            preprocessed_line = self.preprocess(line)
            if len(preprocessed_line) > 0:
                preprocessed_source_code.append(preprocessed_line)
        source_code = preprocessed_source_code

        i = 0
        for instruction in source_code:
            if instruction[0] == '(':
                label = instruction[1:-1]
                self.label_table[label] = i
            else:
                i += 1

        machine_code = []
        for instruction in source_code:
            if instruction[0] == '@':
                machine_code.append(self.assemble_a_type(instruction))
            elif instruction[0] != '(':
                machine_code.append(self.assemble_c_type(instruction))

        machine_code = '\n'.join(machine_code)
        return machine_code

if len(sys.argv) < 2:
    print(sys.argv[1] + " infile [outfile]")
infile = sys.argv[1]
outfile = 'a.hack'
if len(sys.argv) > 2:
    outfile = sys.argv[2]

with open(infile) as f:
    source_code = f.read()
    
ass = assembler()
machine_code = ass.assemble(source_code)

with open(outfile, 'w+') as f:
    f.write(machine_code)

