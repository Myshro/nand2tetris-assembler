# This class takes a parsed .asm file and turns it into machine code 
# according to the HACK machine code specifications.

import my_parser

class Coder():
    def __init__(self, in_file_name, out_file_name):
        self.in_file_name = in_file_name
        self.parser = my_parser.Parser(in_file_name)
        self.out_file = open(out_file_name, "w")

        self.parser.mark_symbols()
        self.machine_code = []

        self.dest = {
            "null": "000",
            "M": "001",
            "D": "010",
            "A": "100",
            "MD": "011",
            "AM": "101",
            "AD": "110",
            "AMD": "111"
        }
        self.comp = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }
        self.jump = {
            "null": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }

    def create_a_command(self, input: int) -> str:
        code = "0"
        MAX_DIGITS = 15
        input = str(input)
        if input.isdigit():
            num = int(input)
            binary = bin(num)
            str_bin = str(binary[2:])
            zero_count = MAX_DIGITS - len(str_bin)
            for i in range(0, zero_count):
                code += "0"
            return (code + str_bin)

    # differentiates between @[number] command versus @[symbol] command
    def finalize_a_command(self, input: str) -> str:
        table = self.parser.table
        no_at = input.replace("@", "")
        if no_at in table:
            return self.create_a_command(table[no_at])
        else:
            return self.create_a_command(no_at)

    def create_c_command(self, input): 
        code = "111"

        c = self.parser.comp(input)
        code += self.comp[c]
        d = self.parser.dest(input)
        code += self.dest["null" if len(d) == 0 else d] 
        j = self.parser.jump(input)
        code += self.jump["null" if len(j) == 0 else j]

        return code
    
    def create_machine_code(self):
        for l in self.parser.cleansed:
            result = ""
            if (self.parser.is_a_command(l)):
                result = self.finalize_a_command(l)
            else:
                result = self.create_c_command(l)
            self.machine_code.append(result)
    
    def write_to_file(self):
        for l in self.machine_code:
            self.out_file.write(l + "\n")
        self.out_file.close()
        

coder = Coder("Pong.asm", "Out.hack")

coder.create_machine_code()
coder.write_to_file()

# print(coder.machine_code)
# print(coder.parser.table)
# print(coder.parser.labels)
# print(coder.parser.symbols)