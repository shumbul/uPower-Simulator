######################################################
#                                                    #
#    Program: To find Maximum of an integer array    #
#                                                    #
######################################################

.data
array: .word 484,-10,2,-7,-3,123,44,-44,50,555   # ten integer elements in an array
message: .asciiz "Max: "

.text
main:
li R4,1               # initialize i=1
li R5,9           # initialize n=9
la R6,array              # load address of array
lwz R11,0(R6)
addi R6,R6,32

loop:
beq R4,R5,done
lwz R8,0(R6)
addi R4,R4,1
addi R6,R6,32
cmp 7,1,r8,r11
bca 0,29,change
j loop

change:
mr r11,r8
j loop

done:
li R0,4
la R3,message
syscall
mr R3,R11
li r0, 1
syscall
li r0, 10
syscall