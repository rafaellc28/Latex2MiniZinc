from Expression import *
from Utils import *

class TupleList(Expression):
    """
    Class representing a list of values in the AST of the MLP
    """

    def __init__(self, values):
        """
        Set the values
        
        :param values : [Identifier|NumericExpression|SymbolicExpression]
        """
        Expression.__init__(self)
        
        self.values = values
        self.i = -1

    def __str__(self):
        """
        to string
        """
        
        return "TupleList: [" + ",".join(map(lambda i: str(i), self.values)) + "]"

    def __len__(self):
        """
        length method
        """

        return len(self.values)

    def __iter__(self):
        return self

    def next(self):
        if self.i < len(self.values)-1:
            self.i += 1         
            return self.values[self.i]
        else:
            self.i = -1
            raise StopIteration
    
    def getValues(self):
        """
        Get the values in this TupleList
        """

        return self.values

    def add(self, value):
        """
        Add a value to the list
        """

        self.values += [value]
        return self
    
    def getDependencies(self, codeGenerator):
        return list(set(Utils._flatten(map(lambda el: el.getDependencies(codeGenerator), self.values))))

    def enableCheckDummyIndices(self):
        map(lambda el: el.enableCheckDummyIndices(), self.values)
        
    def disableCheckDummyIndices(self):
        map(lambda el: el.disableCheckDummyIndices(), self.values)

    def setupEnvironment(self, codeSetup):
        """
        Setup the MiniZinc code for the declaration of identifiers used in this tuple list expression
        """
        codeSetup.setupEnvironment(self)

    def prepare(self, codePrepare):
        """
        Prepare the MiniZinc code for the declaration of identifiers used in this tuple list expression
        """
        codePrepare.prepare(self)
    
    def generateCode(self, codeGenerator):
        """
        Generate the MiniZinc code for this TupleList
        """
        return codeGenerator.generateCode(self)
