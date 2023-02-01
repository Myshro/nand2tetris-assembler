# This class takes a .asm file and removes all comments / white space and 
# breaks each command into its separate parts

class Parser():
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name)
        
        self.labels = {}
        self.symbols = {}
        self.table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
        }
        self.cleansed = []
        self.counter = 16
    
    def remove_whitespace_or_comments(self):
        self.cleansed = []
        # all for loops using "l", the "l" stands for line
        for l in self.file:
            no_space = l.replace(" ", "")
            end = no_space.find("//")
            p_line = no_space[0:end]
            if len(p_line) != 0:
                self.cleansed.append(p_line)

    def mark_labels_then_remove(self):
        self.remove_whitespace_or_comments()
        line_num = 0
        dead_labels = []
        for l in self.cleansed:
            if (self.is_label(l)):
                # line[1:-1] gets rid of ( and )
                self.labels[l[1:-1]] = line_num 
                dead_labels.append(l)
                line_num -= 1
            line_num += 1
        for label in dead_labels:
            self.cleansed.remove(label)
    
    def mark_symbols(self):
        self.mark_labels_then_remove()
        for l in self.cleansed:
            # Used f[1:] as this gets rid of the starting @ symbol
            if (
            self.is_a_command(l) 
            and not l[1:] in self.symbols 
            and not l[1:] in self.labels 
            and not l[1:] in self.table
            and not l[1:].isdigit()):
                self.symbols[l[1:]] = self.counter
                self.counter += 1
            #elif (self.is_c_command(f)):
                #print(f)
                #print("Dest:{}\nComp:{}\nJump:{}\n"
                #    .format(self.dest(f), self.comp(f), self.jump(f)))
                #return
        self.add_symbols_and_labels_to_table()
    
    def add_symbols_and_labels_to_table(self):
        self.table.update(self.labels)
        self.table.update(self.symbols)
        
    
    def is_a_command(self, input):
        return False if input.find("@") == -1 else True 
    

    def is_label(self, input):
        return False if input.find("(") == -1 else True
        
    def is_c_command(self, input):
        return not self.is_label(input) and not self.is_a_command(input)

    def dest(self, input):
        end = input.find("=")
        if end == -1:
            return ""
        return input[:end]

    def comp(self, input):
        start = input.find("=") + 1 if input.find("=") != -1 else 0
        end = input.find(";") if input.find(";") != -1 else len(input)
        return input[start:end]

    def jump(self, input):
        start = input.find(";")
        if start == -1:
            return ""
        return input[start + 1:]


# print(p.remove_whitespace_or_comments())

# p.mark_symbols()
# print(p.table)
# print(p.cleansed)
# p = Parser("Rect.asm")
# p.mark_symbols()
 
# print(p.labels)
# print(p.symbols)