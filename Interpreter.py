import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):

    def add(r1, r2):
        return r1 + r2

    def minus(r1, r2):
        return r1 - r2

    def x(r1, r2):
        return r1 * r2

    def divide(r1, r2):
        return r1 / r2

    def greater(r1, r2):
        return r1 > r2 ? 1 : 0

    def less(r1, r2):
        return r1 < r2 ? 1 : 0

    def greater_eq(r1, r2):
        return r1 >= r2 ? 1 : 0

    def less_eq(r1, r2):
        return r1 <= r2 ? 1 : 0

    def eq(r1, r2):
        return r1 == r2 ? 1 : 0

    def neq(r1, r2):
        return r1 != r2 ? 1 : 0

    def mod(r1, r2):
        return r1 % r2

    def b_and(r1, r2):
        return r1 & r2

    def b_xor(r1, r2):
        return r1 ^ r2

    def b_or(r1, r2):
        return r1 | r2

    def shl(r1, r2):
        return r1 << r2

    def shr(r1, r2):
        return r1 >> r2

    op = {}
    op['+'] = add
    op['-'] = minus
    op['*'] = x
    op['/'] = divide
    op['>'] = greater
    op['<'] = less
    op['>='] = greater_eq
    op['<='] = less_eq
    op['=='] = eq
    op['!='] = neq
    op['%'] = mod
    op['&'] = b_and
    op['^'] = b_xor
    op['|'] = b_or
    op['<<'] = shl
    op['>>'] = shr


    @on('node')
    def visit(self, node):
        pass

	@when(AST.BinExpr)
	def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return op[node.op](r1, r2)

	@when(AST.Const)
	def visit(self, node):
        return node.val

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
        return node.expr.accept(self)

	@when(AST.AssignmentInstr)
	def visit(self, node):
        return node.expr.accept(self)

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
        node.declarations.accept(self)
        return node.instructions_opt.accept(self)

	@when(AST.CastFunction)
	def visit(self, node):
        node.functionName.accept(self)
        node.args.accept(self)

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
        node.args_list_or_empty.accpet(self)
        node.compound_instr.accpet(self)
        node.line.accpet(self)

	@when(AST.Arguments)
	def visit(self, node):
        for expr in node.arguments:
            expr.accept(self)

	@when(AST.Argument)
	def visit(self, node):
        pass

	@when(AST.Block)
	def visit(self, node):
        node.declarations.accpet(self)
        node.fundefs_opt.accpet(self)
        node.instructions_opt.accpet(self)

	@when(AST.Blocks)
	def visit(self, node):
        for expr in node.blocks:
            expr.accept(self)
