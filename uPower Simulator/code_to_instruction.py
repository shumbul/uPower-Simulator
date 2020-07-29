def number_to_binary(number, n):
    num = str(bin(number))
    num = num.split('b')[-1]
    if len(num) < n:
        k = n - len(num)
        while (k > 0):
            num = "0" + num
            k = k - 1
    return num


def sep_bracket(param):
    # param of the D(RA)
    D = param.split('(')[0].rstrip()
    param = param.split('(')[1].lstrip()
    RA = param.split(')')[0].lstrip()
    # returns 2 strings such that we need to find the Reg[RA]+D
    return D, RA


def number_to_2s_complement(num, n):
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


def conversion_to_instruction(mnemonic, params, symbol_table):
    data_size = {0: 1, 1: 2, 2: 4, 3: 8, 4: 1}
    data_table = symbol_table['data']
    text_table = symbol_table['text']
    instruction_32_bits = ""

    if mnemonic == "la":
        instruction_32_bits += (number_to_binary(14, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'la'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
            except:
                raise ValueError("Invalid register name")
            if params[1] not in data_table:
                raise ValueError("Label not found")
            if rt not in range(0, 32):
                raise ValueError("Out of bound register")
            rt = number_to_binary(rt, 5)
            si = number_to_binary(data_table[params[1]][0], 16)
            instruction_32_bits += rt
            instruction_32_bits += "00000"
            instruction_32_bits += si

    elif mnemonic == "add":
        instruction_32_bits+=(number_to_binary(31, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'add'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs or params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(params[1][1:])
                rb = int(params[2][1:])
            except ValueError:
                print("Invalid register name")
            if rt not in range(0,32) or ra not in range(0,32) or rb not in range(0,32):
                    raise ValueError("Out of bound register")

            rt=number_to_binary(rt,5)
            rb=number_to_binary(rb,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rt
            instruction_32_bits+=ra
            instruction_32_bits+=rb
            instruction_32_bits+="0"
            instruction_32_bits+=number_to_binary(266,9)
            instruction_32_bits+="0" 

    elif mnemonic == "add":
        instruction_32_bits+=(number_to_binary(31, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'add'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs or params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(params[1][1:])
                rb = int(params[2][1:])
            except:
                raise ValueError("Invalid register name")
            if rt not in range(0, 32) or ra not in range(0, 32) or rb not in range(0, 32):
                    raise ValueError("Out of bound register")

            rt=number_to_binary(rt,5)
            rb=number_to_binary(rb,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rt
            instruction_32_bits+=ra
            instruction_32_bits+=rb
            instruction_32_bits+="0"
            instruction_32_bits+=number_to_binary(266,9)
            instruction_32_bits+="0"

    elif mnemonic == "addi":
        instruction_32_bits += (number_to_binary(14, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'addi'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(params[1][1:])
                si = int(params[2])
            except:
                raise ValueError("Invalid register name")
            if rt not in range(0, 32) or ra not in range(0,32):
                raise ValueError("Out of bound register")
            if si not in range(-(2 ** 15), (2 ** 15) - 1):
                raise ValueError("Out of bound integer")
            rt = number_to_binary(rt, 5)
            ra = number_to_binary(ra, 5)
            if si >= 0:
              si = number_to_binary(si, 16)
            else:
              si = number_to_2s_complement(si, 16)
            instruction_32_bits+=rt
            instruction_32_bits+=ra
            instruction_32_bits+=si

    elif mnemonic == "subi":
        instruction_32_bits += (number_to_binary(14, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'subi'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(params[1][1:])
                si = int(params[2])
            except:
                raise ValueError("Invalid register name")
            si *= -1
            if rt not in range(0, 32) or ra not in range(0,32):
                raise ValueError("Out of bound register")
            if si not in range(-(2 ** 15), (2 ** 15) - 1):
                raise ValueError("Out of bound integer")
            rt = number_to_binary(rt, 5)
            ra = number_to_binary(ra, 5)
            if si >= 0:
              si = number_to_binary(si, 16)
            else:
              si = number_to_2s_complement(si, 16)
            instruction_32_bits+=rt
            instruction_32_bits+=ra
            instruction_32_bits+=si

    elif mnemonic == "li":
        instruction_32_bits += (number_to_binary(14, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'li'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                si = int(params[1])
            except:
                raise ValueError("Invalid register name")
            if rt not in range(0, 32):
                raise ValueError("Out of bound register")
            if si not in range(-(2 ** 15), (2 ** 15) - 1):
                raise ValueError("Out of bound integer")
            rt = number_to_binary(rt, 5)
            ra = "00000"
            if si >= 0:
                si = number_to_binary(si, 16)
            else:
                si = number_to_2s_complement(si, 16)
            instruction_32_bits += rt
            instruction_32_bits += ra
            instruction_32_bits += si

    elif mnemonic == "addis":
        instruction_32_bits += (number_to_binary(15, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'addis'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(params[1][1:])
                si = int(params[2])
            except:
                raise ValueError("Invalid register name")
            if rt not in range(0,32) or ra not in range(0,32):
                raise ValueError("Out of bound register")
            if si not in range(-(2**15), (2**15) -1):
                raise ValueError("Out of bound integer")
            rt = number_to_binary(rt, 5)
            ra = number_to_binary(ra, 5)
            
            if si >= 0:
                si = number_to_binary(si, 16)
            else:
                si = number_to_2s_complement(si, 16)
            instruction_32_bits += rt
            instruction_32_bits += ra
            instruction_32_bits += si

    elif mnemonic == "subis":
        instruction_32_bits += (number_to_binary(15, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'subis'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(params[1][1:])
                si = int(params[2])
            except:
                raise ValueError("Invalid register name")
            si *= -1
            if rt not in range(0, 32) or ra not in range(0, 32):
                raise ValueError("Out of bound register")
            if si not in range(-(2 ** 15), (2 ** 15) - 1):
                raise ValueError("Out of bound integer")
            rt = number_to_binary(rt, 5)
            ra = number_to_binary(ra, 5)

            if si >= 0:
                si = number_to_binary(si, 16)
            else:
                si = number_to_2s_complement(si, 16)
            instruction_32_bits += rt
            instruction_32_bits += ra
            instruction_32_bits += si

    elif mnemonic == "lis":
        instruction_32_bits += (number_to_binary(15, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'lis'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                si = int(params[1])

            except:
                raise ValueError("Invalid register name")
            if rt not in range(0, 32):
                raise ValueError("Out of bound register")
            if si not in range(-(2 ** 15), (2 ** 15) - 1):
                raise ValueError("Out of bound integer")
            rt = number_to_binary(rt, 5)

            if si >= 0:
                si = number_to_binary(si, 16)
            else:
                si = number_to_2s_complement(si, 16)
            instruction_32_bits += rt
            instruction_32_bits += '00000'
            instruction_32_bits += si

    elif mnemonic == "and":
        instruction_32_bits += (number_to_binary(31, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'and'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs or params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                rb = int(params[2][1:])
            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32) or rb not in range(0,32):
                    raise ValueError("Out of bound register")   
            rs=number_to_binary(rs,5)
            rb=number_to_binary(rb,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rs
            instruction_32_bits+=ra
            instruction_32_bits+=rb
            instruction_32_bits+=(number_to_binary(28,10))
            instruction_32_bits+="0"

    elif mnemonic== "andi":
        instruction_32_bits += (number_to_binary(28, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'andi'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rt = int(params[1][1:])
                si = int(params[2])
            except:
                raise ValueError("Invalid register name")
            if rt not in range(0,32) or ra not in range(0,32):
                raise ValueError("Out of bound register")
            if si not in range(-2**(15), 2**16 -1):
                raise ValueError("Out of bound integer")
            rt = number_to_binary(rt,5)
            ra = number_to_binary(ra,5)
            
            if si >= 0:
              si=number_to_binary(si,16)
            else:
              si=number_to_2s_complement(si, 16)
            instruction_32_bits+=rt
            instruction_32_bits+=ra
            instruction_32_bits+=si

    elif mnemonic == "extsw":
        instruction_32_bits+=(number_to_binary(31, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'extsw'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0, 32):
                    raise ValueError("Out of bound register")

            rs=number_to_binary(rs,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rs
            instruction_32_bits+=ra
            instruction_32_bits+="00000"
            instruction_32_bits+=number_to_binary(986,10)
            instruction_32_bits+="0"

    elif mnemonic == "nand":
        instruction_32_bits += (number_to_binary(31, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'nand'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs or params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                rb = int(params[2][1:])
            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32) or rb not in range(0,32):
                raise ValueError("Out of bound register")
            rs=number_to_binary(rs, 5)
            rb=number_to_binary(rb, 5)
            ra=number_to_binary(ra, 5)
            instruction_32_bits += rs
            instruction_32_bits += ra
            instruction_32_bits += rb
            instruction_32_bits += (number_to_binary(476,10))
            instruction_32_bits += "0"

    elif mnemonic == "or":
        instruction_32_bits += (number_to_binary(31, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'or'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs or params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                rb = int(params[2][1:])
            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32) or rb not in range(0,32):
                raise ValueError("Out of bound register")
            rs=number_to_binary(rs,5)
            rb=number_to_binary(rb,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rs
            instruction_32_bits+=ra
            instruction_32_bits+=rb
            instruction_32_bits+=(number_to_binary(444,10))
            instruction_32_bits+="0"

    elif mnemonic == "mr":
        instruction_32_bits += (number_to_binary(31, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'or'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32):
                raise ValueError("Out of bound register")
            rs = number_to_binary(rs,5)
            ra = number_to_binary(ra,5)
            instruction_32_bits += rs
            instruction_32_bits += ra
            instruction_32_bits += rs
            instruction_32_bits += (number_to_binary(444,10))
            instruction_32_bits += "0"

    elif mnemonic== "ori":
        instruction_32_bits+=(number_to_binary(24, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'ori'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rt = int(params[1][1:])
                si = int(params[2])

            except:
                raise ValueError("Invalid register name")
            if rt not in range(0,32) or ra not in range(0,32):
                    raise ValueError("Out of bound register")   
            if si not in range(-2**(15), 2**16 -1):
                    raise ValueError("Out of bound integer")                
            rt=number_to_binary(rt,5)
            ra=number_to_binary(ra,5)
            
            if(si>=0):
              si=number_to_binary(si,16)
            else:
              si=number_to_2s_complement(si, 16)
              
            instruction_32_bits+=rt
            instruction_32_bits+=ra
            instruction_32_bits+=si

    elif mnemonic == "subf" or mnemonic == "sub":
        instruction_32_bits+=(number_to_binary(31, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'subf'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs or params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(params[1][1:])
                rb = int(params[2][1:])
            except:
                raise ValueError("Invalid register name")
            if rt not in range(0,32) or ra not in range(0,32) or rb not in range(0,32):
                raise ValueError("Out of bound register")

            rt=number_to_binary(rt,5)
            rb=number_to_binary(rb,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rt
            if mnemonic == "subf":
                instruction_32_bits+=ra
                instruction_32_bits+=rb
            else:
                instruction_32_bits+=rb
                instruction_32_bits+=ra
            instruction_32_bits+="0"
            instruction_32_bits+=number_to_binary(40,9)
            instruction_32_bits+="0"

    elif mnemonic== "xor":
        instruction_32_bits+=(number_to_binary(31, 6))
        if len(params) != 3:
          raise ValueError("Not enough parameters for 'xor'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs or params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                rb = int(params[2][1:])
            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32) or rb not in range(0,32):
                    raise ValueError("Out of bound register")   
            rs=number_to_binary(rs,5)
            rb=number_to_binary(rb,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rs
            instruction_32_bits+=ra
            instruction_32_bits+=rb
            instruction_32_bits+=(number_to_binary(316,10))
            instruction_32_bits+="0"


    elif mnemonic== "xori":
        instruction_32_bits+=(number_to_binary(26, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'xori'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                ui = int(params[2])

            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32):
                    raise ValueError("Out of bound register")   
            if ui not in range(-2**(15), 2**16 -1):
                    raise ValueError("Out of bound integer")                
            rs=number_to_binary(rs,5)
            ra=number_to_binary(ra,5)
            if(ui>=0):
              ui=number_to_binary(ui,16)
            else:
              ui=number_to_2s_complement(ui, 16)
            instruction_32_bits+=rs
            instruction_32_bits+=ra
            instruction_32_bits+=ui

    elif mnemonic== "ld":
        instruction_32_bits+=(number_to_binary(58, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'ld'")
        else:
            regs = ['r', 'R']
            D, RA = sep_bracket(params[1])
            try:
                D=int(D)
            except:
                raise ValueError("D in load statement should be an integer")

            if params[0][0] not in regs or RA[0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(RA[1:])
            except:
                raise ValueError("Invalid register name")
            if D >= 0:
                D = number_to_binary(D, 14)
            else:
                D = number_to_2s_complement(D,14)
            if rt not in range(0,32) or ra not in range(0, 32):
                raise ValueError("Out of bound register")
            rt=number_to_binary(rt,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rt+ra+D+"00"


    elif mnemonic== "lwz":
        instruction_32_bits+=(number_to_binary(32, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'lwz'")
        else:
          regs = ['r', 'R']
          D,RA=sep_bracket(params[1])
          D=int(D)

          if params[0][0] not in regs or RA[0] not in regs:
            raise ValueError("Register name should start from r or R")
          try:
            rt = int(params[0][1:])
            ra = int(RA[1:])
          except:
            raise ValueError("Invalid register name")
          if(D>=0):
            D=number_to_binary(D,16)
          else:
            D=number_to_2s_complement(D,16)
          if rt not in range(0,32) or ra not in range(0,32):
            raise ValueError("Out of bound register")   
          rt=number_to_binary(rt,5)
          ra=number_to_binary(ra,5)
          instruction_32_bits+=rt+ra+D

    elif mnemonic== "std":
        instruction_32_bits+=(number_to_binary(62, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'std'")
        else:
            regs = ['r', 'R']
            D,RA=sep_bracket(params[1])
            try:
                D=int(D)
            except:
                raise ValueError("D in load statement should be an integer")

            if params[0][0] not in regs or RA[0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(RA[1:])
            except:
                raise ValueError("Invalid register name")
            if D >= 0:
                D = number_to_binary(D,14)
            else:
                D = number_to_2s_complement(D,14)
            if rt not in range(0,32) or ra not in range(0,32):
                raise ValueError("Out of bound register")
            rt = number_to_binary(rt, 5)
            ra = number_to_binary(ra, 5)
            instruction_32_bits += rt+ra+D+"00"

    elif mnemonic == "stw":
        instruction_32_bits += (number_to_binary(36, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'stw'")
        else:
            regs = ['r', 'R']
            D, RA = sep_bracket(params[1])
            D = int(D)

            if params[0][0] not in regs or RA[0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(RA[1:])
            except:
                raise ValueError("Invalid register name")
            if D >= 0:
                D=number_to_binary(D, 16)
            else:
                D=number_to_2s_complement(D,16)
            if rt not in range(0,32) or ra not in range(0,32):
                raise ValueError("Out of bound register")
            rt=number_to_binary(rt,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rt+ra+D

    elif mnemonic == "stwu":
        instruction_32_bits += (number_to_binary(37, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'stwu'")
        else:
            regs = ['r', 'R']
            D, RA = sep_bracket(params[1])
            D = int(D)

            if params[0][0] not in regs or RA[0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(RA[1:])
            except:
                raise ValueError("Invalid register name")
            if D >= 0:
                D = number_to_binary(D, 16)
            else:
                D = number_to_2s_complement(D, 16)
            if rt not in range(0,32) or ra not in range(0, 32):
                raise ValueError("Out of bound register")
            rt = number_to_binary(rt, 5)
            ra = number_to_binary(ra, 5)
            instruction_32_bits += rt+ra+D

    elif mnemonic == "lhz":
        instruction_32_bits+=(number_to_binary(40, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'lhz'")
        else:
            regs = ['r', 'R']
            D,RA = sep_bracket(params[1])
            D = int(D)
            if params[0][0] not in regs or RA[0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(RA[1:])
            except:
                raise ValueError("Invalid register name")
            if D >= 0:
                D = number_to_binary(D, 16)
            else:
                D=number_to_2s_complement(D, 16)
            if rt not in range(0, 32) or ra not in range(0,32):
                raise ValueError("Out of bound register")
            rt = number_to_binary(rt, 5)
            ra = number_to_binary(ra, 5)
            instruction_32_bits += rt+ra+D

    elif mnemonic == "lha":
        instruction_32_bits+=(number_to_binary(42, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'lha'")
        else:
            regs = ['r', 'R']
            D,RA=sep_bracket(params[1])
            D=int(D)

            if params[0][0] not in regs or RA[0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                rt = int(params[0][1:])
                ra = int(RA[1:])
            except:
                raise ValueError("Invalid register name")
            if D>=0 :
                D=number_to_binary(D,16)
            else:
                D=number_to_2s_complement(D,16)
            if rt not in range(0,32) or ra not in range(0,32):
                raise ValueError("Out of bound register")
            rt=number_to_binary(rt,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rt+ra+D

    elif mnemonic == "sth":
        instruction_32_bits += (number_to_binary(44, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'sth'")
        else:
          regs = ['r', 'R']
          D,RA=sep_bracket(params[1])
          D=int(D)

          if params[0][0] not in regs or RA[0] not in regs:
            raise ValueError("Register name should start from r or R")
          try:
            rt = int(params[0][1:])
            ra = int(RA[1:])
          except:
            raise ValueError("Invalid register name")
          if(D>=0):
            D=number_to_binary(D,16)
          else:
            D=number_to_2s_complement(D,16)
          if rt not in range(0,32) or ra not in range(0,32):
            raise ValueError("Out of bound register")   
          rt=number_to_binary(rt,5)
          ra=number_to_binary(ra,5)
          instruction_32_bits+=rt+ra+D    

    elif mnemonic== "lbz":
        instruction_32_bits+=(number_to_binary(34, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'lbz'")
        else:
          regs = ['r', 'R']
          D,RA=sep_bracket(params[1])
          D=int(D)

          if params[0][0] not in regs or RA[0] not in regs:
            raise ValueError("Register name should start from r or R")
          try:
            rt = int(params[0][1:])
            ra = int(RA[1:])
          except:
            raise ValueError("Invalid register name")
          if(D>=0):
            D=number_to_binary(D,16)
          else:
            D=number_to_2s_complement(D,16)
          if rt not in range(0,32) or ra not in range(0,32):
            raise ValueError("Out of bound register")   
          rt=number_to_binary(rt,5)
          ra=number_to_binary(ra,5)
          instruction_32_bits+=rt+ra+D

    elif mnemonic== "stb":
        instruction_32_bits+=(number_to_binary(38, 6))
        if len(params) != 2:
            raise ValueError("Not enough parameters for 'stb'")
        else:
          regs = ['r', 'R']
          D,RA=sep_bracket(params[1])
          D=int(D)

          if params[0][0] not in regs or RA[0] not in regs:
            raise ValueError("Register name should start from r or R")
          try:
            rt = int(params[0][1:])
            ra = int(RA[1:])
          except:
            raise ValueError("Invalid register name")
          if(D>=0):
            D=number_to_binary(D,16)
          else:
            D=number_to_2s_complement(D,16)
          if rt not in range(0,32) or ra not in range(0,32):
            raise ValueError("Out of bound register")   
          rt=number_to_binary(rt,5)
          ra=number_to_binary(ra,5)
          instruction_32_bits+=rt+ra+D


    elif mnemonic== "rlwinm":
        instruction_32_bits+=(number_to_binary(21, 6))
        if len(params) != 5:
            raise ValueError("Not enough parameters for 'rlwinm'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                sh = int(params[2])
                mb = int(params[3])
                me = int(params[4])

            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32):
                    raise ValueError("Out of bound register")   
            rs=number_to_binary(rs,5)
            ra=number_to_binary(ra,5)

            instruction_32_bits+=rs
            instruction_32_bits+=ra
            instruction_32_bits+=number_to_binary(sh,5)
            instruction_32_bits+=number_to_binary(mb,5)
            instruction_32_bits+=number_to_binary(me,5)
            instruction_32_bits+="0"

    elif mnemonic== "slwi":
        instruction_32_bits+=(number_to_binary(21, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'slwi'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                sh = int(params[2])
                mb = 0
                me = 31 - sh

            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32):
                    raise ValueError("Out of bound register")
            rs=number_to_binary(rs,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rs
            instruction_32_bits+=ra
            instruction_32_bits+=number_to_binary(sh,5)
            instruction_32_bits+=number_to_binary(mb,5)
            instruction_32_bits+=number_to_binary(me,5)
            instruction_32_bits+="0"

    elif mnemonic== "sld":
        instruction_32_bits+=(number_to_binary(31, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'sld'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs or params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                rb = int(params[2][1:])
            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32) or rb not in range(0,32):
                raise ValueError("Out of bound register")
            rs=number_to_binary(rs,5)
            rb=number_to_binary(rb,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits += rs
            instruction_32_bits += ra
            instruction_32_bits += rb
            instruction_32_bits += (number_to_binary(27,10))
            instruction_32_bits += "0"

    elif mnemonic == "srd":
        instruction_32_bits+=(number_to_binary(31, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'srd'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs or params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                rb = int(params[2][1:])
            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32) or rb not in range(0,32):
                raise ValueError("Out of bound register")
            rs=number_to_binary(rs,5)
            rb=number_to_binary(rb,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rs
            instruction_32_bits+=ra
            instruction_32_bits+=rb
            instruction_32_bits+=(number_to_binary(539,10))
            instruction_32_bits+="0"   

    elif mnemonic== "srad":
        instruction_32_bits+=(number_to_binary(31, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'srad'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs or params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                rb = int(params[2][1:])
            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32) or rb not in range(0,32):
                raise ValueError("Out of bound register")
            rs=number_to_binary(rs,5)
            rb=number_to_binary(rb,5)
            ra=number_to_binary(ra,5)
            instruction_32_bits+=rs
            instruction_32_bits+=ra
            instruction_32_bits+=rb
            instruction_32_bits+=(number_to_binary(794,10))
            instruction_32_bits+="0"
  
    elif mnemonic== "sradi":
        instruction_32_bits+=(number_to_binary(31, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'srad'")
        else:
            regs = ['r', 'R']
            if params[0][0] not in regs or params[1][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[0][1:])
                rs = int(params[1][1:])
                sh = int(params[2])
            except:
                raise ValueError("Invalid register name")
            if rs not in range(0,32) or ra not in range(0,32):
              raise ValueError("Out of bound register")   
            rs=number_to_binary(rs,5)
            ra=number_to_binary(ra,5)
            sh=number_to_binary(sh,5)
            instruction_32_bits+=rs
            instruction_32_bits+=ra
            instruction_32_bits+=sh
            instruction_32_bits+=(number_to_binary(413,9))
            instruction_32_bits+="00"

    elif mnemonic == "b":
        instruction_32_bits += (number_to_binary(18, 6))
        if len(params) != 1:
            raise ValueError("Not enough parameters for 'b'")
        else:
            try:
                li = int(params[0])
            except:
                raise ValueError("Parameter to b should be an integer")
            if li not in range(0, (2 ** 24) - 1):
                raise ValueError("Out of bound value")
            instruction_32_bits += number_to_binary(li, 24)
            instruction_32_bits += "00"

    elif mnemonic == "ba":
        instruction_32_bits += (number_to_binary(18, 6))
        if len(params) != 1:
            raise ValueError("Not enough parameters for 'ba'")
        else:
            try:
                li = int(params[0])
            except:
                raise ValueError("Parameter to ba should be an integer")
            if li not in range(0, (2 ** 24) - 1):
                raise ValueError("Out of bound value")
            instruction_32_bits += number_to_binary(li, 24)
            instruction_32_bits += "10"

    elif mnemonic == "bl":
        instruction_32_bits += (number_to_binary(18, 6))
        if len(params) != 1:
            raise ValueError("Not enough parameters for 'bl'")
        else:
            try:
                li = int(params[0])
            except:
              raise ValueError("Parameter to bl should be an integer")
            if li not in range(0,(2**24)-1):
              raise ValueError("Out of bound value")
            instruction_32_bits+=number_to_binary(li, 24)
            instruction_32_bits+="01"

    elif mnemonic == "j":
        instruction_32_bits += (number_to_binary(20, 6))
        if len(params) != 1:
            raise ValueError("Not enough parameters for 'bl'")
        else:
            try:
                li = text_table[params[0]]
                li = int(li/32)
            except:
              raise KeyError("Such a label doesn't exist")
            instruction_32_bits+=number_to_binary(li, 24)
            instruction_32_bits+="11"

    elif mnemonic == "bclr":
        instruction_32_bits+=(number_to_binary(19, 6))
        if not (params == [] or params == ['LR']):
            raise ValueError("Not enough parameters for 'bclr'")
        else:
            instruction_32_bits+="1"*13 + "00" +  number_to_binary(16,10) + "0"

    elif mnemonic == "bc":
        instruction_32_bits += (number_to_binary(19, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'bc'")
        else:
            try:
                bi = int(params[1])
                bd = int(params[2])
            except:
                raise ValueError("Parameter to bc should be an integer")
            if params[2] not in text_table:
                raise ValueError("Label not found")
            if (bi not in range(0, 32)) or (bd not in range(-(2**13), (2**13)-1)):
                raise ValueError("Out of bound value")
            instruction_32_bits += "11111"
            instruction_32_bits += number_to_binary(bi, 5)
            instruction_32_bits += number_to_2s_complement(bd, 14)
            instruction_32_bits += "00"

    elif mnemonic == "bca":
        instruction_32_bits += (number_to_binary(19, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'bca'")
        else:
            try:
                bi = int(params[1])
            except:
                raise ValueError("Parameter to bca should be an integer")
            try:
                li = text_table[params[2]]
                li = int(li / 32)
            except:
                raise KeyError("Such a label doesn't exist")
            if bi not in range(0, 32):
                raise ValueError("Out of bound value")
            instruction_32_bits += "11111"
            instruction_32_bits += number_to_binary(bi, 5)
            instruction_32_bits += number_to_binary(li, 14)
            instruction_32_bits += "10"

    elif mnemonic == "bne":
        instruction_32_bits += (number_to_binary(19, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'bne'")
        else:
            try:
                ra = int(params[0][1:])
                rb = int(params[1][1:])
            except:
                raise ValueError("Parameter to bne should be an integer")
            if params[2] not in text_table:
                raise ValueError("Label not found")
            if ra not in range(0, 32) or rb not in range(0, 32):
                raise ValueError("Out of bound value")
            instruction_32_bits += number_to_binary(ra, 5)
            instruction_32_bits += number_to_binary(rb, 5)
            instruction_32_bits += number_to_binary(text_table[params[2]], 14)
            instruction_32_bits += "01"

    elif mnemonic == "beq":
        instruction_32_bits += (number_to_binary(19, 6))
        if len(params) != 3:
            raise ValueError("Not enough parameters for 'beq'")
        else:
            try:
                ra = int(params[0][1:])
                rb = int(params[1][1:])
            except:
                raise ValueError("Parameter to beq should be an integer")
            if params[2] not in text_table:
                raise ValueError("Label not found")
            if ra not in range(0, 32) or rb not in range(0, 32):
                raise ValueError("Out of bound value")
            instruction_32_bits += number_to_binary(ra, 5)
            instruction_32_bits += number_to_binary(rb, 5)
            instruction_32_bits += number_to_binary(int(text_table[params[2]]/32), 14)
            instruction_32_bits += "11"

    elif mnemonic == "cmp" or mnemonic == "cmpd":
        instruction_32_bits += (number_to_binary(31, 6))
        if len(params) != 4:
            raise ValueError("Not enough parameters for 'cmp'")
        else:
            regs = ['r', 'R']
            if params[0] != "7":
                raise ValueError("Wrong value for parameter 1 (should be 7)")
            elif params[1] != "1":
                raise ValueError("Wrong value for parameter 2 (should be 1)")
            elif params[2][0] not in regs or params[3][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[2][1:])
                rb = int(params[3][1:])
            except:
                raise ValueError("Invalid register name")
            if ra not in range(0, 32) or rb not in range(0, 32):
                raise ValueError("Out of bound register")

            rb = number_to_binary(rb, 5)
            ra = number_to_binary(ra, 5)
            instruction_32_bits += "00000"
            instruction_32_bits += ra
            instruction_32_bits += rb
            instruction_32_bits += "0"*10
            instruction_32_bits += "1"

    elif mnemonic == "cmpi" or mnemonic == "cmpdi":
        instruction_32_bits += (number_to_binary(11, 6))
        if len(params) != 4:
            raise ValueError("Not enough parameters for 'cmpi'")
        else:
            regs = ['r', 'R']
            if params[0] != "7":
                raise ValueError("Wrong value for parameter 1 (should be 7)")
            elif params[1] != "1":
                raise ValueError("Wrong value for parameter 2 (should be 1)")
            elif params[2][0] not in regs:
                raise ValueError("Register name should start from r or R")
            try:
                ra = int(params[2][1:])
                si = int(params[3])
            except:
                raise ValueError("Invalid register name")
            if ra not in range(0, 32):
                raise ValueError("Out of bound register")

            ra = number_to_binary(ra, 5)
            instruction_32_bits += "00000"
            instruction_32_bits += ra
            if si >= 0:
                si = number_to_binary(si, 16)
            else:
                si = number_to_2s_complement(si, 16)
            instruction_32_bits += si

    elif mnemonic == "syscall":
        instruction_32_bits += (number_to_binary(17, 6))
        if len(params) != 0:
            raise ValueError("Not enough parameters for 'syscall'")
        else:
            instruction_32_bits += "0"*26

    else:
        raise KeyError(mnemonic + " -> Such a mnemonic doesn't exist")
    return instruction_32_bits
