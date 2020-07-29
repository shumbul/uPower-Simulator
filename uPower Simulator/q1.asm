#############################################
#                                           #
#    Program: To print "Hello World"        #
#                                           #
#############################################

.data
str: .asciiz "Hello World!"

.text
main:
    # Load string into R1
    la R3, str

    li R0,4
    syscall

    li R0,10
    syscall

