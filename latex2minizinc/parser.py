#!/usr/bin/python -tt

from lexer import tokens

from Main import *
from LinearProgram import *
from LinearEquations import *
from Objectives import *
from Constraints import *
from ConstraintExpression import *
from NumericExpression import *
from SymbolicExpression import *
from IndexingExpression import *
from EntryIndexingExpression import *
from LogicalExpression import *
from EntryLogicalExpression import *
from SetExpression import *
from ValueList import *
from TupleList import *
from Tuple import *
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
    #('right', 'IMPLIES', 'ISIMPLIEDBY', 'IFANDONLYIF'),
    ('right', 'IF', 'THEN', 'ELSE'),
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
    ('right', 'AMPERSAND'),
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
                  | ConstraintExpression'''
    
    if len(t) > 3:
        t[3].setStmtIndexing(True)
        t[0] = Constraint(t[1], t[3])
    else:
        t[0] = Constraint(t[1])

def p_ConstraintExpression(t):
    '''ConstraintExpression : Identifier LE Identifier LE Identifier
                            | Identifier LE Identifier LE NumericSymbolicExpression
                            | Identifier LE NumericSymbolicExpression LE Identifier
                            | Identifier LE NumericSymbolicExpression LE NumericSymbolicExpression
                            
                            | Identifier GE Identifier GE Identifier
                            | Identifier GE Identifier GE NumericSymbolicExpression
                            | Identifier GE NumericSymbolicExpression GE Identifier
                            | Identifier GE NumericSymbolicExpression GE NumericSymbolicExpression
                            
                            | Identifier EQ Identifier
                            | Identifier EQ NumericSymbolicExpression
                            
                            | Identifier LE Identifier
                            | Identifier LE NumericSymbolicExpression
                            
                            | Identifier GE Identifier
                            | Identifier GE NumericSymbolicExpression
                            
                            | NumericSymbolicExpression LE Identifier LE Identifier
                            | NumericSymbolicExpression LE Identifier LE NumericSymbolicExpression
                            | NumericSymbolicExpression LE NumericSymbolicExpression LE Identifier
                            | NumericSymbolicExpression LE NumericSymbolicExpression LE NumericSymbolicExpression
                            
                            | NumericSymbolicExpression GE Identifier GE Identifier
                            | NumericSymbolicExpression GE Identifier GE NumericSymbolicExpression
                            | NumericSymbolicExpression GE NumericSymbolicExpression GE Identifier
                            | NumericSymbolicExpression GE NumericSymbolicExpression GE NumericSymbolicExpression
                            
                            | NumericSymbolicExpression EQ Identifier
                            | NumericSymbolicExpression EQ NumericSymbolicExpression
                            
                            | NumericSymbolicExpression LE Identifier
                            | NumericSymbolicExpression LE NumericSymbolicExpression
                            
                            | NumericSymbolicExpression GE Identifier
                            | NumericSymbolicExpression GE NumericSymbolicExpression'''
    
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
                       | Declaration'''
    if len(t) > 4:
      t[0] = t[1] + [t[4]]
    elif len(t) > 3:
      if isinstance(t[3], Declaration):
        t[0] = t[1] + [t[3]]
      else:
        t[0] = t[1]
    elif len(t) > 2:
      t[0] = t[1]
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
                   
                   | NumericSymbolicExpression FOR IndexingExpression
                   | NumericSymbolicExpression WHERE IndexingExpression
                   | NumericSymbolicExpression COLON IndexingExpression
                   
                   | DeclarationExpression'''

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
    '''DeclarationExpression : ValueList IN SetExpression
                             | ValueList IN Identifier
                             | ValueList SUBSET Identifier
                             | ValueList SUBSET SetExpression
                             | ValueList DEFAULT SetExpression
                             | ValueList DEFAULT Identifier
                             | ValueList DEFAULT NumericSymbolicExpression
                             | ValueList DIMEN Identifier
                             | ValueList DIMEN NumericSymbolicExpression
                             | ValueList ASSIGN SetExpression
                             | ValueList ASSIGN Identifier
                             | ValueList ASSIGN NumericSymbolicExpression
                             | ValueList LT Identifier
                             | ValueList LT NumericSymbolicExpression
                             | ValueList GT Identifier
                             | ValueList GT NumericSymbolicExpression
                             | ValueList NEQ Identifier
                             | ValueList NEQ NumericSymbolicExpression
                             
                             | Identifier IN SetExpression
                             | Identifier IN Identifier
                             | Identifier SUBSET SetExpression
                             | Identifier SUBSET Identifier
                             | Identifier DEFAULT SetExpression
                             | Identifier DEFAULT Identifier
                             | Identifier DEFAULT NumericSymbolicExpression
                             | Identifier DIMEN Identifier
                             | Identifier DIMEN NumericSymbolicExpression
                             | Identifier ASSIGN SetExpression
                             | Identifier ASSIGN Identifier
                             | Identifier ASSIGN NumericSymbolicExpression
                             | Identifier LT Identifier
                             | Identifier LT NumericSymbolicExpression
                             | Identifier GT Identifier
                             | Identifier GT NumericSymbolicExpression
                             | Identifier NEQ Identifier
                             | Identifier NEQ NumericSymbolicExpression
                             
                             | NumericSymbolicExpression IN Identifier
                             | NumericSymbolicExpression IN SetExpression
                             | NumericSymbolicExpression SUBSET SetExpression
                             | NumericSymbolicExpression SUBSET Identifier
                             | NumericSymbolicExpression DEFAULT SetExpression
                             | NumericSymbolicExpression DEFAULT Identifier
                             | NumericSymbolicExpression DEFAULT NumericSymbolicExpression
                             | NumericSymbolicExpression DIMEN Identifier
                             | NumericSymbolicExpression DIMEN NumericSymbolicExpression
                             | NumericSymbolicExpression ASSIGN SetExpression
                             | NumericSymbolicExpression ASSIGN Identifier
                             | NumericSymbolicExpression ASSIGN NumericSymbolicExpression
                             | NumericSymbolicExpression LT Identifier
                             | NumericSymbolicExpression LT NumericSymbolicExpression
                             | NumericSymbolicExpression GT Identifier
                             | NumericSymbolicExpression GT NumericSymbolicExpression
                             | NumericSymbolicExpression NEQ Identifier
                             | NumericSymbolicExpression NEQ NumericSymbolicExpression
                             
                             | ValueList COMMA DeclarationAttributeList
                             | Identifier COMMA DeclarationAttributeList
                             | NumericSymbolicExpression COMMA DeclarationAttributeList
                             | DeclarationExpression COMMA DeclarationAttributeList'''

    _type = t.slice[2].type
    if isinstance(t[1], DeclarationExpression):
      if _type == "COMMA":
        t[1].addAttribute(t[3])
      else:
        t[1].addAttribute(t[2])

      t[0] = t[1]

    else:
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
        #if isinstance(t[3], Range):
        #  t[3] = SetExpressionWithValue(t[3])

        attr = DeclarationAttribute(t[3], DeclarationAttribute.ST)

      elif _type == "LT":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.LT)

      elif _type == "GT":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.GT)

      elif _type == "NEQ":
        attr = DeclarationAttribute(t[3], DeclarationAttribute.NEQ)

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
                          | ASSIGN Identifier
                          | ASSIGN NumericSymbolicExpression
                          
                          | LT Identifier
                          | LT NumericSymbolicExpression
                          
                          | LE Identifier
                          | LE NumericSymbolicExpression
                          
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
    #if isinstance(t[2], Range):
    #  t[2] = SetExpressionWithValue(t[2])
      
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


def p_LogicalExpression(t):
    '''LogicalExpression : EntryLogicalExpression
                         
                         | LogicalExpression OR LogicalExpression
                         | LogicalExpression OR Identifier
                         | LogicalExpression OR NumericSymbolicExpression

                         | Identifier OR LogicalExpression
                         | Identifier OR Identifier
                         | Identifier OR NumericSymbolicExpression

                         | NumericSymbolicExpression OR LogicalExpression
                         | NumericSymbolicExpression OR Identifier
                         | NumericSymbolicExpression OR NumericSymbolicExpression
                         
                         | LogicalExpression AND LogicalExpression
                         | LogicalExpression AND Identifier
                         | LogicalExpression AND NumericSymbolicExpression

                         | Identifier AND LogicalExpression
                         | Identifier AND Identifier
                         | Identifier AND NumericSymbolicExpression

                         | NumericSymbolicExpression AND LogicalExpression
                         | NumericSymbolicExpression AND Identifier
                         | NumericSymbolicExpression AND NumericSymbolicExpression'''

    if len(t) > 3:
      if isinstance(t[3], NumericExpression) or isinstance(t[3], Identifier):
        t[3] = EntryLogicalExpressionNumericOrSymbolic(t[3])

      if t.slice[2].type == "AND":
        t[0] = t[1].addAnd(t[3])
      else:
        t[0] = t[1].addOr(t[3])

    else:
        t[0] = LogicalExpression([t[1]])

def p_EntryLogicalExpression(t):
    '''EntryLogicalExpression : NOT LogicalExpression
                              | NOT Identifier
                              | NOT NumericSymbolicExpression
                              | LPAREN LogicalExpression RPAREN'''
                              
    if isinstance(t[2], NumericExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if isinstance(t[1], str) and t.slice[1].type == "NOT":
      t[0] = EntryLogicalExpressionNot(t[2])

    elif t.slice[1].type == "LPAREN":
      t[0] = EntryLogicalExpressionBetweenParenthesis(t[2])

    else:
      t[0] = t[2]

def p_EntryRelationalLogicalExpression(t):
    '''EntryLogicalExpression : Identifier LE Identifier
                              | Identifier LE NumericSymbolicExpression
                              | Identifier GE Identifier
                              | Identifier GE NumericSymbolicExpression
                              | Identifier EQ Identifier
                              | Identifier EQ NumericSymbolicExpression
                              | Identifier LT Identifier
                              | Identifier LT NumericSymbolicExpression
                              | Identifier GT Identifier
                              | Identifier GT NumericSymbolicExpression
                              | Identifier NEQ Identifier
                              | Identifier NEQ NumericSymbolicExpression
                              
                              | NumericSymbolicExpression LE Identifier
                              | NumericSymbolicExpression LE NumericSymbolicExpression
                              | NumericSymbolicExpression GE Identifier
                              | NumericSymbolicExpression GE NumericSymbolicExpression
                              | NumericSymbolicExpression EQ Identifier
                              | NumericSymbolicExpression EQ NumericSymbolicExpression
                              | NumericSymbolicExpression LT Identifier
                              | NumericSymbolicExpression LT NumericSymbolicExpression
                              | NumericSymbolicExpression GT Identifier
                              | NumericSymbolicExpression GT NumericSymbolicExpression
                              | NumericSymbolicExpression NEQ Identifier
                              | NumericSymbolicExpression NEQ NumericSymbolicExpression'''

    _type = t.slice[2].type
    if _type == "LT":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.LT, t[1], t[3])

    elif _type == "LE":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.LE, t[1], t[3])

    elif _type == "EQ":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.EQ, t[1], t[3])

    elif _type == "GT":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.GT, t[1], t[3])

    elif _type == "GE":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.GE, t[1], t[3])

    elif _type == "NEQ":
        t[0] = EntryLogicalExpressionRelational(EntryLogicalExpressionRelational.NEQ, t[1], t[3])

def p_EntryLogicalExpressionWithSet(t):
    '''EntryLogicalExpression : ValueList IN SetExpression
                              | ValueList IN Identifier
                              | ValueList NOTIN SetExpression
                              | ValueList NOTIN Identifier
                              
                              | Tuple IN SetExpression
                              | Tuple IN Identifier
                              | Tuple NOTIN SetExpression
                              | Tuple NOTIN Identifier
                              
                              | SetExpression SUBSET SetExpression
                              | SetExpression SUBSET Identifier
                              | SetExpression NOTSUBSET SetExpression
                              | SetExpression NOTSUBSET Identifier
                              
                              | Identifier IN SetExpression
                              | Identifier IN Identifier
                              | Identifier NOTIN SetExpression
                              | Identifier NOTIN Identifier
                              | Identifier SUBSET SetExpression
                              | Identifier SUBSET Identifier
                              | Identifier NOTSUBSET SetExpression
                              | Identifier NOTSUBSET Identifier
                              
                              | NumericSymbolicExpression IN SetExpression
                              | NumericSymbolicExpression IN Identifier
                              | NumericSymbolicExpression NOTIN SetExpression
                              | NumericSymbolicExpression NOTIN Identifier'''

    if not isinstance(t[3], SetExpression):
      t[3] = SetExpressionWithValue(t[3])

    if isinstance(t[1], ValueList):
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
                              | FORALL LLBRACE IndexingExpression RRBRACE Identifier
                              
                              | NFORALL LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | NFORALL LLBRACE IndexingExpression RRBRACE Identifier
                              
                              | EXISTS LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | EXISTS LLBRACE IndexingExpression RRBRACE Identifier
                              
                              | NEXISTS LLBRACE IndexingExpression RRBRACE LogicalExpression
                              | NEXISTS LLBRACE IndexingExpression RRBRACE Identifier'''

    if not isinstance(t[5], LogicalExpression):
      t[5] = LogicalExpression([EntryLogicalExpressionNumericOrSymbolic(t[5])])

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
                     
                     | LPAREN SetExpression RPAREN
                     | LLBRACE RRBRACE

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

                     | Range
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
        value = t[1]

        if isinstance(value, ConditionalSetExpression):
          t[0] = t[1]

        else:
          if hasattr(t.slice[1], 'value2'):
            value = t.slice[1].value2
          
          t[0] = SetExpressionWithValue(value)

def p_SetExpressionWithIndices(t):
    '''SetExpression : Identifier LBRACKET ValueList RBRACKET
                     | Identifier LBRACKET Identifier RBRACKET
                     | Identifier LBRACKET NumericSymbolicExpression RBRACKET'''

    if isinstance(t[3], NumericExpression) or isinstance(t[3], SymbolicExpression) or isinstance(t[3], Identifier):
      t[3] = ValueList([t[3]])

    t[0] = SetExpressionWithIndices(t[1], t[3])

def p_IteratedSetExpression(t):
    '''SetExpression : SETOF LLBRACE IndexingExpression RRBRACE TupleListItem
                     | SETOF LLBRACE IndexingExpression RRBRACE Identifier
                     | SETOF LLBRACE IndexingExpression RRBRACE NumericSymbolicExpression'''
    
    t[0] = IteratedSetExpression(t[3], t[5])

def p_ConditionalSetExpression(t):
    '''ConditionalSetExpression : IF LogicalExpression THEN SetExpression ELSE SetExpression
                                | IF LogicalExpression THEN SetExpression ELSE Identifier
                                | IF LogicalExpression THEN Identifier ELSE SetExpression
                                | IF LogicalExpression THEN SetExpression

                                | IF Identifier THEN SetExpression ELSE SetExpression
                                | IF Identifier THEN SetExpression ELSE Identifier
                                | IF Identifier THEN Identifier ELSE SetExpression
                                | IF Identifier THEN SetExpression

                                | IF NumericSymbolicExpression THEN SetExpression ELSE SetExpression
                                | IF NumericSymbolicExpression THEN SetExpression ELSE Identifier
                                | IF NumericSymbolicExpression THEN Identifier ELSE SetExpression
                                | IF NumericSymbolicExpression THEN SetExpression'''

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

def p_IndexingExpression(t):
    '''IndexingExpression : EntryIndexingExpression
                          
                          | IndexingExpression PIPE LogicalExpression
                          | IndexingExpression PIPE Identifier
                          | IndexingExpression PIPE NumericSymbolicExpression
                          
                          | IndexingExpression COMMA EntryIndexingExpression'''

    if len(t) > 3:

        if t.slice[2].type == "PIPE":

            if isinstance(t[3], NumericExpression) or isinstance(t[3], Identifier):
              t[3] = LogicalExpression([EntryLogicalExpressionNumericOrSymbolic(t[3])])

            t[0] = t[1].setLogicalExpression(t[3])

        else:
            t[0] = t[1].add(t[3])

    else:
        t[0] = IndexingExpression([t[1]])

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

def p_EntryIndexingExpressionEq(t):
    '''EntryIndexingExpression : Identifier EQ SetExpression
                               | Identifier EQ Identifier
                               | Identifier EQ NumericSymbolicExpression
                               
                               | Identifier NEQ Identifier
                               | Identifier NEQ NumericSymbolicExpression
                               
                               | Identifier LE Identifier
                               | Identifier LE NumericSymbolicExpression
                               
                               | Identifier GE Identifier
                               | Identifier GE NumericSymbolicExpression
                               
                               | Identifier LT Identifier
                               | Identifier LT NumericSymbolicExpression
                               
                               | Identifier GT Identifier
                               | Identifier GT NumericSymbolicExpression'''

    _type = t.slice[2].type
    if _type == "EQ":
        t[0] = EntryIndexingExpressionEq(EntryIndexingExpressionEq.EQ, t[1], t[3])

    elif _type == "NEQ":
        t[0] = EntryIndexingExpressionEq(EntryIndexingExpressionEq.NEQ, t[1], t[3])

    elif _type == "LE":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.LE, t[1], t[3])

    elif _type == "GE":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.GE, t[1], t[3])

    elif _type == "LT":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.LT, t[1], t[3])

    elif _type == "GT":
        t[0] = EntryIndexingExpressionCmp(EntryIndexingExpressionCmp.GT, t[1], t[3])


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
    '''SymbolicExpression : Identifier AMPERSAND Identifier
                          | Identifier AMPERSAND NumericSymbolicExpression
                          
                          | NumericSymbolicExpression AMPERSAND Identifier
                          | NumericSymbolicExpression AMPERSAND NumericSymbolicExpression'''

    if t.slice[2].type == "AMPERSAND":
        op = SymbolicExpressionWithOperation.CONCAT

    t[0] = SymbolicExpressionWithOperation(op, t[1], t[3])


def p_NumericExpression_binop(t):
    '''NumericExpression : Identifier PLUS Identifier
                         | Identifier PLUS NumericSymbolicExpression
                         | Identifier MINUS Identifier
                         | Identifier MINUS NumericSymbolicExpression
                         | Identifier TIMES Identifier
                         | Identifier TIMES NumericSymbolicExpression
                         | Identifier DIVIDE Identifier
                         | Identifier DIVIDE NumericSymbolicExpression
                         | Identifier MOD Identifier
                         | Identifier MOD NumericSymbolicExpression
                         | Identifier QUOTIENT Identifier
                         | Identifier QUOTIENT NumericSymbolicExpression
                         | Identifier CARET LBRACE Identifier RBRACE
                         | Identifier CARET LBRACE NumericSymbolicExpression RBRACE
                         
                         | NumericSymbolicExpression PLUS Identifier
                         | NumericSymbolicExpression PLUS NumericSymbolicExpression
                         | NumericSymbolicExpression MINUS Identifier
                         | NumericSymbolicExpression MINUS NumericSymbolicExpression
                         | NumericSymbolicExpression TIMES Identifier
                         | NumericSymbolicExpression TIMES NumericSymbolicExpression
                         | NumericSymbolicExpression DIVIDE Identifier
                         | NumericSymbolicExpression DIVIDE NumericSymbolicExpression
                         | NumericSymbolicExpression MOD Identifier
                         | NumericSymbolicExpression MOD NumericSymbolicExpression
                         | NumericSymbolicExpression QUOTIENT Identifier
                         | NumericSymbolicExpression QUOTIENT NumericSymbolicExpression
                         | NumericSymbolicExpression CARET LBRACE Identifier RBRACE
                         | NumericSymbolicExpression CARET LBRACE NumericSymbolicExpression RBRACE'''

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

    elif len(t) > 3 and isinstance(t[3], Identifier):
      t[3] = ValuedNumericExpression(t[3])

    elif isinstance(t[1], Identifier):
      t[1] = ValuedNumericExpression(t[1])

    if _type == "CARET":
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
                         
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | PROD UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                         
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | MAX UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression
                         
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE Identifier RBRACE NumericSymbolicExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE CARET LBRACE NumericSymbolicExpression RBRACE NumericSymbolicExpression
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE Identifier
                         | MIN UNDERLINE LBRACE IndexingExpression RBRACE NumericSymbolicExpression'''

    _type = t.slice[1].type
    if _type == "SUM":
        op = IteratedNumericExpression.SUM

    elif _type == "PROD":
        op = IteratedNumericExpression.PROD

    elif _type == "MAX":
        op = IteratedNumericExpression.MAX

    elif _type == "MIN":
        op = IteratedNumericExpression.MIN

    if len(t) > 7:
        if isinstance(t[8], Identifier):
          t[8] = ValuedNumericExpression(t[8])

        if isinstance(t[10], Identifier):
          t[10] = ValuedNumericExpression(t[10])

        t[0] = IteratedNumericExpression(op, t[10], t[4], t[8])
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
    '''ConditionalNumericExpression : IF LogicalExpression THEN Identifier ELSE Identifier
                                    | IF LogicalExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF LogicalExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF LogicalExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF LogicalExpression THEN Identifier
                                    | IF LogicalExpression THEN NumericSymbolicExpression

                                    | IF Identifier THEN Identifier ELSE Identifier
                                    | IF Identifier THEN Identifier ELSE NumericSymbolicExpression
                                    | IF Identifier THEN NumericSymbolicExpression ELSE Identifier
                                    | IF Identifier THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF Identifier THEN Identifier
                                    | IF Identifier THEN NumericSymbolicExpression

                                    | IF NumericSymbolicExpression THEN Identifier ELSE Identifier
                                    | IF NumericSymbolicExpression THEN Identifier ELSE NumericSymbolicExpression
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression ELSE Identifier
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression ELSE NumericSymbolicExpression
                                    | IF NumericSymbolicExpression THEN Identifier
                                    | IF NumericSymbolicExpression THEN NumericSymbolicExpression'''

    if isinstance(t[2], NumericExpression) or isinstance(t[2], SymbolicExpression) or isinstance(t[2], Identifier):
      t[2] = EntryLogicalExpressionNumericOrSymbolic(t[2])

    if not isinstance(t[2], LogicalExpression):
      t[2] = LogicalExpression([t[2]])
    
    if isinstance(t[4], Identifier):
      t[4] = ValuedNumericExpression(t[4])

    if len(t) > 5 and isinstance(t[6], Identifier):
      t[6] = ValuedNumericExpression(t[6])

    t[0] = ConditionalNumericExpression(t[2], t[4])

    if len(t) > 5:
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
                  
                  | ID LBRACKET ValueList RBRACKET
                  | ID LBRACKET Identifier RBRACKET
                  | ID LBRACKET NumericSymbolicExpression RBRACKET
                  
                  | ID'''

    if len(t) > 5:
        if isinstance(t[4], ValueList):
          t[0] = Identifier(ID(t[1]), t[4].getValues())
        else:
          t[0] = Identifier(ID(t[1]), [t[4]])
    elif len(t) > 2:
        if isinstance(t[3], ValueList):
          t[0] = Identifier(ID(t[1]), t[3].getValues())
        else:
          t[0] = Identifier(ID(t[1]), [t[3]])
    else:
        t[0] = Identifier(ID(t[1]))

def p_ValueList(t):
    '''ValueList : ValueList COMMA SetExpression
                 | ValueList COMMA Identifier
                 | ValueList COMMA NumericSymbolicExpression

                 | SetExpression COMMA SetExpression
                 | SetExpression COMMA Identifier
                 | SetExpression COMMA NumericSymbolicExpression
                 
                 | Identifier COMMA SetExpression
                 | Identifier COMMA Identifier
                 | Identifier COMMA NumericSymbolicExpression
                 
                 | NumericSymbolicExpression COMMA SetExpression
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

def p_error(t):
  if t:
    raise SyntaxException(t.lineno, t.lexpos, t.value, t)
  else:
    raise SyntaxException("EOF")