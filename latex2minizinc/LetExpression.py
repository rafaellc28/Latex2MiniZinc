from Expression import *

class LetExpression(Expression):
    """
    Class representing a let expression node in the AST
    """

    def __init__(self, arguments, expression):
        """
        :param arguments  : ArgumentList
        :param expression : NumericExpression | SymbolicExpression | LetExpression
        """

        Expression.__init__(self)

        self.arguments = arguments
        self.expression = expression
        self.preparedArguments = None

    def __str__(self):
        """
        to string
        """
        return "LetExpression: let ("+str(self.arguments)+") in " + str(self.expression)

    def setPreparedArguments(self, preparedArguments):
        self.preparedArguments = preparedArguments

    def getDependencies(self, codeGenerator):
        dep = self.arguments.getDependencies(codeGenerator) + self.expression.getDependencies(codeGenerator)
        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for this let expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for this let expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this let expression
        """
        return codeGenerator.generateCode(self)
