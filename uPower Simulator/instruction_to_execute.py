def number_to_binary(number,n):
  num=str(bin(number))
  num = num.split('b')[-1]
  if len(num)<n:
    k=n-len(num)
    while(k>0):
      num="0"+num
      k=k-1
  return num


def sep_bracket(param):
  # param of the D(RA)
  D=param.split('(')[0].rstrip(' ').rstrip('\t').rstrip(' ')
  param=param.split('(')[1].lstrip(' ').lstrip('\t').lstrip(' ')
  RA= param.split(')')[0].lstrip(' ').lstrip('\t').lstrip(' ')
  #returns 2 strings such that we need to find the Reg[RA]+D
  return D,RA


def number_to_2Scomplement(num, n):
    if  n<=0 :
      raise ValueError("Number of bits should be greater than 0")
    if num in range (-2**(n-1),2**(n-1)):
      if num>0:
        return "0" + number_to_binary(num,n-1)
      elif num==0:
        return "0"*n
      else :
        k=2**(n-1) + num
        return "1" + number_to_binary(k,n-1)
    else :
      raise ValueError("Number out of bound")

def bin_to_dec(binstr):
    bin=int(binstr)
    decimal, i, n = 0, 0, 0
    while(bin != 0):
      dec = bin % 10
      decimal = decimal + dec * pow(2, i)
      bin = bin//10
      i += 1
    return decimal


def exts(number, N=64, unsign = False):
    n = len(number)
    e = '1'
    if(unsign):
        e = '0'
    while n<N:
        number = e + number
    return number


def twos_complement_to_decimal(number):
    length = len(number) - 1
    return int(number[1:], 2) - int(number[0])*(2**length)


def decimal_to_twoscomplement(number, n = 64):
  num = (2**(n+1))-1
  b = (number ^ num) + 1
  return str(bin(b)).split('b')[-1]


def rotl64(x, n):
    return (x << n) | (x >> (64-n))


def rotl32(x, n):
    return (x << n) | (x >> (32-n))


def mask(m,n):
    if m > n:
        return 64*'1'
    return '0'*m + (n-m+1)*'1' + (63-n)*'0'


def execute_instruction(instruction, regs, memory_file, symbol_table):
    data_size = {0: 1, 1: 2, 2: 4, 3: 8, 4: 1}
    data_table = symbol_table['data']
    text_table = symbol_table['text']
    opcode = int(instruction[0:6], 2)

    # add -XO
    if opcode == 31 and int(instruction[21:22], 2) == 0 and int(instruction[31:32], 2) == 0 and int(instruction[22:31],
                                                                                                    2) == 266:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        rb = 'R' + str(int(instruction[16:21], 2))
        regs[rt] = regs[ra] + regs[rb]

    # addi -D
    elif opcode == 14:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        si = int(instruction[17:32], 2) - int(instruction[16]) * (2 ** 15)
        if ra == 'R0':
            regs[rt] = si
        else:
            regs[rt] = regs[ra] + si

    #  -D
    elif opcode == 14:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        si = int(instruction[17:32], 2) - int(instruction[16]) * (2 ** 15)
        regs[rt] = regs[ra] + si

    # addis -D
    elif opcode == 15:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        si = int(instruction[17:32], 2) - int(instruction[16]) * (2 ** 15)
        if ra == 'R0':
            regs[rt] = si * (2 ** 16)
        else:
            regs[rt] = regs[ra] + si

    # and -X
    elif opcode == 31 and int(instruction[21:31], 2) == 28:
        rs = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        rb = 'R' + str(int(instruction[16:21], 2))
        regs[ra] = regs[rs] & regs[rb]

    # andi -D
    elif opcode == 28:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        si = int(instruction[16:32], 2)
        regs[rt] = regs[ra] & si

    #extsw -X
    elif opcode == 31 and int(instruction[21:31], 2) == 986:
      rs = 'R' + str(int(instruction[6:11], 2))
      ra = 'R' + str(int(instruction[11:16], 2))
      c = number_to_2Scomplement(regs[rs], 64)
      c = (c[32]*32) + c[32:64]
      regs[ra] = twos_complement_to_decimal(c)

    # Nand -X
    elif opcode == 31 and int(instruction[21:31], 2) == 476:
        rs = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        rb = 'R' + str(int(instruction[16:21], 2))
        regs[ra] = ~ (regs[rs] & regs[rb])

    # OR -X
    elif opcode == 31 and int(instruction[21:31], 2) == 444 and int(instruction[31:32], 2) == 0:
        rs = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        rb = 'R' + str(int(instruction[16:21], 2))
        regs[ra] = regs[rs] | regs[rb]

    # ORi -D
    elif opcode == 24:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        si = int(instruction[16:32], 2)
        regs[rt] = regs[ra] | si

    # ld - DS
    elif opcode == 58 and int(instruction[30:32], 2) == 0:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        ds = int(instruction[16:30] + "00", 2)
        if ra == 'R0':
            b = 0
        else:
            b = regs[ra]
        ea = b + ds
        memory_file.seek(ea, 0)
        regs[rt] = twos_complement_to_decimal(memory_file.read(64).decode('ascii'))

    # lwz - D
    elif opcode == 32:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        ds = int(instruction[16:32], 2)
        if ra == 'R0':
            b = 0
        else:
            b = regs[ra]
        ea = b + ds
        memory_file.seek(ea, 0)
        regs[rt] = twos_complement_to_decimal(memory_file.read(32).decode('ascii'))

    # std - DS
    elif opcode == 62 and int(instruction[30:32], 2) == 0:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        ds = int(instruction[16:30] + "00", 2)
        if ra == 'R0':
            b = 0
        else:
            b = regs[ra]
        ea = b + ds
        memory_file.seek(ea, 0)
        memory_file.write(bytearray(number_to_2Scomplement(regs[rt], 64), encoding="ascii"))

    # stw - D
    elif opcode == 36:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        ds = int(instruction[16:32], 2)
        if ra == 'R0':
            b = 0
        else:
            b = regs[ra]
        ea = b + ds
        rt = twos_complement_to_decimal(number_to_2Scomplement(regs[rt], 64)[32:64])
        memory_file.seek(ea, 0)
        memory_file.write(bytearray(number_to_2Scomplement(rt, 32), encoding="ascii"))

    #stwu - D
    elif opcode == 37:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        ds = int(instruction[16:32], 2)
        if ra == 'R0':
            print("Invalid instruction form")
            return regs
        else:
            ea = regs[ra] + ds
            rt = twos_complement_to_decimal(number_to_2Scomplement(regs[rt], 64)[32:64])
            memory_file.seek(ea, 0)
            memory_file.write(bytearray(number_to_2Scomplement(rt, 32), encoding="ascii"))
            regs[rt] = ea

    #lhz - D
    elif opcode == 40:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        ds = int(instruction[16:32], 2)
        if ra == 'R0':
            b = 0
        else:
            b = regs[ra]
        ea = b + ds
        memory_file.seek(ea, 0)
        regs[rt] = twos_complement_to_decimal(memory_file.read(16).decode('ascii'))

    #lha - D
    elif opcode == 42:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        ds = int(instruction[16:32], 2)
        if ra == 'R0':
            b = 0
        else:
            b = regs[ra]
        ea = b + ds
        memory_file.seek(ea, 0)
        ea = memory_file.read(16).decode('ascii')
        ea = ea[0]*48 + ea
        regs[rt] = twos_complement_to_decimal(ea)

    # sth - D
    elif opcode == 44:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        ds = int(instruction[16:32], 2)
        if ra == 'R0':
            b = 0
        else:
            b = regs[ra]
        ea = b + ds
        rt = twos_complement_to_decimal(number_to_2Scomplement(regs[rt], 64)[48:64])
        memory_file.seek(ea, 0)
        memory_file.write(bytearray(number_to_2Scomplement(rt, 16), encoding="ascii"))

    #lbz - D
    elif opcode == 34:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        ds = int(instruction[16:32], 2)
        if ra == 'R0':
            b = 0
        else:
            b = regs[ra]
        ea = b + ds
        memory_file.seek(ea, 0)
        regs[rt] = twos_complement_to_decimal(memory_file.read(8).decode('ascii'))

    # stb - D
    elif opcode == 38:
        rt = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        ds = int(instruction[16:32], 2)
        if ra == 'R0':
            b = 0
        else:
            b = regs[ra]
        ea = b + ds
        rt = twos_complement_to_decimal(number_to_2Scomplement(regs[rt], 64)[56:64])
        memory_file.seek(ea, 0)
        memory_file.write(bytearray(number_to_2Scomplement(rt, 8), encoding="ascii"))

    # rlwinm - M
    elif opcode == 21 and int(instruction[31:32], 2) == 0:
        rs = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        sh = int(instruction[16:21], 2)
        mb = int(instruction[21:26], 2)
        me = int(instruction[26:31], 2)
        rs = twos_complement_to_decimal(number_to_2Scomplement(regs[rs], 64)[32:64])
        n = sh
        r = rotl32(rs, n)
        m = mask(mb+32, me+32)
        regs[ra] = r & m

    # sld -X
    elif opcode == 31 and int(instruction[21:31], 2) == 27 and int(instruction[31:32], 2) == 0:
        rs = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        rb = 'R' + str(int(instruction[16:21], 2))
        rb = number_to_2Scomplement(regs[rb], 64)
        n = int(rb[58:64], 2)
        r = rotl64(regs[rs], n)
        if rb[57] == '0':
            m = mask(0, 63-n)
        else:
            m = '0'*64
        regs[ra] = r & m


    # srd -X
    elif opcode == 31 and int(instruction[21:31], 2) == 539 and int(instruction[31:32], 2) == 0:
        rs = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        rb = 'R' + str(int(instruction[16:21], 2))
        rb = number_to_2Scomplement(regs[rb], 64)
        n = int(rb[58:64], 2)
        r = rotl64(regs[rs], 64-n)
        if rb[57] == '0':
            m = mask(n, 63)
        else:
            m = '0'*64
        regs[ra] = r & m

    # srad -X
    elif opcode == 31 and int(instruction[21:31], 2) == 794 and int(instruction[31:32], 2) == 0:
        rs = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        rb = 'R' + str(int(instruction[16:21], 2))
        rb = number_to_2Scomplement(regs[rb], 64)
        n = int(rb[58:64], 2)
        r = rotl64(regs[rs], 64-n)
        if rb[57] == '0':
            m = mask(n, 63)
        else:
            m = '0'*64
        if regs[rs] >= 0:
            s = 0   # '0'*64
        else:
            s = -1       # '1'*64
        regs[ra] = (r & m) | (s & ~m)

    # sradi -X
    elif opcode == 31 and int(instruction[21:30], 2) == 413 and int(instruction[31:32], 2) == 0:
        rs = 'R' + str(int(instruction[6:11], 2))
        ra = 'R' + str(int(instruction[11:16], 2))
        sh = instruction[30] + instruction[16:21]
        n = int(sh, 2)
        r = rotl64(regs[rs], 64-n)
        m = mask(n, 63)
        if regs[rs] >= 0:
            s = 0   # '0'*64
        else:
            s = -1       # '1'*64
        regs[ra] = (r & m) | (s & ~m)

    # b -I
    elif opcode == 18 and int(instruction[30:32], 2) == 0:
        li = int(instruction[6:30], 2)
        regs['NIA'] = li*4 + regs['CIA']

    # ba -I
    elif opcode == 18 and int(instruction[30:32], 2) == 2:
        li = int(instruction[6:30], 2)
        regs['NIA'] = li*4

    # bl -I
    elif opcode == 18 and int(instruction[30:32], 2) == 1:
        li = int(instruction[6:30], 2)
        regs['NIA'] = li*4 + regs['CIA']
        regs['LR'] = regs['CIA'] + 32

    # j -I
    elif opcode == 20:
        li = int(instruction[6:30], 2)
        regs['NIA'] = li

    # bclr -XL
    elif opcode == 19 and int(instruction[21:31], 2) == 16 and int(instruction[31:32], 2) == 0 and int(instruction[19:21], 2) == 0:
        regs['NIA'] = regs['LR']

    # bc -B
    elif opcode == 19 and int(instruction[6:11], 2) == 31 and int(instruction[30:32], 2) == 0:
        bi = int(instruction[11:16], 2)
        bd = int(instruction[16:30], 2)
        if bi == 28 and regs['CR'] == 8:
            regs['NIA'] = bd + regs['CIA']
        elif bi == 29 and regs['CR'] == 4:
            regs['NIA'] = bd + regs['CIA']
        elif bi == 30 and regs['CR'] == 2:
            regs['NIA'] = bd + regs['CIA']

    # bca -B
    elif opcode == 19 and int(instruction[6:11], 2) == 31 and int(instruction[30:32], 2) == 2:
        bi = int(instruction[11:16], 2)
        bd = int(instruction[16:30], 2)
        if bi == 28 and regs['CR'] == 8:
            regs['NIA'] = bd
        elif bi == 29 and regs['CR'] == 4:
            regs['NIA'] = bd
        elif bi == 30 and regs['CR'] == 2:
            regs['NIA'] = bd

    # bne -B
    elif opcode == 19 and int(instruction[30:32], 2) == 1:
        ra = 'R' + str(int(instruction[6:11], 2))
        rb = 'R' + str(int(instruction[11:16], 2))
        bd = int(instruction[16:30], 2)
        if regs[ra] != regs[rb]:
            regs['NIA'] = bd

    # beq -B
    elif opcode == 19 and int(instruction[30:32], 2) == 3:
        ra = 'R' + str(int(instruction[6:11], 2))
        rb = 'R' + str(int(instruction[11:16], 2))
        bd = int(instruction[16:30], 2)
        if regs[ra] == regs[rb]:
            regs['NIA'] = bd

    # cmp -X
    elif opcode == 31 and int(instruction[21:32], 2) == 1 and int(instruction[6:11], 2) == 0:
        ra = 'R' + str(int(instruction[11:16], 2))
        rb = 'R' + str(int(instruction[16:21], 2))
        if regs[ra] < regs[rb]:
            regs['CR'] = 8
        elif regs[ra] > regs[rb]:
            regs['CR'] = 4
        else:
            regs['CR'] = 2

    # cmpi -D
    elif opcode == 11:
        ra = 'R' + str(int(instruction[11:16], 2))
        si = twos_complement_to_decimal(instruction[16:32])
        if regs[ra] < si:
            regs['CR'] = 8
        elif regs[ra] > si:
            regs['CR'] = 4
        else:
            regs['CR'] = 2

    # system call
    elif opcode == 17:  # System call
        syscall = regs['R0']
        if syscall == 1:  # Print word(integer)
            value = regs['R3']
            if value >=0:
                value = value % 2**32
            print(value, end='')
        elif syscall == 5:  # Read word(integer)
            value = int(input())
            value = value % (2 ** 32)
            regs['R3'] = value
        elif syscall == 11:  # Print a character
            value = regs['R3'] % (2 ** 8)
            print(chr(value), end='')
        elif syscall == 12:  # Read a character
            value = input()
            value = value[0:1]
            regs['R3'] = ord(value)
        elif syscall == 4:  # Print a string
            mem = regs['R3']
            memory_file.seek(mem, 0)
            flag = True
            while flag:
                byte = memory_file.read(8)
                character = chr(int(byte.decode('ascii'), 2))
                if character != '\0':
                    print(character, end="")
                else:
                    flag = False
        elif syscall == 8:  # Read a string
            mem = regs['R3']
            num = regs['R4']
            memory_file.seek(mem, 0)
            value = input()
            value = value.rstrip()
            value += '\0'
            if len(value) > num+1:
                value = value[0:num+2]
            for val in value:
                val = number_to_binary(ord(val), 8)
                value_bin = bytearray(val, encoding="ascii")
                memory_file.write(value_bin)
        elif syscall == 10:
            return regs, False
        else:
            print('Invalid argument for system call : ' + str(syscall))


    # When all cases fail
    else:
        raise ValueError("Instruction not decodable")
    return regs, True