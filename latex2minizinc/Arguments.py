class Arguments:
    """
    Class that encapsulate a list of all nodes in the AST that represent a argument list in a MLP
    """

    def __init__(self, arguments):
        """
        Set the list of arguments
        
        :param arguments: [Argument]
        """
        
        self.arguments = arguments
        self.symbolTable = None
    
    def __str__(self):
        """
        to string
        """
        
        return "\nArguments:\n" + "\n".join(map(lambda i: str(i), self.arguments))
 
    def getSymbolTable(self):
        return self.symbolTable
        
    def setSymbolTable(self, symbolTable):
        self.symbolTable = symbolTable

    def addArgument(self, argument):
        self.arguments.add(argument)

    def getDependencies(self, codeGenerator):
        dep = Utils._flatten(map(lambda el: el.getDependencies(codeGenerator), self.arguments))
        return list(set(dep))
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in these arguments
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in these arguments
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the code in MiniZinc for these arguments
        """
        return codeGenerator.generateCode(self)
    
class Argument:
    """
    Class representing a argument node in the AST of a MLP
    """
    
    def __init__(self, argumentType, indexingExpression = None, expression = None):
        """
        Set the argument type and the indexing expression of an argument
        
        :param argumentType        : ArgumentType
        :param indexingExpressions : IndexingExpression
        :param expression          : NumericSymbolicExpression
        """
        
        self.argumentType = argumentType
        self.indexingExpression = indexingExpression
        self.expression = expression
        self.symbolTable = None
    
    def __str__(self):
        """
        to string
        """
        res = str(self.argumentType)
        
        if self.indexingExpression:
            res += ",\nfor " + str(self.indexingExpression)

        if self.expression:
            res += " = " + str(self.expression)
        
        return "Argument:" + res
    
    def getSymbolTable(self):
        return self.symbolTable
        
    def setSymbolTable(self, symbolTable):
        self.symbolTable = symbolTable
    
    def setIndexingExpression(self, indexingExpression):
        self.indexingExpression = indexingExpression

    def getDependencies(self, codeGenerator):
        dep = self.declarationExpression.getDependencies(codeGenerator)

        if self.indexingExpression != None:
            dep += self.indexingExpression.getDependencies(codeGenerator)

        if self.expression != None:
            dep += self.expression.getDependencies(codeGenerator)

        return list(set(dep))
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for argument of identifiers and sets in this argument
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for argument of identifiers and sets in this argument
        """
        codePrepare.prepare(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this argument
        """
        return codeGenerator.generateCode(self)


class ArgumentType:
    """
    Class representing a argument type node in the AST of a MLP
    """
    
    def __init__(self, _type, isVariable = False):
        """
        Set the argument type and the indexing expression of an argument
        
        :param type       : Identifier | NaturalSet | IntegerSet ...
        :param isVariable : Boolean
        """
        
        self.type = _type
        self.isVariable = isVariable
        self.symbolTable = None
    
    def __str__(self):
        """
        to string
        """
        var = "var " if self.isVariable else ""
        res = var + str(self.type)
        
        return "ArgumentType:" + res
    
    def getSymbolTable(self):
        return self.symbolTable
        
    def setSymbolTable(self, symbolTable):
        self.symbolTable = symbolTable
    
    def setStmtIndexing(self, stmtIndex):
        self.stmtIndex = stmtIndex

    def getDependencies(self, codeGenerator):
        return self.type.getDependencies(codeGenerator)
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for argument type of identifiers and sets in this argument
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for argument type of identifiers and sets in this argument
        """
        codePrepare.prepare(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this argument type
        """
        return codeGenerator.generateCode(self)