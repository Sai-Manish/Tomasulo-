# Base Model of Tomasulo machine, It is single memory access and using only R-format minstructions from RISC-V ISA
### How to run the code :

- > Run tomasulo.py 
- > In tomasulo.py code the encodings are for these instruction : LW R3,0(R2), DIV R2,R3,R4, MUL R1,R5,R6, ADD R3,R7,R8, MUL R1,R1,R3, SUB R4,R1,R5, ADD R1,R4,R2
- > To to run different instructions need to change the entries in Bin_Instruction list.
- > To run on different instructions you can comment down the Bin_Assembly function instead enter in assembly
