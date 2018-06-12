from SymbolTable import *
from Constants import *

class SymbolTables(object):
    def __init__(self):
        """
        Constructor
        """
        self.tables = {}
        self.types = [Constants.PARAMETERS, Constants.VARIABLES, Constants.SETS]

    def __len__(self):
        return len(self.tables)

    def __iter__(self):
        """
        Get the iterator of the class
        """
        return self.tables.iteritems()

    def insert(self, statement, table, level = 0, isDeclaration = False):
        if not statement in self.tables:
            self.tables[statement] = {LASTSCOPE: 0, ISDECLARATION: isDeclaration, TABLES: [{SCOPE: 0, LEVEL: level, TABLE: table}]}
        elif isDeclaration:
            self.tables[statement][LASTSCOPE] = 0
            table.setScope(self.tables[statement][LASTSCOPE])
            self.tables[statement][TABLES].append({SCOPE: self.tables[statement][LASTSCOPE] , LEVEL: level, TABLE: table})
        else:
            self.tables[statement][LASTSCOPE] += 1
            table.setScope(self.tables[statement][LASTSCOPE])
            self.tables[statement][TABLES].append({SCOPE: self.tables[statement][LASTSCOPE] , LEVEL: level, TABLE: table})
        
        return table

    def lookup(self, statement, scope = 0):
        if not statement in self.tables:
            return None

        for table in self.tables[statement][TABLES]:
            if table[SCOPE] == scope:
                return table[TABLE]

        return None

    def lastLevel(self, statement):
        if not statement in self.tables:
            return None

        levels = []
        for table in self.tables[statement][TABLES]:
            levels.append(table[LEVEL])

        return max(levels)

    def getStatements(self):
        statements = {k: v for k, v in self.tables.iteritems()}
        return statements

    def getStatementsByKey(self, key):
        statements = self.getStatements()
        return {k:v for k,v in statements.iteritems() for k2 in [k1 for k1 in [t[TABLE].getTable() for t in v[TABLES]]] if key in k2}

    def getDeclarations(self):
        declarations = {k: v for k, v in self.tables.iteritems() if v[ISDECLARATION]}
        return declarations

    def getDeclarationsByStatement(self, statement):
        declarations = self.getDeclarations()
        return {k:v for k,v in declarations.iteritems() if k == statement}
    
    def getDeclarationsByKey(self, key):
        declarations = self.getDeclarations()
        return {k:v for k,v in declarations.iteritems() for k2 in [k1 for k1 in [t[TABLE].getTable() for t in v[TABLES]]] if key in k2}

    def getDeclarationsWhereKeyIsDefined(self, key):
        res = {}
        declarations = self.getDeclarations()
        for k, decl in declarations.iteritems():
            inserted = False
            for t in decl[TABLES]:
                table = t[TABLE].getTable()
                for k1,v1 in table.iteritems():
                    if k1 == key and v1.getIsDefined():
                        res[k] = decl
                        inserted = True
                        break

                if inserted:
                    break

        return res

    def getDeclarationsWhereKeyIsUsed(self, key):
        res = {}
        declarations = self.getDeclarations()
        for k,decl in declarations.iteritems():
            inserted = False
            for t in decl[TABLES]:
                table = t[TABLE].getTable()
                for k1,v1 in table.iteritems():
                    if k1 == key and not v1.getIsDefined():
                        res[k] = decl
                        inserted = True
                        break

                if inserted:
                    break

        return res

    def getConstraints(self):
        constraints = {k: v for k, v in self.tables.iteritems() if not v[ISDECLARATION]}
        return constraints

    def getConstraintsByStatement(self, statement):
        constraints = self.getConstraints()
        return {k:v for k,v in constraints.iteritems() if k == statement}

    def getConstraintsByKey(self, key):
        constraints = self.getConstraints()
        return {k:v for k,v in constraints.iteritems() for k2 in [k1 for k1 in [t[TABLE].getTable() for t in v[TABLES]]] if key in k2}

    def getLeafs(self, statement):
        leafs = [table for table in self.tables[statement][TABLES] if table[TABLE].getIsLeaf()]
        return leafs

    def getScopesWhereKeyIsDefined(self, key, statement):
        scopes = []
        for table in self.tables[statement][TABLES]:
            for k1,v1 in table[TABLE].getTable().iteritems():
                if k1 == key and v1.getIsDefined():
                    scopes.append(table)
                    break
        
        return scopes

    def getFirstScopeByKey(self, key, statement):
        scopes = []
        for table in self.tables[statement][TABLES]:
            for k1,v1 in table[TABLE].getTable().iteritems():
                if k1 == key and table[SCOPE] == 0:
                    scopes.append(table)
                    break
        
        return scopes

    def getFirstScope(self, statement):
        scopes = []
        for table in self.tables[statement][TABLES]:
            if table[SCOPE] == 0:
                scopes.append(table)
                break
                
        return scopes
