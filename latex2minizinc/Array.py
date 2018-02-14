from Expression import *

class Array(Expression):
    """
    Class representing a Array node in the AST of the MLP
    """
    
    def __init__(self, value):
        """
        Set the ValueList inside the array
        
        :param value: ValueList
        """

        Expression.__init__(self)
        
        self.value = value
    
    def __str__(self):
        """
        to string
        """
        
        return "Array: [" +str(self.value) + "]"

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return [self]
    
    def getDependencies(self, codeGenerator):
        return [self.getSymbolName(codeGenerator)]
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MathProg code for the declaration of this ID
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MathProg code for this Identifier
        """
        return codeGenerator.generateCode(self)
