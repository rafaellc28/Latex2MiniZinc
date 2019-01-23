from Expression import *

class TestExpression(Expression):
    """
    Class representing a test expression node in the AST
    """

    def __init__(self, name, arguments, expression = None):
        """
        :param name       : Identifier
        :param arguments  : Declarations
        :param expression : NumericExpression | SymbolicExpression | LetExpression
        """

        Expression.__init__(self)

        self.name = name
        self.arguments = arguments
        self.expression = expression

    def __str__(self):
        """
        to string
        """
        res = "TestExpression: test "+str(self.name)+"("+str(self.arguments)+")"

        if self.expression:
            res += " { " + str(self.expression) + " }"

        return res

    def getDependencies(self, codeGenerator):
        dep = self.name.getDependencies(codeGenerator) + self.arguments.getDependencies(codeGenerator)


        if self.expression:
            deps += self.expression.getDependencies(codeGenerator)
            
        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for this test expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the this test expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this test expression
        """
        return codeGenerator.generateCode(self)
