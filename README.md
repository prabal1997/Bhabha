# Bhabha
A 16-bit assembly simulator that allows you to view the internal machine state as the code is being executed.
--insert a photo--
## What does Bhabha do?
Bhabha allows users to emulate a computer of desired configuration, and then run the desired assembly code on it. Morover, Bhabha will display the internal state of the computer as the code is being executed.

Bhabha is an excellent way of learning about Assembly programming, as it allows users to understand how computers operate at the fundamental level.

## Running Bhabha
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
