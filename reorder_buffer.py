class reorder_buffer:

    
    def __init__(self, length=8):
        
        self.length = length
        self.commit_pointer = 0
        self.add_pointer = 0
	
	#Free = 0 means Rob entry is free
        self.ROB = {1: {'Instruction': None, 'Instruction_type' : None, 'Destination': None, 'Value': None, 'Free': True}, 
           	    2: {'Instruction': None, 'Instruction_type' : None, 'Destination': None, 'Value': None, 'Free': True}, 
           	    3: {'Instruction': None, 'Instruction_type' : None, 'Destination': None, 'Value': None, 'Free': True}, 
                    4: {'Instruction': None, 'Instruction_type' : None, 'Destination': None, 'Value': None, 'Free': True}, 
                    5: {'Instruction': None, 'Instruction_type' : None, 'Destination': None, 'Value': None, 'Free': True},
                    6: {'Instruction': None, 'Instruction_type' : None, 'Destination': None, 'Value': None, 'Free': True}, 
                    7: {'Instruction': None, 'Instruction_type' : None, 'Destination': None, 'Value': None, 'Free': True}, 
                    8: {'Instruction': None, 'Instruction_type' : None, 'Destination': None, 'Value': None, 'Free': True}}


    def add(self,instruction):
        if self.is_full():
            raise Exception ("ROB is Full Sorry")
        
        self.ROB[instruction.ROB_index]['Instruction'] = instruction
        self.ROB[instruction.ROB_index]['Instruction_type'] = instruction.opcode
        self.ROB[instruction.ROB_index]['Destination'] = instruction.destination_register
        self.ROB[instruction.ROB_index]['Free'] = False
        self.add_pointer = (self.add_pointer + 1) % 8

    def is_full(self):
        if self.add_pointer == self.commit_pointer and self.ROB[self.add_pointer + 1]['Free'] == False:
            return True
        else:
            return False

    def update_rob(self,Cdb_value):
        
        self.ROB[Cdb_value['Tag']]['Value'] = Cdb_value['Value']
        Cdb_value['Instruction'].writeback()
    
    def commit(self,Regfile,cycle):
        if self.add_pointer == 0 and self.commit_pointer == 0 and self.ROB[1]['Free'] == True:
            return
        
        head = self.ROB[self.commit_pointer+1]['Instruction']
        
        if head:
 
            if head.ready_to_commit():
                
                Regfile[head.destination_register]['Value'] = self.ROB[self.commit_pointer+1]['Value']
               
                if Regfile[head.destination_register]['Tag'] == self.commit_pointer+1:
                
                    Regfile[head.destination_register]['Tag'] = None

                    Regfile[head.destination_register]['Valid'] = 1
            
                head.commit()
                self.ROB[self.commit_pointer+1]['Free'] = True
            
                self.commit_pointer = (self.commit_pointer + 1) % 8
               

    