class Constraints:
    """
    Class that encapsulate a list of all nodes in the AST that represent a contraint in a MLP
    """

    def __init__(self, constraints):
        """
        Set the list of constraints
        
        :param constraints: [Constraint]
        """
        
        self.constraints = constraints
    
    def __str__(self):
        """
        to string
        """
        
        return "\nCnts:\n" + "\n".join(map(lambda i: str(i), self.constraints))
        
    def getConstraints(self):
        return self.constraints

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in these constraints
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in these constraints
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the code in MiniZinc for these Constraints
        """
        return codeGenerator.generateCode(self)
    
class Constraint:
    """
    Class representing a constraint node in the AST of a MLP
    """
    
    def __init__(self, constraintExpression, indexingExpression = None):
        """
        Set the constraint expression and the indexing expression of an constraint
        
        :param constraintExpression: ConstraintExpression
        :param indexingExpressions: IndexingExpression
        """
        
        self.constraintExpression = constraintExpression
        self.indexingExpression   = indexingExpression
        self.symbolTable = None
        
    def __str__(self):
        """
        to string
        """
        
        res = str(self.constraintExpression)

        if self.indexingExpression:
            res += ",\nfor " + str(self.indexingExpression)
        
        return "Cnt:" + res
        
    def getSymbolTable(self):
        return self.symbolTable
        
    def setSymbolTable(self, symbolTable):
        self.symbolTable = symbolTable

    def setIndexingExpression(self, indexingExpression):
        self.indexingExpression = indexingExpression
        
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for declaration of identifiers and sets in this constraint
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for declaration of identifiers and sets in this constraint
        """
        codePrepare.prepare(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this constraint
        """
        return codeGenerator.generateCode(self)
