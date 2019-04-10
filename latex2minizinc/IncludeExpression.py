from Expression import *

class IncludeExpression(Expression):
    """
    Class representing a function expression node in the AST
    """

    def __init__(self, values):
        """
        :param name : [StringSymbolicExpression]
        """

        Expression.__init__(self)

        self.values = values
        
    def __str__(self):
        """
        to string
        """
        return "include " + ", ".join(map(lambda el: str(el), self.values))

    def getDependencies(self, codeGenerator):
        return list(set(map(lambda el: el.getDependencies(codeGenerator), self.values)))

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
