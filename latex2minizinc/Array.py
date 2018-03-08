from Expression import *

class Array(Expression):
    """
    Class representing a Array node in the AST of the MLP
    """
    
    def __init__(self, value):
        """
        Set the ValueList inside the array
        
        :param value: ValueList
        """

        Expression.__init__(self)
        
        self.value = value
    
    def __str__(self):
        """
        to string
        """
        
        return "Array: [" +str(self.value) + "]"

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return [self]
    
    def getDependencies(self, codeGenerator):
        deps = self.getSymbolName(codeGenerator)

        if not isinstance(deps, list):
            deps = list(deps)

        return deps
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MiniZinc code for the declaration of this ID
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this Identifier
        """
        return codeGenerator.generateCode(self)

class ArrayWithOperation(Array):
    """
    Class representing a array expression with operation node in the AST of a MLP
    """
    
    CONCAT  = "++"

    def __init__(self, op, array1, array2):
        """
        Set the expressions participating in the operation
        
        :param op                 : (CONCAT)
        :param array1 : Array | Identifier
        :param array2 : Array | Identifier
        """

        Expression.__init__(self)
        
        self.op                  = op
        self.array1 = array1
        self.array2 = array2
    
    def __str__(self):
        """
        to string
        """
        
        return "Array: " + str(self.array1) + " " + self.op + " " + str(self.array2)

    def getDependencies(self, codeGenerator):
        return list(set(self.array1.getDependencies(codeGenerator) + self.array2.getDependencies(codeGenerator)))
    
    def setupEnvironment(self, codeSetup):
        """
        Generate the MiniZinc code for the identifiers and sets used in this array expression
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this array expression with operation
        """
        return codeGenerator.generateCode(self)

class ArrayChoose(Expression):
    """
    Class representing a ArrayChoose node in the AST of the MLP
    """
    
    def __init__(self, value1, value2):
        """
        Set the ValueList inside the arrayChoose
        
        :param value : ValueList
        :param value2: ValueList
        """

        Expression.__init__(self)
        
        self.value1 = value1
        self.value2 = value2
    
    def __str__(self):
        """
        to string
        """
        return "ArrayChoose: [" +str(self.value1) + "]["+str(self.value2)+"]"

    def __iter__(self):
        """
        Get the iterator of the class
        """

        return [self]
    
    def getDependencies(self, codeGenerator):
        deps = self.value.getSymbolName(codeGenerator)
        
        if not isinstance(deps, list):
            deps = list(deps)

        deps2 = self.value2.getSymbolName(codeGenerator)

        if isinstance(deps2, list):
            for dep in deps2:
                deps.append(dep)

        else:
            deps.append(deps2)

        return deps
        
    def setupEnvironment(self, codeSetup):
        """
        Generate the MiniZinc code for the declaration of this ID
        """
        codeSetup.setupEnvironment(self)

    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this Identifier
        """
        return codeGenerator.generateCode(self)
