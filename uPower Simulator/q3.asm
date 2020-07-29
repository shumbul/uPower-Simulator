#############################################
#                                           #
#    Program: To add 10 two digit numbers   #
#                                           #
#############################################

.data

array: .word 10,20,30,40,50,60,70,80,90,-95
# array =[10, 20, 30, 40, 50, 60, 70, 80, 90, -95]
message: .asciiz "Result: "

.text

# R2=counter
# R3=sum
# const R4=10 [to compare the counter]
# R5 = address of array elements


main:
li R4,0               # initialize i=0
li R5,0            # initialize sum=0
li R6,10           # initialize R4=10
la R7,array              # load address of array

# Iterative loop
loop:
beq R4,R6,end     # if(counter==10) exit else continue
lwz R8,0(R7)         # R6=R5[counter]
add R5,R5,R8        # sum+=t4
addi R4,R4,1         # counter++
addi R7,R7,32         # R5+=4    (R5+4) point to next element
j loop

end:
li R0,4
la R3,message
syscall

li R0,1
mr R3,R5
syscall

li R0,10
syscall