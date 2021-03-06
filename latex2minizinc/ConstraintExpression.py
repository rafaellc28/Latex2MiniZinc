from Expression import *

class ConstraintExpression(Expression):
    """
    Class representing a constraint expression node in the AST of a MLP
    """
    EQ  = "="
    LE  = "<="
    GE  = ">="
    NEQ = "!="
    LT  = "<"
    GT  = ">"

    def __init__(self):
        Expression.__init__(self)

class ConstraintExpression2(ConstraintExpression):
    """
    Class representing a constraint expression node in the AST of a MLP
    """

    def __init__(self, linearExpression1, linearExpression2, op = ConstraintExpression.LE):
        """
        Set the expressions being related
        
        :param linearExpression1: LinearExpression
        :param linearExpression2: LinearExpression
        """
        
        ConstraintExpression.__init__(self)

        self.linearExpression1 = linearExpression1
        self.linearExpression2 = linearExpression2
        self.op = op
        
    def __str__(self):
        """
        to string
        """
        
        return "CntExprWith2:" + str(self.linearExpression1) + " " + self.op + " " + str(self.linearExpression2)

    def getDependencies(self, codeGenerator):
        return list(set(self.linearExpression1.getDependencies(codeGenerator) + self.linearExpression2.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets in this constraint
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets in this constraint
        """
        codePrepare.prepare(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this constraint expression
        """
        return codeGenerator.generateCode(self)


class ConstraintExpression3(ConstraintExpression):
    """
    Class representing a constraint expression node in the AST of a MLP
    """

    def __init__(self, linearExpression, numericExpression1, numericExpression2, op = ConstraintExpression.LE):
        """
        Set the expressions being related
        
        :param linearExpression   : LinearExpression
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        """
        
        ConstraintExpression.__init__(self)

        self.linearExpression   = linearExpression
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2
        self.op = op
        
    def __str__(self):
        """
        to string
        """
        
        return "CntExprWith3:" + str(self.numericExpression1) + " " + self.op + " " + str(self.linearExpression) + " " + self.op + " " + str(self.numericExpression2)
    
    def getDependencies(self, codeGenerator):
        return list(set(self.linearExpression.getDependencies(codeGenerator) + self.numericExpression1.getDependencies(codeGenerator) + self.numericExpression2.getDependencies(codeGenerator)))
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets in this constraint
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets in this constraint
        """
        codePrepare.prepare(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this constraint expression
        """
        return codeGenerator.generateCode(self)


class LogicalConstraintExpression(ConstraintExpression):
    """
    Class representing a conditional constraint expression node in the AST of a MLP
    """
    
    IMPLIES = "->"
    ISIMPLIEDBY = "<-"
    IFANDONLYIF = "<->"

    def __init__(self, op, logicalExpression, constraintExpression1, constraintExpression2 = None):
        """
        Set the conditional constraint expression
        
        :param op : IMPLIES | ISIMPLIEDBY | IFANDONLYIF
        :param logicalExpression : LogicalExpression
        :param constraintExpression1 : ConstraintExpression
        :param constraintExpression2 : ConstraintExpression
        """
        
        ConstraintExpression.__init__(self)
        
        self.op = op
        self.logicalExpression = logicalExpression
        self.constraintExpression1 = constraintExpression1
        self.constraintExpression2 = constraintExpression2
    
    def __str__(self):
        """
        to string
        """
        res = "LogicalConstraintExpression: " + str(self.logicalExpression) + " " + self.op + " " + str(self.constraintExpression1)

        if self.constraintExpression2 != None:
            res += " ELSE " + str(self.constraintExpression2)

        return res
        
    def addElseExpression(self, elseExpression):
        self.constraintExpression2 = elseExpression

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this conditional constraint expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this conditional constraint expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this contitional constraint expression
        """
        return codeGenerator.generateCode(self)

class ConditionalConstraintExpression(ConstraintExpression):
    """
    Class representing a conditional constraint expression node in the AST of a MLP
    """
    
    def __init__(self, logicalExpression, constraintExpression1, constraintExpression2 = None, elseIfExpression = None):
        """
        Set the conditional constraint expression
        
        :param logicalExpression     : LogicalExpression
        :param constraintExpression1 : ConstraintExpression
        :param constraintExpression2 : ConstraintExpression
        :param elseIfExpression      : ElseIfExpressionList
        """
        ConstraintExpression.__init__(self)
        
        self.logicalExpression     = logicalExpression
        self.constraintExpression1 = constraintExpression1
        self.constraintExpression2 = constraintExpression2
        self.elseIfExpression   = elseIfExpression
        
    def __str__(self):
        """
        to string
        """
        res = "ConditionalConstraintExpression: " + "IF ("+str(self.logicalExpression)+") THEN " + str(self.constraintExpression1)
        
        if self.elseIfExpression != None:
            res += str(self.elseIfExpression)

        if self.constraintExpression2 != None:
            res += "ELSE " + str(self.constraintExpression2)
        
        return res

    def addElseIfExpression(self, elseIfExpression):
        self.elseIfExpression = elseIfExpression

    def addElseExpression(self, elseExpression):
        self.constraintExpression2 = elseExpression

    def getDependencies(self, codeGenerator):
        dep = self.logicalExpression.getDependencies(codeGenerator) + self.constraintExpression1.getDependencies(codeGenerator)

        if self.elseIfExpression != None:
            dep += self.elseIfExpression.getDependencies(codeGenerator)

        if self.constraintExpression2 != None:
            dep += self.constraintExpression2.getDependencies(codeGenerator)

        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this conditional constraint expression
        """
        codeSetup.setupEnvironment(self)
        
    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this conditional constraint expression
        """
        codePrepare.prepare(self)
        
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this contitional constraint expression
        """
        return codeGenerator.generateCode(self)
        