def init_assembler(file_name):
    import re
    import code_to_instruction
    datatypes = {'.byte': [1, 0], '.halfword': [2, 1], '.word': [4, 2], '.doubleword': [8, 3], '.asciiz': [1, 4], '.ascii': [1, 5], '.space': [1, 6]}
    try:
        file_in = open(file_name, 'r')  # Start reading a file
    except FileNotFoundError:
        print("File does not exist")
        return 0, None, None
    memory_file = open('memory.b', 'r+b')  # Writing data section to a file
    instruction = open('instruction.b', 'wb')  # Writing instruction part
    file = []

    def number_to_binary(number, n):
        num = str(bin(number))
        num = num.split('b')[-1]
        if len(num) < n:
            k = n - len(num)
            while k > 0:
                num = "0" + num
                k = k - 1
        return num

    def number_to_2Scomplement(num, n):
        if n <= 0:
            raise ValueError("Number of bits should be greater than 0")
        if num in range(-2 ** (n - 1), 2 ** (n - 1)):
            if num > 0:
                return "0" + number_to_binary(num, n - 1)
            elif num == 0:
                return "0" * n
            else:
                k = 2 ** (n - 1) + num
                return "1" + number_to_binary(k, n - 1)
        else:
            raise ValueError("Number out of bound")

    def preprocessing_file(file_in):
        for line in file_in:  # Create a list of instructions
            # Remove comments, extra spaces and tabs in the boundary
            line = line.split('#')[0]
            line = line.rstrip('\n').rstrip().lstrip()
            if line == '':
                continue
            file.append(line)
        return file

    def data_and_text_section(file):
        i = 0
        data_and_text = {'data': None, 'text': None}
        data_section = []
        text_section = []

        for line in file:
            if line == ".data":
                if data_and_text['data'] is None:
                    data_and_text['data'] = i
                else:
                    raise KeyError('.data declaration already exists.')
            elif line == ".text":
                if data_and_text['text'] is None:
                    data_and_text['text'] = i
                else:
                    raise KeyError(".text declaration already exists.")
            i += 1

        # Separate the data and text section

        if data_and_text['text'] is None:
            raise NameError('.text not found!')

        if data_and_text['data'] is None:
            if data_and_text['text'] != 0:
                raise KeyError("Misplaced instructions before .text in line 1")
            else:
                text_section = file
        else:
            if not (data_and_text['text'] == 0 or data_and_text['data'] == 0):
                raise KeyError('Misplaced instructions in line 1. Neither in .text or .data')
            else:
                if data_and_text['text'] == 0:
                    text_section = file[1:data_and_text['data']]
                    data_section = file[data_and_text['data'] + 1:]
                else:
                    data_section = file[1:data_and_text['text']]
                    text_section = file[data_and_text['text'] + 1:]

        return data_section, text_section

    def build_symbol_table(data_section, text_section):
        symbol_table = {"data": {}, "text": {}}
        labelRex = re.compile(r':$')  # RegEx for labels

        i = 0
        while i < len(text_section):
            each = text_section[i]
            line = re.split(', |,| | , ', each)
            if labelRex.search(line[0]) is not None:
                line[0] = line[0].rstrip(':')
                if line[0] in symbol_table["text"]:
                    raise ValueError('Label already exists.')
                else:
                    symbol_table["text"].update({line[0]: i*32})
                    text_section = text_section[0:i] + text_section[i+1:]
            i += 1

        j = 0
        for each in data_section:
            line = each.split(' ')
            if labelRex.search(line[0]) is not None:
                line[0] = line[0].rstrip(':')
                if line[0] in symbol_table["data"]:
                    raise ValueError('Label already exists.')
                else:
                    if len(line) > 3:
                        if line[1] in ['.ascii', '.asciiz']:
                            st = line[2]
                            i = 3
                            while i < len(line):
                                st += ' ' + str(line[i])
                                i += 1
                            line = line[0:3]
                            line[2] = st
                        else:
                            raise ValueError("Avoid unnecessary spaces in data section. Usually before and after commas.")
                    label, type_of, value = line[0], line[1], line[2]
                    if type_of not in datatypes:
                        raise KeyError('Invalid data-type.')
                    if type_of == '.asciiz':
                        value = value.rstrip().lstrip()
                        if (value.startswith('"') and value.endswith('"')) or (
                            value.startswith("'") and value.endswith("'")):
                            value = value.rstrip("'").lstrip("'").rstrip('"').lstrip('"')
                            value += '\0'
                            symbol_table["data"].update({label: [j, datatypes[type_of][1], 8*len(value)]})
                            j += len(value) * 8
                        else:
                             raise ValueError('Invalid initialisaton of asciiz type.')
                    elif type_of == '.ascii':
                        value = value.rstrip().lstrip()
                        if (value.startswith('"') and value.endswith('"')) or (
                            value.startswith("'") and value.endswith("'")):
                            value = value.rstrip("'").lstrip("'").rstrip('"').lstrip('"')
                            symbol_table["data"].update({label: [j, datatypes[type_of][1], 8*len(value)]})
                            j += len(value) * 8
                        else:
                            raise ValueError('Invalid initialisaton of ascii type.')
                    elif type_of == '.space':
                        value = value.rstrip().lstrip()
                        try:
                            val = int(value)
                        except:
                            raise ValueError('Invalid length for space type.')
                        symbol_table["data"].update({label: [j, datatypes[type_of][1], 8*val]})
                        j += val * 8
                    else:
                        value = value.split(',')
                        l = datatypes[type_of][0]
                        symbol_table["data"].update({label: [j, datatypes[type_of][1], l * 8 * len(value)]})
                        j += l * 8 * len(value)
            else:
                raise ValueError('Label not found in a data section.')
        return symbol_table, data_section, text_section

    def write_to_file(text_section, data_section, symbol_table):
        for line in text_section:
            line = re.split(', |,| | , ', line)
            instruction_str = code_to_instruction.conversion_to_instruction(line[0], line[1:], symbol_table)
            instruction_bin = bytearray(instruction_str, encoding="ascii")
            instruction.write(instruction_bin)
        instruction.close()

        for each in data_section:
            line = re.split(' ', each)
            if len(line) > 3:
                if line[1] in ['.ascii', '.asciiz']:
                    st = line[2]
                    i = 3
                    while i < len(line):
                        st += ' ' + str(line[i])
                        i += 1
                    line = line[0:3]
                    line[2] = st
            label, type_of, value = line
            if type_of == '.asciiz':
                value = value.rstrip().lstrip()
                value = value.rstrip("'").lstrip("'").rstrip('"').lstrip('"')
                value += '\0'
                for val in value:
                    val = number_to_binary(ord(val), 8)
                    value_bin = bytearray(val, encoding="ascii")
                    memory_file.write(value_bin)
            elif type_of == '.ascii':
                value = value.rstrip().lstrip()
                value = value.rstrip("'").lstrip("'").rstrip('"').lstrip('"')
                for val in value:
                    val = number_to_binary(ord(val), 8)
                    value_bin = bytearray(val, encoding="ascii")
                    memory_file.write(value_bin)
            elif type_of == '.space':
                value = value.rstrip().lstrip()
                val = int(value)
                val = '0'*val
                value_bin = bytearray(val, encoding="ascii")
                memory_file.write(value_bin)
            elif type_of == '.byte':
                value = value.split(',')
                for l in value:
                    if len(l) > 1:
                        raise ValueError("Invalid input for byte")
                    else:
                        value_bin = bytearray(number_to_binary(ord(l), 8), encoding="ascii")
                        memory_file.write(value_bin)
            elif type_of == '.halfword':
                value = value.split(',')
                for l in value:
                    try:
                        if l[0] == "-":
                            val = -1*(int(l[1:]))
                        else:
                            val = int(l)
                    except:
                        raise ValueError('Input not a integer')
                    if val not in range(0, (2**16)-1):
                        raise OverflowError('Input not a .halfword datatype')
                    else:
                        val = number_to_binary(val, 16)
                        value_bin = bytearray(val, encoding="ascii")
                        memory_file.write(value_bin)
            elif type_of == '.word':
                value = value.split(',')
                for l in value:
                    try:
                        if l[0] == "-":
                            val = -1*(int(l[1:]))
                        else:
                            val = int(l)
                    except:
                        raise ValueError('Input not a integer')
                    if val not in range(-(2**31), 2**31):
                        raise OverflowError('Input not a .word datatype')
                    else:
                        val = number_to_2Scomplement(val, 32)
                        value_bin = bytearray(val, encoding="ascii")
                        memory_file.write(value_bin)
            elif type_of == '.doubleword':
                value = value.split(',')
                for l in value:
                    try:
                        if l[0] == "-":
                            val = -1*(int(l[1:]))
                        else:
                            val = int(l)
                    except:
                        raise ValueError('Input not a integer')
                    if val not in range(-2**64, 2**64):
                        raise OverflowError('Input not a .doubleword datatype')
                    else:
                        val = number_to_2Scomplement(val, 64)
                        value_bin = bytearray(val, encoding="ascii")
                        memory_file.write(value_bin)
            else:
                raise KeyError(type_of + 'Datatype is not supported')
        st = bytearray(number_to_binary(ord('\0'), 8), encoding="ascii")
        memory_file.write(st)
        memory_file.close()

    asm_file = preprocessing_file(file_in)
    section_data, section_text = data_and_text_section(asm_file)
    if 'main:' not in section_text:
        print("main: not found!!!")
        return 0, None, None
    s_table, section_data, section_text = build_symbol_table(section_data, section_text)
    write_to_file(section_text, section_data, s_table)
    return 1, section_data, s_table
