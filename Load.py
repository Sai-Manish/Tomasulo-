class Load:
    
    def __init__(self):
        self.duration = 5
        #self.name = name
        self.end_cycle = None
        self.current_instruction = None
        self.address = None
        self.cdb_form = {'Instruction': None, 'Tag': None, 'Value': None}
        self.Mem = list(range(0, 101))
        self.started = False
        self.queue = list()
    
    def add_to_queue(self,LW_entry):
        self.temp = LW_entry.copy()  #Changed here
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

    def update(self,cdb,current_cycle):
        
        if current_cycle == self.end_cycle:

            self.current_instruction['Instruction'].queued_to_write()
            self.cdb_form['Instruction'] = self.current_instruction['Instruction']
            self.cdb_form['Tag'] = self.current_instruction['Instruction'].ROB_index
            self.address = int(self.current_instruction['Address_offset']) + self.current_instruction['Source_value']
            self.cdb_form['Value'] = self.Mem[self.address]

            cdb.append(self.cdb_form)
            self.current_instruction = None
            
        if not self.current_instruction:
                self.do_enqueue(current_cycle)

