class Track_Instructions:

#this outer class will have a track of all the given instructions and there status
    
    class Each_Instruction:
        #this inner class will be updating it status and all for every cycle

        States = ["unissued","IS","EX","WB","CM","waiting_to_execute","waiting_to_WB","not_yet_commited"]
        
        #log = [] #has log of at which cycle each stage has occured.

        def __init__(self,instruction,index):
            self.opcode = instruction.opcode
            self.destination_register = instruction.destination_register
            self.source_register = instruction.source_register
            self.index = index #index is used for maintaining inorder issue and inorder commit
            self.ROB_index = index%8
            self.log = list()
            self.current_state = "unissued"
            self.new_state = None
        def set_state(self,state):
            self.new_state = state
            
        def issue(self):
            self.set_state('IS')

        def execute(self):
            self.set_state('EX')

        def commit(self):
            self.set_state('CM')

        def writeback(self):
            self.set_state("WB")

        def queued_to_execute(self):
            self.set_state("waiting_to_execute")

        def queued_to_write(self):
            self.set_state("waiting_to_WB")

        def not_commited(self):
            self.set_state("not_yet_commited")
        
        def ready_to_commit(self):
            return self.current_state in ('WB', 'not_yet_committed')


        def update(self, new_cycle):
            
            if self.new_state:
                if self.new_state in set(('IS', 'EX', 'WB', 'CM')):
                    if self.new_state == 'WB' or self.new_state == 'CM':
                        self.log.append((self.new_state, new_cycle-1))
                    else:
                        self.log.append((self.new_state, new_cycle))
                if self.current_state == 'EX':
                    self.log.append(('EX-end', new_cycle - 1))
                
                self.current_state = self.new_state
                self.new_state = None


    def __init__(self, instructions):
        self.instructions = [
            Track_Instructions.Each_Instruction(instr, i)
            for i, instr in enumerate(instructions,1)]

    def issue_next(self,reorder_buffer,RS,LW,Regfile):
        self.reg = Regfile.copy()
        unissued = [i for i in self.instructions if i.current_state == "unissued"]
        if unissued and not reorder_buffer.is_full():
            
           self.is_RS_Free = False
           self.Free_RS = None

           if unissued[0].opcode == "ADD" or unissued[0].opcode == "SUB":

                for rs in RS[0].values():
                    
                    if rs['Busy'] == 0:
                        self.is_RS_Free = True
                        self.Free_Rs = rs
                        
                        break
                
                if self.is_RS_Free == True and reorder_buffer.ROB[unissued[0].ROB_index]['Free'] == True:
                    
                    if self.reg[unissued[0].source_register[0]]['valid'] != 1:
                        
                        self.Free_Rs['Source_tag1'] = self.reg[unissued[0].source_register[0]]['Tag']

                    #if Regfile[unissued[0].source_register[0]]['valid'] != 1:
                        
                        #self.Free_Rs['Source_tag1'] = Regfile[unissued[0].source_register[0]]['Tag']

                    else:
                        self.Free_Rs['Value_of_source_1'] = self.reg[unissued[0].source_register[0]]['Value']

                    if self.reg[unissued[0].source_register[1]]['valid'] != 1:

                        self.Free_Rs['Source_tag2'] = self.reg[unissued[0].source_register[1]]['Tag']

                    else:
                        self.Free_Rs['Value_of_source_2'] = self.reg[unissued[0].source_register[1]]['Value']
                    
                    self.Free_Rs['Instruction'] = unissued[0]
                    self.Free_Rs['Destination_tag'] = unissued[0].ROB_index
                    Regfile[unissued[0].destination_register]['Tag'] = unissued[0].ROB_index
                    Regfile[unissued[0].destination_register]['valid'] = 0
                    reorder_buffer.add(unissued[0])
                    unissued[0].issue()
                    self.Free_Rs['Busy'] = 1
           
           if unissued[0].opcode == "MUL" or unissued[0].opcode == "DIV":

                for rs in RS[1].values():

                    if rs['Busy'] == 0:
                        self.is_RS_Free = True
                        self.Free_Rs = rs
                        break

                if self.is_RS_Free == True and reorder_buffer.ROB[unissued[0].ROB_index]['Free'] == True:
                   
                    if Regfile[unissued[0].source_register[0]]['valid'] != 1:

                        self.Free_Rs['Source_tag1'] = Regfile[unissued[0].source_register[0]]['Tag']

                    else:
                        self.Free_Rs['Value_of_source_1'] = Regfile[unissued[0].source_register[0]]['Value']

                    if Regfile[unissued[0].source_register[1]]['valid'] != 1:

                        self.Free_Rs['Source_tag2'] = Regfile[unissued[0].source_register[1]]['Tag']

                    else:
                        self.Free_Rs['Value_of_source_2'] = Regfile[unissued[0].source_register[1]]['Value']
                    
                    self.Free_Rs['Instruction'] = unissued[0]
                    self.Free_Rs['Destination_tag'] = unissued[0].ROB_index

                    Regfile[unissued[0].destination_register]['Tag'] = unissued[0].ROB_index
                    Regfile[unissued[0].destination_register]['valid'] = 0
                    reorder_buffer.add(unissued[0])
                    unissued[0].issue()
                    self.Free_Rs['Busy'] = 1

           if unissued[0].opcode == 'LW':
               for lw in LW.values():
                   if lw['Busy'] == 0:
                       is_lw_Free = True
                       Free_lw = lw
                       break

               if is_lw_Free == True and reorder_buffer.ROB[unissued[0].ROB_index]['Free'] == True:
                   
                   Free_lw['Instruction'] = unissued[0]
                   Free_lw['Destination_tag'] = unissued[0].ROB_index
                   Regfile[unissued[0].destination_register]['Tag'] = unissued[0].ROB_index
                   Regfile[unissued[0].destination_register]['valid'] = 0

                   if Regfile[unissued[0].source_register[1]]['valid'] != 1:

                       Free_lw['Source_tag'] = Regfile[unissued[0].source_register[1]]['Tag']

                   else:
                       
                       Free_lw['Source_value'] = Regfile[unissued[0].source_register[1]]['Value']


                   Free_lw['Address_offset'] = unissued[0].source_register[0]

                   reorder_buffer.add(unissued[0])
                   unissued[0].issue()
                   Free_lw['Busy'] = 1

    def update(self, new_cycle, maxcycle):
        for instruction in self.instructions:
            instruction.update(new_cycle)
        if self.instructions[-1].current_state == 'CM':
        
            return True
        if new_cycle >= maxcycle:
            return True
        #else:
         #   return False