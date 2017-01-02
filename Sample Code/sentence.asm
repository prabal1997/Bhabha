#this program repetedly prints and erases 'Hello!' on the text console under default configuration

#we store the number of iterations in register 'R1'
LDi 5, R1

#we repeat the following code
     #we set a label here
     jumpHere:

     #printing 'Hello!'
     SDi 0x48, 248
     SDi 0x65, 249
     SDi 0x6C, 250
     SDi 0x6C, 251
     SDi 0x6F, 252
     SDi 0x21, 253
     
     #erasing 'Hello!'
     SDi 0, 253
     SDi 0, 252
     SDi 0, 251
     SDi 0, 250
     SDi 0, 249
     SDi 0, 248
     
     #decrementing value of register 'R1'
     SUB R1, 1, R1

     #we jump back to the beginning of the loop
     JNZ R1, jumpHere 

#we indicate the end of program by printing 'END'
SDi 0x45, 248
SDi 0x4E, 249
SDi 0x44, 250