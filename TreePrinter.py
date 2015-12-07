import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    #wyrazenie np. a + b
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        return "| " * indent + self.op + "\n" + self.left.printTree(indent+1) + self.right.printTree(indent+1)

    @addToClass(AST.Const)
    def printTree(self, indent=0):
        return "| " * indent + str(self.val) + "\n"

    @addToClass(AST.Declarations)
    def printTree(self, indent=0):
        ret = ''
        for declaration in self.declarations:
            if declaration is not None:
                ret += declaration.printTree(indent)
        return ret

    @addToClass(AST.Declaration)
    def printTree(self, indent=0):
        return "| " * indent + "DECL\n" + self.inits.printTree(indent + 1)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        ret = ''
        for declaration in self.instructions:
            ret += declaration.printTree(indent)
        return ret

    @addToClass(AST.ReturnInstr)
    def printTree(self, indent=0):
		return "| " * indent + "RETURN" + "\n" + self.expr.printTree(indent + 1)

    @addToClass(AST.PrintInstr)
    def printTree(self, indent=0):
		return "| " * indent + "PRINT" + "\n" + self.expr.printTree(indent + 1)


    @addToClass(AST.Inits)
    def printTree(self, indent=0):
        ret = ''
        for declaration in self.inits:
            ret += declaration.printTree(indent)
        return ret

    @addToClass(AST.Init)
    def printTree(self, indent=0):
		return "| " * indent + "=\n" + "| " * (indent + 1) + self.id + "\n" + self.expr.printTree(indent + 1)

    @addToClass(AST.AssignmentInstr)
    def printTree(self, indent=0):
		return "| " * indent + "=\n" + "| " * (indent + 1) + self.id + "\n" + self.expr.printTree(indent+1)

    @addToClass(AST.ChoiceInstr)
    def printTree(self, indent=0):
        ret = "| " * indent + "IF\n" + self.condition.printTree(indent+1) + self.instruction.printTree(indent+1)
        if self.else_instr is not None:
            ret += "| " * indent + "ELSE\n" + self.else_instr.printTree(indent+1)
        return ret

    @addToClass(AST.WhileInstr)
    def printTree(self, indent=0):
		return "| " * indent + "WHILE\n" + self.condition.printTree(indent+1) + self.instruction.printTree(indent+1)

    @addToClass(AST.RepeatInstr)
    def printTree(self, indent=0):
		return "| " * indent + "REPEAT\n" + self.condition.printTree(indent+1) + "| " * indent + "UNTIL" + self.instruction.printTree(indent+1)

    @addToClass(AST.ContinueInstr)
    def printTree(self, indent=0):
		return "| " * indent + "CONTINUE\n"

    @addToClass(AST.BreakInstr)
    def printTree(self, indent=0):
		return "| " * indent + "BREAK\n"

    @addToClass(AST.CompoundInstr)
    def printTree(self, indent=0):
        ret = ''
        if self.declarations is not None:
            ret += self.declarations.printTree(indent)
        ret += self.instructions_opt.printTree(indent)
        return ret

    @addToClass(AST.CastFunction)
    def printTree(self, indent=0):
		return "| " * indent + "FUNCALL\n" + "| " * (indent + 1) + self.functionName + "\n" + self.args.printTree(indent+1)

    @addToClass(AST.ExprInBrackets)
    def printTree(self, indent=0):
		return self.expr.printTree(indent)

    @addToClass(AST.ExprList)
    def printTree(self, indent=0):
        ret = ''
        for expression in self.expressions:
            ret += expression.printTree(indent)
        return ret

    @addToClass(AST.FunctionList)
    def printTree(self, indent=0):
        ret = ''
        for function in self.functions:
            ret += function.printTree(indent)
        return ret

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        return "| " * indent + "FUNDEF\n" + "| " * (indent + 1) + self.id + "\n" + "| " * (indent + 1) + "RET " + self.type + "\n" + self.args_list_or_empty.printTree(indent+1) + self.compound_instr.printTree(indent+1)

    @addToClass(AST.Arguments)
    def printTree(self, indent=0):
        ret = ''
        for argument in self.arguments:
            ret += argument.printTree(indent)
        return ret

    @addToClass(AST.Argument)
    def printTree(self, indent=0):
		return "| " * indent + "ARG " + self.id + "\n"

    #do nowej gramatyki
    @addToClass(AST.Block)
    def printTree(self, indent=0):
        ret = ''
        if self.declarations is not None:
            ret += self.declarations.printTree(indent)
        if self.fundefs_opt is not None:
            ret += self.fundefs_opt.printTree(indent)
        if self.instructions_opt is not None:
            ret += self.instructions_opt.printTree(indent)
        return ret

    #do nowej gramatyki
    @addToClass(AST.Blocks)
    def printTree(self, indent=0):
        ret = ''
        for block in self.blocks:
            ret += block.printTree(indent)
        return ret
