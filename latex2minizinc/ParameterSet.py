from SetExpression import *

class ParameterSet(SetExpression):
    def __init__(self):
        SetExpression.__init__(self)

    def getSymbolName(self, codeGenerator):
        return self.generateCode(codeGenerator)

    def getDependencies(self, codeGenerator):
        return []

    def setupEnvironment(self, codeSetup):
        """
        Setup environment
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare environment
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this Number
        """
        return codeGenerator.generateCode(self)
