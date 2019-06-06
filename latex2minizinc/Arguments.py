class Arguments:
    """
    Class that encapsulate a list of all nodes in the AST that represent a argument list in a MLP
    """

    def __init__(self, arguments, origin = None):
        """
        Set the list of arguments
        
        :param arguments: [Argument|Constraint]
        """
        
        self.arguments = arguments
        self.origin = origin
        self.symbolTable = None
    
    def __str__(self):
        """
        to string
        """
        
        return "\nArguments:\n" + "\n".join(map(lambda i: str(i), self.arguments))
 
    def getTotalNames(self):
        total = 0

        for arg in self.arguments:
            if isinstance(arg, Argument):
                total += len(arg.names)

        return total

    def getNames(self, codeGenerator):
        names = []

        for arg in self.arguments:
            if isinstance(arg, Argument):
                for name in arg.names:
                    names.append(name.getSymbolName(codeGenerator))

        return names


    def getSymbolTable(self):
        return self.symbolTable
        
    def setSymbolTable(self, symbolTable):
        self.symbolTable = symbolTable

    def addArgument(self, argument):
        self.arguments.append(argument)

    def setOrigin(self, origin):
        self.origin = origin

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
    
    def __init__(self, names, argumentType, expression = None, indexingExpression = None):
        """
        Set the argument type and the indexing expression of an argument
        
        :param names               : ValueList[Identifier]
        :param argumentType        : ArgumentType
        :param expression          : NumericSymbolicExpression
        :param indexingExpressions : IndexingExpression
        """
        
        self.names = names
        self.argumentType = argumentType
        self.expression = expression
        self.indexingExpression = indexingExpression
        self.symbolTable = None
    
    def __str__(self):
        """
        to string
        """
        res = ""

        if self.argumentType:
            res += str(self.argumentType) + ": "

        res += str(self.names)

        if self.expression:
            res += " = " + str(self.expression)

        if self.indexingExpression:
            res += ",\nfor " + str(self.indexingExpression)

        return "Argument:" + res
    
    def getSymbolTable(self):
        return self.symbolTable
        
    def setSymbolTable(self, symbolTable):
        self.symbolTable = symbolTable
    
    def setIndexingExpression(self, indexingExpression):
        self.indexingExpression = indexingExpression

    def getDependencies(self, codeGenerator):
        dep = self.names.getDependencies(codeGenerator) + self.argumentType.getDependencies(codeGenerator)
        
        if self.expression != None:
            dep += self.expression.getDependencies(codeGenerator)
            
        if self.indexingExpression != None:
            dep += self.indexingExpression.getDependencies(codeGenerator)
            
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
