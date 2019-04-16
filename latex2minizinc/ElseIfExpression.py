from Expression import *

class ElseIfExpressionList(Expression):
    """
    Class representing a elseif expression list node in the AST of a MLP
    """
    def __init__(self, expressions):
        Expression.__init__(self)

        self.expressions = expressions


    def __str__(self):
        """
        to string
        """
        return "ElseIfExpressionList: [" + " ".join(map(lambda el: str(el), self.expressions)) + "]"

    def addElseIfExpression(self, expression):
    	self.expressions.append(expression)

    def getDependencies(self, codeGenerator):
        return list(set(map(lambda el: el.getDependencies(codeGenerator), self.expressions)))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this elseif expression list
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this elseif expression list
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this elseif expression list
        """
        return codeGenerator.generateCode(self)

class ElseIfExpression(Expression):
    """
    Class representing a elseif expression list node in the AST of a MLP
    """
    def __init__(self, logicalExpression, expression):
        Expression.__init__(self)

        self.logicalExpression = logicalExpression
        self.expression 	   = expression


    def __str__(self):
        """
        to string
        """
        return "ElseIfExpression: ELSEIF " + str(self.logicalExpression) + " THEN " + str(self.expression)

    def addElseIfExpression(self, expression):
    	self.expressions.append(expression)

    def getDependencies(self, codeGenerator):
        return list(set(self.logicalExpression.generateCode(codeGenerator) + self.expression.generateCode(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this elseif expression list
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this elseif expression list
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this elseif expression list
        """
        return codeGenerator.generateCode(self)
