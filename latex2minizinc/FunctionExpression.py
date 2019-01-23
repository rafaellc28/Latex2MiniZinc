from Expression import *

class FunctionExpression(Expression):
    """
    Class representing a function expression node in the AST
    """

    def __init__(self, _type, name, arguments, expression = None):
        """
        :param name       : Identifier
        :param arguments  : Declarations
        :param expression : NumericExpression | SymbolicExpression | LetExpression
        :param _type      : ID | NaturalSet | IntegerSet | RealSet
        """

        Expression.__init__(self)

        self.type = _type
        self.name = name
        self.arguments = arguments
        self.expression = expression
        
    def __str__(self):
        """
        to string
        """
        res = "FunctionExpression: function "+str(self.type)+": "+str(self.name)+"("+str(self.arguments)+")"

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
        Setup the MiniZinc code for this function expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the this function expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this function expression
        """
        return codeGenerator.generateCode(self)
