import AST
import SymbolTab
from Memory import *
from Exceptions import  *
from visit import *
import sys
import re

sys.setrecursionlimit(10000)

called = 0

class Interpreter(object):

    def __init__(self):
        self.memoryStack = MemoryStack()
        self.op = {}
        self.op['+'] = self.add
        self.op['-'] = self.minus
        self.op['*'] = self.x
        self.op['/'] = self.divide
        self.op['>'] = self.greater
        self.op['<'] = self.less
        self.op['>='] = self.greater_eq
        self.op['<='] = self.less_eq
        self.op['=='] = self.eq
        self.op['!='] = self.neq
        self.op['%'] = self.mod
        self.op['&'] = self.b_and
        self.op['^'] = self.b_xor
        self.op['|'] = self.b_or
        self.op['<<'] = self.shl
        self.op['>>'] = self.shr

    def add(self, r1, r2):
        return r1 + r2

    def minus(self, r1, r2):
        return r1 - r2

    def x(self, r1, r2):
        return r1 * r2

    def divide(self, r1, r2):
        return r1 / r2

    def greater(self, r1, r2):
        return 1 if r1 > r2 else 0

    def less(self, r1, r2):
        return 1 if r1 < r2 else 0

    def greater_eq(self, r1, r2):
        return 1 if r1 >= r2 else 0

    def less_eq(self, r1, r2):
        return 1 if r1 <= r2 else 0

    def eq(self, r1, r2):
        return 1 if r1 == r2 else 0

    def neq(self, r1, r2):
        return 1 if r1 != r2 else 0

    def mod(self, r1, r2):
        return r1 % r2

    def b_and(self, r1, r2):
        return r1 & r2

    def b_xor(self, r1, r2):
        return r1 ^ r2

    def b_or(self, r1, r2):
        return r1 | r2

    def shl(self, r1, r2):
        return r1 << r2

    def shr(self, r1, r2):
        return r1 >> r2

###################
    def float(self, node):
        return float(node.val)

    def integer(self, node):
        return int(node.val)

    def string(self, node):
        return node.val

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        to_return = None if (r1 is None) or (r2 is None) else self.op[node.op](r1, r2)
        return to_return

    @when(AST.Const)
    def visit(self, node):
        if re.match(r"(\+|-){0,1}(\d+\.\d+|\.\d+)", node.val):
            return self.float(node)
        elif re.match(r"(\+|-){0,1}\d+", node.val):
            return self.integer(node)
        elif re.match(r"\A('.*'|\".*\")\Z", node.val):
            return self.string(node)
        else:
            from_stack = self.memoryStack.get(node.val)
            #print from_stack
            return from_stack if from_stack is not None else None

    @when(AST.Declarations)
    def visit(self, node):
        for expr in node.declarations:
            expr.accept(self)

    @when(AST.Declaration)
    def visit(self, node):
        return node.inits.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for expr in node.instructions:
            expr.accept(self)

    @when(AST.ReturnInstr)
    def visit(self, node):
        raise ReturnValueException(node.expr)

    @when(AST.PrintInstr)
    def visit(self, node):
        data = node.expr.accept(self)
        print data[0]
        return data

    @when(AST.Inits)
    def visit(self, node):
        tab = []
        for expr in node.inits:
            tab.append(expr.accept(self))
        return tab

    @when(AST.Init)
    def visit(self, node):
        expr = node.expr.accept(self)
        # print 'Creating', node.id, 'with value', expr
        self.memoryStack.insert(node.id, expr)
        return expr

    @when(AST.AssignmentInstr)
    def visit(self, node):
        expr = node.expr.accept(self)
        self.memoryStack.set(node.id, expr)
        return expr

    @when(AST.ChoiceInstr)
    def visit(self, node):
        rc = node.condition
        ri = node.instruction
        re = node.else_instr

        if rc.accept(self) == 1:
            return ri.accept(self)
        else:
            if re is not None:
                return re.accept(self)

    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.condition.accept(self):
            try:
                r = node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        return r

    @when(AST.RepeatInstr)
    def visit(self, node):
        try:
            r = node.instruction.accept(self)
        except BreakException:
            return None
        except ContinueException:
            #ok
            pass

        while not node.condition.accept(self):
            try:
                r = node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        return r

    @when(AST.ContinueInstr)
    def visit(self, node):
        raise ContinueException()

    @when(AST.BreakInstr)
    def visit(self, node):
        raise BreakException()

    @when(AST.CompoundInstr)
    def visit(self, node):

        if node.declarations is not None:
            self.memoryStack.push(Memory('comp'))
            node.declarations.accept(self)
        ret = node.instructions_opt.accept(self)
        if node.declarations is not None:
            self.memoryStack.pop()

    @when(AST.CastFunction)
    def visit(self, node):
        fun = self.memoryStack.get(node.functionName)
        funM = Memory(node.functionName)
        exc = None


        try:
            arguments_f = node.args.accept(self)
            self.memoryStack.push(funM)
            node.args.accept(self)
            arguments = fun.args_list_or_empty.accept(self)

            i = 0
            for argument in arguments:
                self.memoryStack.insert(argument, arguments_f[i])
            i += 1

            fun.compound_instr.accept(self)
        except ReturnValueException as e:
            exc = e.value.accept(self)
        finally:
            self.memoryStack.pop()
            return exc

    @when(AST.ExprInBrackets)
    def visit(self, node):
        return node.expr.accept(self)

    @when(AST.ExprList)
    def visit(self, node):
        return_val = []
        for expr in node.expressions:
            return_val.append(expr.accept(self))
        return return_val

    @when(AST.FunctionList)
    def visit(self, node):
        return_val = ''
        for expr in node.functions:
            return_val += str(expr.accept(self))
        return return_val

    @when(AST.Function)
    def visit(self, node):
        self.memoryStack.insert(node.id, node)
        # node.args_list_or_empty.accpet(self)
        # node.compound_instr.accpet(self)
        # node.line.accpet(self)

    @when(AST.Arguments)
    def visit(self, node):
        tab = []
        for expr in node.arguments:
            tab.append(expr.accept(self))
        return tab

    @when(AST.Argument)
    def visit(self, node):
        self.memoryStack.insert(node.id, node)
        return node.id

    @when(AST.Block)
    def visit(self, node):
        self.memoryStack.push(Memory('block'))
        node.declarations.accept(self)
        if node.fundefs_opt is not None:
            node.fundefs_opt.accept(self)
        node.instructions_opt.accept(self)
        self.memoryStack.pop()

    @when(AST.Blocks)
    def visit(self, node):
        for expr in node.blocks:
            expr.accept(self)

