from Expression import *
from Identifier import *
from ValueList import *
from Utils import *

class SetExpression(Expression):
    """
    Class representing a set in the AST
    """
    def __init__(self, dimension = 0):
        Expression.__init__(self)
        self.dimension = dimension

    def setDimension(self, dimension):
        self.dimension = dimension

    def getDimension(self):
        return self.dimension

class SetExpressionWithValue(SetExpression):
    """
    Class representing a set with value in the AST
    """

    def __init__(self, value, dimension = 0):
        """
        Set the value that correspond to the Set expression
        
        :param value : Identifier | ValueList | Range
        """
        SetExpression.__init__(self, dimension)

        self.value = value
        
    
    def __str__(self):
        """
        to string
        """
        if isinstance(self.value, ValueList):
            return "SetExpressionWithValue: {" + str(self.value) + "}"
        else:
            return "SetExpressionWithValue: "+str(self.value)

    def setDimension(self, dimension):
        self.dimension = dimension

        if isinstance(self.value, Identifier):
            self.value.setDimenSet(dimension)
            
    def getDimension(self):
        return self.dimension
        
    def getSymbol(self):
        return self.value
        
    def getSymbolName(self, codeGenerator):
        if isinstance(self.value, Identifier):
            res = self.value.getSymbolNameWithIndices(codeGenerator)
        else:
            res = self.value.getSymbolName(codeGenerator)
            
        return res
        
    def getDependencies(self, codeGenerator):
        if not isinstance(self.value, str):
            return self.value.getDependencies(codeGenerator)

        return [self.value]

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for declaration of identifiers and sets used in this set expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for declaration of identifiers and sets used in this set expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this Set expression
        """
        return codeGenerator.generateCode(self)


class SetExpressionWithIndices(SetExpression):
    """
    Class representing a set with indices in the AST
    """

    def __init__(self, identifier, indices, dimension = 0):
        """
        Set the value that correspond to the Set expression
        
        :param identifier : Identifier
        :param indices    : ValueList | Identifier
        """
        SetExpression.__init__(self, dimension)

        self.identifier = identifier
        self.indices = indices
        self.dimension = dimension

    def __str__(self):
        """
        to string
        """

        return "SetExpressionWithIndices: " + str(self.identifier)

    def setDimension(self, dimension):
        self.dimension = dimension
        self.identifier.setDimenSet(dimension)

    def getDimension(self):
        return self.dimension

    def getDependencies(self, codeGenerator):
        return list(set(self.identifier.getDependencies(codeGenerator) + self.indices.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for declaration of identifiers and sets used in this set expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for declaration of identifiers and sets used in this set expression
        """
        codePrepare.prepare(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this Set expression
        """
        return codeGenerator.generateCode(self)


class SetExpressionWithOperation(SetExpression):
    """
    Class representing a set with operation in the AST
    """

    DIFF    = "diff"
    SYMDIFF = "symdiff"
    UNION   = "union"
    INTER   = "intersect"
    CROSS   = "cross"

    def __init__(self, op, setExpression1, setExpression2):
        """
        Set the operator and the expressions
        """
        SetExpression.__init__(self)

        self.op             = op
        self.setExpression1 = setExpression1
        self.setExpression2 = setExpression2

    def __str__(self):
        """
        to string
        """

        return "SetExpressionWithOperation: " + str(self.setExpression1) + " " + self.op + " " + str(self.setExpression2)

    def getDependencies(self, codeGenerator):
        return list(set(self.setExpression1.getDependencies(codeGenerator) + self.setExpression2.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for declaration of identifiers and sets used in this set expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for declaration of identifiers and sets used in this set expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this Set expression
        """
        return codeGenerator.generateCode(self)

class SetExpressionBetweenParenthesis(SetExpression):
    """
    Class representing a set expression between parenthesis node in the AST
    """

    def __init__(self, setExpression):
        """
        Set the set expression

        :param setExpression : SetExpression
        """
        SetExpression.__init__(self)

        self.setExpression = setExpression

    def __str__(self):
        """
        to string
        """
        
        return "SetExpressionBetweenParenthesis: (" + str(self.setExpression) + ")"

    def getDependencies(self, codeGenerator):
        return self.setExpression.getDependencies(codeGenerator)
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this set expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this set expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this set expression
        """
        return codeGenerator.generateCode(self)

class SetExpressionBetweenBraces(SetExpression):
    """
    Class representing a set expression between braces node in the AST
    """

    def __init__(self, setExpression):
        """
        Set the set expression

        :param setExpression : SetExpression|ValueList|Range|TupleList|IndexingExpression
        """
        SetExpression.__init__(self)

        self.setExpression = setExpression

    def __str__(self):
        """
        to string
        """
        setExpr = str(self.setExpression) if self.setExpression != None else ""
        return "SetExpressionBetweenBraces: {" + setExpr + "}"

    def getDependencies(self, codeGenerator):
        if self.setExpression != None:
            return self.setExpression.getDependencies(codeGenerator)

        return []
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this set expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this set expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this set expression
        """
        return codeGenerator.generateCode(self)

class IteratedSetExpression(SetExpression):
    """
    Class representing a iterated set expression node in the AST
    """
    
    def __init__(self, indexingExpression, integrand, inferred = False):
        """
        Set the iterated set expression
        
        :param indexingExpression : IndexingExpression
        :param integrand          : NumericExpression | SymbolicExpression | Identifier | Tuple
        """
        SetExpression.__init__(self)

        self.indexingExpression = indexingExpression
        self.integrand          = integrand
        self.inferred           = inferred
        
    def __str__(self):
        """
        to string
        """
        res = "setof "

        if self.indexingExpression:
            res += "{" + str(self.indexingExpression) + "} "

        res += str(self.integrand)

        return "IteratedSetExpression: " + res

    def getDependencies(self, codeGenerator):
        deps = []

        if self.indexingExpression:
            deps += self.indexingExpression.getDependencies(codeGenerator)

        deps += self.integrand.getDependencies(codeGenerator)

        return list(set(deps))
        
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this iterated set expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this iterated set expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this contitional set expression
        """
        return codeGenerator.generateCode(self)


class ConditionalSetExpression(SetExpression):
    """
    Class representing a conditional set expression node in the AST
    """
    
    def __init__(self, logicalExpression, setExpression1, setExpression2 = None):
        """
        Set the conditional set expression
        
        :param logicalExpression : LogicalExpression
        :param setExpression1    : SetExpression
        :param setExpression2    : SetExpression
        """
        SetExpression.__init__(self)

        self.logicalExpression = logicalExpression
        self.setExpression1    = setExpression1
        self.setExpression2    = setExpression2
    
    def __str__(self):
        """
        to string
        """
        res = "ConditionalSetExpression: " + "("+str(self.logicalExpression)+")?" + str(self.setExpression1)
        
        if self.setExpression2 != None:
            res += ": " + str(self.setExpression2)
        
        return res

    def addElseExpression(self, elseExpression):
        self.setExpression2 = elseExpression

    def getDependencies(self, codeGenerator):
        dep = self.logicalExpression.getDependencies(codeGenerator) + self.setExpression1.getDependencies(codeGenerator)

        if self.setExpression2 != None:
            dep += self.setExpression2.getDependencies(codeGenerator)

        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this conditional set expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this conditional set expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this contitional set expression
        """
        return codeGenerator.generateCode(self)
