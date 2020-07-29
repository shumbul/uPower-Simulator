#############################################
#                                           #
#    Program: To add two variables          #
#                                           #
#############################################

.data
str1: .asciiz "Enter first number : "
str2: .asciiz "Enter second number : "
number1: .word 0   # number1 = 0 (dummy initial value)
number2: .word 0   # number2 = 0 (dummy initial value)
add_sign: .asciiz ' + '
equal_sign: .asciiz ' = '

.text

main:
#Input first number
la R3, str1
li R0, 4
syscall
li R0, 5
syscall
addi R4,R3,0

#Input second number
li R0,4
la R3,str2
syscall
li R0, 5
syscall
addi R5,R3,0

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