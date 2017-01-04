# Bhabha
A 16-bit assembly simulator that allows you to view the internal machine state as the code is being executed. Bhabha is highly configurable, and allows you to choose from wide a array of options. Bhabha can also parse your code to detect multiple types of errors and warnings before you run your code, and while it is being executed.

![Screenshot of Bhabha](http://i.imgur.com/2o8PRVe.png)

## What does Bhabha do?
Bhabha allows users to emulate a computer of desired configuration, and then run the desired assembly code on it. Moreover, Bhabha will display the internal state of the computer as the code is being executed.

Bhabha is an excellent way of learning about Assembly programming, as it allows users to understand how computers operate at the fundamental level.

## Running Bhabha


### Installing Dependencies
To install and run Bhabha, the required dependencies need to be installed. Please follow the provided links to install required dependencies.

| Dependency Name | Reason           | Required Link |
| ------------- |:-------------:|:-------------:|
| `Python 2.7`    | Running Bhabha   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `Tabulate`      | Graphics Display |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |

### Interpreting Assembly Code
The following syntax can be used to interpret `file_name.asm`:
```sh
python parser.py file_name.asm
```
If you would like to see the configuration of the emulated machine, you can do the following to display the default settings of the emulated machine:
```sh
python parser.py file_name.asm -defaultProcessor
```
You can also change the various properties of the emulated machine as follows:
```sh
# this will cause Bhabha to interpret the file 'file_name.asm', change the RAM size to 512 memory cells,
# set the number of registers to 20, and modify the text-console size to 10 characters
python parser.py file_name.asm -ramSize=512 -stackCount=15 -registerCount=20 -consoleSize=10

# By default, each memory cell that Bhabha emulates is 16-bit unsigned, but you can
# change that to make Bhabha operate in 8-bit mode as follows:
python parser.py file_name.asm -16BitMode=False

# You can choose to change the speed at which code execution occurs by setting the 'executionSpeed' flag
# to a desired value (NOTE: a value of 0 indicates that you want to execute code on keypress)
python parser.py file_name.asm -executionSpeed=5
```
Please refer to the `help` flag to learn about more flags that you can.

### Seeking Help
Use the `help` flag as follows to receive a detailed explanation of all available options and more information.

```sh
python parser.py -help
```

### Sample Code
You can download the code to run Bhabha with from the folder `Sample Code` which is a part of this repository.

## Assembly Code Dialect
The instruction set that Bhabha uses has been derived from University of Waterloo's ECE 150 course, and closely resembles the general RISC dialect. Any file you wish Bhabha to interpret should have a `.asm` extension. Please refer to the following legend to understand the instruction list.

### Legend

| Syntax | Meaning           | Examples |
| ------------- |:-------------:|:-------------:|
| `Ri`, `Rj`, `Rk`...    | Register   | `R1`, `R7`, `R3`...  |
| `<nnnn>`, `<mmmm>`...      | Memory Address | `0x0`, `10`, `0x2D0`, `0b010110` |
| `nnnn`, `mmmm`...      | Unsigned Integer | `0x9F`, `120`, `0xA1`, `0b1101` |

All the instructions that Bhabha uses can be classified into the following categories:

### Load/Store Instructions

| Instruction | Syntax           | Description |
| ------------- |:-------------:|:-------------:|
| `LD`    | `LD <nnnn>, Ri` or `LD Rj, Ri`   | `Causes register Ri to store the data stored in memory location <nnnn>` or `Causes register Ri to store the data stored in memory location contained in Rj`  |
| `LDi`      | `LDi nnnn, Ri` | `Causes integer nnnn to be stored in register Ri` |
| `SD`    | `SD Ri, <nnnn>` or `SD Ri, Rj`   | `Causes data in Ri to be stored to memory location <nnnn>` or `Causes data in Ri to be stored to memory location contained in register Rj`|
| `SDi`      | `SDi mmmm, <nnnn>` or `SDi mmmm, Ri` |  `Causes integer mmmm to be stored in memory location <nnnn>` or `Causes integer mmmm to be stored in memory location contained in register Ri` |

### Arithmetic Instructions

| Instruction | Syntax           | Description |
| ------------- |:-------------:|:-------------:|
| `ADD`    | `ADD Ri, Rj, Rk` or `ADD Ri, nnnn, Rk`   |  `Adds Ri and Rj, and stores the sum to register Rk` or `Adds Ri and integer nnnn and stores the result in register Rk` |
| `SUB`      | `SUB Ri, Rj, Rk` or `SUB Ri, nnnn, Rk` |  `Subtracts Rj from Ri, and stores the result to register Rk` or `Subtracts integer nnnn from Ri and stores the result in register Rk` |
| `MUL`    | `MUL Ri, Rj, Rk` or `MUL Ri, nnnn, Rk`   |  `Multiplies Ri and Rj, and stores the product to register Rk` or `Adds Ri and integer nnnn and stores the product to register Rk` |
| `DIV`      | `DIV Ri, Rj, Rk` or `DIV Ri, nnnn, Rk` |  `Divides Ri by Rj, and stores the result to register Rk` or `Divides Ri by integer nnnn and stores the result in register Rk` |

### Flow Control Instructions

| Instruction | Syntax           | Description |
| ------------- |:-------------:|:-------------:|
| `JMP`    | `JMP <label-name>`   |  `Causes program control to jump to label <label-name>` |
| `JZ`      | `JZ Ri, <label-name>` |  `Causes program control to jump to label <label-name> if Ri is zero` |
| `JNZ`    | `JNZ Ri, <label-name>`   |  `Causes program control to jump to label <label-name> if Ri is zero` |
| Label Name      | `<label-name>:` |  `Defines a new label with name <label-name>` |

### Comparison Instructions

| Instruction | Syntax           | Description |
| ------------- |:-------------:|:-------------:|
| `MORE`      | `MORE Ri, Rj, Rk` or `Ri, nnnn, Rk` | `Causes Rk to become 1 if Ri > Rj, 0 otherwise` or `Causes Rk to become 1 if R1 > nnnn, 0 otherwise` |
| `LESS`    | `LESS Ri, Rj, Rk` or `LESS Ri, nnnn, Rk`  |  `Causes Rk to become 1 if Ri < Rj, 0 otherwise` or `Causes Rk to become 1 if R1 < nnnn, 0 otherwise` |
| `SAME`      | `SAME Ri, Rj, Rk` or `SAME Ri, nnnn, Rk` |  `Causes Rk to become 1 if Ri and Rj are equal, 0 otherwise` or `Causes Rk to become 1 if R1 and integer nnnn are equal, 0 otherwise` |

### Logical Operation Instructions

| Instruction | Syntax           | Description |
| ------------- |:-------------:|:-------------:|
| `AND`    | `AND Ri, Rj, Rk` or `AND Ri, nnnn, Rk`   | `Calculates the bitwise AND of Ri and Rj, and stores the result in Rk` or `Calculates the bitwise AND of Ri and nnnn, and stores the result in Rk` ) |
| `OR`      | `OR Ri, Rj, Rk` or `OR Ri, nnnn, Rk` |  `Calculates the bitwise OR of Ri and Rj, and stores the result in Rk` or `Calculates the bitwise OR of Ri and nnnn, and stores the result in Rk` |
| `XOR`    | `XOR Ri, Rj, Rk` or `XOR Ri, nnnn, Rk`   |  `Calculates the bitwise XOR of Ri and Rj, and stores the result in Rk` or `Calculates the bitwise XOR of Ri and nnnn, and stores the result in Rk` |
| `NOT`      | `NOT Ri, Rj` or `NOT nnnn, Ri` |  `Calculates the bitwise NOT of Ri and stores the result in Rj` or `Calculates the bitwise NOT of nnnn and stores the result in Rj` |

### Stack Instructions

| Instruction | Syntax           | Description |
| ------------- |:-------------:|:-------------:|
| `PUSH`    | `PUSH Ri` or `PUSH nnnn`   |  `Pushes value stored in Ri onto the stack` or `Pushes integer nnnn onto the stack` |
| `POP`      | `POP Ri` or `POP <nnnn>` |  `Pops off an element from the stack, and stores it in Ri` or `Pops off an element from the stack, and stores it in memory location <nnnn>`  |

### Code Comments
You can also comment your code as follows:
```sh
#this is a comment, and this code will print 'Hello!' on the console when Bhabha is operating under default configuration
SDi 0x48, 248
SDi 0x65, 249
SDi 0x6C, 250
    #Not only can you place comments anywhere, you can also indent your code/comments as you wish to
  SDi 0x6C, 251
SDi 0x6F, 252
    SDi 0x21, 253
#every line in this file is syntactically valid
```
