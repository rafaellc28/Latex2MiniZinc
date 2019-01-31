class Declarations:
    """
    Class that encapsulate a list of all nodes in the AST that represent a declaration in a MLP
    """

    def __init__(self, declarations):
        """
        Set the list of declarations
        
        :param declarations: [Declaration]
        """
        
        self.declarations = declarations

        self.symbolTable = None
    
    def __str__(self):
        """
        to string
        """
        
        return "\nDecls:\n" + "\n".join(map(lambda i: str(i), self.declarations))
 
    def getSymbolTable(self):
        return self.symbolTable
        
    def setSymbolTable(self, symbolTable):
        self.symbolTable = symbolTable

    def getDependencies(self, codeGenerator):
        dep = Utils._flatten(map(lambda el: el.getDependencies(codeGenerator), self.declarations))
        return list(set(dep))
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in these declarations
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in these declarations
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the code in MiniZinc for these declarations
        """
        return codeGenerator.generateCode(self)
    
class Declaration:
    """
    Class representing a declaration node in the AST of a MLP
    """
    
    def __init__(self, declarationExpression, indexingExpression = None, stmtIndex = False):
        """
        Set the declaration expression and the indexing expression of an declaration
        
        :param declarationExpression: DeclarationExpression
        :param indexingExpressions: IndexingExpression
        """
        
        self.declarationExpression = declarationExpression
        self.indexingExpression   = indexingExpression
        self.stmtIndex = stmtIndex
        self.symbolTable = None
    
    def __str__(self):
        """
        to string
        """
        res = str(self.declarationExpression)
        
        if self.indexingExpression:
            res += ",\nfor " + str(self.indexingExpression)
        
        return "Decl:" + res
    
    def getSymbolTable(self):
        return self.symbolTable
        
    def setSymbolTable(self, symbolTable):
        self.symbolTable = symbolTable
    
    def setStmtIndexing(self, stmtIndex):
        self.stmtIndex = stmtIndex

    def setIndexingExpression(self, indexingExpression):
        self.indexingExpression = indexingExpression

    def getDependencies(self, codeGenerator):
        dep = self.declarationExpression.getDependencies(codeGenerator)

        if self.indexingExpression != None:
            dep += self.indexingExpression.getDependencies(codeGenerator)

        return list(set(dep))
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for declaration of identifiers and sets in this declaration
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for declaration of identifiers and sets in this declaration
        """
        codePrepare.prepare(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this constraint
        """
        return codeGenerator.generateCode(self)
