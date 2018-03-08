from Expression import *

class TrueFalse(Expression):
    """
    Class representing a numeric expression node in the AST of a MLP
    """

    TRUE  = "true"
    FALSE = "false"

    def __init__(self, value):
        Expression.__init__(self)
        self.value = value

    def __str__(self):
        """
        to string
        """
        return "TrueFalse: " + str(self.value)

    def getDependencies(self, codeGenerator):
        return []

    def setupEnvironment(self, codeSetup):
        """
        Generate the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this numeric expression with function
        """
        return codeGenerator.generateCode(self)
