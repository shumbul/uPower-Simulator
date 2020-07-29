import assembler
import instruction_to_execute
import os
data_section, symbol_table = None, None


def initialize(N, load=False):
    regs = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'R7': 0, 'R8': 0, 'R9': 0, 'R10': 0, 'R11': 0, 'R12': 0, 'R13': 0, 'R14': 0, 'R15': 0, 'R16': 0, 'R17': 0, 'R18' : 0, 'R19' : 0, 'R20' : 0, 'R21' : 0, 'R22' : 0, 'R23' : 0, 'R24' : 0, 'R25' : 0, 'R26' : 0, 'R27' : 0, 'R28' : 0, 'R29' : 0, 'R30' : 0, 'R31' : 0, 'CIA' : 0, 'NIA' : 0, 'SRR0' : 0, 'CR' : 0, 'LR' : 0}
    if load:
        statinfo = os.stat('instruction.b')
        N = int(statinfo.st_size)
        if N % 32 != 0:
            raise ValueError("Error in encoding the assembly file")
        N = int(N/32)
    return regs, N


def execute_instruction(instruction, regs, memory_file, symbol_table):
    regs = instruction_to_execute.execute_instruction(instruction, regs, memory_file, symbol_table)
    return regs


def step(regs, instructions, memory_file, n=1):
    global N
    '''
    if regs['CIA'] == int(symbol_table["text"]['main']/32):
        regs = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'R7': 0, 'R8': 0, 'R9': 0, 'R10': 0,
                'R11': 0, 'R12': 0, 'R13': 0, 'R14': 0, 'R15': 0, 'R16': 0, 'R17': 0, 'R18': 0, 'R19': 0, 'R20': 0,
                'R21': 0, 'R22': 0, 'R23': 0, 'R24': 0, 'R25': 0, 'R26': 0, 'R27': 0, 'R28': 0, 'R29': 0, 'R30': 0,
                'R31': 0, 'CIA': int(symbol_table["text"]['main'] / 32),
                'NIA': int(symbol_table["text"]['main'] / 32), 'SRR0': 0, 'CR': 0, 'LR': 0}
    '''
    while regs['CIA'] < N and n > 0:
        n -= 1
        regs['CIA'] = regs['NIA']
        regs['NIA'] += 1
        if regs['CIA'] >= N:
            break
        instructions.seek(regs['CIA']*32, 0)
        instr = instructions.read(32).decode('ascii')
        regs, _ = execute_instruction(instr, regs, memory_file, symbol_table)
    if regs['CIA'] >= N:
        regs['CIA'] = int(symbol_table["text"]['main']/32)
        regs['NIA'] = regs['CIA']


def run(regs, instructions, memory_file):
    global N
    '''
    if regs['CIA'] == int(symbol_table["text"]['main']/32):
        regs = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'R7': 0, 'R8': 0, 'R9': 0, 'R10': 0,
                'R11': 0, 'R12': 0, 'R13': 0, 'R14': 0, 'R15': 0, 'R16': 0, 'R17': 0, 'R18': 0, 'R19': 0, 'R20': 0,
                'R21': 0, 'R22': 0, 'R23': 0, 'R24': 0, 'R25': 0, 'R26': 0, 'R27': 0, 'R28': 0, 'R29': 0, 'R30': 0,
                'R31': 0, 'CIA': int(symbol_table["text"]['main'] / 32),
                'NIA': int(symbol_table["text"]['main'] / 32) + 1, 'SRR0': 0, 'CR': 0, 'LR': 0}
    '''
    cont = True
    while regs['CIA'] < N and cont:
        regs['CIA'] = regs['NIA']
        regs['NIA'] += 1
        if regs['CIA'] >= N:
            break
        instructions.seek(regs['CIA'] * 32, 0)
        instr = instructions.read(32).decode('ascii')
        regs, cont = execute_instruction(instr, regs, memory_file, symbol_table)
    regs['CIA'] = int(symbol_table["text"]['main'] / 32)
    regs['NIA'] = regs['CIA']
    print()


def help_fun(param):
    helper_function = {'exit': ['exit', 'Exits from the simulator.'],
                       'load': ['load FILE', 'Load FILE of assembly code into memory.'],
                       'quit': ['quit', 'Quits from the simulator. Same as exit.'],
                       'print': ['print Rn', 'Print register n.'],
                       'print_all_regs': ['print_all_regs', 'Print all uPower registers.'],
                       'print_all_regs_hex': ['print_all_regs_hex', 'Print all uPower registers in hex.'],
                       'read': ['read FILE', 'Read FILE of assembly code into memory. Same as load.'],
                       'run': ['run', 'runs the assembly program till the end'],
                       'step': ['step', 'executes the next instruction'],
                       'step_N': ['step_N', 'executes the next N instructions'],
                       'reinitialize': ['reinitialize', 'Clears the whole memory and registers.'],
                       }
    if not param:
        print("Following are the functionalities provided by uPowerSimulator\n" + "--"*60)
        for defn in helper_function.values():
            print(defn[0] + "\t" + defn[1])
        print("--" * 60)
    elif len(param) != 1:
        print('Invalid input. Type "help" for more information')
    else:
        param = param[0]
        if param in helper_function:
            print(helper_function[param][0] + "\t" + helper_function[param][1])
        else:
            print('Invalid option. Type "help" for more information')


N = 0   # Stores number of instructions
regs, N = initialize(N)
file_loaded = False
instructions, memory_file, stack_file = None, None, None
regs['CIA'] = 0  # Stores the current instruction number
regs['NIA'] = 1  # Stores the next instruction number
print("\n" + "=="*84)
print(" \t\t\t\t\t\t\t uPowerSimulator \t A Text-based simulator for uPower ISA\n")
print('Type "help" to display all options, or "help <option>" to learn more about any particular option\n')
print("=="*84)
inp = input(">> ")
inp = inp.rstrip().lstrip()
while inp != "exit" and inp != "quit":
    if inp == "":
        inp = input(">> ")
        inp = inp.rstrip().lstrip()
        continue
    inp = inp.split(' ')
    if inp[0] == "help":
        help_fun(inp[1:])
    elif inp[0] == "load" or inp[0] == "read":
        if file_loaded:
            print("A file is already loaded")
        elif len(inp) > 2:
            print("Invalid number of arguments")
        elif inp[1].endswith('.asm'):
            open('instruction.b', 'wb').close()
            open('memory.b', 'r+b').close()
            open('stack.b', 'r+b').close()
            flag, data_section, symbol_table = assembler.init_assembler(inp[1])
            if flag:
                file_loaded = True
                regs, N = initialize(N, True)
                regs['CIA'] = int(symbol_table["text"]['main']/32)
                regs['NIA'] = regs['CIA'] + 1
                instructions = open('instruction.b', 'rb')
                memory_file = open('memory.b', 'r+b')       # Check the mode
                stack_file = open('stack.b', 'r+b')          # Check the mode
        else:
            print('Invalid file type')
    elif inp[0] == "reinitialize":
        if len(inp) > 1:
            print("Invalid number of input for reinitialize")
        else:
            regs, N = initialize(N)
            instructions.close()
            stack_file.close()
            memory_file.close()
            file_loaded = False
            pass        # Fill this part # Fill this part # Fill this part # Fill this part # Fill this part # Fill this part
    elif inp[0] == "print":
        if len(inp) != 2:
            print("Invalid number of arguments for print")
        else:
            if inp[1] in regs:
                print(inp[1] + '\t' + str(regs[inp[1]]))
            else:
                print('Wrong argument for print register')
    elif inp[0] == "print_all_regs":
        if len(inp) != 1:
            print("Invalid number of arguments for print")
        else:
            i = 0
            print("\nGeneral purpose registers")
            for reg, value in regs.items():
                if i % 8 == 0:
                    print()
                if i == 32:
                    print("\nSpecial purpose registers\n")
                print(reg + " : " + str(value)+'\t\t', end='')
                i += 1
            print()
    elif inp[0] == "print_all_regs_hex":
        if len(inp) != 1:
            print("Invalid number of arguments for print")
        else:
            i = 0
            print("\nGeneral purpose registers")
            for reg, value in regs.items():
                if i % 6 == 0 and i<32:
                    print()
                if i == 32:
                    print("\n\nSpecial purpose registers\n")
                print(reg + " : " + str(hex(value)) + '\t\t', end='')
                i += 1
            print()
    elif inp[0] == 'run':
        if len(inp) != 1:
            print("Invalid number of arguments for run")
        elif not file_loaded:
            print("No file is loaded")
        else:
            run(regs, instructions, memory_file)
    elif inp[0] == 'step':
        if not file_loaded:
            print("No file is loaded")
        elif len(inp) == 1:
            step(regs, instructions, memory_file)
        elif len(inp) == 2:
            try:
                t = int(inp[1])
            except:
                raise ValueError("Enter valid integer as argument for step")
            step(regs, instructions, memory_file, t)
        else:
            print("Invalid number of arguments for step")
    else:
        print('Unknown uPowerSimulator command. Type "help" for more information ')
    inp = input(">> ")
    inp = inp.rstrip().lstrip()

'''
instructions.close()
stack_file.close()
memory_file.close()
'''

print("Exiting the simulator ...")
