#############################################
#                                           #
#    Program: To add two constants          #
#                                           #
#############################################

.data
number1: .word 2346   # number1 = 2346
number2: .word 36345   # number2 = 36345
add_sign: .asciiz ' + '
equal_sign: .asciiz ' = '

.text

main:
la R6,number1
la R7,number2
lwz R4,0(R6)   # R4 = number1
lwz R5,0(R7)   # R5 = number2

add R8,R4,R5   # R8 = R4 + R5

# To display the result
li R0,1
mr R3,R4
syscall

li R0,4
la R3,add_sign
syscall

li R0,1
mr R3,R5
syscall

li R0,4
la R3,equal_sign
syscall

li R0,1
mr R3,R8
syscall

# To exit the program
li R0,10
syscall