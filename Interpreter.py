import AST
import SymbolTab
from Memory import *
from Exceptions import  *
from visit import *
import sys
import re

sys.setrecursionlimit(10000)

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
        return None if (r1 is None) or (r2 is None) else self.op[node.op](r1, r2)

    @when(AST.Const)
    def visit(self, node):
        if re.match(r"(\+|-){0,1}(\d+\.\d+|\.\d+)", node.val):
            return self.float(node)
        elif re.match(r"(\+|-){0,1}\d+", node.val):
            return self.integer(node)
        elif re.match(r"\A('.*'|\".*\")\Z", node.val):
            return self.string(node)
        else:
            return self.memoryStack.get(node.val)


    @when(AST.Declarations)
    def visit(self, node):
        for expr in node.declarations:
            expr.accept(self)

    @when(AST.Declaration)
    def visit(self, node):
        r1 = node.inits.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for expr in node.instructions:
            expr.accept(self)

    @when(AST.ReturnInstr)
    def visit(self, node):
        raise ReturnValueException(node.expr)

    @when(AST.PrintInstr)
    def visit(self, node):
        return node.expr.accept(self)

    @when(AST.Inits)
    def visit(self, node):
        for expr in node.inits:
            expr.accept(self)

    @when(AST.Init)
    def visit(self, node):
        expr = node.expr.accept(self)
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
        if rc.accept(self):
            return ri.accept(self)
        else:
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
        r = node.instruction.accept(self)
        while node.condition.accept(self):
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
            node.declarations.accept(self)
        return node.instructions_opt.accept(self)

    @when(AST.CastFunction)
    def visit(self, node):
        fun = self.memoryStack.get(node.functionName)
        funM = Memory(node.functionName)

        self.memoryStack.push(funM)
        try:
            node.args.accept(self)
        except ReturnValueException as e:
            return e.expr.accept(self)
        finally:
            self.memoryStack.pself.op()

    @when(AST.ExprInBrackets)
    def visit(self, node):
        return node.expr.accept(self)

    @when(AST.ExprList)
    def visit(self, node):
        for expr in node.expressions:
            expr.accept(self)

    @when(AST.FunctionList)
    def visit(self, node):
        for expr in node.functions:
            expr.accept(self)

    @when(AST.Function)
    def visit(self, node):
        self.memoryStack.insert(node.id, node)
        # node.args_list_or_empty.accpet(self)
        # node.compound_instr.accpet(self)
        # node.line.accpet(self)

    @when(AST.Arguments)
    def visit(self, node):
        for expr in node.arguments:
            expr.accept(self)

    @when(AST.Argument)
    def visit(self, node):
        self.memoryStack.insert(node.id, node)

    @when(AST.Block)
    def visit(self, node):
        self.memoryStack.push(Memory('block'))
        node.declarations.accept(self)
        node.fundefs_opt.accept(self)
        node.instructions_opt.accept(self)
        self.memoryStack.pop()

    @when(AST.Blocks)
    def visit(self, node):
        for expr in node.blocks:
            expr.accept(self)
