#!/usr/bin/python -tt

from lexer import tokens

from Main import *
from LinearProgram import *
from LinearEquations import *
from LinearExpression import *
from Objectives import *
from Constraints import *
from ConstraintExpression import *
from NumericExpression import *
from SymbolicExpression import *
from ExpressionList import *
from IndexingExpression import *
from EntryIndexingExpression import *
from LogicalExpression import *
from EntryLogicalExpression import *
from SetExpression import *
from ValueList import *
from TupleList import *
from Tuple import *
from Array import *
from Range import *
from Value import *
from Identifier import *
from ID import *
from SyntaxException import *
from Declarations import *
from DeclarationExpression import *

import objects as obj

precedence = (
    ('left', 'ID'),
    ('left', 'NUMBER', 'INFINITY'),
    ('right', 'COMMA'),
    ('right', 'SLASHES', 'SEMICOLON'),
    ('right', 'FOR', 'WHERE', 'COLON'),
    ('right', 'PIPE'),
    ('right', 'DEFAULT', 'DIMEN', 'ASSIGN'),
    ('right', 'LPAREN', 'RPAREN', 'LLBRACE', 'RRBRACE', 'LBRACKET', 'RBRACKET'),
    ('right', 'LBRACE', 'RBRACE', 'UNDERLINE', 'FRAC'),
    ('left', 'MAXIMIZE', 'MINIMIZE'),
    ('right', 'IMPLIES', 'ISIMPLIEDBY', 'IFANDONLYIF'),
    ('right', 'IF', 'THEN', 'ELSE', 'ENDIF'),
    ('left', 'OR'),
    ('left', 'FORALL', 'EXISTS', 'NEXISTS'),
    ('left', 'AND'),
    ('right', 'LE', 'GE', 'LT', 'GT', 'EQ', 'NEQ'),
    ('left', 'IN', 'NOTIN'),
    ('left', 'SUBSET', 'NOTSUBSET'),
    ('left', 'NOT'),
    ('left', 'DIFF', 'SYMDIFF', 'UNION'),
    ('left', 'INTER'),
    ('left', 'CROSS'),
    ('left', 'SETOF'),
    ('right', 'DOTS', 'BY'),
    ('right', 'CONCAT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'SUM', 'PROD', 'MAX', 'MIN'),
    ('left', 'TIMES', 'DIVIDE', 'MOD', 'QUOTIENT'),
    ('left', 'UPLUS', 'UMINUS'),
    ('right', 'CARET'),
    ('left', 'LFLOOR', 'RFLOOR', 'LCEIL', 'RCEIL', 'SIN', 'ASIN', 'SINH', 'ASINH', 'COS', 'ACOS', 'COSH', 'ACOSH', 'TAN', 'ATAN', 'ATANH', 'TANH', 'SQRT', 'LN', 'LOG', 'EXP'),
    ('left', 'INTEGERSET', 'INTEGERSETPOSITIVE', 'INTEGERSETNEGATIVE', 'INTEGERSETWITHONELIMIT', 'INTEGERSETWITHTWOLIMITS', 
      'REALSET', 'REALSETPOSITIVE', 'REALSETNEGATIVE', 'REALSETWITHONELIMIT', 'REALSETWITHTWOLIMITS', 
      'NATURALSET', 'NATURALSETWITHONELIMIT', 'NATURALSETWITHTWOLIMITS', 'BINARYSET', 'SYMBOLIC', 'LOGICAL')
)

def p_Main(t):
  '''MAIN : LinearEquations'''
  t[0] = Main(t[1])

def p_LinearEquations(t):
    '''LinearEquations : ConstraintList'''
    t[0] = LinearEquations(Constraints(t[1]))

def p_Objective(t):
    '''Objective : MAXIMIZE Identifier FOR IndexingExpression
                 | MAXIMIZE Identifier WHERE IndexingExpression
                 | MAXIMIZE Identifier COLON IndexingExpression
                 | MAXIMIZE Identifier
                 | MAXIMIZE NumericSymbolicExpression FOR IndexingExpression
                 | MAXIMIZE NumericSymbolicExpression WHERE IndexingExpression
                 | MAXIMIZE NumericSymbolicExpression COLON IndexingExpression
                 | MAXIMIZE NumericSymbolicExpression
                 
                 | MINIMIZE Identifier FOR IndexingExpression
                 | MINIMIZE Identifier WHERE IndexingExpression
                 | MINIMIZE Identifier COLON IndexingExpression
                 | MINIMIZE Identifier
                 | MINIMIZE NumericSymbolicExpression WHERE IndexingExpression
                 | MINIMIZE NumericSymbolicExpression FOR IndexingExpression
                 | MINIMIZE NumericSymbolicExpression COLON IndexingExpression
                 | MINIMIZE NumericSymbolicExpression'''

    _type = t.slice[1].type

    if len(t) > 3:
        t[4].setStmtIndexing(True)

        obj = Objective.MINIMIZE
        
        if _type == "MAXIMIZE":
            obj = Objective.MAXIMIZE

        t[0] = Objective(t[2], obj, t[4])

    else:

        if _type == "MINIMIZE":
            t[0] = Objective(t[2])
        else:
            t[0] = Objective(t[2], Objective.MAXIMIZE)

def p_ConstraintList(t):
    '''ConstraintList : ConstraintList Objective SLASHES
                      | ConstraintList Constraint SLASHES
                      | ConstraintList Declarations SLASHES
                      
                      | ConstraintList Objective
                      | ConstraintList Constraint
                      | ConstraintList Declarations
                      
                      | Objective SLASHES
                      | Constraint SLASHES
                      | Declarations SLASHES
                      
                      | Objective
                      | Constraint
                      | Declarations'''

    if len(t) > 2 and not isinstance(t[2], str):
        t[0] = t[1] + [t[2]]

    else:
        t[0] = [t[1]]

def p_Constraint(t):
    '''Constraint : ConstraintExpression FOR IndexingExpression
                  | ConstraintExpression WHERE IndexingExpression
                  | ConstraintExpression COLON IndexingExpression
                  | ConstraintExpression

                  | LogicalExpression FOR IndexingExpression
                  | LogicalExpression WHERE IndexingExpression
                  | LogicalExpression COLON IndexingExpression
                  | LogicalExpression

                  | EntryConstraintLogicalExpression FOR IndexingExpression
                  | EntryConstraintLogicalExpression WHERE IndexingExpression
                  | EntryConstraintLogicalExpression COLON IndexingExpression

                  | ValueListInExpression FOR IndexingExpression
                  | ValueListInExpression WHERE IndexingExpression
                  | ValueListInExpression COLON IndexingExpression
                  | ValueListInExpression

                  | NumericSymbolicExpression FOR IndexingExpression
                  | NumericSymbolicExpression WHERE IndexingExpression
                  | NumericSymbolicExpression COLON IndexingExpression
                  | NumericSymbolicExpression'''

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = ValueList([t[1]])
    
    if not isinstance(t[1], ConstraintExpression) and not isinstance(t[1], LogicalExpression):
      t[1] = LogicalExpression([t[1]])

    if len(t) > 3:
        t[3].setStmtIndexing(True)
        t[0] = Constraint(t[1], t[3])
    else:
        t[0] = Constraint(t[1])


def p_ConstraintExpressionConnectorsAndIterated(t):
    '''ConstraintExpression : ConstraintExpression AND ConstraintExpression
                            | ConstraintExpression AND LogicalExpression
                            | ConstraintExpression AND ValueListInExpression

                            | LogicalExpression AND ConstraintExpression
                            | ValueListInExpression AND ConstraintExpression

                            | ConstraintExpression OR ConstraintExpression
                            | ConstraintExpression OR LogicalExpression
                            | ConstraintExpression OR ValueListInExpression

                            | LogicalExpression OR ConstraintExpression
                            | ValueListInExpression OR ConstraintExpression

                            | FORALL LLBRACE IndexingExpression RRBRACE ConstraintExpression
                            | NFORALL LLBRACE IndexingExpression RRBRACE ConstraintExpression
                            | EXISTS LLBRACE IndexingExpression RRBRACE ConstraintExpression
                            | NEXISTS LLBRACE IndexingExpression RRBRACE ConstraintExpression

                            | NOT ConstraintExpression
                            | LPAREN ConstraintExpression RPAREN'''

    if t.slice[1].type == "LPAREN":
        entry = LogicalExpression([t[2]])
        t[0] = EntryLogicalExpressionBetweenParenthesis(entry)

    elif t.slice[1].type == "NOT":
        entry = EntryLogicalExpressionNot(t[2])
        t[0] = LogicalExpression([entry])

    elif len(t) > 2 and (t.slice[2].type == "AND" or t.slice[2].type == "OR"):

        if not isinstance(t[1], LogicalExpression):
          entry = LogicalExpression([t[1]])
        else:
          entry = t[1]

        if t.slice[2].type == "AND":
          entry = entry.addAnd(t[3])
        else:
          entry = entry.addOr(t[3])

        t[0] = entry

    else:
        entry = None
        _type = t.slice[1].type
        if _type == "FORALL":
            entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.FORALL, t[3], t[5])

        elif _type == "NFORALL":
            entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NFORALL, t[3], t[5])

        elif _type == "EXISTS":
            entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.EXISTS, t[3], t[5])

        elif _type == "NEXISTS":
            entry = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NEXISTS, t[3], t[5])
        else:
            entry = t[1]

        t[0] = LogicalExpression([entry])

def p_ConstraintExpressionLogical(t):
    '''ConstraintExpression : Identifier IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | Identifier IMPLIES ConstraintExpression ELSE Identifier
                            | Identifier IMPLIES Identifier ELSE Identifier
                            | Identifier IMPLIES Identifier ELSE LogicalExpression
                            | Identifier IMPLIES Identifier ELSE ValueListInExpression
                            | Identifier IMPLIES Identifier ELSE ConstraintExpression

                            | Identifier IMPLIES ConstraintExpression ELSE LogicalExpression
                            | Identifier IMPLIES LogicalExpression ELSE Identifier
                            | Identifier IMPLIES LogicalExpression ELSE LogicalExpression
                            | Identifier IMPLIES LogicalExpression ELSE ValueListInExpression
                            | Identifier IMPLIES LogicalExpression ELSE ConstraintExpression

                            | Identifier IMPLIES ConstraintExpression ELSE ValueListInExpression
                            | Identifier IMPLIES ValueListInExpression ELSE Identifier
                            | Identifier IMPLIES ValueListInExpression ELSE LogicalExpression
                            | Identifier IMPLIES ValueListInExpression ELSE ValueListInExpression
                            | Identifier IMPLIES ValueListInExpression ELSE ConstraintExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE Identifier
                            | NumericSymbolicExpression IMPLIES Identifier ELSE Identifier
                            | NumericSymbolicExpression IMPLIES Identifier ELSE LogicalExpression
                            | NumericSymbolicExpression IMPLIES Identifier ELSE ValueListInExpression
                            | NumericSymbolicExpression IMPLIES Identifier ELSE ConstraintExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE LogicalExpression
                            | NumericSymbolicExpression IMPLIES LogicalExpression ELSE Identifier
                            | NumericSymbolicExpression IMPLIES LogicalExpression ELSE LogicalExpression
                            | NumericSymbolicExpression IMPLIES LogicalExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression IMPLIES LogicalExpression ELSE ConstraintExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression IMPLIES ValueListInExpression ELSE Identifier
                            | NumericSymbolicExpression IMPLIES ValueListInExpression ELSE LogicalExpression
                            | NumericSymbolicExpression IMPLIES ValueListInExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression IMPLIES ValueListInExpression ELSE ConstraintExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE Identifier
                            | ConstraintExpression IMPLIES Identifier ELSE Identifier
                            | ConstraintExpression IMPLIES Identifier ELSE LogicalExpression
                            | ConstraintExpression IMPLIES Identifier ELSE ValueListInExpression
                            | ConstraintExpression IMPLIES Identifier ELSE ConstraintExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE LogicalExpression
                            | ConstraintExpression IMPLIES LogicalExpression ELSE Identifier
                            | ConstraintExpression IMPLIES LogicalExpression ELSE LogicalExpression
                            | ConstraintExpression IMPLIES LogicalExpression ELSE ValueListInExpression
                            | ConstraintExpression IMPLIES LogicalExpression ELSE ConstraintExpression

                            | ConstraintExpression IMPLIES ConstraintExpression ELSE ValueListInExpression
                            | ConstraintExpression IMPLIES ValueListInExpression ELSE Identifier
                            | ConstraintExpression IMPLIES ValueListInExpression ELSE LogicalExpression
                            | ConstraintExpression IMPLIES ValueListInExpression ELSE ValueListInExpression
                            | ConstraintExpression IMPLIES ValueListInExpression ELSE ConstraintExpression

                            | LogicalExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | LogicalExpression IMPLIES ConstraintExpression ELSE Identifier
                            | LogicalExpression IMPLIES Identifier ELSE Identifier
                            | LogicalExpression IMPLIES Identifier ELSE LogicalExpression
                            | LogicalExpression IMPLIES Identifier ELSE ValueListInExpression
                            | LogicalExpression IMPLIES Identifier ELSE ConstraintExpression

                            | LogicalExpression IMPLIES ConstraintExpression ELSE LogicalExpression
                            | LogicalExpression IMPLIES LogicalExpression ELSE Identifier
                            | LogicalExpression IMPLIES LogicalExpression ELSE LogicalExpression
                            | LogicalExpression IMPLIES LogicalExpression ELSE ValueListInExpression
                            | LogicalExpression IMPLIES LogicalExpression ELSE ConstraintExpression

                            | LogicalExpression IMPLIES ConstraintExpression ELSE ValueListInExpression
                            | LogicalExpression IMPLIES ValueListInExpression ELSE Identifier
                            | LogicalExpression IMPLIES ValueListInExpression ELSE LogicalExpression
                            | LogicalExpression IMPLIES ValueListInExpression ELSE ValueListInExpression
                            | LogicalExpression IMPLIES ValueListInExpression ELSE ConstraintExpression

                            | ValueListInExpression IMPLIES ConstraintExpression ELSE ConstraintExpression

                            | ValueListInExpression IMPLIES ConstraintExpression ELSE Identifier
                            | ValueListInExpression IMPLIES Identifier ELSE Identifier
                            | ValueListInExpression IMPLIES Identifier ELSE LogicalExpression
                            | ValueListInExpression IMPLIES Identifier ELSE ValueListInExpression
                            | ValueListInExpression IMPLIES Identifier ELSE ConstraintExpression

                            | ValueListInExpression IMPLIES ConstraintExpression ELSE LogicalExpression
                            | ValueListInExpression IMPLIES LogicalExpression ELSE Identifier
                            | ValueListInExpression IMPLIES LogicalExpression ELSE LogicalExpression
                            | ValueListInExpression IMPLIES LogicalExpression ELSE ValueListInExpression
                            | ValueListInExpression IMPLIES LogicalExpression ELSE ConstraintExpression

                            | ValueListInExpression IMPLIES ConstraintExpression ELSE ValueListInExpression
                            | ValueListInExpression IMPLIES ValueListInExpression ELSE Identifier
                            | ValueListInExpression IMPLIES ValueListInExpression ELSE LogicalExpression
                            | ValueListInExpression IMPLIES ValueListInExpression ELSE ValueListInExpression
                            | ValueListInExpression IMPLIES ValueListInExpression ELSE ConstraintExpression


                            
                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE Identifier
                            | Identifier ISIMPLIEDBY Identifier ELSE Identifier
                            | Identifier ISIMPLIEDBY Identifier ELSE LogicalExpression
                            | Identifier ISIMPLIEDBY Identifier ELSE ValueListInExpression
                            | Identifier ISIMPLIEDBY Identifier ELSE ConstraintExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE LogicalExpression
                            | Identifier ISIMPLIEDBY LogicalExpression ELSE Identifier
                            | Identifier ISIMPLIEDBY LogicalExpression ELSE LogicalExpression
                            | Identifier ISIMPLIEDBY LogicalExpression ELSE ValueListInExpression
                            | Identifier ISIMPLIEDBY LogicalExpression ELSE ConstraintExpression

                            | Identifier ISIMPLIEDBY ConstraintExpression ELSE ValueListInExpression
                            | Identifier ISIMPLIEDBY ValueListInExpression ELSE Identifier
                            | Identifier ISIMPLIEDBY ValueListInExpression ELSE LogicalExpression
                            | Identifier ISIMPLIEDBY ValueListInExpression ELSE ValueListInExpression
                            | Identifier ISIMPLIEDBY ValueListInExpression ELSE ConstraintExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier ELSE Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier ELSE LogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier ELSE ValueListInExpression
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier ELSE ConstraintExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE LogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY LogicalExpression ELSE Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY LogicalExpression ELSE LogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY LogicalExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression ISIMPLIEDBY LogicalExpression ELSE ConstraintExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression ELSE Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression ELSE LogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression ELSE ValueListInExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression ELSE ConstraintExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE Identifier
                            | ConstraintExpression ISIMPLIEDBY Identifier ELSE Identifier
                            | ConstraintExpression ISIMPLIEDBY Identifier ELSE LogicalExpression
                            | ConstraintExpression ISIMPLIEDBY Identifier ELSE ValueListInExpression
                            | ConstraintExpression ISIMPLIEDBY Identifier ELSE ConstraintExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE LogicalExpression
                            | ConstraintExpression ISIMPLIEDBY LogicalExpression ELSE Identifier
                            | ConstraintExpression ISIMPLIEDBY LogicalExpression ELSE LogicalExpression
                            | ConstraintExpression ISIMPLIEDBY LogicalExpression ELSE ValueListInExpression
                            | ConstraintExpression ISIMPLIEDBY LogicalExpression ELSE ConstraintExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression ELSE ValueListInExpression
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression ELSE Identifier
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression ELSE LogicalExpression
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression ELSE ValueListInExpression
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression ELSE ConstraintExpression
                            | LogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | LogicalExpression ISIMPLIEDBY ConstraintExpression ELSE Identifier
                            | LogicalExpression ISIMPLIEDBY Identifier ELSE Identifier
                            | LogicalExpression ISIMPLIEDBY Identifier ELSE LogicalExpression
                            | LogicalExpression ISIMPLIEDBY Identifier ELSE ValueListInExpression
                            | LogicalExpression ISIMPLIEDBY Identifier ELSE ConstraintExpression

                            | LogicalExpression ISIMPLIEDBY ConstraintExpression ELSE LogicalExpression
                            | LogicalExpression ISIMPLIEDBY LogicalExpression ELSE Identifier
                            | LogicalExpression ISIMPLIEDBY LogicalExpression ELSE LogicalExpression
                            | LogicalExpression ISIMPLIEDBY LogicalExpression ELSE ValueListInExpression
                            | LogicalExpression ISIMPLIEDBY LogicalExpression ELSE ConstraintExpression

                            | LogicalExpression ISIMPLIEDBY ConstraintExpression ELSE ValueListInExpression
                            | LogicalExpression ISIMPLIEDBY ValueListInExpression ELSE Identifier
                            | LogicalExpression ISIMPLIEDBY ValueListInExpression ELSE LogicalExpression
                            | LogicalExpression ISIMPLIEDBY ValueListInExpression ELSE ValueListInExpression
                            | LogicalExpression ISIMPLIEDBY ValueListInExpression ELSE ConstraintExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression ELSE ConstraintExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression ELSE Identifier
                            | ValueListInExpression ISIMPLIEDBY Identifier ELSE Identifier
                            | ValueListInExpression ISIMPLIEDBY Identifier ELSE LogicalExpression
                            | ValueListInExpression ISIMPLIEDBY Identifier ELSE ValueListInExpression
                            | ValueListInExpression ISIMPLIEDBY Identifier ELSE ConstraintExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression ELSE LogicalExpression
                            | ValueListInExpression ISIMPLIEDBY LogicalExpression ELSE Identifier
                            | ValueListInExpression ISIMPLIEDBY LogicalExpression ELSE LogicalExpression
                            | ValueListInExpression ISIMPLIEDBY LogicalExpression ELSE ValueListInExpression
                            | ValueListInExpression ISIMPLIEDBY LogicalExpression ELSE ConstraintExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression ELSE ValueListInExpression
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression ELSE Identifier
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression ELSE LogicalExpression
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression ELSE ValueListInExpression
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression ELSE ConstraintExpression



                            | Identifier IMPLIES ConstraintExpression
                            | Identifier IMPLIES Identifier
                            | Identifier IMPLIES LogicalExpression
                            | Identifier IMPLIES ValueListInExpression

                            | NumericSymbolicExpression IMPLIES ConstraintExpression
                            | NumericSymbolicExpression IMPLIES Identifier
                            | NumericSymbolicExpression IMPLIES LogicalExpression
                            | NumericSymbolicExpression IMPLIES ValueListInExpression

                            | ConstraintExpression IMPLIES ConstraintExpression
                            | ConstraintExpression IMPLIES Identifier
                            | ConstraintExpression IMPLIES LogicalExpression
                            | ConstraintExpression IMPLIES ValueListInExpression

                            | LogicalExpression IMPLIES ConstraintExpression
                            | LogicalExpression IMPLIES Identifier
                            | LogicalExpression IMPLIES LogicalExpression
                            | LogicalExpression IMPLIES ValueListInExpression

                            | ValueListInExpression IMPLIES ConstraintExpression
                            | ValueListInExpression IMPLIES Identifier
                            | ValueListInExpression IMPLIES LogicalExpression
                            | ValueListInExpression IMPLIES ValueListInExpression



                            | Identifier ISIMPLIEDBY ConstraintExpression
                            | Identifier ISIMPLIEDBY Identifier
                            | Identifier ISIMPLIEDBY LogicalExpression
                            | Identifier ISIMPLIEDBY ValueListInExpression

                            | NumericSymbolicExpression ISIMPLIEDBY ConstraintExpression
                            | NumericSymbolicExpression ISIMPLIEDBY Identifier
                            | NumericSymbolicExpression ISIMPLIEDBY LogicalExpression
                            | NumericSymbolicExpression ISIMPLIEDBY ValueListInExpression

                            | ConstraintExpression ISIMPLIEDBY ConstraintExpression
                            | ConstraintExpression ISIMPLIEDBY Identifier
                            | ConstraintExpression ISIMPLIEDBY LogicalExpression
                            | ConstraintExpression ISIMPLIEDBY ValueListInExpression

                            | LogicalExpression ISIMPLIEDBY ConstraintExpression
                            | LogicalExpression ISIMPLIEDBY Identifier
                            | LogicalExpression ISIMPLIEDBY LogicalExpression
                            | LogicalExpression ISIMPLIEDBY ValueListInExpression

                            | ValueListInExpression ISIMPLIEDBY ConstraintExpression
                            | ValueListInExpression ISIMPLIEDBY Identifier
                            | ValueListInExpression ISIMPLIEDBY LogicalExpression
                            | ValueListInExpression ISIMPLIEDBY ValueListInExpression



                            | Identifier IFANDONLYIF ConstraintExpression
                            | Identifier IFANDONLYIF Identifier
                            | Identifier IFANDONLYIF LogicalExpression
                            | Identifier IFANDONLYIF ValueListInExpression

                            | NumericSymbolicExpression IFANDONLYIF ConstraintExpression
                            | NumericSymbolicExpression IFANDONLYIF Identifier
                            | NumericSymbolicExpression IFANDONLYIF LogicalExpression
                            | NumericSymbolicExpression IFANDONLYIF ValueListInExpression

                            | ConstraintExpression IFANDONLYIF ConstraintExpression
                            | ConstraintExpression IFANDONLYIF Identifier
                            | ConstraintExpression IFANDONLYIF LogicalExpression
                            | ConstraintExpression IFANDONLYIF ValueListInExpression

                            | LogicalExpression IFANDONLYIF ConstraintExpression
                            | LogicalExpression IFANDONLYIF Identifier
                            | LogicalExpression IFANDONLYIF LogicalExpression
                            | LogicalExpression IFANDONLYIF ValueListInExpression

                            | ValueListInExpression IFANDONLYIF ConstraintExpression
                            | ValueListInExpression IFANDONLYIF Identifier
                            | ValueListInExpression IFANDONLYIF LogicalExpression
                            | ValueListInExpression IFANDONLYIF ValueListInExpression'''

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = EntryLogicalExpressionNumericOrSymbolic(t[1])

    if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
      t[3] = EntryLogicalExpressionNumericOrSymbolic(t[3])

    if len(t) > 5 and (isinstance(t[5], NumericExpression) or isinstance(t[5], SymbolicExpression) or isinstance(t[5], Identifier)):
      t[5] = EntryLogicalExpressionNumericOrSymbolic(t[5])

    if not isinstance(t[1], LogicalExpression):
      t[1] = LogicalExpression([t[1]])

    _type = t.slice[2].type

    if _type == "IMPLIES":
      op = LogicalConstraintExpression.IMPLIES
    elif _type == "ISIMPLIEDBY":
      op = LogicalConstraintExpression.ISIMPLIEDBY
    elif _type == "IFANDONLYIF":
      op = LogicalConstraintExpression.IFANDONLYIF

    if len(t) > 4:
      t[0] = LogicalConstraintExpression(op, t[1], t[3], t[5])
    else:
      t[0] = LogicalConstraintExpression(op, t[1], t[3])

def p_ConstraintExpression(t):
    '''ConstraintExpression : Identifier LE Identifier LE Identifier
                            | Identifier LE Identifier LE NumericSymbolicExpression
                            | Identifier LE NumericSymbolicExpression LE Identifier
                            | Identifier LE NumericSymbolicExpression LE NumericSymbolicExpression
                            
                            | Identifier GE Identifier GE Identifier
                            | Identifier GE Identifier GE NumericSymbolicExpression
                            | Identifier GE NumericSymbolicExpression GE Identifier
                            | Identifier GE NumericSymbolicExpression GE NumericSymbolicExpression
                            | NumericSymbolicExpression LE Identifier LE Identifier
                            | NumericSymbolicExpression LE Identifier LE NumericSymbolicExpression
                            | NumericSymbolicExpression LE NumericSymbolicExpression LE Identifier
                            | NumericSymbolicExpression LE NumericSymbolicExpression LE NumericSymbolicExpression
                            
                            | NumericSymbolicExpression GE Identifier GE Identifier
                            | NumericSymbolicExpression GE Identifier GE NumericSymbolicExpression
                            | NumericSymbolicExpression GE NumericSymbolicExpression GE Identifier
                            | NumericSymbolicExpression GE NumericSymbolicExpression GE NumericSymbolicExpression'''

    if len(t) > 4:
        if t.slice[4].type == "LE":
            t[0] = ConstraintExpression3(t[3], t[1], t[5], ConstraintExpression.LE)

        elif t.slice[4].type == "GE":
            t[0] = ConstraintExpression3(t[3], t[1], t[5], ConstraintExpression.GE)

    elif t.slice[2].type == "EQ":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.EQ)

    elif t.slice[2].type == "LE":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.LE)

    elif t.slice[2].type == "GE":
        t[0] = ConstraintExpression2(t[1], t[3], ConstraintExpression.GE)

def p_ConditionalConstraintExpression(t):
    '''ConstraintExpression : IF LogicalExpression THEN ConstraintExpression ELSE ConstraintExpression ENDIF
                            | IF LogicalExpression THEN ConstraintExpression ELSE LogicalExpression ENDIF
                            | IF LogicalExpression THEN ConstraintExpression ELSE ValueListInExpression ENDIF
                            | IF LogicalExpression THEN ConstraintExpression ELSE Identifier ENDIF

                            | IF LogicalExpression THEN LogicalExpression ELSE ConstraintExpression ENDIF
                            | IF LogicalExpression THEN LogicalExpression ELSE LogicalExpression ENDIF
                            | IF LogicalExpression THEN LogicalExpression ELSE ValueListInExpression ENDIF
                            | IF LogicalExpression THEN LogicalExpression ELSE Identifier ENDIF

                            | IF LogicalExpression THEN ValueListInExpression ELSE ConstraintExpression ENDIF
                            | IF LogicalExpression THEN ValueListInExpression ELSE LogicalExpression ENDIF
                            | IF LogicalExpression THEN ValueListInExpression ELSE ValueListInExpression ENDIF
                            | IF LogicalExpression THEN ValueListInExpression ELSE Identifier ENDIF

                            | IF LogicalExpression THEN Identifier ELSE ConstraintExpression ENDIF
                            | IF LogicalExpression THEN Identifier ELSE LogicalExpression ENDIF
                            | IF LogicalExpression THEN Identifier ELSE ValueListInExpression ENDIF
  


                            | IF ValueListInExpression THEN ConstraintExpression ELSE ConstraintExpression ENDIF
                            | IF ValueListInExpression THEN ConstraintExpression ELSE LogicalExpression ENDIF
                            | IF ValueListInExpression THEN ConstraintExpression ELSE ValueListInExpression ENDIF
                            | IF ValueListInExpression THEN ConstraintExpression ELSE Identifier ENDIF

                            | IF ValueListInExpression THEN LogicalExpression ELSE ConstraintExpression ENDIF
                            | IF ValueListInExpression THEN LogicalExpression ELSE LogicalExpression ENDIF
                            | IF ValueListInExpression THEN LogicalExpression ELSE ValueListInExpression ENDIF
                            | IF ValueListInExpression THEN LogicalExpression ELSE Identifier ENDIF

                            | IF ValueListInExpression THEN ValueListInExpression ELSE ConstraintExpression ENDIF
                            | IF ValueListInExpression THEN ValueListInExpression ELSE LogicalExpression ENDIF
                            | IF ValueListInExpression THEN ValueListInExpression ELSE ValueListInExpression ENDIF
                            | IF ValueListInExpression THEN ValueListInExpression ELSE Identifier ENDIF

                            | IF ValueListInExpression THEN Identifier ELSE ConstraintExpression ENDIF
                            | IF ValueListInExpression THEN Identifier ELSE LogicalExpression ENDIF
                            | IF ValueListInExpression THEN Identifier ELSE ValueListInExpression ENDIF



                            | IF Identifier THEN ConstraintExpression ELSE ConstraintExpression ENDIF
                            | IF Identifier THEN ConstraintExpression ELSE LogicalExpression ENDIF
                            | IF Identifier THEN ConstraintExpression ELSE ValueListInExpression ENDIF
                            | IF Identifier THEN ConstraintExpression ELSE Identifier ENDIF

                            | IF Identifier THEN LogicalExpression ELSE ConstraintExpression ENDIF
                            | IF Identifier THEN LogicalExpression ELSE LogicalExpression ENDIF
                            | IF Identifier THEN LogicalExpression ELSE ValueListInExpression ENDIF
                            | IF Identifier THEN LogicalExpression ELSE Identifier ENDIF

                            | IF Identifier THEN ValueListInExpression ELSE ConstraintExpression ENDIF
                            | IF Identifier THEN ValueListInExpression ELSE LogicalExpression ENDIF
                            | IF Identifier THEN ValueListInExpression ELSE ValueListInExpression ENDIF
                            | IF Identifier THEN ValueListInExpression ELSE Identifier ENDIF

                            | IF Identifier THEN Identifier ELSE ConstraintExpression ENDIF
                            | IF Identifier THEN Identifier ELSE LogicalExpression ENDIF
                            | IF Identifier THEN Identifier ELSE ValueListInExpression ENDIF



                            | IF NumericSymbolicExpression THEN ConstraintExpression ELSE ConstraintExpression ENDIF
                            | IF NumericSymbolicExpression THEN ConstraintExpression ELSE LogicalExpression ENDIF
                            | IF NumericSymbolicExpression THEN ConstraintExpression ELSE ValueListInExpression ENDIF
                            | IF NumericSymbolicExpression THEN ConstraintExpression ELSE Identifier ENDIF

                            | IF NumericSymbolicExpression THEN LogicalExpression ELSE ConstraintExpression ENDIF
                            | IF NumericSymbolicExpression THEN LogicalExpression ELSE LogicalExpression ENDIF
                            | IF NumericSymbolicExpression THEN LogicalExpression ELSE ValueListInExpression ENDIF
                            | IF NumericSymbolicExpression THEN LogicalExpression ELSE Identifier ENDIF

                            | IF NumericSymbolicExpression THEN ValueListInExpression ELSE ConstraintExpression ENDIF
                            | IF NumericSymbolicExpression THEN ValueListInExpression ELSE LogicalExpression ENDIF
                            | IF NumericSymbolicExpression THEN ValueListInExpression ELSE ValueListInExpression ENDIF
                            | IF NumericSymbolicExpression THEN ValueListInExpression ELSE Identifier ENDIF

                            | IF NumericSymbolicExpression THEN Identifier ELSE ConstraintExpression ENDIF
                            | IF NumericSymbolicExpression THEN Identifier ELSE LogicalExpression ENDIF
                            | IF NumericSymbolicExpression THEN Identifier ELSE ValueListInExpression ENDIF'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if not isinstance(t[2], LogicalExpression):
      t[2] = LogicalExpression([t[2]])
      
    if isinstance(t[4], Identifier):
      t[4] = LogicalExpression([EntryLogicalExpressionNumericOrSymbolic(t[4])])

    if isinstance(t[6], Identifier):
      t[6] = LogicalExpression([EntryLogicalExpressionNumericOrSymbolic(t[6])])

    t[0] = ConditionalConstraintExpression(t[2], t[4])
    t[0].addElseExpression(t[6])

def p_EntryConstraintLogicalExpression(t):
    '''EntryConstraintLogicalExpression : NumericSymbolicExpression LE NumericSymbolicExpression
                                        | NumericSymbolicExpression LE Identifier
                                        | NumericSymbolicExpression EQ NumericSymbolicExpression
                                        | NumericSymbolicExpression EQ Identifier
                                        | NumericSymbolicExpression GE NumericSymbolicExpression
                                        | NumericSymbolicExpression GE Identifier

                                        | Identifier LE NumericSymbolicExpression
                                        | Identifier LE Identifier
                                        | Identifier EQ SetExpression
                                        | Identifier EQ Array
                                        | Identifier EQ NumericSymbolicExpression
                                        | Identifier EQ Identifier
                                        | Identifier GE NumericSymbolicExpression
                                        | Identifier GE Identifier

                                        | NumericSymbolicExpression LT NumericSymbolicExpression
                                        | NumericSymbolicExpression LT Identifier
                                        | NumericSymbolicExpression GT NumericSymbolicExpression
                                        | NumericSymbolicExpression GT Identifier
                                        | NumericSymbolicExpression NEQ NumericSymbolicExpression
                                        | NumericSymbolicExpression NEQ Identifier

                                        | Identifier LT NumericSymbolicExpression
                                        | Identifier LT Identifier
                                        | Identifier GT NumericSymbolicExpression
                                        | Identifier GT Identifier
                                        | Identifier NEQ NumericSymbolicExpression
                                        | Identifier NEQ Identifier

                                        | NumericSymbolicExpression IN SetExpression
                                        | NumericSymbolicExpression IN Identifier
                                        | NumericSymbolicExpression SUBSET SetExpression
                                        | NumericSymbolicExpression SUBSET Identifier

                                        | Identifier IN SetExpression
                                        | Identifier IN Identifier
                                        | Identifier SUBSET SetExpression
                                        | Identifier SUBSET Identifier'''

    _type = t.slice[1].type
    if _type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    elif _type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    else:

      _type = t.slice[2].type
      if _type == "LE":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.LE, t[1], t[3])

      elif _type == "EQ":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.EQ, t[1], t[3])

      elif _type == "GE":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.GE, t[1], t[3])

      elif _type == "LT":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.LT, t[1], t[3])

      elif _type == "GT":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.GT, t[1], t[3])

      elif _type == "NEQ":
          t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.NEQ, t[1], t[3])

      elif _type == "IN":
        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

        t[0] = EntryLogicalExpressionWithSet(EntryLogicalExpressionWithSet.IN, t[1], t[3])

      elif _type == "SUBSET":
        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

        if t.slice[2].type == "SUBSET" and not isinstance(t[1], SetExpression):
          t[1] = SetExpressionWithValue(t[1])

        t[0] = EntryLogicalExpressionWithSetOperation(EntryLogicalExpressionWithSetOperation.SUBSET, t[1], t[3])


def _getDeclarationExpression(entryConstraintLogicalExpression):

    attr = None
    numNot = 0
    putNot = False

    while isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionBetweenParenthesis) or \
          isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionNot):

          if isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionNot):
            numNot += 1

          entryConstraintLogicalExpression = entryConstraintLogicalExpression.logicalExpression

    # discard not expressions because it is not allowed in declaration attributes
    if numNot % 2 != 0:
      putNot = True

    op = entryConstraintLogicalExpression.op

    if isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionRelational):
      expr1 = entryConstraintLogicalExpression.numericExpression1
      expr2 = entryConstraintLogicalExpression.numericExpression2

    elif isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionWithSet):
      expr1 = entryConstraintLogicalExpression.identifier
      expr2 = entryConstraintLogicalExpression.setExpression

    elif isinstance(entryConstraintLogicalExpression, EntryLogicalExpressionWithSetOperation):
      expr1 = entryConstraintLogicalExpression.setExpression1
      expr2 = entryConstraintLogicalExpression.setExpression2

    if putNot:
      expr2 = EntryLogicalExpressionNot(expr2)

    if op == EntryLogicalExpressionWithSet.IN:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.IN)

    if op == EntryLogicalExpressionWithSetOperation.SUBSET:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.WT)

    elif op == EntryLogicalExpressionRelational.LT:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.LT)

    elif op == EntryLogicalExpressionRelational.GT:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.GT)

    elif op == EntryLogicalExpressionRelational.NEQ:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.NEQ)

    if op == EntryLogicalExpressionRelational.LE:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.LE)

    elif op == EntryLogicalExpressionRelational.GE:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.GE)

    elif op == EntryLogicalExpressionRelational.EQ:
      attr = DeclarationAttribute(expr2, DeclarationAttribute.EQ)

    if not isinstance(expr1, ValueList):
      entryConstraintLogicalExpression = ValueList([expr1])

    else:
      entryConstraintLogicalExpression = expr1

    declarationExpression = DeclarationExpression(entryConstraintLogicalExpression)
    declarationExpression.addAttribute(attr)

    return declarationExpression


def p_Declarations(t):
  '''Declarations : DeclarationList'''

  i = 1
  length = len(t[1])
  lastDecl = t[1][length-i]
  while (not lastDecl or lastDecl.indexingExpression == None) and i < length:
    i += 1
    lastDecl = t[1][length-i]
  
  if lastDecl and lastDecl.indexingExpression != None:
    for i in range(length-i):
      decl = t[1][i]
      if decl.indexingExpression == None:
        decl.setIndexingExpression(lastDecl.indexingExpression)

  t[0] = Declarations(t[1])

def p_DeclarationList(t):
    '''DeclarationList : DeclarationList SEMICOLON Declaration
                       | DeclarationList SEMICOLON ValueListInExpression
                       | DeclarationList SEMICOLON EntryConstraintLogicalExpression

                       | DeclarationList SEMICOLON ValueListInExpression FOR IndexingExpression
                       | DeclarationList SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | DeclarationList SEMICOLON ValueListInExpression COLON IndexingExpression

                       | DeclarationList SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | DeclarationList SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | DeclarationList SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | ValueListInExpression SEMICOLON Declaration
                       | ValueListInExpression SEMICOLON ValueListInExpression
                       | ValueListInExpression SEMICOLON EntryConstraintLogicalExpression

                       | ValueListInExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | ValueListInExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | ValueListInExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | ValueListInExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | ValueListInExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | ValueListInExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | ValueListInExpression FOR IndexingExpression SEMICOLON Declaration
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON Declaration
                       | ValueListInExpression COLON IndexingExpression SEMICOLON Declaration
                        
                       | ValueListInExpression FOR IndexingExpression SEMICOLON ValueListInExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON ValueListInExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON ValueListInExpression

                       | ValueListInExpression FOR IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | ValueListInExpression FOR IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | ValueListInExpression FOR IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | ValueListInExpression WHERE IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | ValueListInExpression COLON IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | ValueListInExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression

                       | ValueListInExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | ValueListInExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | ValueListInExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | ValueListInExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | ValueListInExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | ValueListInExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | ValueListInExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression SEMICOLON Declaration
                       | EntryConstraintLogicalExpression SEMICOLON ValueListInExpression
                       | EntryConstraintLogicalExpression SEMICOLON EntryConstraintLogicalExpression

                       | EntryConstraintLogicalExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON Declaration
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON Declaration
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON Declaration

                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON ValueListInExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON ValueListInExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON ValueListInExpression

                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON ValueListInExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON ValueListInExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON ValueListInExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression

                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression FOR IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression WHERE IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression FOR IndexingExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression WHERE IndexingExpression
                       | EntryConstraintLogicalExpression COLON IndexingExpression SEMICOLON EntryConstraintLogicalExpression COLON IndexingExpression

                       | Declaration'''

    if len(t) > 7:

      t[3].setStmtIndexing(True)

      if isinstance(t[1], EntryLogicalExpression):
        declaration = _getDeclarationExpression(t[1])
        t[1] = Declaration(declaration, t[3]) # turn into Declaration
        t[1] = [t[1]] # turn into DeclarationList


      t[7].setStmtIndexing(True)

      if isinstance(t[5], EntryLogicalExpression):
        declaration = _getDeclarationExpression(t[5])
        t[5] = Declaration(declaration, t[7]) # turn into Declaration

      t[0] = t[1] + [t[5]]

    elif len(t) > 5:

      if t.slice[2].type == "SEMICOLON":

        t[5].setStmtIndexing(True)

        if isinstance(t[1], EntryLogicalExpression):
          declaration = _getDeclarationExpression(t[1])
          t[1] = Declaration(declaration) # turn into Declaration
          t[1] = [t[1]] # turn into DeclarationList

        if isinstance(t[3], EntryLogicalExpression):
          declaration = _getDeclarationExpression(t[3])
          t[3] = Declaration(declaration, t[5]) # turn into Declaration

        t[0] = t[1] + [t[3]]

      else:

        t[3].setStmtIndexing(True)

        if isinstance(t[1], EntryLogicalExpression):
          declaration = _getDeclarationExpression(t[1])
          t[1] = Declaration(declaration, t[3]) # turn into Declaration
          t[1] = [t[1]] # turn into DeclarationList

        if isinstance(t[5], EntryLogicalExpression):
          declaration = _getDeclarationExpression(t[5])
          t[5] = Declaration(declaration) # turn into Declaration

        t[0] = t[1] + [t[5]]

    elif len(t) > 3:

      if isinstance(t[1], EntryLogicalExpression):
        declaration = _getDeclarationExpression(t[1])
        t[1] = Declaration(declaration) # turn into Declaration
        t[1] = [t[1]] # turn into DeclarationList

      if isinstance(t[3], EntryLogicalExpression):
        declaration = _getDeclarationExpression(t[3])
        t[3] = Declaration(declaration) # turn into Declaration

      t[0] = t[1] + [t[3]]

    else:
      t[0] = [t[1]]

def p_Declaration(t):
    '''Declaration : DeclarationExpression FOR IndexingExpression
                   | DeclarationExpression WHERE IndexingExpression
                   | DeclarationExpression COLON IndexingExpression
                   
                   | ValueList FOR IndexingExpression
                   | ValueList WHERE IndexingExpression
                   | ValueList COLON IndexingExpression
                   
                   | Identifier FOR IndexingExpression
                   | Identifier WHERE IndexingExpression
                   | Identifier COLON IndexingExpression
                   
                   | DeclarationExpression'''

    if isinstance(t[1], EntryLogicalExpression):
      t[1] = _getDeclarationExpression(t[1])

    if len(t) > 3:
        t[3].setStmtIndexing(True)

        if isinstance(t[1], ValueList):
          t[1] = DeclarationExpression(t[1], [])

        elif isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
          t[1] = DeclarationExpression(ValueList([t[1]]), [])

        t[0] = Declaration(t[1], t[3])

    else:
        t[0] = Declaration(t[1])

def p_DeclarationExpression(t):
    '''DeclarationExpression : ValueList SUBSET SetExpression
                             | ValueList SUBSET Identifier
                             | ValueList DEFAULT SetExpression
                             | ValueList DEFAULT Identifier
                             | ValueList DEFAULT NumericSymbolicExpression
                             | ValueList DIMEN Identifier
                             | ValueList DIMEN NumericSymbolicExpression
                             | ValueList ASSIGN SetExpression
                             | ValueList ASSIGN Array
                             | ValueList ASSIGN Identifier
                             | ValueList ASSIGN NumericSymbolicExpression
                             | ValueList LE Identifier
                             | ValueList LE NumericSymbolicExpression
                             | ValueList GE Identifier
                             | ValueList GE NumericSymbolicExpression
                             | ValueList EQ SetExpression
                             | ValueList EQ Array
                             | ValueList EQ Identifier
                             | ValueList EQ NumericSymbolicExpression
                             | ValueList LT Identifier
                             | ValueList LT NumericSymbolicExpression
                             | ValueList GT Identifier
                             | ValueList GT NumericSymbolicExpression
                             | ValueList NEQ Identifier
                             | ValueList NEQ NumericSymbolicExpression
                             | ValueList COMMA DeclarationAttributeList

                             | NumericSymbolicExpression DEFAULT SetExpression
                             | NumericSymbolicExpression DEFAULT Identifier
                             | NumericSymbolicExpression DEFAULT NumericSymbolicExpression
                             | NumericSymbolicExpression DIMEN Identifier
                             | NumericSymbolicExpression DIMEN NumericSymbolicExpression
                             | NumericSymbolicExpression ASSIGN SetExpression
                             | NumericSymbolicExpression ASSIGN Array
                             | NumericSymbolicExpression ASSIGN Identifier
                             | NumericSymbolicExpression ASSIGN NumericSymbolicExpression
                             | NumericSymbolicExpression COMMA DeclarationAttributeList

                             | Identifier DEFAULT SetExpression
                             | Identifier DEFAULT Identifier
                             | Identifier DEFAULT NumericSymbolicExpression
                             | Identifier DIMEN Identifier
                             | Identifier DIMEN NumericSymbolicExpression
                             | Identifier ASSIGN SetExpression
                             | Identifier ASSIGN Array
                             | Identifier ASSIGN Identifier
                             | Identifier ASSIGN NumericSymbolicExpression
                             | Identifier COMMA DeclarationAttributeList

                             | EntryConstraintLogicalExpression COMMA DeclarationAttributeList
                             | ValueListInExpression COMMA DeclarationAttributeList
                             | DeclarationExpression COMMA DeclarationAttributeList'''

    
    if isinstance(t[1], DeclarationExpression):
      if t.slice[2].type == "COMMA":
        t[1].addAttribute(t[3])
      else:
        t[1].addAttribute(t[2])

      t[0] = t[1]

    elif t.slice[1].type == "ValueListInExpression" or t.slice[1].type == "EntryConstraintLogicalExpression":
      t[0] = _getDeclarationExpression(t[1])
      t[0].addAttribute(t[3])

    else:
      _type = t.slice[2].type

      attr = None
      if _type == "COMMA":
        attr = t[3]

      elif _type == "IN":
        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

        attr = DeclarationAttribute(t[3], DeclarationAttribute.IN)

      elif _type == "SUBSET":
        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

        attr = DeclarationAttribute(t[3], DeclarationAttribute.WT)

      elif _type == "DEFAULT":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.DF)

      elif _type == "DIMEN":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.DM)

      elif _type == "ASSIGN":
        if isinstance(t[3], Range):
          t[3] = SetExpressionWithValue(t[3])

        attr = DeclarationAttribute(t[3], DeclarationAttribute.ST)

      elif _type == "LT":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.LT)

      elif _type == "GT":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.GT)

      elif _type == "NEQ":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.NEQ)

      elif _type == "LE":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.LE)

      elif _type == "GE":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.GE)

      elif _type == "EQ":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.EQ)


      if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
        t[1] = ValueList([t[1]])

      t[0] = DeclarationExpression(t[1])
      t[0].addAttribute(attr)

def p_DeclarationAttributeList(t):
  '''DeclarationAttributeList : DeclarationAttributeList COMMA DeclarationAttribute
                              | DeclarationAttribute'''
  if len(t) > 3:
    t[0] = t[1] + [t[3]]
  else:
    t[0] = [t[1]]

def p_DeclarationAttribute(t):
  '''DeclarationAttribute : IN SetExpression
                          | IN Identifier
                          
                          | SUBSET SetExpression
                          | SUBSET Identifier
                          
                          | DEFAULT SetExpression
                          | DEFAULT Identifier
                          | DEFAULT NumericSymbolicExpression
                          
                          | DIMEN Identifier
                          | DIMEN NumericSymbolicExpression
                          
                          | ASSIGN SetExpression
                          | ASSIGN Array
                          | ASSIGN Identifier
                          | ASSIGN NumericSymbolicExpression
                          
                          | LT Identifier
                          | LT NumericSymbolicExpression
                          
                          | LE Identifier
                          | LE NumericSymbolicExpression
                          
                          | EQ SetExpression
                          | EQ Array
                          | EQ Identifier
                          | EQ NumericSymbolicExpression
                          
                          | GT Identifier
                          | GT NumericSymbolicExpression
                          
                          | GE Identifier
                          | GE NumericSymbolicExpression
                          
                          | NEQ Identifier
                          | NEQ NumericSymbolicExpression'''

  _type = t.slice[1].type
  if _type == "IN":
    if not isinstance(t[2], SetExpression):
      t[2] = SetExpressionWithValue(t[2])    

    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.IN)

  elif _type == "SUBSET":
    if not isinstance(t[2], SetExpression):
      t[2] = SetExpressionWithValue(t[2])    

    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.WT)

  elif _type == "DEFAULT":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.DF)

  elif _type == "DIMEN":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.DM)

  elif _type == "ASSIGN":
    if isinstance(t[2], Range):
      t[2] = SetExpressionWithValue(t[2])

    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.ST)

  elif _type == "LT":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.LT)

  elif _type == "LE":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.LE)

  elif _type == "GT":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.GT)

  elif _type == "GE":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.GE)

  elif _type == "NEQ":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.NEQ)

  elif _type == "EQ":
    t[0] = DeclarationAttribute(t[2], DeclarationAttribute.EQ)


def p_ValueListInExpression(t):
    '''ValueListInExpression : ValueList IN SetExpression
                             | ValueList IN Identifier

                             | LPAREN ValueListInExpression RPAREN
                             | NOT ValueListInExpression'''

    if t.slice[1].type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    elif t.slice[1].type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    else:

      if not isinstance(t[3], SetExpression):
        t[3] = SetExpressionWithValue(t[3])

      t[0] = EntryLogicalExpressionWithSet(EntryLogicalExpressionWithSet.IN, t[1], t[3])


def p_LogicalExpression(t):
    '''LogicalExpression : EntryLogicalExpression

                         | EntryConstraintLogicalExpression

                         | LogicalExpression OR LogicalExpression
                         | LogicalExpression OR ValueListInExpression
                         | LogicalExpression OR NumericSymbolicExpression
                         | LogicalExpression OR Identifier

                         | ValueListInExpression OR LogicalExpression
                         | ValueListInExpression OR ValueListInExpression
                         | ValueListInExpression OR NumericSymbolicExpression
                         | ValueListInExpression OR Identifier

                         | NumericSymbolicExpression OR LogicalExpression
                         | NumericSymbolicExpression OR ValueListInExpression
                         | NumericSymbolicExpression OR NumericSymbolicExpression
                         | NumericSymbolicExpression OR Identifier

                         | Identifier OR LogicalExpression
                         | Identifier OR ValueListInExpression
                         | Identifier OR NumericSymbolicExpression
                         | Identifier OR Identifier

                         | LogicalExpression AND LogicalExpression
                         | LogicalExpression AND ValueListInExpression
                         | LogicalExpression AND NumericSymbolicExpression
                         | LogicalExpression AND Identifier

                         | ValueListInExpression AND LogicalExpression
                         | ValueListInExpression AND ValueListInExpression
                         | ValueListInExpression AND NumericSymbolicExpression
                         | ValueListInExpression AND Identifier

                         | NumericSymbolicExpression AND LogicalExpression
                         | NumericSymbolicExpression AND ValueListInExpression
                         | NumericSymbolicExpression AND NumericSymbolicExpression
                         | NumericSymbolicExpression AND Identifier

                         | Identifier AND LogicalExpression
                         | Identifier AND ValueListInExpression
                         | Identifier AND NumericSymbolicExpression
                         | Identifier AND Identifier'''

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = EntryLogicalExpressionNumericOrSymbolic(t[1])

    if not isinstance(t[1], LogicalExpression):
      t[1] = LogicalExpression([t[1]])

    if len(t) > 3:
      if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
        t[3] = EntryLogicalExpressionNumericOrSymbolic(t[3])

      if t.slice[2].type == "AND":
        t[0] = t[1].addAnd(t[3])
      else:
        t[0] = t[1].addOr(t[3])

    else:
        t[0] = t[1]

def p_EntryLogicalExpression(t):
    '''EntryLogicalExpression : NOT LogicalExpression
                              | NOT NumericSymbolicExpression
                              | NOT Identifier
                              | LPAREN LogicalExpression RPAREN'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    _type = t.slice[1].type
    if _type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    elif _type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    else:
      t[0] = t[2]


def p_EntryLogicalExpressionWithSet(t):
    '''EntryLogicalExpression : ValueList NOTIN SetExpression
                              | ValueList NOTIN Identifier
                              
                              | Tuple IN SetExpression
                              | Tuple IN Identifier
                              | Tuple NOTIN SetExpression
                              | Tuple NOTIN Identifier

                              | NumericSymbolicExpression NOTIN SetExpression
                              | NumericSymbolicExpression NOTIN Identifier

                              | Identifier NOTIN SetExpression
                              | Identifier NOTIN Identifier
                              | Identifier NOTSUBSET SetExpression
                              | Identifier NOTSUBSET Identifier

                              | SetExpression SUBSET SetExpression
                              | SetExpression SUBSET Identifier
                              | SetExpression NOTSUBSET SetExpression
                              | SetExpression NOTSUBSET Identifier'''

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    if (t.slice[2].type == "SUBSET" or t.slice[2].type == "NOTSUBSET") and not isinstance(t[1], SetExpression):
      t[1] = SetExpressionWithValue(t[1])

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = ValueList([t[1]])

    _type = t.slice[2].type
    if _type == "IN":
        t[0] = EntryLogicalExpressionWithSet(EntryLogicalExpressionWithSet.IN, t[1], t[3])

    elif _type == "NOTIN":
        t[0] = EntryLogicalExpressionWithSet(EntryLogicalExpressionWithSet.NOTIN, t[1], t[3])

    elif _type == "SUBSET":
        t[0] = EntryLogicalExpressionWithSetOperation(EntryLogicalExpressionWithSetOperation.SUBSET, t[1], t[3])

    elif _type == "NOTSUBSET":
        t[0] = EntryLogicalExpressionWithSetOperation(EntryLogicalExpressionWithSetOperation.NOTSUBSET, t[1], t[3])


def p_EntryIteratedLogicalExpression(t):
    '''EntryLogicalExpression : FORALL LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | FORALL LLBRACE IndexingExpression RRBRACE ValueListInExpression
                              | FORALL LLBRACE IndexingExpression RRBRACE Identifier
                              | FORALL LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE ValueListInExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE Identifier
                              | NFORALL LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE ValueListInExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE Identifier
                              | EXISTS LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE ValueListInExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE Identifier
                              | NEXISTS LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression'''

    if isinstance(t[5], Identifier) or isinstance(t[5], NumericExpression) or isinstance(t[5], SymbolicExpression):
      t[5] = EntryLogicalExpressionNumericOrSymbolic(t[5])

    if not isinstance(t[5], LogicalExpression):
      t[5] = LogicalExpression([t[5]])

    _type = t.slice[1].type
    if _type == "FORALL":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.FORALL, t[3], t[5])

    elif _type == "NFORALL":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NFORALL, t[3], t[5])

    elif _type == "EXISTS":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.EXISTS, t[3], t[5])

    elif _type == "NEXISTS":
        t[0] = EntryLogicalExpressionIterated(EntryLogicalExpressionIterated.NEXISTS, t[3], t[5])

def p_SetExpressionWithOperation(t):
    '''SetExpression : SetExpression DIFF SetExpression
                     | SetExpression DIFF Identifier
                     | SetExpression SYMDIFF SetExpression
                     | SetExpression SYMDIFF Identifier
                     | SetExpression UNION SetExpression
                     | SetExpression UNION Identifier
                     | SetExpression INTER SetExpression
                     | SetExpression INTER Identifier
                     | SetExpression CROSS SetExpression
                     | SetExpression CROSS Identifier
                     
                     | Identifier DIFF SetExpression
                     | Identifier DIFF Identifier
                     | Identifier SYMDIFF SetExpression
                     | Identifier SYMDIFF Identifier
                     | Identifier UNION SetExpression
                     | Identifier UNION Identifier
                     | Identifier INTER SetExpression
                     | Identifier INTER Identifier
                     | Identifier CROSS SetExpression
                     | Identifier CROSS Identifier'''

    _type = t.slice[2].type
    if _type == "DIFF":
        op = SetExpressionWithOperation.DIFF

    elif _type == "SYMDIFF":
        op = SetExpressionWithOperation.SYMDIFF

    elif _type == "UNION":
        op = SetExpressionWithOperation.UNION

    elif _type == "INTER":
        op = SetExpressionWithOperation.INTER

    elif _type == "CROSS":
        op = SetExpressionWithOperation.CROSS

    if not isinstance(t[1], SetExpression):
      t[1] = SetExpressionWithValue(t[1])

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    t[0] = SetExpressionWithOperation(op, t[1], t[3])

def p_SetExpressionWithValue(t):
    '''SetExpression : LLBRACE ValueList RRBRACE
                     | LLBRACE TupleList RRBRACE
                     | LLBRACE SetExpression RRBRACE
                     | LLBRACE Identifier RRBRACE
                     | LLBRACE NumericSymbolicExpression RRBRACE
                     | LLBRACE IndexingExpression RRBRACE
                     | LLBRACE RRBRACE

                     | LPAREN SetExpression RPAREN

                     | Range
                     | EMPTYSET
                     | NATURALSET
                     | NATURALSETWITHONELIMIT
                     | NATURALSETWITHTWOLIMITS
                     | INTEGERSET
                     | INTEGERSETPOSITIVE
                     | INTEGERSETNEGATIVE
                     | INTEGERSETWITHONELIMIT
                     | INTEGERSETWITHTWOLIMITS
                     | REALSET
                     | REALSETPOSITIVE
                     | REALSETNEGATIVE
                     | REALSETWITHONELIMIT
                     | REALSETWITHTWOLIMITS
                     | BINARYSET
                     | SYMBOLIC
                     | LOGICAL

                     | PARAMETERS
                     | SETS
                     | VARIABLES

                     | ConditionalSetExpression'''

    _type = t.slice[1].type
    if len(t) > 2:

        if isinstance(t[1], str) and _type == "LLBRACE":

          if not (isinstance(t[2], str) and t.slice[2].type == "RRBRACE"):
            if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
              t[2] = ValueList([t[2]])

            if not isinstance(t[2], SetExpression):
              t[2] = SetExpressionWithValue(t[2])

            t[0] = SetExpressionBetweenBraces(t[2])

          else:
            t[0] = SetExpressionBetweenBraces(None)

        elif _type == "LPAREN":
          t[0] = SetExpressionBetweenParenthesis(t[2])

    elif _type == "EMPTYSET":
        t[0] = SetExpressionBetweenBraces(None)

    else:

        if t.slice[1].type == "ConditionalSetExpression":
          t[0] = t[1]

        else:
          value = t[1]
          if hasattr(t.slice[1], 'value2'):
            value = t.slice[1].value2
          
          t[0] = SetExpressionWithValue(value)


def p_SetExpressionWithIndices(t):
    '''SetExpression : Identifier Array'''

    t[0] = SetExpressionWithIndices(t[1], t[2].value)

def p_IteratedSetExpression(t):
    '''SetExpression : SETOF LLBRACE IndexingExpression RRBRACE TupleListItem
                     | SETOF LLBRACE IndexingExpression RRBRACE Identifier
                     | SETOF LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression
                     | SETOF TupleListItem
                     | SETOF Identifier
                     | SETOF NumericSymbolicExpression
                     | SETOF INTEGERSET'''
    
    if len(t) > 3:
      t[0] = IteratedSetExpression(t[3], t[5])
    else:

      if t.slice[2].type == "INTEGERSET":
        t[2] = SetExpressionWithValue(t.slice[2].value2)

      t[0] = IteratedSetExpression(None, t[2])

def p_ConditionalSetExpression(t):
    '''ConditionalSetExpression : IF LogicalExpression THEN SetExpression ELSE SetExpression ENDIF
                                | IF LogicalExpression THEN SetExpression ELSE Identifier ENDIF
                                | IF LogicalExpression THEN Identifier ELSE SetExpression ENDIF
                                | IF LogicalExpression THEN SetExpression ENDIF

                                | IF ValueListInExpression THEN SetExpression ELSE SetExpression ENDIF
                                | IF ValueListInExpression THEN SetExpression ELSE Identifier ENDIF
                                | IF ValueListInExpression THEN Identifier ELSE SetExpression ENDIF
                                | IF ValueListInExpression THEN SetExpression ENDIF

                                | IF Identifier THEN SetExpression ELSE SetExpression ENDIF
                                | IF Identifier THEN SetExpression ELSE Identifier ENDIF
                                | IF Identifier THEN Identifier ELSE SetExpression ENDIF
                                | IF Identifier THEN SetExpression ENDIF

                                | IF NumericSymbolicExpression THEN SetExpression ELSE SetExpression ENDIF
                                | IF NumericSymbolicExpression THEN SetExpression ELSE Identifier ENDIF
                                | IF NumericSymbolicExpression THEN Identifier ELSE SetExpression ENDIF
                                | IF NumericSymbolicExpression THEN SetExpression ENDIF'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if not isinstance(t[2], LogicalExpression):
      t[2] = LogicalExpression([t[2]])
    
    if isinstance(t[4], Identifier):
      t[4] = SetExpressionWithValue(t[4])

    if len(t) > 5 and isinstance(t[6], Identifier):
      t[6] = SetExpressionWithValue(t[6])

    t[0] = ConditionalSetExpression(t[2], t[4])

    if len(t) > 5:
      t[0].addElseExpression(t[6])

def p_ExpressionList(t):
    '''ExpressionList : Identifier PIPE LogicalExpression
                      | Identifier PIPE ValueListInExpression
                      | Identifier PIPE Identifier
                      | Identifier PIPE NumericSymbolicExpression

                      | NumericSymbolicExpression PIPE LogicalExpression
                      | NumericSymbolicExpression PIPE ValueListInExpression
                      | NumericSymbolicExpression PIPE Identifier
                      | NumericSymbolicExpression PIPE NumericSymbolicExpression'''

    t[1] = ExpressionList([t[1]])

    if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
      t[3] = EntryLogicalExpressionNumericOrSymbolic(t[3])

    if not isinstance(t[3], LogicalExpression):
      t[3] = LogicalExpression([t[3]])

    t[0] = t[1].setLogicalExpression(t[3])



def p_IndexingExpression(t):
    '''IndexingExpression : EntryIndexingExpression
                          | LogicalIndexExpression

                          | IndexingExpression PIPE LogicalExpression
                          | IndexingExpression PIPE ValueListInExpression
                          | IndexingExpression PIPE Identifier
                          | IndexingExpression PIPE NumericSymbolicExpression

                          | IndexingExpression COMMA EntryIndexingExpression'''

    if len(t) > 3:

        if t.slice[2].type == "PIPE":

            if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
              t[1] = EntryLogicalExpressionNumericOrSymbolic(t[1])
              t[1] = LogicalExpression([t[1]])
              t[1] = IndexingExpression([t[1]])

            if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
              t[3] = EntryLogicalExpressionNumericOrSymbolic(t[3])

            if not isinstance(t[3], LogicalExpression):
              t[3] = LogicalExpression([t[3]])

            t[0] = t[1].setLogicalExpression(t[3])

        else:
            t[0] = t[1].add(t[3])

    else:
        t[0] = IndexingExpression([t[1]])

def p_LogicalIndexExpression(t):
    '''LogicalIndexExpression : IF LogicalExpression
                              | IF ValueListInExpression
                              | IF Identifier
                              | IF NumericSymbolicExpression'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if not isinstance(t[2], LogicalExpression):
      t[2] = LogicalExpression([t[2]])

    t[0] = ConditionalLinearExpression(t[2])

def p_EntryIndexingExpressionWithSet(t):
    '''EntryIndexingExpression : ValueList IN SetExpression
                               | ValueList IN Identifier
                               
                               | Tuple IN SetExpression
                               | Tuple IN Identifier
                               
                               | Identifier IN SetExpression
                               | Identifier IN Identifier
                               
                               | NumericSymbolicExpression IN SetExpression
                               | NumericSymbolicExpression IN Identifier'''

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    if isinstance(t[1], NumericExpression) or isinstance(t[1], SymbolicExpression) or isinstance(t[1], Identifier):
      t[1] = ValueList([t[1]])

    t[0] = EntryIndexingExpressionWithSet(t[1], t[3])

def p_NumericSymbolicExpression(t):
    '''NumericSymbolicExpression : NumericExpression
                                 | SymbolicExpression
                                 | LPAREN NumericSymbolicExpression RPAREN'''

    if len(t) > 2:
        t[0] = NumericExpressionBetweenParenthesis(t[2])

    else:
        t[0] = t[1]


def p_StringSymbolicExpression(t):
    '''SymbolicExpression : STRING'''
    t[0] = StringSymbolicExpression(t[1])

def p_SymbolicExpression_binop(t):
    '''SymbolicExpression : Identifier CONCAT Identifier
                          | Identifier CONCAT NumericSymbolicExpression
                          
                          | NumericSymbolicExpression CONCAT Identifier
                          | NumericSymbolicExpression CONCAT NumericSymbolicExpression'''

    if t.slice[2].type == "CONCAT":
        op = SymbolicExpressionWithOperation.CONCAT

    t[0] = SymbolicExpressionWithOperation(op, t[1], t[3])


def p_NumericExpression_binop(t):
    '''NumericExpression : Identifier PLUS Identifier
                         | Identifier PLUS NumericSymbolicExpression
                         | Identifier PLUS LPAREN LogicalExpression RPAREN
                         | Identifier MINUS Identifier
                         | Identifier MINUS NumericSymbolicExpression
                         | Identifier MINUS LPAREN LogicalExpression RPAREN
                         | Identifier TIMES Identifier
                         | Identifier TIMES NumericSymbolicExpression
                         | Identifier TIMES LPAREN LogicalExpression RPAREN
                         | Identifier DIVIDE Identifier
                         | Identifier DIVIDE NumericSymbolicExpression
                         | Identifier DIVIDE LPAREN LogicalExpression RPAREN
                         | Identifier MOD Identifier
                         | Identifier MOD NumericSymbolicExpression
                         | Identifier MOD LPAREN LogicalExpression RPAREN
                         | Identifier QUOTIENT Identifier
                         | Identifier QUOTIENT NumericSymbolicExpression
                         | Identifier QUOTIENT LPAREN LogicalExpression RPAREN
                         | Identifier CARET LBRACE Identifier RBRACE
                         | Identifier CARET LBRACE NumericSymbolicExpression RBRACE
                         | Identifier CARET LBRACE LogicalExpression RBRACE
                         
                         | NumericSymbolicExpression PLUS Identifier
                         | NumericSymbolicExpression PLUS NumericSymbolicExpression
                         | NumericSymbolicExpression PLUS LPAREN LogicalExpression RPAREN
                         | NumericSymbolicExpression MINUS Identifier
                         | NumericSymbolicExpression MINUS NumericSymbolicExpression
                         | NumericSymbolicExpression MINUS LPAREN LogicalExpression RPAREN
                         | NumericSymbolicExpression TIMES Identifier
                         | NumericSymbolicExpression TIMES NumericSymbolicExpression
                         | NumericSymbolicExpression TIMES LPAREN LogicalExpression RPAREN
                         | NumericSymbolicExpression DIVIDE Identifier
                         | NumericSymbolicExpression DIVIDE NumericSymbolicExpression
                         | NumericSymbolicExpression DIVIDE LPAREN LogicalExpression RPAREN
                         | NumericSymbolicExpression MOD Identifier
                         | NumericSymbolicExpression MOD NumericSymbolicExpression
                         | NumericSymbolicExpression MOD LPAREN LogicalExpression RPAREN
                         | NumericSymbolicExpression QUOTIENT Identifier
                         | NumericSymbolicExpression QUOTIENT NumericSymbolicExpression
                         | NumericSymbolicExpression QUOTIENT LPAREN LogicalExpression RPAREN
                         | NumericSymbolicExpression CARET LBRACE Identifier RBRACE
                         | NumericSymbolicExpression CARET LBRACE NumericSymbolicExpression RBRACE
                         | NumericSymbolicExpression CARET LBRACE LogicalExpression RBRACE

                         | LPAREN LogicalExpression RPAREN PLUS Identifier
                         | LPAREN LogicalExpression RPAREN PLUS NumericSymbolicExpression
                         | LPAREN LogicalExpression RPAREN PLUS LPAREN LogicalExpression RPAREN
                         | LPAREN LogicalExpression RPAREN MINUS Identifier
                         | LPAREN LogicalExpression RPAREN MINUS NumericSymbolicExpression
                         | LPAREN LogicalExpression RPAREN MINUS LPAREN LogicalExpression RPAREN
                         | LPAREN LogicalExpression RPAREN TIMES Identifier
                         | LPAREN LogicalExpression RPAREN TIMES NumericSymbolicExpression
                         | LPAREN LogicalExpression RPAREN TIMES LPAREN LogicalExpression RPAREN
                         | LPAREN LogicalExpression RPAREN DIVIDE Identifier
                         | LPAREN LogicalExpression RPAREN DIVIDE NumericSymbolicExpression
                         | LPAREN LogicalExpression RPAREN DIVIDE LPAREN LogicalExpression RPAREN
                         | LPAREN LogicalExpression RPAREN MOD Identifier
                         | LPAREN LogicalExpression RPAREN MOD NumericSymbolicExpression
                         | LPAREN LogicalExpression RPAREN MOD LPAREN LogicalExpression RPAREN
                         | LPAREN LogicalExpression RPAREN QUOTIENT Identifier
                         | LPAREN LogicalExpression RPAREN QUOTIENT NumericSymbolicExpression
                         | LPAREN LogicalExpression RPAREN QUOTIENT LPAREN LogicalExpression RPAREN
                         | LPAREN LogicalExpression RPAREN CARET LBRACE Identifier RBRACE
                         | LPAREN LogicalExpression RPAREN CARET LBRACE NumericSymbolicExpression RBRACE
                         | LPAREN LogicalExpression RPAREN CARET LBRACE LogicalExpression RBRACE'''

    if t.slice[1].type == "LPAREN":

      _type = t.slice[4].type
      if _type == "PLUS":
          op = NumericExpressionWithArithmeticOperation.PLUS

      elif _type == "MINUS":
          op = NumericExpressionWithArithmeticOperation.MINUS

      elif _type == "TIMES":
          op = NumericExpressionWithArithmeticOperation.TIMES

      elif _type == "QUOTIENT":
          op = NumericExpressionWithArithmeticOperation.QUOT

      elif _type == "DIVIDE":
          op = NumericExpressionWithArithmeticOperation.DIV

      elif _type == "MOD":
          op = NumericExpressionWithArithmeticOperation.MOD

      elif _type == "CARET":
          op = NumericExpressionWithArithmeticOperation.POW

      if len(t) > 6 and isinstance(t[6], Identifier):
        t[6] = ValuedNumericExpression(t[6])
        
      elif isinstance(t[5], Identifier):
        t[5] = ValuedNumericExpression(t[5])
        
      if isinstance(t[2], Identifier):
        t[2] = ValuedNumericExpression(t[2])

      if isinstance(t[2], LogicalExpression) and not isinstance(t[2], EntryLogicalExpressionBetweenParenthesis):
        t[2] = EntryLogicalExpressionBetweenParenthesis(t[2])

      if isinstance(t[5], LogicalExpression) and not isinstance(t[5], EntryLogicalExpressionBetweenParenthesis):
        t[5] = EntryLogicalExpressionBetweenParenthesis(t[5])

      if len(t) > 6 and isinstance(t[6], LogicalExpression) and not isinstance(t[6], EntryLogicalExpressionBetweenParenthesis):
        t[6] = EntryLogicalExpressionBetweenParenthesis(t[6])
        
      if t.slice[5].type == "LPAREN" or t.slice[5].type == "LBRACE":
        t[0] = NumericExpressionWithArithmeticOperation(op, t[2], t[6])
        
      else:
        t[0] = NumericExpressionWithArithmeticOperation(op, t[2], t[5])

    else:

      _type = t.slice[2].type
      if _type == "PLUS":
          op = NumericExpressionWithArithmeticOperation.PLUS

      elif _type == "MINUS":
          op = NumericExpressionWithArithmeticOperation.MINUS

      elif _type == "TIMES":
          op = NumericExpressionWithArithmeticOperation.TIMES

      elif _type == "QUOTIENT":
          op = NumericExpressionWithArithmeticOperation.QUOT

      elif _type == "DIVIDE":
          op = NumericExpressionWithArithmeticOperation.DIV

      elif _type == "MOD":
          op = NumericExpressionWithArithmeticOperation.MOD

      elif _type == "CARET":
          op = NumericExpressionWithArithmeticOperation.POW

      if len(t) > 4 and isinstance(t[4], Identifier):
        t[4] = ValuedNumericExpression(t[4])

      elif isinstance(t[3], Identifier):
        t[3] = ValuedNumericExpression(t[3])

      if isinstance(t[1], Identifier):
        t[1] = ValuedNumericExpression(t[1])

      if isinstance(t[1], LogicalExpression) and not isinstance(t[1], EntryLogicalExpressionBetweenParenthesis):
        t[1] = EntryLogicalExpressionBetweenParenthesis(t[1])

      if isinstance(t[3], LogicalExpression) and not isinstance(t[3], EntryLogicalExpressionBetweenParenthesis):
        t[3] = EntryLogicalExpressionBetweenParenthesis(t[3])

      if len(t) > 4 and isinstance(t[4], LogicalExpression) and not isinstance(t[4], EntryLogicalExpressionBetweenParenthesis):
        t[4] = EntryLogicalExpressionBetweenParenthesis(t[4])

      if t.slice[3].type == "LPAREN" or t.slice[3].type == "LBRACE":
        t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[4])

      else:
        t[0] = NumericExpressionWithArithmeticOperation(op, t[1], t[3])

def p_IteratedNumericExpression(t):
    '''NumericExpression : SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                         | SUM UNDERLINE LBRACE IndexingExpression RBRACE LPAREN LogicalExpression RPAREN
                         
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE LPAREN LogicalExpression RPAREN
                         
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE LPAREN LogicalExpression RPAREN
                         
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE LPAREN LogicalExpression RPAREN'''

    _type = t.slice[1].type
    if _type == "SUM":
        op = IteratedNumericExpression.SUM

    elif _type == "PROD":
        op = IteratedNumericExpression.PROD

    elif _type == "MAX":
        op = IteratedNumericExpression.MAX

    elif _type == "MIN":
        op = IteratedNumericExpression.MIN

    if len(t) > 9:
        if isinstance(t[8], Identifier):
          t[8] = ValuedNumericExpression(t[8])

        if isinstance(t[10], Identifier):
          t[10] = ValuedNumericExpression(t[10])

        t[0] = IteratedNumericExpression(op, t[10], t[4], t[8])

    elif len(t) > 7:
        t[0] = IteratedNumericExpression(op, t[7], t[4])

    else:
        if isinstance(t[6], Identifier):
          t[6] = ValuedNumericExpression(t[6])

        t[0] = IteratedNumericExpression(op, t[6], t[4])

def p_NumericExpression(t):
    '''NumericExpression : PLUS Identifier %prec UPLUS
                         | PLUS NumericSymbolicExpression %prec UPLUS
                         
                         | MINUS Identifier %prec UMINUS
                         | MINUS NumericSymbolicExpression %prec UMINUS
                         
                         | LPAREN Identifier RPAREN
                         
                         | ConditionalNumericExpression
                         | NUMBER
                         | INFINITY'''

    if len(t) > 2 and isinstance(t[2], Identifier):
      t[2] = ValuedNumericExpression(t[2])

    if len(t) > 3:
      t[0] = NumericExpressionBetweenParenthesis(t[2])

    elif t.slice[1].type == "PLUS":
      t[0] = t[2]

    elif t.slice[1].type == "MINUS":
      t[0] = MinusNumericExpression(t[2])

    elif isinstance(t[1], ConditionalNumericExpression):
      t[0] = t[1]

    else:
      t[0] = ValuedNumericExpression(t[1])

def p_FractionalNumericExpression(t):
    '''NumericExpression : FRAC LBRACE Identifier RBRACE LBRACE Identifier RBRACE
                         | FRAC LBRACE Identifier RBRACE LBRACE NumericSymbolicExpression RBRACE
                         | FRAC LBRACE NumericSymbolicExpression RBRACE LBRACE Identifier RBRACE
                         | FRAC LBRACE NumericSymbolicExpression RBRACE LBRACE NumericSymbolicExpression RBRACE'''

    t[0] = FractionalNumericExpression(t[3], t[6])

def p_FunctionNumericExpression(t):
    '''NumericExpression : SQRT LBRACE Identifier RBRACE
                         | SQRT LBRACE NumericSymbolicExpression RBRACE
                         
                         | LFLOOR Identifier RFLOOR
                         | LFLOOR NumericSymbolicExpression RFLOOR
                         
                         | LCEIL Identifier RCEIL
                         | LCEIL NumericSymbolicExpression RCEIL
                         
                         | PIPE Identifier PIPE
                         | PIPE NumericSymbolicExpression PIPE
                         
                         | MAX LPAREN ValueList RPAREN
                         | MAX LPAREN Identifier RPAREN
                         | MAX LPAREN NumericSymbolicExpression RPAREN
                         
                         | MIN LPAREN ValueList RPAREN
                         | MIN LPAREN Identifier RPAREN
                         | MIN LPAREN NumericSymbolicExpression RPAREN
                         
                         | SIN LPAREN Identifier RPAREN
                         | SIN LPAREN NumericSymbolicExpression RPAREN
                         
                         | COS LPAREN Identifier RPAREN
                         | COS LPAREN NumericSymbolicExpression RPAREN
                         
                         | TAN LPAREN Identifier RPAREN
                         | TAN LPAREN NumericSymbolicExpression RPAREN
                         
                         | ASIN LPAREN Identifier RPAREN
                         | ASIN LPAREN NumericSymbolicExpression RPAREN
                         
                         | ACOS LPAREN Identifier RPAREN
                         | ACOS LPAREN NumericSymbolicExpression RPAREN
                         
                         | ATAN LPAREN Identifier COMMA Identifier RPAREN
                         | ATAN LPAREN Identifier COMMA NumericSymbolicExpression RPAREN
                         | ATAN LPAREN NumericSymbolicExpression COMMA Identifier RPAREN
                         | ATAN LPAREN NumericSymbolicExpression COMMA NumericSymbolicExpression RPAREN
                         | ATAN LPAREN Identifier RPAREN
                         | ATAN LPAREN NumericSymbolicExpression RPAREN

                         | SINH LPAREN Identifier RPAREN
                         | SINH LPAREN NumericSymbolicExpression RPAREN
                         
                         | COSH LPAREN Identifier RPAREN
                         | COSH LPAREN NumericSymbolicExpression RPAREN
                         
                         | TANH LPAREN Identifier RPAREN
                         | TANH LPAREN NumericSymbolicExpression RPAREN
                         
                         | ASINH LPAREN Identifier RPAREN
                         | ASINH LPAREN NumericSymbolicExpression RPAREN
                         
                         | ACOSH LPAREN Identifier RPAREN
                         | ACOSH LPAREN NumericSymbolicExpression RPAREN
                         
                         | ATANH LPAREN Identifier RPAREN
                         | ATANH LPAREN NumericSymbolicExpression RPAREN
                         
                         | LOG LPAREN Identifier RPAREN
                         | LOG LPAREN NumericSymbolicExpression RPAREN
                         
                         | LN LPAREN Identifier RPAREN
                         | LN LPAREN NumericSymbolicExpression RPAREN
                         
                         | EXP LPAREN Identifier RPAREN
                         | EXP LPAREN NumericSymbolicExpression RPAREN

                         | CARD LPAREN SetExpression RPAREN
                         | CARD LPAREN Identifier RPAREN
                         
                         | ID LPAREN ValueList RPAREN
                         | ID LPAREN SetExpression RPAREN
                         | ID LPAREN Identifier RPAREN
                         | ID LPAREN NumericSymbolicExpression RPAREN
                         | ID LPAREN Array RPAREN
                         
                         | ID LPAREN RPAREN'''

    _type = t.slice[1].type
    if _type == "ID":
        op = ID(t[1])

    elif _type == "CARD":
        op = NumericExpressionWithFunction.CARD

        if not isinstance(t[3], SetExpression):
          t[3] = SetExpressionWithValue(t[3])

    elif _type == "SQRT":
        op = NumericExpressionWithFunction.SQRT

    elif _type == "LFLOOR":
        op = NumericExpressionWithFunction.FLOOR

    elif _type == "LCEIL":
        op = NumericExpressionWithFunction.CEIL

    elif _type == "PIPE":
        op = NumericExpressionWithFunction.ABS

    elif _type == "MAX":
        op = NumericExpressionWithFunction.MAX

    elif _type == "MIN":
        op = NumericExpressionWithFunction.MIN

    elif _type == "SIN":
        op = NumericExpressionWithFunction.SIN

    elif _type == "COS":
        op = NumericExpressionWithFunction.COS

    elif _type == "TAN":
        op = NumericExpressionWithFunction.TAN

    elif _type == "ASIN":
        op = NumericExpressionWithFunction.ASIN

    elif _type == "ACOS":
        op = NumericExpressionWithFunction.ACOS

    elif _type == "ATAN":
        op = NumericExpressionWithFunction.ATAN

    elif _type == "SINH":
        op = NumericExpressionWithFunction.SINH

    elif _type == "COSH":
        op = NumericExpressionWithFunction.COSH

    elif _type == "TANH":
        op = NumericExpressionWithFunction.TANH

    elif _type == "ASINH":
        op = NumericExpressionWithFunction.ASINH

    elif _type == "ACOSH":
        op = NumericExpressionWithFunction.ACOSH

    elif _type == "ATANH":
        op = NumericExpressionWithFunction.ATANH

    elif _type == "LOG":
        op = NumericExpressionWithFunction.LOG10

    elif _type == "LN":
        op = NumericExpressionWithFunction.LOG

    elif _type == "EXP":
        op = NumericExpressionWithFunction.EXP

    if len(t) > 5:
        t[0] = NumericExpressionWithFunction(op, t[3], t[5])

    elif len(t) > 4:
        t[0] = NumericExpressionWithFunction(op, t[3])

    else:
        if t.slice[2].type == "LPAREN":
          t[0] = NumericExpressionWithFunction(op)
        else:
          t[0] = NumericExpressionWithFunction(op, t[2])

def p_ConditionalNumericExpression(t):
    '''ConditionalNumericExpression : IF LogicalExpression THEN Identifier ELSE Identifier ENDIF
                                    | IF LogicalExpression THEN Identifier ELSE NumericSymbolicExpression ENDIF
                                    | IF LogicalExpression THEN NumericSymbolicExpression ELSE Identifier ENDIF
                                    | IF LogicalExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression ENDIF
                                    | IF LogicalExpression THEN Identifier ENDIF
                                    | IF LogicalExpression THEN NumericSymbolicExpression ENDIF

                                    | IF ValueListInExpression THEN Identifier ELSE Identifier ENDIF
                                    | IF ValueListInExpression THEN Identifier ELSE NumericSymbolicExpression ENDIF
                                    | IF ValueListInExpression THEN NumericSymbolicExpression ELSE Identifier ENDIF
                                    | IF ValueListInExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression ENDIF
                                    | IF ValueListInExpression THEN Identifier ENDIF
                                    | IF ValueListInExpression THEN NumericSymbolicExpression ENDIF

                                    | IF Identifier THEN Identifier ELSE Identifier ENDIF
                                    | IF Identifier THEN Identifier ELSE NumericSymbolicExpression ENDIF
                                    | IF Identifier THEN NumericSymbolicExpression ELSE Identifier ENDIF
                                    | IF Identifier THEN NumericSymbolicExpression ELSE NumericSymbolicExpression ENDIF
                                    | IF Identifier THEN Identifier ENDIF
                                    | IF Identifier THEN NumericSymbolicExpression ENDIF

                                    | IF NumericSymbolicExpression THEN Identifier ELSE Identifier ENDIF
                                    | IF NumericSymbolicExpression THEN Identifier ELSE NumericSymbolicExpression ENDIF
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression ELSE Identifier ENDIF
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression ENDIF
                                    | IF NumericSymbolicExpression THEN Identifier ENDIF
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression ENDIF'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if not isinstance(t[2], LogicalExpression):
      t[2] = LogicalExpression([t[2]])
    
    if isinstance(t[4], Identifier):
      t[4] = ValuedNumericExpression(t[4])

    if len(t) > 6 and isinstance(t[6], Identifier):
      t[6] = ValuedNumericExpression(t[6])

    t[0] = ConditionalNumericExpression(t[2], t[4])

    if len(t) > 6:
      t[0].addElseExpression(t[6])

def p_Range(t):
    '''Range : Identifier DOTS Identifier BY Identifier
             | Identifier DOTS Identifier BY NumericSymbolicExpression
             | Identifier DOTS NumericSymbolicExpression BY Identifier
             | Identifier DOTS NumericSymbolicExpression BY NumericSymbolicExpression
             | Identifier DOTS Identifier
             | Identifier DOTS NumericSymbolicExpression
             
             | NumericSymbolicExpression DOTS Identifier BY Identifier
             | NumericSymbolicExpression DOTS Identifier BY NumericSymbolicExpression
             | NumericSymbolicExpression DOTS NumericSymbolicExpression BY Identifier
             | NumericSymbolicExpression DOTS NumericSymbolicExpression BY NumericSymbolicExpression
             | NumericSymbolicExpression DOTS Identifier
             | NumericSymbolicExpression DOTS NumericSymbolicExpression'''

    if len(t) > 4:
      t[0] = Range(t[1], t[3], t[5])
    else:
      t[0] = Range(t[1], t[3])

def p_Identifier(t):
    '''Identifier : ID UNDERLINE LBRACE ValueList RBRACE
                  | ID UNDERLINE LBRACE Identifier RBRACE
                  | ID UNDERLINE LBRACE NumericSymbolicExpression RBRACE
                  
                  | ID Array
                  
                  | ID'''

    if len(t) > 5:

        if isinstance(t[4], ValueList):
          t[0] = Identifier(ID(t[1]), t[4].getValues())

        else:
          t[0] = Identifier(ID(t[1]), [t[4]])

    elif len(t) > 2:
        t[0] = Identifier(ID(t[1]), t[2].value.getValues())

    else:
        t[0] = Identifier(ID(t[1]))

def p_ValueList(t):
    '''ValueList : ValueList COMMA SetExpression
                 | ValueList COMMA TupleList
                 | ValueList COMMA Array
                 | ValueList COMMA Identifier
                 | ValueList COMMA NumericSymbolicExpression

                 | SetExpression COMMA SetExpression
                 | SetExpression COMMA TupleList
                 | SetExpression COMMA Array
                 | SetExpression COMMA Identifier
                 | SetExpression COMMA NumericSymbolicExpression

                 | TupleList COMMA SetExpression
                 | TupleList COMMA Array
                 | TupleList COMMA Identifier
                 | TupleList COMMA NumericSymbolicExpression

                 | Array COMMA SetExpression
                 | Array COMMA TupleList
                 | Array COMMA Array
                 | Array COMMA Identifier
                 | Array COMMA NumericSymbolicExpression
                 
                 | Identifier COMMA SetExpression
                 | Identifier COMMA TupleList
                 | Identifier COMMA Array
                 | Identifier COMMA Identifier
                 | Identifier COMMA NumericSymbolicExpression
                 
                 | NumericSymbolicExpression COMMA SetExpression
                 | NumericSymbolicExpression COMMA TupleList
                 | NumericSymbolicExpression COMMA Array
                 | NumericSymbolicExpression COMMA Identifier
                 | NumericSymbolicExpression COMMA NumericSymbolicExpression'''

    if not isinstance(t[1], ValueList):
        t[0] = ValueList([t[1],t[3]])
    else:
        t[0] = t[1].add(t[3])

def p_IdentifierList(t):
    '''IdentifierList : IdentifierList COMMA ID
                      | ID COMMA ID'''

    if not isinstance(t[1], ValueList):
        t[0] = ValueList([Identifier(ID(t[1])),Identifier(ID(t[3]))])
    else:
        t[0] = t[1].add(Identifier(ID(t[3])))

def p_Tuple(t):
    '''Tuple : LPAREN IdentifierList RPAREN'''

    t[0] = Tuple(t[2].getValues())

def p_TupleListItem(t):
    '''TupleListItem : LPAREN ValueList RPAREN
                     | Tuple'''

    if len(t) > 2:
      t[0] = Tuple(t[2].getValues())
    else:
      t[0] = t[1]


def p_TupleList(t):
    '''TupleList : TupleList COMMA TupleListItem
                 | TupleListItem'''

    if not isinstance(t[1], TupleList):
        t[0] = TupleList([t[1]])
    else:
        t[0] = t[1].add(t[3])

def p_Array(t):
  '''Array : LBRACKET ValueList RBRACKET
           | LBRACKET SetExpression RBRACKET
           | LBRACKET TupleList RBRACKET
           | LBRACKET ExpressionList RBRACKET
           | LBRACKET Array RBRACKET
           | LBRACKET Identifier RBRACKET
           | LBRACKET NumericSymbolicExpression RBRACKET
           | Array CONCAT Array
           | Identifier CONCAT Array
           | Array CONCAT Identifier'''

  if t.slice[2].type == "CONCAT":
    t[0] = ArrayWithOperation(ArrayWithOperation.CONCAT, t[1], t[3])

  else:

    if not isinstance(t[2], ValueList) and not isinstance(t[2], TupleList):
        t[2] = ValueList([t[2]])

    t[0] = Array(t[2])

def p_error(t):
  if t:
    raise SyntaxException(t.lineno, t.lexpos, t.value, t)
  else:
    raise SyntaxException("EOF")
