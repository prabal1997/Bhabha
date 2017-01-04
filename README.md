# Bhabha
A 16-bit assembly simulator that allows you to view the internal machine state as the code is being executed.
--insert a photo--
## What does Bhabha do?
Bhabha allows users to emulate a computer of desired configuration, and then run the desired assembly code on it. Morover, Bhabha will display the internal state of the computer as the code is being executed.

Bhabha is an excellent way of learning about Assembly programming, as it allows users to understand how computers operate at the fundamental level.

## Running Bhabha
To install and run Bhabha, the required dependencies need to be installed.

| Dependency Name | Reason           | Required Link |
| ------------- |:-------------:|:-------------:|
| `Python 2.7`    | Running Bhabha   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `Tabulate`      | Graphics Display |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |

### Installing Dependencies
### Running Bhabha
### Seeking Help

## Assembly Code Dialect

## Features
Bhabha is highly configurable, and allows you to choose from an array of options. Bhabha can also parse your code to detect multiple types of errors and warnings before you run your code, and while it is being executed.

This section higlights the most important features that Bhabha offers to users.

### Custom Configuration
#### Parameter Suggestions

### Error Detection

#### Code Analysis
#### Code Suggestions
##### Static Analysis
##### Runtime Analysis

### Internal State Display

shows the internal state of the machine as the user code executes
                "LD"   , ["<nnnn>, Ri", "Ri, Rj"]
                "LDi"  , ["nnnn, Ri"]
                "SD"   , ["Ri, <nnnn>", "Ri, Rj"]
                "SDi"  , ["mmmm, <nnnn>", "mmmm, Ri"]
                "ADD"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"]
                "SUB"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"]
                "MUL"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"]
                "DIV"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"]
                "JMP"  , ["<label-name>"]
                "JZ"   , ["Ri, <label-name>"]
                "JNZ"  , ["Ri, <label-name>"]
                "MORE" , ["Ri, Rj, Rk", "Ri, nnnn, Rk"]
                "LESS" , ["Ri, Rj, Rk", "Ri, nnnn, Rk"]
                "SAME" , ["Ri, Rj, Rk", "Ri, nnnn, Rk"]
                "AND"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"]
                "OR"   , ["Ri, Rj, Rk", "Ri, nnnn, Rk"]
                "XOR"  , ["Ri, Rj, Rk", "Ri, nnnn, Rk"]
                "NOT"  , ["Ri, Rj", "nnnn, Ri"]
                "PUSH" , ["Ri", "nnnn"]
                "POP"  , ["Ri", "<nnnn>"]
                "<label-name>:"

| Instruction | Syntax           | Description |
| ------------- |:-------------:|:-------------:|
| `LD`    | `LD <nnnn>, Ri` or `LD Rj, Ri`   | `Causes register Ri to store the data stored in memory location <nnnn>` or `Causes register Ri to store the data stored in memory location contained in Rj`  |
| `LDi`      | `LDi nnnn, Ri` | `Causes integer nnnn to be stored in register Ri` |
| `SD`    | `SD Ri, <nnnn>` or `SD Ri, Rj`   | `Causes data in Ri to be stored to memory location <nnnn>` or `Causes data in Ri to be stored to memory location contained in register Rj`|
| `SDi`      | `SDi mmmm, <nnnn>` or `SDi mmmm, Ri` |  `Causes integer mmmm to be stored in memory location <nnnn>` or `Causes integer mmmm to be stored in memory location containted in register Ri` |
| `ADD`    | `ADD Ri, Rj, Rk` or `ADD Ri, nnnn, Rk`   |  `Adds Ri and Rj, and stores the sum to register Rk` or `Adds Ri and integer nnnn and stores the result in register Rk` |
| `SUB`      | `SUB Ri, Rj, Rk` or `SUB Ri, nnnn, Rk` |  `Subtracts Rj from Ri, and stores the result to register Rk` or `Subtracts integer nnnn from Ri and stores the result in register Rk` |
| `MUL`    | `MUL Ri, Rj, Rk` or `MUL Ri, nnnn, Rk`   |  `Multiplies Ri and Rj, and stores the product to register Rk` or `Adds Ri and integer nnnn and stores the product to register Rk` |
| `DIV`      | `DIV Ri, Rj, Rk` or `DIV Ri, nnnn, Rk` |  `Divides Ri by Rj, and stores the result to register Rk` or `Divides Ri by integer nnnn and stores the result in register Rk` |
| `JMP`    | `JMP <label-name>`   |  `Causes program control to jump to label <label-name>` |
| `JZ`      | `JZ Ri, <label-name>` |  `Causes program control to jump to label <label-name> if Ri is zero` |
| `JNZ`    | `JNZ Ri, <label-name>`   |  `Causes program control to jump to label <label-name> if Ri is zero` |
| `MORE`      | `MORE Ri, Rj, Rk` or `Ri, nnnn, Rk` | `Causes Rk to become 1 if Ri > Rj, 0 otherwise` or `Causes Rk to become 1 if R1 > nnnn, 0 otherwise` |
| `LESS`    | `LESS Ri, Rj, Rk` or `LESS Ri, nnnn, Rk`  |  `Causes Rk to become 1 if Ri < Rj, 0 otherwise` or `Causes Rk to become 1 if R1 < nnnn, 0 otherwise` |
| `SAME`      | `SAME Ri, Rj, Rk` or `SAME Ri, nnnn, Rk` |  `Causes Rk to become 1 if Ri and Rj are equal, 0 otherwise` or `Causes Rk to become 1 if R1 and integer nnnn are equal, 0 otherwise` |
| `AND`    | `AND Ri, Rj, Rk` or `AND Ri, nnnn, Rk`   | `Calculates the bitwise AND of Ri and Rj, and stores the result in Rk` or `Calculates the bitwise AND of Ri and nnnn, and stores the result in Rk` ) |
| `OR`      | `OR Ri, Rj, Rk` or `OR Ri, nnnn, Rk` |  `Calculates the bitwise OR of Ri and Rj, and stores the result in Rk` or `Calculates the bitwise OR of Ri and nnnn, and stores the result in Rk` |
| `XOR`    | `XOR Ri, Rj, Rk` or `XOR Ri, nnnn, Rk`   |  `Calculates the bitwise XOR of Ri and Rj, and stores the result in Rk` or `Calculates the bitwise XOR of Ri and nnnn, and stores the result in Rk` |
| `NOT`      | `NOT Ri, Rj` or `NOT nnnn, Ri` |  `Calculates the bitwise NOT of Ri and stores the result in Rj` or `Calculates the bitwise NOT of nnnn and stores the result in Rj` |
| `PUSH`    | `PUSH Ri` or `PUSH nnnn`   |  `Pushes value stored in Ri onto the stack` or `Pushes integer nnnn onto the stack` |
| `POP`      | `POP Ri` or `POP <nnnn>` |  `Pops off an element from the stack, and stores it in Ri` or `Pops off an element from the stack, and stores it in memory location <nnnn>`  |
| Label Name      | `<label-name>:` |  `Defines a new label with name <label-name>` |
