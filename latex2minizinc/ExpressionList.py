from Expression import *
from Utils import *

class ExpressionList(Expression):
    """
    Class representing an indexing expression in the AST
    """

    # Get the MiniZinc code for a given constraint
    @staticmethod
    def _getCodePredicateEntry(entry): return entry.generatePredicateCode()

    def __init__(self, entriesIndexingExpression, logicalExpression = None, stmtIndexing = False):
        """
        Set the entries for the indexing expression
        """

        Expression.__init__(self)

        self.entriesIndexingExpression = entriesIndexingExpression
        self.logicalExpression = logicalExpression
        self.hasSup = False
        self.stmtIndexing = stmtIndexing
        self.supExpression = None

    def __str__(self):
        """
        to string
        """

        res = "\nExpressionList:\n["
        res += "\n".join(filter(Utils._deleteEmpty, map(lambda i: str(i), self.entriesIndexingExpression)))

        if self.logicalExpression:
            res += " | " + str(self.logicalExpression)

        res += "]"

        return res


    def __len__(self):
        """
        length method
        """

        return len(self.entriesIndexingExpression)

    def add(self, entry):
        """
        Add an entry to the indexing expression
        """

        self.entriesIndexingExpression += [entry]
        return self

    def setLogicalExpression(self, logicalExpression):
        """
        Set the logical expression
        """

        self.logicalExpression = logicalExpression
        return self

    def setStmtIndexing(self, stmtIndexing):
        self.stmtIndexing = stmtIndexing

    def setHasSup(self, hasSup):
        self.hasSup = hasSup

    def setSupExpression(self, supExpression):
        self.supExpression = supExpression

    def getDependencies(self, codeGenerator):
        dep = Utils._flatten(map(lambda el: el.getDependencies(codeGenerator), self.entriesIndexingExpression))
        
        if self.logicalExpression != None:
            dep += self.logicalExpression.getDependencies(codeGenerator)
        
        return list(set(dep))

    def enableCheckDummyIndices(self):
        map(lambda el: el.enableCheckDummyIndices(), self.entriesIndexingExpression)

        if self.logicalExpression:
            self.logicalExpression.enableCheckDummyIndices()

    def disableCheckDummyIndices(self):
        map(lambda el: el.disableCheckDummyIndices(), self.entriesIndexingExpression)

        if self.logicalExpression:
            self.logicalExpression.disableCheckDummyIndices()

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
        Generate the MiniZinc code for this indexing expression
        """
        return codeGenerator.generateCode(self)
