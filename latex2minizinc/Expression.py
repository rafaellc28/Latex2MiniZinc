class Expression:
    """
    Class representing a expression node in the AST of a MLP
    """
    def __init__(self):
        self.indice = -1
        self.identifier = None
        self.identifierName = None
        self.identifierList = None

        self.isInSet = False
        self.isSet = None
        self.isVar = None
        self.isParam = None
        self.isReal = False
        self.isSymbolic = False
        self.isLogical = False
        self.isBinary = False
        self.isInteger = False
        self.isNatural = False
        self.isSubIndice = False
        self.isInt = False
        self.isDeclaredAsParam = None
        self.isDeclaredAsSet = None
        self.isDeclaredAsVar = None
        self.checkIfIsDummyIndex = False

    def getSymbol(self):
        return self

    def getSymbolName(self, codeGenerator):
        return self.generateCode(codeGenerator)

    def getDimension(self):
        return 1

    def getIndice(self):
        return self.indice

    def setIndice(self, indice):
        self.indice = indice

    def getIdentifier(self):
        return self.identifier

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def getIdentifierName(self):
        return self.identifierName

    def setIdentifierName(self, identifierName):
        self.identifierName = identifierName

    def getIdentifierList(self):
        return self.identifierList

    def setIdentifierList(self, identifierList):
        self.identifierList = identifierList

    def enableCheckDummyIndices(self):
        pass

    def disableCheckDummyIndices(self):
        pass
