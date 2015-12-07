#!/usr/bin/python

from scanner import Scanner
import AST


class Cparser(object):


    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens


    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno(1), self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")


    #do nowej gramatyki:
    def p_program(self, p):
        """program : blocks"""
        p[0] = p[1]
        print p[0]

    #do nowej gramatyki:
    def p_blocks(self, p):
        """blocks : blocks block
                  | block"""
        if len(p) != 3:
            #after |
            p[0] = AST.Blocks()
            p[0].push(p[1])
        else:
            if p[1] is None:
                p[0] = AST.Blocks()
            else:
                p[0] = p[1]
            p[0].push(p[2])

    #do nowej gramatyki:
    def p_block(self, p):
        """block : declarations fundefs_opt instructions_opt"""
        p[0] = AST.Block(p[1], p[2], p[3])


    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        if len(p) != 3:
            #after |
            p[0] = AST.Declarations()
        else:
            #put right `declarations` to left `declarations` and append `declaration`
            if p[1] is None:
                p[0] = AST.Declarations()
            else:
                p[0] = p[1]
            p[0].push(p[2])


    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        if len(p) == 4:
            type = p[1]
            inits = p[2]
            p[0] = AST.Declaration(type, inits, p.lineno(1))

    #variable initialization
    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 4:
            p[0] = p[1]
            p[0].push(p[3])
        else:
            p[0] = AST.Inits()
            p[0].push(p[1])


    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = AST.Init(p[1], p[3], p.lineno(1))


    def p_instructions_opt(self, p):
        """instructions_opt : instructions
                            | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = None


    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        #almost same as declarations
        if len(p) != 3:
            #after |
            p[0] = AST.Instructions()
            p[0].push(p[1])
        else:
            if p[1] is None:
                p[0] = Instructions()
            else:
                p[0] = p[1]
            p[0].push(p[2])


    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        p[0] = p[1] #bo zamieniamy instruction na cos po prawej

    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """
        expr = p[2]
        p[0] = AST.PrintInstr(expr, p.lineno(1))

    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        id = p[1]
        instr = p[3]
        p[0] = AST.LabeledInstr(id, instr)

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        id = p[1]
        expr = p[3]
        p[0] = AST.AssignmentInstr(id, expr, p.lineno(1))

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        condition = p[3]
        instruction = p[5]
        if len(p) >= 8:
            else_instr = p[7]
        else:
            else_instr = None
        p[0] = AST.ChoiceInstr(condition, instruction, else_instr, p.lineno(1) )

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        condition = p[3]
        instruction = p[5]
        p[0] = AST.WhileInstr(condition, instruction)


    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        condition = p[2]
        instruction = p[4]
        p[0] = AST.RepeatInstr(condition, instruction)

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        expr = p[2]
        p[0] = AST.ReturnInstr(expr, p.lineno(1))

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstr(p.lineno(1))

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstr(p.lineno(1))

    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions_opt '}' """
        if len(p[2].declarations) != 0:
            p[0] = AST.CompoundInstr(p[2], p[3], p.lineno(1))
        else:
            p[0] = AST.CompoundInstr(None, p[3], p.lineno(1))

    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]

    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        p[0] = p[1]

    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')'"""
        #typ 0 - const i ID
        #typ 1 - wszystkie te `expression` cos `expression`
        #typ 2 - to w nawiasach
        #typ 3 - to z ID na poczatku
        if len(p) == 2:
            p[0] = AST.Const(p[1], p.lineno(1))
        elif p[1] != "(" and p[2] == "(": #lapiemy 3 typ czyli wywolanie funkcji
            functionName = p[1]
            args = p[3]
            p[0] = AST.CastFunction(functionName, args, p.lineno(1))
        elif p[1] == "(": #2 typ
            p[0] = AST.ExprInBrackets(p[2])
        else: #1 typ
            p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(1))


    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) != 1:
            p[0] = p[1]
        else:
            p[0] = None


    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) != 4:
            p[0] = AST.ExprList()
            p[0].push(p[1])
        else:
            p[0] = AST.ExprList() if p[1] is None else p[1]
            p[0].push(p[3])

    def p_fundefs_opt(self, p):
        """fundefs_opt : fundefs
                       | """
        if len(p) > 1:
            p[0] = p[1]
        else:
            p[0] = None

    def p_fundefs(self, p):
        """fundefs : fundefs fundef
                   | fundef """
        if len(p) == 3:
            p[0] = p[1]
            p[0].push(p[2])
        else:
            p[0] = AST.FunctionList()
            p[0].push(p[1])

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = AST.Function(p[1], p[2], p[4], p[6], p.lineno(1))

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 1:
            p[0] = None
        else:
            p[0] = p[1]

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        if len(p) == 4:
            if p[1] is None:
                p[0] = AST.Arguments()
            else:
                p[0] = p[1]
            p[0].push(p[3])
        else:
            p[0] = AST.Arguments()
            p[0].push(p[1])

    def p_arg(self, p):
        """arg : TYPE ID """
        type = p[1]
        id = p[2]
        p[0] = AST.Argument(type, id, p.lineno(1))
