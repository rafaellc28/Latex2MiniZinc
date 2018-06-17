from Expression import *

class EntryLogicalExpression(Expression):
    """
    Class representing an entry of logical expression in the AST of the MLP
    """

    def __init__(self):
        Expression.__init__(self)

class EntryLogicalExpressionRelational(EntryLogicalExpression):
    """
    Class representing an entry of relational logical expression in the AST of the MLP
    """

    LT = "<"
    LE = "<="
    EQ = "="
    GT = ">"
    GE = ">="
    NEQ = "<>"

    def __init__(self, op, numericExpression1, numericExpression2):
        """
        Set the operator and the numeric expressions

        :param op : (LT, LE, EQ, GT, GE, NEQ)
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        """

        EntryLogicalExpression.__init__(self)

        self.op = op
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2

    def __str__(self):
        """
        to string
        """

        return "EntryLogicalExpressionRelational: " + str(self.numericExpression1) + " " + self.op + " " + str(self.numericExpression2)

    def getDependencies(self, codeGenerator):
        return list(set(self.numericExpression1.getDependencies(codeGenerator) + self.numericExpression2.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the declaration of identifiers and sets used in this entry for logical expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the declaration of identifiers and sets used in this entry for logical expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for Entry of Relational Logical Expression
        """
        return codeGenerator.generateCode(self)
    

class EntryLogicalExpressionWithSet(EntryLogicalExpression):
    """
    Class representing an entry of logical expression with sets in the AST of the MLP
    """

    IN = "in"
    NOTIN = "not in"

    def __init__(self, op, identifier, setExpression):
        """
        Set the operator, the identifier and the set expression

        :param op : op
        :param identifier : ValueList| Identifier | TupleList
        :param setExpression : setExpression
        """
        
        EntryLogicalExpression.__init__(self)

        self.op = op
        self.identifier = identifier
        self.setExpression = setExpression
        self.isBinary = False
        self.isInteger = False
        self.isNatural = False
        self.isReal = False
        self.isSymbolic = False
        self.isLogical = False
        self.isDeclaredAsVar = False
        self.isDeclaredAsSet = False
        self.isDeclaredAsParam = False

    def __str__(self):
        """
        to string
        """

        return "EntryLogicalExpressionWithSet: " + str(self.identifier) + " " + self.op + " " + str(self.setExpression)

    def getDependencies(self, codeGenerator):
        return list(set(self.identifier.getDependencies(codeGenerator) + self.setExpression.getDependencies(codeGenerator)))

    def enableCheckDummyIndices(self):
        self.identifier.enableCheckDummyIndices()
        
    def disableCheckDummyIndices(self):
        self.identifier.disableCheckDummyIndices()

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the declaration of identifiers and sets used in this entry for logical expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the declaration of identifiers and sets used in this entry for logical expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for Entry of Logical Expression with Set
        """
        return codeGenerator.generateCode(self)


class EntryLogicalExpressionWithSetOperation(EntryLogicalExpression):
    """
    Class representing an entry of logical expression with sets in the AST of the MLP
    """

    SUBSET = "subset"
    NOTSUBSET = "not subset"

    def __init__(self, op, setExpression1, setExpression2):
        """
        Set the operator and the set expressions

        :param op : (SUBSET, NOTSUBSET)
        :param setExpression1 : SetExpression
        :param setExpression2 : SetExpression
        """

        EntryLogicalExpression.__init__(self)

        self.op = op
        self.setExpression1 = setExpression1
        self.setExpression2 = setExpression2

    def __str__(self):
        """
        to string
        """

        return "EntryLogicalExpressionWithSetOperation: " + str(self.setExpression1) + " " + self.op + " " + str(self.setExpression2)

    def getDependencies(self, codeGenerator):
        return list(set(self.setExpression1.getDependencies(codeGenerator) + self.setExpression2.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the declaration of identifiers and sets used in this entry for logical expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the declaration of identifiers and sets used in this entry for logical expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for Entry of Logical Expression with Set
        """
        return codeGenerator.generateCode(self)


class EntryLogicalExpressionIterated(EntryLogicalExpression):
    """
    Class representing an entry of iterated logical expression in the AST of the MLP
    """

    FORALL  = "forall"
    NFORALL = "not forall"
    EXISTS  = "exists"
    NEXISTS = "not exists"

    def __init__(self, op, indexingExpression, logicalExpression):
        """
        Set the operator and the numeric expressions

        :param op : (FORALL, NFORALL, EXISTS, NEXISTS)
        :param indexingExpression : IndexingExpression
        :param logicalExpression  : LogicalExpression
        """

        EntryLogicalExpression.__init__(self)

        self.op = op
        self.indexingExpression = indexingExpression
        self.logicalExpression  = logicalExpression

    def __str__(self):
        """
        to string
        """

        return "EntryLogicalExpressionIterated: " + self.op + "{" + str(self.indexingExpression) + "} " +  str(self.logicalExpression)

    def getDependencies(self, codeGenerator):
        return list(set(self.indexingExpression.getDependencies(codeGenerator) + self.logicalExpression.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the declaration of identifiers and sets used in this entry for logical expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the declaration of identifiers and sets used in this entry for logical expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for Entry of Iterated Logical Expression
        """
        return codeGenerator.generateCode(self)
        

class EntryLogicalExpressionBetweenParenthesis(EntryLogicalExpression):
    """
    Class representing a logical expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, logicalExpression):
        """
        Set the logical expression

        :param logicalExpression : LogicalExpression
        """

        EntryLogicalExpression.__init__(self)

        self.logicalExpression = logicalExpression

    def __str__(self):
        """
        to string
        """
        
        return "EntryLogicalExpressionBetweenParenthesis: (" + str(self.logicalExpression) + ")"
 
    def getDependencies(self, codeGenerator):
        return self.logicalExpression.getDependencies(codeGenerator)

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this logical expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this logical expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this logical expression
        """
        return codeGenerator.generateCode(self)

class EntryLogicalExpressionNumericOrSymbolic(EntryLogicalExpression):
    """
    Class representing a logical expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, numericOrSymbolicExpression):
        """
        Set the logical expression

        :param numericOrSymbolicExpression : NumericExpression|SymbolicExpression
        """

        EntryLogicalExpression.__init__(self)

        self.numericOrSymbolicExpression = numericOrSymbolicExpression

    def __str__(self):
        """
        to string
        """
        
        return "EntryLogicalExpressionNumericOrSymbolic: (" + str(self.numericOrSymbolicExpression) + ")"

    def getDependencies(self, codeGenerator):
        return self.numericOrSymbolicExpression.getDependencies(codeGenerator)
   
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this logical expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this logical expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this logical expression
        """
        return codeGenerator.generateCode(self)

class EntryLogicalExpressionNot(EntryLogicalExpression):
    """
    Class representing a logical expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, logicalExpression):
        """
        Set the logical expression with negation

        :param logicalExpression : LogicalExpression
        """

        EntryLogicalExpression.__init__(self)
        
        self.logicalExpression = logicalExpression

    def __str__(self):
        """
        to string
        """
        
        return "EntryLogicalExpressionNot: (NOT " + str(self.logicalExpression) + ")"

    def getDependencies(self, codeGenerator):
        return self.logicalExpression.getDependencies(codeGenerator)
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this logical expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this logical expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this logical expression
        """
        return codeGenerator.generateCode(self)
