from Expression import *

class Value(Expression):
    """
    Class representing an Value in the AST of the MLP
    """

    def __init__(self, value):
        """
        Set the value

        :param value: float|Identifier
        """
        Expression.__init__(self)
        
        if isinstance(value, float):
            self.value = Number(value)
        else:
            self.value = value

    def __str__(self):
        """
        to string
        """

        return "Value: "  + str(self.value)

    def getDependencies(self, codeGenerator):
        return self.value.getDependencies(codeGenerator)

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the declaration of the identifier of this value
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the declaration of the identifier of this value
        """
        codePrepare.prepare(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this Value
        """
        return codeGenerator.generateCode(self)
