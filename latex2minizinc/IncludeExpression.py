from Expression import *

class IncludeExpression(Expression):
    """
    Class representing a function expression node in the AST
    """

    def __init__(self, name):
        """
        :param name : StringSymbolicExpression
        """

        Expression.__init__(self)

        self.name = name
        
    def __str__(self):
        """
        to string
        """
        return "include " + str(self.name)

    def getDependencies(self, codeGenerator):
        return self.name.getDependencies(codeGenerator)

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for this include expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the this include expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this include expression
        """
        return codeGenerator.generateCode(self)
