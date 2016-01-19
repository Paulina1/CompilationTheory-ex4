class Memory:

    def __init__(self, name): # memory name
        self.memory = {}

    def has_key(self, name):  # variable name
        return self.memory.has_key(name)

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
        # print 'Indices:', indices
        for i in indices:
            # print 'Looking at indice:', i
            for item in self.memList[i].memory:
                # print 'Contains', item
                if (item == name):
                    # print 'Memory has key:', name
                    # print item
                    # print self.memList[i].memory
                    return self.memList[i].get(name)
                # else:
                    # print 'Memory doesnt have key', name
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.memList[-1].put(name, value)
        # print "Memory top: ", self.memList[-1].get(name)

    def set(self, name, value): # sets variable <name> to value <value>
        indices = range(len(self.memList))
        indices.reverse()
        for i in indices:
            if self.memList[i].has_key(name):
                self.memList[i].put(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.memList.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.memList.pop()
