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
| `LD`    | `LD <nnnn>, Ri` or `LD Ri, Rj`   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `LDi`      | `nnnn, Ri` |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
| `SD`    | 'Ri, <nnnn>' or 'Ri, Rj'   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `SDi`      | "mmmm, <nnnn>", "mmmm, Ri"] |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
| `ADD`    | "Ri, Rj, Rk", "Ri, nnnn, Rk"   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `SUB`      | "Ri, Rj, Rk", "Ri, nnnn, Rk" |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
| `MUL`    | "Ri, Rj, Rk", "Ri, nnnn, Rk"   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `DIV`      | "Ri, Rj, Rk", "Ri, nnnn, Rk" |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
| `JMP`    | "<label-name>"   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `JZ`      | "Ri, <label-name>" |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
| `JNZ`    | "Ri, <label-name>"   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `MORE`      | "Ri, Rj, Rk", "Ri, nnnn, Rk" |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
| `LESS`    | "Ri, Rj, Rk", "Ri, nnnn, Rk"  |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `SAME`      | "Ri, Rj, Rk", "Ri, nnnn, Rk" |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
| `AND`    | "Ri, Rj, Rk", "Ri, nnnn, Rk"   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `OR`      | "Ri, Rj, Rk", "Ri, nnnn, Rk" |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
| `XOR`    | "Ri, Rj, Rk", "Ri, nnnn, Rk"   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `NOT`      | "Ri, Rj", "nnnn, Ri" |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
| `PUSH`    | "Ri", "nnnn"   |  [Download Python 2.7](https://www.python.org/downloads/release/python-2712/) |
| `POP`      | "Ri", "<nnnn>" |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
| Label Name      | "<label-name>:" |  [Download Tablulate](https://pypi.python.org/pypi/tabulate) |
