#this program will multiply two numbers using iteration under default configuration

#we intialize the registers using the numbers we want to multiply
LDi 4, R1 #Number One
LDi 56, R2 #Number Two

#we add number two enough times to get the product
     #this is the beginning of our loop
     multiplyJump:
     
          #we store the sum in register 'R3'
          ADD R2, R3, R3
          
          #we decrement the counter
          SUB R1, 1, R1
          
     #we jump back if the multiplication isn't complete
     JNZ R1, multiplyJump

#we determine the number of digits in the output
MORE R3, 99, R4
MORE R3, 9,  R5

JZ R5, singleDigit
JNZ R4, tripleDigit

#we print a two digit number to the console
     #we separate the digits from the LSB to MSB
          #we calculate the first digit
          ADD R3, 0, R8
          
          DIV R8, 10, R2
          MUL R2, 10, R2
          SUB R8, R2, R8
          
          #we store the second digit in the proper register
          DIV R2, 10, R2
          ADD R2, 0, R7
JMP donePrinting

#we print the only digit that the number has to the console
singleDigit:
     ADD R3, 0, R8
JMP donePrinting

#we print a three digit number the console
tripleDigit:
     #we separate the digits from the LSB to MSB
          #we calculate the first digit
          ADD R3, 0, R8
          
          DIV R8, 10, R2
          MUL R2, 10, R2
          SUB R8, R2, R8
          
          #we now calculate the second digit
          ADD R2, 0, R7
          
          DIV R7, 100, R2
          MUL R2, 100, R2
          SUB R7, R2, R7
          DIV R7, 10, R7
          
          #we now calculate the third digit
          ADD R3, 0, R6
          
          MUL R7, 10, R1
          MUL R8, 1, R2
          ADD R1, R2, R2
          SUB R6, R2, R6
          DIV R6, 100, R6

#we now print the values of the register to the console 
donePrinting: 
     #we convert all digits to their ASCII value 
     ADD R6, 48, R6 
     ADD R7, 48, R7 
     ADD R8, 48, R8 
     
     SD R6, 248 
     SD R7, 249 
     SD R8, 250 
