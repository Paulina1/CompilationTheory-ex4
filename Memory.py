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
        self.memList = []
        if memory is not None:
            self.memList.append(memory)
        else:
            self.memList.append(Memory("toplevel"))

    def get(self, name):             # gets from memory stack current value of variable <name>
        indices = range(len(self.memList))
        indices.reverse()
        for i in indices:
            if self.memList[i].has_key(name):
                return self.memList[i].get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.memList[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        indices = range(len(self.memList))
        indices.reverse()
        for i in indices:
            if self.memList[i].has_key(name):
                self.memList[i].put(name, value)
                break

    def push(self, memory): # pushes memory <memory> onto the stack
        self.memList.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.memList.pop()
