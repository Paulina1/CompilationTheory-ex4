from collections import defaultdict
import AST
from SymbolTab import SymbolTable, FunctionSymbol, VariableSymbol
import re


ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

ttype['*']['string']['int'] = 'string'

ttype['&']['int']['int'] = 'int'
ttype['^']['int']['int'] = 'int'
ttype['|']['int']['int'] = 'int'
ttype['AND']['int']['int'] = 'int'
ttype['OR']['int']['int'] = 'int'
ttype['SHL']['int']['int'] = 'int'
ttype['SHR']['int']['int'] = 'int'

ttype['+']['float']['int'] = 'float'
ttype['+']['int']['float'] = 'float'
ttype['+']['float']['float'] = 'float'
ttype['+']['int']['int'] = 'int'
ttype['-']['float']['int'] = 'float'
ttype['-']['int']['float'] = 'float'
ttype['-']['float']['float'] = 'float'
ttype['-']['int']['int'] = 'int'
ttype['*']['float']['int'] = 'float'
ttype['*']['int']['float'] = 'float'
ttype['*']['float']['float'] = 'float'
ttype['*']['int']['int'] = 'int'
ttype['/']['float']['int'] = 'float'
ttype['/']['int']['float'] = 'float'
ttype['/']['float']['float'] = 'float'
ttype['/']['int']['int'] = 'int'

ttype['>']['int']['int'] = 'int'
ttype['<']['int']['int'] = 'int'
ttype['LE']['int']['int'] = 'int'
ttype['GE']['int']['int'] = 'int'
ttype['EQ']['int']['int'] = 'int'
ttype['==']['int']['int'] = 'int'
ttype['NEQ']['int']['int'] = 'int'
ttype['>=']['int']['int'] = 'int'
ttype['<=']['int']['int'] = 'int'
ttype['!=']['int']['int'] = 'int'
ttype['%']['int']['int'] = 'int'

ttype['>']['int']['float'] = 'int'
ttype['<']['int']['float'] = 'int'
ttype['LE']['int']['float'] = 'int'
ttype['GE']['int']['float'] = 'int'
ttype['EQ']['int']['float'] = 'int'
ttype['==']['int']['float'] = 'int'
ttype['NEQ']['int']['float'] = 'int'
ttype['>=']['int']['float'] = 'int'
ttype['<=']['int']['float'] = 'int'
ttype['!=']['int']['float'] = 'int'
ttype['>']['float']['int'] = 'int'
ttype['<']['float']['int'] = 'int'
ttype['LE']['float']['int'] = 'int'
ttype['GE']['float']['int'] = 'int'
ttype['EQ']['float']['int'] = 'int'
ttype['==']['float']['int'] = 'int'
ttype['NEQ']['float']['int'] = 'int'
ttype['>=']['float']['int'] = 'int'
ttype['>=']['float']['int'] = 'int'
ttype['!=']['float']['int'] = 'int'
ttype['>']['float']['float'] = 'int'
ttype['<']['float']['float'] = 'int'
ttype['LE']['float']['float'] = 'int'
ttype['GE']['float']['float'] = 'int'
ttype['EQ']['float']['float'] = 'int'
ttype['==']['float']['float'] = 'int'
ttype['NEQ']['float']['float'] = 'int'
ttype['>=']['float']['float'] = 'int'
ttype['<=']['float']['float'] = 'int'
ttype['!=']['float']['float'] = 'int'

ttype['+']['string']['string'] = 'string'

ttype['>']['string']['string'] = 'int'
ttype['<']['string']['string'] = 'int'
ttype['>=']['string']['string'] = 'int'
ttype['<=']['string']['string'] = 'int'
ttype['==']['string']['string'] = 'int'
ttype['!=']['string']['string'] = 'int'
ttype['LE']['string']['string'] = 'int'
ttype['GE']['string']['string'] = 'int'
ttype['EQ']['string']['string'] = 'int'
ttype['NEQ']['string']['string'] = 'int'




class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            array = []
            for elem in node:
                array.append(self.visit(elem))
            return array
        else:
            if node is not None:
                array = []
                for child in node.children():
                    if isinstance(child, list):
                        for item in child:
                            if isinstance(item, AST.Node):
                                array.append(self.visit(item))
                    elif isinstance(child, AST.Node):
                        array.append(self.visit(child))

                return array


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.scope = SymbolTable(None, 'main')

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        if ttype[node.op][type1][type2] is None:
            print "Bad expression {} in line {}".format(node.op, node.line)
        return ttype[node.op][type1][type2]

    def visit_Const(self, node):
        if re.match(r"(\+|-){0,1}(\d+\.\d+|\.\d+)", node.val):
            return self.visit_Float(node)
        elif re.match(r"(\+|-){0,1}\d+", node.val):
            return self.visit_Integer(node)
        elif re.match(r"\A('.*'|\".*\")\Z", node.val):
            return self.visit_String(node)
        else:
            variable = self.scope.get(node.val)
            if variable is None:
                print "Variable {} in line {} hasn't been declared".format(node.val, node.line)
            else:
                return variable.type


    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self,node):
        return 'float'

    def visit_String(self,node):
        return 'string'

    def visit_Declaration(self, node):
        visited_inits = self.visit(node.inits)
        if visited_inits is not None:
            for curr in self.visit(node.inits):
                if self.scope.get(curr[0]) is not None:
                    print "Variable {} in line {} has been declared earlier".format(curr[0], node.line)
                else:
                    if node.type == curr[1] or (node.type == 'float' and curr[1] == 'int'):
                        self.scope.put(curr[0], VariableSymbol(curr[0], node.type))
                    elif node.type == 'int' and curr[1] == 'float':
                        print "Warning! You lost float precision in line {}".format(node.line)
                        self.scope.put(curr[0], VariableSymbol(curr[0], node.type))
                    else:
                        print "Type mismatch in line {}".format(node.line)

    def visit_ReturnInstr(self, node):
        if not isinstance(self.scope.get(self.scope.name), FunctionSymbol):
            print "Return outside function in line {}".format(node.line)
        if self.scope.parent.get(self.scope.name) is not None:
            if self.scope.parent.get(self.scope.name).type == 'int' and self.visit(node.expr) == 'float':
                print "Warning! You lost float precision in line {}".format(node.line)
            elif not (self.scope.parent.get(self.scope.name).type == self.visit(node.expr) or (self.scope.parent.get(self.scope.name).type == 'float' and self.visit(node.expr)=='int')):
                print "Type mismatch in line {}".format(node.line)

    def visit_PrintInstr(self, node):
        self.visit(node.expr)

    def visit_Init(self, node):
        return (node.id, self.visit(node.expr))

    def visit_AssignmentInstr(self, node):
        type = self.visit(node.expr)
        var_from_scope = self.scope.get(node.id)
        if var_from_scope is None:
            print "Variable {} in line {} hasn't been declared".format(node.id, node.line)
        else:
            if var_from_scope.type == 'int' and type == 'float':
                print "Warning! You lost float precision in line {}".format(node.line)
                self.scope.put(node.id, VariableSymbol(node.id, type))
            elif not (var_from_scope.type == type or (var_from_scope.type == 'float' and type=='int')):
                print "Type mismatch in line {}".format(node.line)


        return (node.id, self.visit(node.expr))

    def visit_ChoiceInstr(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)
        self.visit(node.else_instr)

    def visit_WhileInstr(self, node):
        self.visit(node.condition)
        self.scope = self.scope.pushScope("loop")
        self.visit(node.instruction)
        self.scope = self.scope.popScope()

    def visit_RepeatInstr(self, node):
        self.visit(node.condition)
        self.scope = self.scope.pushScope("loop")
        self.visit(node.instruction)
        self.scope = self.scope.popScope()

    def visit_ContinueInstr(self, node):
        if self.scope.name != "loop":
            print "Continue outside the loop in line {}".format(node.line)

    def visit_BreakInstr(self, node):
        if self.scope.name != "loop":
            print "Break outside the loop in line {}".format(node.line)

    def visit_CompoundInstr(self, node):
        self.visit(node.declarations)
        self.visit(node.instructions_opt)

    def visit_CastFunction(self, node):
        function = self.scope.get(node.functionName)
        if function is None:
            print "Function {} in line {} has not been declared".format(node.functionName, node.line)
            return
        args_cast = self.visit(node.args)
        args_scope = self.visit(function.arguments)
        if len(args_cast) != len(args_scope):
            print "Wrong numbers of arguments in line {}".format(node.line)
        else:
            for arg in args_scope:
                i = args_scope.index(arg)
                if arg[1] == 'int' and args_cast[i] == 'float':
                    print "Warning! You lost float precision in line {}".format(node.line)
                elif not (arg[1] == args_cast[i] or (arg[1] == 'float' and args_cast[i] == 'int')):
                    print "Function arguments mismatch in line {}".format(node.line)

        return function.type


    def visit_ExprInBrackets(self, node):
        return self.visit(node.expr)

    def visit_Function(self, node):
        if self.scope.get(node.id) is not None:
            print "Function {} in line {} has been declared earlier".format(node.id, node.line)
        else:
            self.scope.put(node.id, FunctionSymbol(node.id, node.type, node.args_list_or_empty))
            self.scope = self.scope.pushScope(node.id)
            self.visit(node.args_list_or_empty)
            self.visit(node.compound_instr)
            self.scope = self.scope.popScope()

    def visit_Argument(self, node):
        self.scope.put(node.id, VariableSymbol(node.id, node.type))
        return (node.id, node.type)

    def visit_Block(self, node):
        self.scope = self.scope.pushScope("block")
        self.visit(node.declarations)
        self.visit(node.fundefs_opt)
        self.visit(node.instructions_opt)
        self.scope = self.scope.popScope()
