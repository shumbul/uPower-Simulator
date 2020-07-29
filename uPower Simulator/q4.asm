######################################################
#                                                    #
#    Program: To input an integer and display it     #
#                                                    #
######################################################

.data
prompt: .asciiz "Enter any integer : "
message: .asciiz "Input value : "
num: .word 300

.text
main:

la R3,prompt
li R0,4
syscall

la R4,num
li R0,5
syscall

stw R3,0(R4)

li R0,4
la R3,message
syscall

la R5,num
lwz R5,0(R5)
mr R3,R5

li R0,1
syscall

li R0,10
syscall