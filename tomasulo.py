import collections
from collections import namedtuple
import itertools
from Track_Instruction import Track_Instructions
from reorder_buffer import reorder_buffer
from FunctionalUnits import FunctionalUnits
from Load import Load

Instruction = namedtuple('Instruction',('opcode','destination_register','source_register')) 

def InstructionCreator(string):
    tokens = string.split(' ')
    opcode = tokens[0]
    write = tokens[1]
    read = []
    for i in range(2, len(tokens)):
        read.append(tokens[i])
    read = tuple(read)
    newInstr = Instruction(
        opcode=opcode, destination_register=write, source_register=read)
    return newInstr

def Bin_to_assembly(input):
    opcode = int(input[25:32])
    InstType = None
    Dest = None
    source1 = None
    source2 = None

    if(opcode == 110011):
        if(int(input[17:20]) == 0):
            if(int(input[0:7],2) == 0):
                InstType = 'ADD'
            elif(int(input[0:7],2) == 32):
                InstType = 'SUB'
            elif(int(input[0:7],2) == 1):
                InstType = 'MUL'
            else:
                print("Current processor does not support the given function")
            Dest = "R"+str(int(input[20:25],2))
            source1 = "R"+str(int(input[12:17],2))
            source2 = "R"+str(int(input[7:12],2))
        elif(int(input[17:20],2) == 4):
            if(int(input[0:7],2) == 1):
                InstType = 'DIV'
                Dest = "R"+str(int(input[20:25],2))
                source1 = "R"+str(int(input[12:17],2))
                source2 = "R"+str(int(input[7:12],2))
            else:
                print("Wrong Instruction, does not support the given function")
        else:
            print("Wrong Instruction, does not support the given function")
    elif(opcode == 11):
        if(int(input[17:20],2) == 2):
            InstType= 'LW'
            Dest = "R"+str(int(input[20:25],2))
            source2 = "R"+str(int(input[12:17],2))
            source1 = str(-int(input[0])*2**11 + int(input[1:12],2))          
        else:
            print("Wrong Instruction, does not support the given function")
    
    decoded = InstType + " " + Dest + " " + source1 + " " + source2
    return decoded

    

if __name__ == "__main__" :  
    Bin_Instruction = ["00000000000000010010000110000011", "00000010010000011100000100110011", "00000010011000101000000010110011", "00000000100000111000000110110011", "00000010001100001000000010110011", "01000000010100001000001000110011", "00000000001000100000000010110011"]
    
    #The above 32bit instruction form corresponding to this - ["LW R3 0 R2","DIV R2 R3 R4", "MUL R1 R5 R6", "ADD R3 R7 R8", "MUL R1 R1 R3", "SUB R4 R1 R5", "ADD R1 R4 R2"] # Original Instructions
    instruction = []

    for Bintstruc in Bin_Instruction:
        instruction.append(Bin_to_assembly(Bintstruc))

    #instructions = ["LW R3 0 R2","DIV R2 R3 R4", "MUL R1 R5 R6", "ADD R3 R7 R8", "MUL R1 R1 R3", "SUB R4 R1 R5", "ADD R1 R4 R2"] # Original Instructions
    
    #instructions = ["LW R6 12 R2","LW R2 45 R3","MUL R1 R2 R4", "SUB R8 R6 R2", "DIV R5 R1 R6", "ADD R6 R8 R2"] # Other test case

    #instructions = ["LW R3 0 R2","SUB R4 R1 R5","DIV R2 R3 R4","SUB R1 R4 R2","MUL R1 R5 R6"]  # Sample testing - This is working fine
    converted_instructions = []

    for instruct in instruction:
        converted_instructions.append(InstructionCreator(instruct))

###########################################################################################################################################################################################################                                                                     #####   Below is format of Regfile, RS's   #####
##########################################################################################################################################################################################################

    Regfile = {'R1': {'Name':'R1', 'Value':12, 'Tag':None, 'valid':1},
               'R2': {'Name':'R2', 'Value':16, 'Tag':None, 'valid':1},
               'R3': {'Name':'R3', 'Value':45, 'Tag':None, 'valid':1},
               'R4': {'Name':'R4', 'Value':5, 'Tag':None, 'valid':1},
               'R5': {'Name':'R5', 'Value':4, 'Tag':None, 'valid':1},
               'R6': {'Name':'R6', 'Value':1, 'Tag':None, 'valid':1},
               'R7': {'Name':'R7', 'Value':1, 'Tag':None, 'valid':1},
               'R8': {'Name':'R8', 'Value':2, 'Tag':None, 'valid':1},
               'R9': {'Name':'R9', 'Value':2, 'Tag':None, 'valid':1},
               'R10':{'Name':'R10','Value':3, 'Tag':None, 'valid':1}}

    MD_RS = {'RS4': {'Instruction' : None, 'Busy': 0, 'Destination_tag': None, 'Source_tag1': None, 'Source_tag2': None, 'Value_of_source_1': None, 'Value_of_source_2': None},
             'RS5': {'Instruction' : None, 'Busy': 0, 'Destination_tag': None, 'Source_tag1': None, 'Source_tag2': None, 'Value_of_source_1': None, 'Value_of_source_2': None}}

    AS_RS = {'RS1': {'Instruction' : None, 'Busy': 0, 'Destination_tag': None, 'Source_tag1': None, 'Source_tag2': None, 'Value_of_source_1': None, 'Value_of_source_2': None},
             'RS2': {'Instruction' : None, 'Busy': 0, 'Destination_tag': None, 'Source_tag1': None, 'Source_tag2': None, 'Value_of_source_1': None, 'Value_of_source_2': None},
             'RS3': {'Instruction' : None, 'Busy': 0, 'Destination_tag': None, 'Source_tag1': None, 'Source_tag2': None, 'Value_of_source_1': None, 'Value_of_source_2': None}}

    LW_buffer = {'LB1': {'Instruction' : None, 'Busy': 0, 'Destination_tag': None, 'Address_offset': None, 'Source_tag': None, 'Source_value': None},
            'LB2': {'Instruction' : None, 'Busy': 0, 'Destination_tag': None, 'Address_offset': None, 'Source_tag': None, 'Source_value': None},
            'LB3': {'Instruction' : None, 'Busy': 0, 'Destination_tag': None, 'Address_offset': None, 'Source_tag': None, 'Source_value': None }}

    RS = [AS_RS,MD_RS]

###########################################################################################################################################################################################################
                                                                                 ##### End of Format #####                                                                                                 ###########################################################################################################################################################################################################

    cycle = 0
    track_instructions = Track_Instructions(converted_instructions)
    rob = reorder_buffer()
    functional_units = FunctionalUnits()
    load_unit = Load()

    # The cdb is a list of instructions queued up to enter writeback.  At the WB
    # stage, the instruction with the lowest index is put on the cdb, and the
    # others wait until a later cycle.
    cdb = list()

    maxcycle = 100

    while not track_instructions.update(cycle, maxcycle):

        # Deal with CM stage
        rob.commit(Regfile,cycle)
                
        # Dealing with WB stage
        if cdb:
            sorted(cdb, key=lambda x: x['Instruction'].index)
            
            cdb_data = cdb.pop(0)

            for rs in RS:
                for j,k in rs.items():
                    if k['Busy'] == 1:
                        if k['Source_tag1'] == cdb_data['Tag']:

                            k['Value_of_source_1'] = cdb_data['Value']

                            k['Source_tag1'] = None

                        if k['Source_tag2'] == cdb_data['Tag']:
                            
                            k['Value_of_source_2'] = cdb_data['Value']

                            k['Source_tag2'] = None
            
            for lw in LW_buffer.values():
                if lw['Busy'] == 1:
                    
                    if lw['Source_tag'] == cdb_data['Tag']:
                        
                        lw['Source_value'] = cdb_data['Value']

                        lw['Source_tag'] = None

            rob.update_rob(cdb_data)
            
        # Deal with instructions currently in issue stage and in RS
        
        for rs in RS:
            for j,k in rs.items():
                if k['Busy'] == 1:
                    if k['Source_tag1'] == None and k['Source_tag2'] == None:
                        functional_units.enqueue(k)
                        k['Busy'] = 0
                        k['Value_of_source_1'] = None
                        k['Value_of_source_1'] = None

        for lw in LW_buffer.values():
            if lw['Busy'] == 1:
                if lw['Source_tag'] == None:
                    load_unit.add_to_queue(lw)
                    lw['Busy'] = 0
                    lw['Source_value'] = None
        
        # Deal with EX stage
       
        functional_units.update(track_instructions, cdb, cycle)
        load_unit.update(cdb,cycle)
    
        # Set up next instruction to issue next time
        track_instructions.issue_next(rob,RS,LW_buffer,Regfile)

        cycle += 1

    
    print("\nTotal cycles taken is : ", cycle-1,"\n")

    print("Instruction Table : \n")
    for instruction in track_instructions.instructions:

            print(instruction.opcode,instruction.destination_register,",",instruction.source_register[0],",",instruction.source_register[1]," : ",instruction.log,"\n")
