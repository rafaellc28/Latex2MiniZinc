from Expression import *

class NumericExpression(Expression):
    """
    Class representing a numeric expression node in the AST of a MLP
    """
    def __init__(self):
        Expression.__init__(self)

class NumericExpressionWithFunction(NumericExpression):
    """
    Class representing a numeric expression with function node in the AST of a MLP
    """

    CARD      = "card"
    LENGTH    = "length"
    ABS       = "abs"
    CEIL      = "ceil"
    FLOOR     = "floor"
    EXP       = "exp"
    LN        = "ln"
    LOG       = "log"
    SQRT      = "sqrt"
    MIN       = "min"
    MAX       = "max"
    
    SIN       = "sin"
    COS       = "cos"
    TAN       = "tan"
    ASIN      = "asin"
    ACOS      = "acos"
    ATAN      = "atan"

    SINH      = "sin"
    COSH      = "cos"
    TANH      = "tan"
    ASINH     = "asin"
    ACOSH     = "acos"
    ATANH     = "atan"

    def __init__(self, function, numericExpression1 = None, numericExpression2 = None):
        """
        Set the numeric expression and the function
        
        :param function           : (abs | atan | card | ceil | cos | floor | exp | log | log10 | sin | sqrt  ...)
        :param numericExpression  : NumericExpression | SymbolicExpression | ValueList
        :param numericExpression2 : NumericExpression | SymbolicExpression
        """

        NumericExpression.__init__(self)

        self.function = function
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2

    def __str__(self):
        """
        to string
        """
        res = "NumericExpressionWithFunction: " + str(self.function) + "("

        if self.numericExpression1 != None:
            res += str(self.numericExpression1)

        if self.numericExpression2 != None:
            res += ", " + str(self.numericExpression2)

        res += ")"
        
        return res

    def getDependencies(self, codeGenerator):
        dep = []

        if self.numericExpression1 != None:
            dep += self.numericExpression1.getDependencies(codeGenerator)

        if self.numericExpression2 != None:
            dep += self.numericExpression2.getDependencies(codeGenerator)

        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this numeric expression with function
        """
        return codeGenerator.generateCode(self)
    

class FractionalNumericExpression(NumericExpression):
    """
    Class representing a fractional numeric expression node in the AST of a MLP
    """

    def __init__(self, numerator, denominator):
        """
        Set the single value of this numeric expression
        :param numerator   : Identifier | NumericExpression
        :param denominator : Identifier | NumericExpression
        """

        NumericExpression.__init__(self)

        self.numerator   = numerator
        self.denominator = denominator

    def __str__(self):
        """
        to string
        """
        return "FractionalNumericExpression: " + str(self.numerator) + "/"+str(self.denominator)

    def __len__(self):
        """
        length method
        """

        return 1

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return [self]

    def getDependencies(self, codeGenerator):
        dep = []

        if self.numerator != None:
            dep += self.numerator.getDependencies(codeGenerator)

        if self.denominator != None:
            dep += self.denominator.getDependencies(codeGenerator)

        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this fractional numeric expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this fractional numeric expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this fractional numeric expression
        """
        return codeGenerator.generateCode(self)


class ValuedNumericExpression(NumericExpression):
    """
    Class representing a valued numeric expression node in the AST of a MLP
    """

    def __init__(self, value):
        """
        Set the single value of this numeric expression

        :param value : Identifier | Number
        """

        NumericExpression.__init__(self)

        self.value = value

    def __str__(self):
        """
        to string
        """
        
        return "ValuedNumExpr:" + str(self.value)

    def __len__(self):
        """
        length method
        """

        return 1

    def __iter__(self):
        """
        Get the iterator of the class
        """
        return [self]
        
    def getValue(self):
        return self.value
        
    def getSymbol(self):
        return self.value
        
    def getDependencies(self, codeGenerator):
        return self.value.getDependencies(codeGenerator)
        
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codePrepare.prepare(self)
        
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this valued linear expression
        """
        return codeGenerator.generateCode(self)


class NumericExpressionBetweenParenthesis(NumericExpression):
    """
    Class representing a numeric expression between parenthesis node in the AST of a MLP
    """

    def __init__(self, numericExpression):
        """
        Set the numeric expression

        :param numericExpression : NumericExpression
        """

        NumericExpression.__init__(self)

        self.numericExpression = numericExpression

    def __str__(self):
        """
        to string
        """
        
        return "NEBetweenParenthesis: (" + str(self.numericExpression) + ")"

    def getDependencies(self, codeGenerator):
        return self.numericExpression.getDependencies(codeGenerator)
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this numeric expression
        """
        return codeGenerator.generateCode(self)


class NumericExpressionWithArithmeticOperation(NumericExpression):
    """
    Class representing a numeric expression with arithmetic operation node in the AST of a MLP
    """
    
    PLUS  = "+"
    MINUS = "-"
    TIMES = "*"
    DIV   = "/"
    MOD   = "mod"
    POW   = "^"
    QUOT  = "div"

    def __init__(self, op, numericExpression1, numericExpression2):
        """
        Set the expressions participating in the arithmetic operation
        
        :param op                 : (PLUS, MINUS, TIMES, MOD, POW)
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        """

        NumericExpression.__init__(self)
        
        self.op                 = op
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2
    
    def __str__(self):
        """
        to string
        """
        res = "OpArthNE:" + str(self.numericExpression1) + " " + self.op + " "
        if self.op == NumericExpressionWithArithmeticOperation.POW and not (isinstance(self.numericExpression2, ValuedNumericExpression) or isinstance(self.numericExpression2, NumericExpressionBetweenParenthesis)):
            res += "{" + str(self.numericExpression2) + "}"
        else:
            res += str(self.numericExpression2)

        return res

    def getDependencies(self, codeGenerator):
        return list(set(self.numericExpression1.getDependencies(codeGenerator) + self.numericExpression2.getDependencies(codeGenerator)))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this numeric expression with arithmetic operation
        """
        return codeGenerator.generateCode(self)


class MinusNumericExpression(NumericExpression):
    """
    Class representing a minus numeric expression node in the AST of a MLP
    """
    
    def __init__(self, numericExpression):
        """
        Set the numeric expression being negated
        
        :param numericExpression: NumericExpression
        """

        NumericExpression.__init__(self)
        
        self.numericExpression = numericExpression
    
    def __str__(self):
        """
        to string
        """
        
        return "MinusNE:" + "-(" + str(self.numericExpression) + ")"

    def getDependencies(self, codeGenerator):
        return self.numericExpression.getDependencies(codeGenerator)

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this minus numeric expression
        """
        return codeGenerator.generateCode(self)


class IteratedNumericExpression(NumericExpression):
    """
    Class representing a iterated numeric expression node in the AST of a MLP
    """

    SUM  = "sum"
    PROD = "product"
    MAX  = "max"
    MIN  = "min"

    def __init__(self, op, numericExpression, indexingExpression, supNumericExpression = None):
        """
        Set the components of the iterated linear expression

        :param op                   : op
        :param numericExpression    : NumericExpression
        :param indexingExpression   : IndexingExpression
        :param supNumericExpression : NumericExpression
        """

        NumericExpression.__init__(self)
        
        self.op                   = op
        self.numericExpression    = numericExpression
        self.indexingExpression   = indexingExpression
        self.supNumericExpression = supNumericExpression

    def __str__(self):
        """
        to string
        """
        
        res = str(self.op) + "(" + str(self.indexingExpression) + ")"

        if self.supNumericExpression:
            res += "^" + str(self.supNumericExpression)

        res += str(self.numericExpression)

        return "ItNumExp:" + res + "|"

    def getDependencies(self, codeGenerator):
        dep = self.numericExpression.getDependencies(codeGenerator) + self.indexingExpression.getDependencies(codeGenerator)

        if self.supNumericExpression != None:
            dep += self.supNumericExpression.getDependencies(codeGenerator)

        return list(set(dep))
    
    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this numeric expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this iterated numeric expression
        """
        return codeGenerator.generateCode(self)

class ConditionalNumericExpression(NumericExpression):
    """
    Class representing a conditional numeric expression node in the AST of a MLP
    """
    
    def __init__(self, logicalExpression, numericExpression1, numericExpression2 = None, elseIfExpression = None):
        """
        Set the conditional numeric expression
        
        :param logicalExpression  : LogicalExpression
        :param numericExpression1 : NumericExpression
        :param numericExpression2 : NumericExpression
        :param elseIfExpression   : ElseIfExpressionList
        """

        NumericExpression.__init__(self)
        
        self.logicalExpression  = logicalExpression
        self.numericExpression1 = numericExpression1
        self.numericExpression2 = numericExpression2
        self.elseIfExpression   = elseIfExpression
    
    def __str__(self):
        """
        to string
        """
        res = "ConditionalNumericExpression: " + "IF ("+str(self.logicalExpression)+") THEN " + str(self.numericExpression1)

        if self.elseIfExpression != None:
            res += str(self.elseIfExpression)

        if self.numericExpression2 != None:
            res += "ELSE " + str(self.numericExpression2)

        return res

    def addElseIfExpression(self, elseIfExpression):
        self.elseIfExpression = elseIfExpression

    def addElseExpression(self, elseExpression):
        self.numericExpression2 = elseExpression
    
    def getDependencies(self, codeGenerator):
        dep = self.logicalExpression.getDependencies(codeGenerator) + self.numericExpression1.getDependencies(codeGenerator)

        if self.elseIfExpression != None:
            dep += self.elseIfExpression.getDependencies(codeGenerator)

        if self.numericExpression2 != None:
            dep += self.numericExpression2.getDependencies(codeGenerator)

        return list(set(dep))

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the identifiers and sets used in this conditional numeric expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the identifiers and sets used in this conditional numeric expression
        """
        codePrepare.prepare(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this conditional numeric expression
        """
        return codeGenerator.generateCode(self)
