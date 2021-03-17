import collections
from collections import namedtuple
import itertools
global MAXCYCLE

class FunctionalUnits:

    class Fu_unit:
        
        def __init__(self, duration, name):
            self.duration = duration
            self.name = name
            self.queue = list()
            self.cdb_form = {'Instruction': None, 'Tag': None, 'Value': None}
            self.end_cycle = None
            self.current_instruction = None
            
        def add_to_queue(self,RS_entry):
            self.temp = RS_entry.copy()  #Changed here
            self.queue.append(self.temp)
            self.temp['Instruction'].queued_to_execute()
        
        def busy(self, cycle):
            return self.end_cycle and cycle < self.end_cycle

        def do_enqueue(self, current_cycle):
            if self.queue:
                
                sorted(self.queue, key=lambda i: i['Instruction'].index)
                self.current_instruction = self.queue.pop(0)
                self.current_instruction['Instruction'].execute()
                self.end_cycle = current_cycle + self.duration

        def update(self, cdb, current_cycle):
    
            if current_cycle == self.end_cycle:
                
                self.current_instruction['Instruction'].queued_to_write()
                #self.current_instruction['Instruction'].writeback()
                self.cdb_form['Instruction'] = self.current_instruction['Instruction']
                self.cdb_form['Tag'] = self.current_instruction['Instruction'].ROB_index 
                
                if self.current_instruction['Instruction'].opcode == 'ADD':
                    self.value = self.current_instruction['Value_of_source_1'] + self.current_instruction['Value_of_source_2']
                    self.cdb_form['Value'] = self.value
                    
                elif self.current_instruction['Instruction'].opcode == 'SUB':
                    self.value = self.current_instruction['Value_of_source_1'] - self.current_instruction['Value_of_source_2']
                    self.cdb_form['Value'] = self.value

                elif self.current_instruction['Instruction'].opcode == 'MUL':
                    self.value = self.current_instruction['Value_of_source_1'] * self.current_instruction['Value_of_source_2']
                    self.cdb_form['Value'] = self.value
                
                elif self.current_instruction['Instruction'].opcode == 'DIV':
                    if self.current_instruction['Value_of_source_2'] == 0:
                        self.value = 0
                    else:
                        self.value = self.current_instruction['Value_of_source_1'] / self.current_instruction['Value_of_source_2']
                    self.cdb_form['Value'] = self.value


                cdb.append(self.cdb_form)
                self.current_instruction = None
            
            if not self.current_instruction:
             
                self.do_enqueue(current_cycle)

            
    def __init__(self):

        dummy_fu = FunctionalUnits.Fu_unit(1, 'dummy_FU')
        add_fu = FunctionalUnits.Fu_unit(1,  'Add FU')
        mul_fu = FunctionalUnits.Fu_unit(10, 'Mul FU')
        div_fu = FunctionalUnits.Fu_unit(40, 'Div FU')
        self.opcode_map = collections.defaultdict(lambda: dummy_fu)
        self.opcode_map.update({
            'ADD': add_fu,
            'SUB': add_fu,
            'MUL': mul_fu,
            'DIV': div_fu
        })
        self.fu_list = [add_fu, mul_fu, div_fu]

    def enqueue(self, RS_entry):
        self.opcode_map[RS_entry['Instruction'].opcode].add_to_queue(RS_entry)

    def update(self, instruction_tracker, cdb, current_cycle):
        for fu in self.fu_list:
            fu.update(cdb, current_cycle)

