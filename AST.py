
class Node(object):

    def __str__(self):
        return self.printTree()

    def accept(self, visitor):
        return visitor.visit(self)


class BinExpr(Node):

    def __init__(self, op, left, right, line):
        self.line = line
        self.op = op
        self.left = left
        self.right = right

class Const(Node):
    def __init__(self, val, line):
        self.val = val
        self.line = line

class Declarations(Node):
    def __init__(self):
        self.declarations = []

    def push(self, declaration):
        self.declarations.append(declaration)

    def children(self):
        return self.declarations

class Declaration(Node):
    def __init__(self, type, inits, line):
        self.line = line
        self.type = type
        self.inits = inits

class Instructions(Node):
    def __init__(self):
        self.instructions = []

    def push(self, instruction):
        self.instructions.append(instruction)

    def children(self):
        return self.instructions

class ReturnInstr(Node):
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line

class PrintInstr(Node):
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line

class Inits(Node):
    def __init__(self):
        self.inits = []

    def push(self, init):
        self.inits.append(init)

    def children(self):
        return self.inits

class Init(Node):
    def __init__(self, id, expr, line):
        self.id = id
        self.expr = expr
        self.line = line

class AssignmentInstr(Node):
    def __init__(self, id, expr, line):
        self.id = id
        self.expr = expr
        self.line = line

class ChoiceInstr(Node):
    def __init__(self, condition, instruction, else_instr, line):
        self.condition = condition
        self.instruction = instruction
        self.else_instr = else_instr
        self.line = line

class WhileInstr(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction

class RepeatInstr(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction

class ContinueInstr(Node):
    def __init__(self, line):
        self.line = line

class BreakInstr(Node):
    def __init__(self, line):
        self.line = line

class CompoundInstr(Node):
    def __init__(self, declarations, instructions_opt, line):
        self.line = line
        self.declarations = declarations
        self.instructions_opt = instructions_opt

class CastFunction(Node):
    def __init__(self, functionName, args, line):
        self.functionName = functionName
        self.args = args
        self.line = line

class ExprInBrackets(Node):
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line

class ExprList(Node):
    def __init__(self):
        self.expressions = []

    def push(self, expr):
        self.expressions.append(expr)

    def children(self):
        return self.expressions

class FunctionList(Node):
    def __init__(self):
        self.functions = []

    def push(self, expr):
        self.functions.append(expr)

    def children(self):
        return self.functions

class Function(Node):
    def __init__(self, type, id, args_list_or_empty, compound_instr, line):
        self.type = type
        self.id = id
        self.args_list_or_empty = args_list_or_empty
        self.compound_instr = compound_instr
        self.line = line

class Arguments(Node):
    def __init__(self):
        self.arguments = []

    def push(self, argument):
        self.arguments.append(argument)

    def children(self):
        return self.arguments

class Argument(Node):
    def __init__(self, type, id, line):
        self.type = type
        self.line = line
        self.id = id

#do nowej gramatyki: program -> blocks -- blocks -> blocks block -- block -> declarations fundefs instructions
class Block(Node):
    def __init__(self, declarations, fundefs_opt, instructions_opt):
        self.declarations = declarations
        self.fundefs_opt = fundefs_opt
        self.instructions_opt = instructions_opt

#do nowej gramatyki:
class Blocks(Node):
    def __init__(self):
        self.blocks = []

    def push(self, block):
        self.blocks.append(block)

    def children(self):
        return self.blocks
