class Memory:

    def __init__(self, name): # memory name
        self.memory = {}

    def has_key(self, name):  # variable name
        self.memory.has_key(name)

    def get(self, name):         # gets from memory current value of variable <name>
        return self.memory[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory[name] = value

class MemoryStack:

    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.memory = memory
        self.memList = []

    def get(self, name):             # gets from memory stack current value of variable <name>
        return self.memory.get(name)

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.memory.put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        self.memory.put(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.memList.append(self.memory)
        self.memory = memory

    def pop(self):          # pops the top memory from the stack
        self.memory = self.memList.pop()
