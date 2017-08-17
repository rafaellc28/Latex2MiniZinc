from Utils import *
from ValueList import *
from Tuple import *
from Constraints import *
from ConstraintExpression import *
from SetExpression import *
from EntryIndexingExpression import *
from EntryLogicalExpression import *
from SymbolicExpression import *
from TopologicalSort import *
from GenSets import *
from GenVariables import *
from GenParameters import *
from GenDeclarations import *
from GenBelongsToList import *
from GenBelongsTo import *
from Constants import *
from SymbolTables import *

import re

class CodeGenerator:
    """ Visitor in the Visitor Pattern """
    
    def __init__(self):

        self.genSets = GenSets()
        self.genVariables = GenVariables()
        self.genParameters = GenParameters()
        self.genDeclarations = GenDeclarations()
        self.genBelongsToList = GenBelongsToList()
        self.genValueAssigned = GenList()
        self.topological_order = []

        self.totalObjectives = 0
        self.objectiveNumber = 0
        self.constraintNumber = 0
        self.stmtIndex = 0

        self.symbolTables = None
        self.symbolTables = SymbolTables()

        self.parameters = []
        self.sets = []
        self.variables = []
        self.parameters_and_sets = []

        self.identifiers = {}

        self.additionalConstraints = []

        self.turnStringsIntoInts = False
        self.additionalParameters = {}

        self.tuples = {}
        self.tuplesDeclared = {}

        self.scopes = {}
        self.scope = 0
        self.parentScope = -1
        self.stmtIndex = -1

        self.countNewIndices = 0
        self.includeNewIndices = False
        self.replaceNewIndices = True
        self.newIndexExpression = ""
        self.newType = "int"



    def generateCode(self, node):
        cls = node.__class__
        method_name = 'generateCode_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    def init(self):
        self.parameters = map(lambda el: el.getName(), self.genParameters.getAll())
        self.sets = map(lambda el: el.getName(), self.genSets.getAll())
        self.variables = map(lambda el: el.getName(), self.genVariables.getAll())

        self.parameters_and_sets = self.parameters + self.sets

        if len(self.genVariables) > 0:
            for var in self.genVariables.getAll():
                if not self.genParameters.has(var) and not self.genSets.has(var):
                    domain, domain_list, dependencies, sub_indices = self._getSubIndicesDomains(var)
                    _types, dim, minVal, maxVal = self._getDomain(var)
                    self.identifiers[var.getName()] = {"types": _types,
                                                       "dim": dim,
                                                       "minVal": minVal,
                                                       "maxVal": maxVal,
                                                       "domain": domain, 
                                                       "domain_list": domain_list, 
                                                       "dependencies": dependencies, 
                                                       "sub_indices": sub_indices}

        if len(self.genParameters) > 0:
            for var in self.genParameters.getAll():
                domain, domain_list, dependencies, sub_indices = self._getSubIndicesDomains(var)
                _types, dim, minVal, maxVal = self._getDomain(var)
                self.identifiers[var.getName()] = {"types": _types,
                                                   "dim": dim,
                                                   "minVal": minVal,
                                                   "maxVal": maxVal,
                                                   "domain": domain, 
                                                   "domain_list": domain_list, 
                                                   "dependencies": dependencies, 
                                                   "sub_indices": sub_indices}

        if len(self.genSets) > 0:
            for var in self.genSets.getAll():
                domain, domain_list, dependencies, sub_indices = self._getSubIndicesDomains(var)
                _types, dim, minVal, maxVal = self._getDomain(var)
                self.identifiers[var.getName()] = {"types": _types,
                                                   "dim": dim,
                                                   "minVal": minVal,
                                                   "maxVal": maxVal,
                                                   "domain": domain, 
                                                   "domain_list": domain_list, 
                                                   "dependencies": dependencies, 
                                                   "sub_indices": sub_indices}

        self._getTuples()

        '''
        print("Symbol Tables")
        self._printSymbolTables(self.symbolTables)
        print("")
        
        print("Declarations")
        declarations = self.symbolTables.getDeclarations()
        self._printSymbolTables(declarations.iteritems())
        print("")
        
        print("Leafs")
        self._printLeafs()
        print("")
        '''

    def _printTables(self, tables):
        for dictStmt in tables:
            print("SymbolTable Scope " + str(dictStmt["scope"]) + ". Level: " + str(dictStmt["level"]) + ". Leaf: " + str(dictStmt["table"].getIsLeaf()) + 
                  ". Parent Scope: " + (str(None) if dictStmt["table"].getParent() == None else str(dictStmt["table"].getParent().getScope())))

            print("\n".join([str(key) + ": type = " + str(value.getType()) + "; scope = " + str(value.getScope()) + 
                   "; properties = [name: " + str(value.getProperties().getName()) + ", domains: " + 
                   str(map(lambda el: "{" + str(el.getOp()) + " " + el.getName() + ", dependencies: " + str(el.getDependencies()) + "}", value.getProperties().getDomains())) + 
                   ", minVal: " + str(value.getProperties().getMinVal()) + ", maxVal: " + str(value.getProperties().getMaxVal()) + 
                   ", dimension: " + str(value.getProperties().getDimension()) + ", default: " + str(value.getProperties().getDefault()) + 
                   ", attributes: " + str(value.getProperties().getAttributes()) + "]; inferred = " + str(value.getInferred()) + 
                   "; sub_indices = " + str(value.getSubIndices()) + "; isDefined = " + str(value.getIsDefined()) + ";"
                   for key, value in dictStmt["table"]]))
            print("")

    def _printStatementSymbolTable(self, statement, tables):
        print("SymbolTable Stmt " + str(statement) + ". Declaration: " + str(tables["isDeclaration"]))
        self._printTables(tables["tables"])


    def _printLeafs(self):
        for stmt, tables in self.symbolTables:
            print("SymbolTable Stmt " + str(stmt) + ". Declaration: " + str(tables["isDeclaration"]))
            leafs = self.symbolTables.getLeafs(stmt)
            self._printTables(leafs)

    def _printSymbolTables(self, symbolTables):
        for stmt, tables in symbolTables:
            self._printStatementSymbolTable(stmt, tables)

    def _printScopes(self):
        print("Scopes")

        for stmt, scopes in self.scopes.iteritems():
            print("Statement: " + str(stmt))

            for scope, value in scopes.iteritems():
                print("Scope: " + str(scope))
                print("Value: " + str(value))

        print("")

    def _getLogicalExpressionOfDeclaration(self, declaration, varName, dependencies, sub_indices):
        if declaration == None or declaration.getIndexingExpression() == None or declaration.getIndexingExpression().logicalExpression == None:
            return None

        logicalExpression = declaration.getIndexingExpression().logicalExpression
        logicalExpressionDependencies = set(logicalExpression.getDependencies(self))

        if varName in logicalExpressionDependencies:
            return logicalExpression.generateCode(self)

        if len(logicalExpressionDependencies.intersection(sub_indices)) > 0:
            return logicalExpression.generateCode(self)

        if len(logicalExpressionDependencies.intersection(dependencies)) > 0:
            return logicalExpression.generateCode(self)

        return None

    def _getDomainByIdentifier(self, ident):
        if ident in self.identifiers:
            res = self.identifiers[ident]
            return res["domain"]

        return None

    def _getSubIndicesDomainsAndDependencies(self, var):
        if var in self.identifiers:
            res = self.identifiers[var]
            return res["domain"], res["domain_list"], res["dependencies"], res["sub_indices"]

        return None, [], [], []

    def _getProperties(self, var):
        if var in self.identifiers:
            res = self.identifiers[var]
            return res["types"], res["dim"], res["minVal"], res["maxVal"]

        return None, [], [], []

    def _getKeyForIndex(self, index, table):
        t = table
        while t != None:
            for key, value in t:

                sub_indices_list = list(value.getSubIndices())
                sub_indices_list.reverse()

                for subInd in sub_indices_list:
                    if index in subInd:
                        pos = subInd.index(index)
                        return key, pos

            t = t.getParent()

        return None, None

    def _isIndexOf(self, index, table, stmt, isLeafs = False):
        while table != None:
            key, pos = self._getKeyForIndex(index, table)
            if key != None:
                return key, pos

            table = table.getParent()

        #if not isLeafs:
        leafs = self.symbolTables.getLeafs(stmt)
        for table in sorted(leafs, key=lambda el: el["scope"], reverse=True):
            table = table["table"]

            while table != None:
                key, pos = self._getKeyForIndex(index, table)

                if key != None:
                    return key, pos

                table = table.getParent()

        return None, None

    def _tupleContainIndex(self, index, _tuple):
        for el in _tuple:
            if el["index"] == index:
                return True

        return False

    def _addTuple(self, _tuple, stmt, index, ident = None, pos = None):
        if not _tuple in self.tuples:
            self.tuples[_tuple] = {}
        
        if not stmt in self.tuples[_tuple]:
            self.tuples[_tuple][stmt] = []

        if not self._tupleContainIndex(index, self.tuples[_tuple][stmt]):
            self.tuples[_tuple][stmt].append({"index": index, "identifier": ident, "pos": pos})

    def _getTuplesByTables(self, tables, stmt, isLeafs = False):
        for table in sorted(tables, key=lambda el: el["scope"], reverse=True):
            scope = table["scope"]
            table = table["table"]
            
            while table != None:
                for key, value in table:
                    if "," in key:

                        domains = value.getProperties().getDomains()
                        
                        if len(domains) > 0:
                            indices = key.split(",")
                            for domain in domains:
                                for index in indices:
                                    ident, pos = self._isIndexOf(index, table, stmt, isLeafs)
                                    self._addTuple(domain.getName(), stmt, index, ident, pos)

                table = table.getParent()

    def _getTuples(self):
        statements = self.symbolTables.getStatements()
        for stmt in sorted(statements, reverse=True):

            scopes = self.symbolTables.getFirstScope(stmt)
            self._getTuplesByTables(scopes, stmt)

            leafs = self.symbolTables.getLeafs(stmt)
            self._getTuplesByTables(leafs, stmt, True)

        for name in self.tuples:

            
            index1 = None
            _type = None
            pos = {}

            for stmt in sorted(self.tuples[name], reverse=True):
                _tuple = self.tuples[name][stmt]

                sizeTuple = len(_tuple)
                sizeTupleNotNull = sizeTuple
                index2 = "1.."+str(sizeTuple)

                domainIdents = []

                for t in _tuple:
                    ident = t["identifier"]
                    pos[ident] = t["pos"]

                    domain = self._getDomainByIdentifier(ident)

                    if domain == None:
                        sizeTupleNotNull -= 1
                    else:
                        domainIdents.append(domain)

                if len(domainIdents) != sizeTupleNotNull or not all(map(lambda el: el == domainIdents[0], domainIdents)):
                    index1 = None
                    _type = None
                    pos = {}

                    continue

                if len(domainIdents) == 0:
                    index1 = None
                    _type = None
                    pos = {}

                    continue

                domainIdents = [domainIdents[0]]

                if len(domainIdents) == 1 and domainIdents[0] != None and domainIdents[0].strip() != "":
                    _type  = domainIdents[0]
                    domains = _type.split(",")
                    
                    if len(domains) > 1 and domains[0].strip() != "":
                        domains = map(lambda el: el.strip(), domains)
                        if all(map(lambda el: el == domains[0], domains)):
                            _type = domains[0]
                        else:
                            index1 = None
                            _type = None
                            pos = {}

                            continue

                    if _type == name or _type == ident or _type in self.tuples:
                        index1 = None
                        _type = None
                        pos = {}

                        continue

                    index1 = "INDEX_SET_"+_type
                    setint = "set of int: "+index1+" = index_set("+_type+");\n\n"
                    self.additionalParameters[index1] = setint

                    break

                index1 = None
                _type = None
                pos = {}

            if index1 == None:
                index1 = "INDEX_SET_"+name
                setint = "set of int: "+index1+";\n\n"

                self.additionalParameters[index1] = setint

            if _type == None:
                _type = "int"

            self.tuplesDeclared[name] = {"index1": index1, "index2": index2, "type": _type}

    def _getItemDomain(self, domains, totalIndices):
        size = len(domains)
        if size == 0:
            return None, None, None

        while size > 0:
            size -= 1
            domain = domains[size]
            dependencies = list(domain.getDependencies())

            if domain.getName() in dependencies:
                dependencies.remove(domain.getName())

            if len(dependencies) > 0:
                if not set(dependencies).issubset(set(totalIndices+self.parameters_and_sets)):
                    break

            deps = set(domain.getDependencies())
            deps.discard(set(totalIndices))

            return domain.getOp(), domain.getName(), list(deps)

        return None, None, None

    def _getDomainSubIndices(self, table, selectedIndices, totalIndices):
        if not isinstance(selectedIndices, str):
            selectedIndices = ",".join(selectedIndices)

        while table != None:
            value = table.lookup(selectedIndices)
            if value != None:
                op, domain, deps = self._getItemDomain(value.getProperties().getDomains(), totalIndices)

                if domain != None:
                    return op, domain, deps

            table = table.getParent()

        return None, None, None

    def _getSubIndicesDomainsByTables(self, name, tables, skip_outermost_scope = False):

        domain = ""
        domain_with_indices = ""
        dependencies_ret = []
        sub_indices_ret = []
        

        for table in sorted(tables, key=lambda el: el["scope"], reverse=True):

            table = table["table"]

            while table != None:

                if skip_outermost_scope and table.getParent() == None:
                    break

                t = table.lookup(name)
                while t == None and table != None:
                    table = table.getParent()

                    if table != None:
                        t = table.lookup(name)

                if skip_outermost_scope and table != None and table.getParent() == None:
                    break

                if t == None:
                    continue

                sub_indices_list = list(t.getSubIndices())
                sub_indices_list.reverse()

                domains = {}
                domains_with_indices = {}
                dependencies = {}
                
                for _subIndices in sub_indices_list:
                    totalIndices = list(_subIndices)
                    idx = 0
                    totalSubIndices = len(_subIndices)
                    indexes = range(totalSubIndices)
                    _subIndicesRemaining = list(_subIndices)

                    while idx < totalSubIndices:
                        _combIndices = _subIndices[idx:]
                        
                        if len(_combIndices) <= 1:
                            idx += 1
                            continue

                        op, _tuple, deps = self._getDomainSubIndices(table, _combIndices, totalIndices)
                        while _tuple == None and len(_combIndices) > 0:
                            _combIndices = _combIndices[:-1];
                            
                            if len(_combIndices) <= 1:
                                break

                            op, _tuple, deps = self._getDomainSubIndices(table, _combIndices, totalIndices)
                            
                        if _tuple != None:
                            domains[idx] = _tuple
                            domains_with_indices[idx] = {"indices": _combIndices, "set": _tuple}#"(" + ",".join(_combIndices) + ") " + op + " " + _tuple
                            dependencies[idx] = deps
                            
                            for i in range(idx, idx+len(_combIndices)):
                                indexes.remove(i)

                            idx += len(_combIndices)

                            for _comb in _combIndices:
                                _subIndicesRemaining.remove(_comb)

                        else:
                            idx += 1
                        
                    if len(indexes) > 0:
                        subIdxDomains = [self._getDomainSubIndices(table, _subIndice, totalIndices) for _subIndice in _subIndicesRemaining]
                        subIdxDomains = [d for d in subIdxDomains if d[1] != None]
                        
                        if len(subIdxDomains) == len(_subIndicesRemaining):

                            varNameSubIndices = []
                            indexes = sorted(indexes)
                            for i in range(len(subIdxDomains)):
                                ind = indexes.pop(0)
                                domains[ind] = subIdxDomains[i][1]
                                if not _subIndicesRemaining[i] in varNameSubIndices:
                                    domains_with_indices[ind] = _subIndicesRemaining[i] + " " + subIdxDomains[i][0] + " " + subIdxDomains[i][1]
                                    varNameSubIndices.append(_subIndicesRemaining[i])

                                dependencies[ind] = subIdxDomains[i][2]

                        else:
                            domains = {}
                            domains_with_indices = {}
                            dependencies = {}

                    if domains:
                        break 
                
                if len(domains) > 0:
                    domains_str = []
                    domains_ret = []
                    dependencies_ret = []
                    sub_indices_ret = _subIndices

                    for key in sorted(domains.iterkeys()):
                        if domains[key] != None:
                            domains_str.append(domains[key])
                            domains_ret.append(domains_with_indices[key])
                            dependencies_ret += dependencies[key]

                    domain += ", ".join(domains_str)
                    domain_with_indices = domains_ret#+= ", ".join(domains_ret)

                if domain != "":
                    break

                table = table.getParent()

            if domain != "":
                break

        return domain, domain_with_indices, list(set(dependencies_ret)), sub_indices_ret


    def _getSubIndicesDomainsByStatements(self, name, statements):
        domain = ""
        domains = []
        dependencies = []
        sub_indices = []
        
        for stmt in sorted(statements, reverse=True):
            
            scopes = self.symbolTables.getFirstScopeByKey(name, stmt)
            domain, domains, dependencies, sub_indices = self._getSubIndicesDomainsByTables(name, scopes)

            if domain != "":
                break
            
            leafs = self.symbolTables.getLeafs(stmt)
            domain, domains, dependencies, sub_indices = self._getSubIndicesDomainsByTables(name, leafs, True)

            if domain != "":
                break

        return domain, domains, dependencies, sub_indices

    def _getSubIndicesDomains(self, identifier):
        name = identifier.getName()
        declarations = self.symbolTables.getDeclarationsWhereKeyIsDefined(name)
        domain, domains, dependencies, sub_indices = self._getSubIndicesDomainsByStatements(name, declarations)

        if domain == "":
            statements = self.symbolTables.getStatementsByKey(name)
            domain, domains, dependencies, sub_indices = self._getSubIndicesDomainsByStatements(name, statements)

        return domain, domains, dependencies, sub_indices


    def _getDomainsByTables(self, name, tables, _types, dim, minVal, maxVal, skip_outermost_scope = False):
        
        for table in sorted(tables, key=lambda el: el["scope"], reverse=True):

            table = table["table"]

            while table != None:

                if skip_outermost_scope and table.getParent() == None:
                    break

                t = table.lookup(name)
                while t == None and table != None:
                    table = table.getParent()

                    if table != None:
                        t = table.lookup(name)

                if skip_outermost_scope and table != None and table.getParent() == None:
                    break

                if t == None:
                    continue

                prop = t.getProperties()
                domains = prop.getDomains()

                for domain in domains:
                    inserted = False
                    for _type in _types:
                        if domain.getName() == _type.getName():
                            inserted = True # last occurrence prevails (it is scanning from bottom to top, right to left)
                            break

                    if not inserted:
                        _types.append(domain)

                if prop.getDimension() != None and prop.getDimension() > 1 and dim == None:
                    dim = prop.getDimension()

                if prop.getMinVal() != None:
                    if minVal == None or minVal > prop.getMinVal():
                        minVal = prop.getMinVal()

                if prop.getMaxVal() != None:
                    if maxVal == None or maxVal < prop.getMaxVal():
                        maxVal = prop.getMaxVal()

                table = table.getParent()

        return _types, dim, minVal, maxVal

    def _getDomainsByStatements(self, name, statements, _types, dim, minVal, maxVal):
        
        for stmt in sorted(statements, reverse=True):
            
            scopes = self.symbolTables.getFirstScopeByKey(name, stmt)
            _types, dim, minVal, maxVal = self._getDomainsByTables(name, scopes, _types, dim, minVal, maxVal, False)

            leafs = self.symbolTables.getLeafs(stmt)
            _types, dim, minVal, maxVal = self._getDomainsByTables(name, leafs, _types, dim, minVal, maxVal, True)

        return _types, dim, minVal, maxVal

    def _getDomain(self, identifier):
        _types = []
        dim = None
        minVal = None
        maxVal = None

        name = identifier.getName()
        declarations = self.symbolTables.getDeclarationsWhereKeyIsDefined(name)
        _types, dim, minVal, maxVal = self._getDomainsByStatements(name, declarations, _types, dim, minVal, maxVal)

        statements = self.symbolTables.getStatementsByKey(name)
        _types, dim, minVal, maxVal = self._getDomainsByStatements(name, statements, _types, dim, minVal, maxVal)

        return _types, dim, minVal, maxVal

    def _addDependences(self, value, stmtIndex, dependences):
        names = value.getDependencies(self)

        if names != None and len(names) > 0:
            for name in names:
                if not self.genBelongsToList.has(GenBelongsTo(name, stmtIndex)):
                    dependences.append(name)

    def _getDependences(self, identifier):
        dependences = []

        decl = self.genDeclarations.get(identifier.getName())
        if decl != None:
            value = decl.getValue()
            if value != None:
                self._addDependences(value.attribute, decl.getStmtIndex(), dependences)

            value = decl.getDefault()
            if value != None:
                self._addDependences(value.attribute, decl.getStmtIndex(), dependences)

            ins = decl.getIn()
            if ins != None and len(ins) > 0:
                for pSet in ins:
                    self._addDependences(pSet.attribute, decl.getStmtIndex(), dependences)

            withins = decl.getWithin()
            if withins != None and len(withins) > 0:
                for pSet in withins:
                    self._addDependences(pSet.attribute, decl.getStmtIndex(), dependences)

            relations = decl.getRelations()
            if relations != None and len(relations) > 0:
                for pRel in relations:
                    self._addDependences(pRel.attribute, decl.getStmtIndex(), dependences)

            idxExpression = decl.getIndexingExpression()
            if idxExpression != None:
                self._addDependences(idxExpression, decl.getStmtIndex(), dependences)

        return dependences

    def _checkAddDependence(self, graph, name, dep):
        return dep != name and not dep in graph[name] and dep in self.parameters_and_sets

    def _generateGraphAux(self, graph, genObj):
        if len(genObj) > 0:
            for identifier in genObj.getAll():
                
                name = identifier.getName()
                if not name in graph:
                    graph[name] = []
                
                dependences = self._getDependences(identifier)

                if len(dependences) > 0:
                    for dep in dependences:
                        if self._checkAddDependence(graph, name, dep):
                            graph[name].append(dep)

                _domain, domains_vec, dependencies_vec, sub_indices = self._getSubIndicesDomainsAndDependencies(identifier.getName())

                if len(dependencies_vec) > 0:
                    for dep in dependencies_vec:
                        if self._checkAddDependence(graph, name, dep):
                            graph[name].append(dep)

    # Auxiliary Methods
    def _generateGraph(self):
        
        graph = {}

        self._generateGraphAux(graph, self.genSets)
        self._generateGraphAux(graph, self.genParameters)

        return graph

    # Get the MathProg code for a given relational expression
    def _getCodeValue(self, value):
        val = value.generateCode(self)
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    # Get the MathProg code for a given sub-indice
    def _getCodeID(self, id_):
        if isinstance(id_, ValuedNumericExpression):
            if isinstance(id_.value, Identifier):
                id_.value.setIsSubIndice(True)

        elif isinstance(id_, Identifier):
            id_.setIsSubIndice(True)

        val = id_.generateCode(self)
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    # Get the MathProg code for a given entry
    def _getCodeEntry(self, entry): return entry.generateCode(self)

    # Get the MathProg code for a given entry
    def _getCodeEntryByKey(self, entry):
        for key in entry:
            conj = "/\\" if key == "and" else "\\/"
            return conj, entry[key].generateCode(self)

    # Get the MathProg code for a given objective
    def _getCodeObjective(self, objective):
        self.objectiveNumber += 1
        return objective.generateCode(self)

    # Get the MathProg code for a given constraint
    def _getCodeConstraint(self, constraint):
        if isinstance(constraint, Constraint):
            self.constraintNumber += 1
            return "constraint " + constraint.generateCode(self)

        return ""

    def formatNumber(self, number):
        return ("0" if number[0] == "." else "") + number

    def notInTypesThatAreNotDeclarable(self, value):
        if isinstance(value, Tuple):
            return True
        
        value = value.getSymbol()
        
        return not value.isBinary and not value.isInteger and not value.isNatural and not value.isReal and not value.isSymbolic and not \
                value.isLogical and not value.isDeclaredAsVar and not value.isDeclaredAsParam and not value.isDeclaredAsSet and not \
                isinstance(value, str)

    def _removeTypesThatAreNotDeclarable(self, _types):
        return filter(lambda el: not el.getName() in [Constants.VARIABLES, Constants.PARAMETERS, Constants.SETS], _types)

    def _removePreDefinedTypes(self, _types):
        return filter(lambda el: not el in [Constants.VARIABLES, Constants.PARAMETERS, Constants.SETS] and 
                        el != Constants.BINARY and el.replace(" ", "") != Constants.BINARY_0_1 and 
                        not el.startswith(Constants.INTEGER) and not el.startswith(Constants.REALSET) and 
                        not el.startswith(Constants.SYMBOLIC) and not el.startswith(Constants.LOGICAL), _types)

    def _getTypes(self, _types):
        return filter(lambda el: el.getName().startswith(Constants.BINARY) or el.getName().replace(" ", "") == Constants.BINARY_0_1 or el.getName().startswith(Constants.INTEGER) or el.getName().startswith(Constants.REALSET), _types)

    def _getModifiers(self, _types):
        return filter(lambda el: el.getName().startswith(Constants.LOGICAL) or el.getName().startswith(Constants.SYMBOLIC), _types)

    def _getIndices(self, sub_indices, domains_with_indices):
        indices_ins = list(sub_indices)

        for d in domains_with_indices:
            
            if not isinstance(d, str):
                setName = d["set"]
                
                if setName in self.tuplesDeclared:
                    index1 = self.tuplesDeclared[setName]["index1"]
                    indices = d["indices"]
                    index = indices[0]

                    c = 0
                    cs = []
                    for i in indices:
                        if not c in cs:
                            repl = setName + "["+index+","+str(c)+"]"
                            cs.append(c)
                            c += 1

                            ind = [j for j, v in enumerate(indices_ins) if v == i]
                            for j in ind:
                                indices_ins[j] = repl

        return indices_ins

    def _getDomainsWithIndices(self, domains_with_indices):
        domains = []
        for d in domains_with_indices:
            
            if isinstance(d, str):
                domains.append(d)

            else:
                setName = d["set"]
                
                if setName in self.tuplesDeclared:
                    index1 = self.tuplesDeclared[setName]["index1"]
                    indices = d["indices"]
                    index = indices[0]
                    domains.append(index + " in " + index1)

                else:
                    domains.append("")

        return domains

    def _getDomains(self, domains):
        res = []
        for d in domains:
            
            if d in self.tuplesDeclared:
                _type = self.tuplesDeclared[d]["type"]
                index2 = self.tuplesDeclared[d]["index2"]
                size = int(index2[3:])

                for i in range(size):
                    res.append(_type)

            else:
                res.append(d)

        return res

    def _getRelationalConstraints(self, _type, varName, isArray, sub_indices, domains_with_indices):
        rest = _type
        rest = rest.strip()

        if rest != "":
            var = ""
            const = ""

            if isArray:
                indices_ins = self._getIndices(sub_indices, domains_with_indices)
                var = varName + "[" + ",".join(indices_ins) + "]"

            else:
                var = varName
                
            m = re.search(r"(>|>=)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?", rest)
            if m:
                rel = ""
                groups = m.groups(0)
                rel += " " + groups[0] + " "
                rel += self.formatNumber(groups[1])

                if groups[2] != None and groups[2] != 0:
                    rel += groups[2]

                const += var + rel

            m = re.search(r"(<|<=)\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?", rest)
            if m:
                rel = ""
                groups = m.groups(0)
                rel += " " + groups[0] + " "
                rel += self.formatNumber(groups[1])

                if groups[2] != None and groups[2] != 0:
                    rel += groups[2]
                
                if const != "":
                    const += " /\\ "

                const += var + rel

            cnt = ""
            if isArray:
                domains = self._getDomainsWithIndices(domains_with_indices)
                cnt += "constraint forall("+", ".join(domains)+")("+const+");";
            else:
                cnt += "constraint "+const + ";";

            return cnt

        return None

    def _declareVars(self):
        """
        Generate the MathProg code for the declaration of identifiers
        """

        varStr = ""
        if len(self.genVariables) > 0:
            
            for var in self.genVariables.getAll():
                if not self.genParameters.has(var) and not self.genSets.has(var):
                    
                    domain = None
                    varName = var.getName()
                    _type = None
                    isArray = False
                    includedVar = False

                    varDecl = self.genDeclarations.get(varName)

                    domain, domains_with_indices, dependencies_vec, sub_indices_vec = self._getSubIndicesDomainsAndDependencies(varName)
                    _types, dim, minVal, maxVal = self._getProperties(varName)

                    if domain and domain.strip() != "":
                        domains = domain.split(",")
                        domains = self._getDomains(domains)
                        domain = ",".join(domains)
                        #logical = self._getLogicalExpressionOfDeclaration(varDecl, varName, dependencies_vec, sub_indices_vec)
                        varStr += "array[" + domain + "]"; #("" if logical == None else " : " + logical) + "}"
                        isArray = True

                    elif minVal != None and maxVal != None:
                        domain = str(minVal)+".."+str(maxVal)
                        varStr += "array["+domain+"]"
                        isArray = True
                    
                    if not domain and varDecl != None:
                        size = len(varDecl.getSubIndices())
                        if size > 0:
                            varStr += "array[" + ",".join(["int"]*size) + "] of "
                        #if varDecl.getIndexingExpression() != None:
                        #    domain = varDecl.getIndexingExpression().generateCode(self)
                        #    varStr += "array[" + domain + "] of "
                    

                    _types = self._removeTypesThatAreNotDeclarable(_types)
                    _types = self._getTypes(_types)
                    
                    if len(_types) > 0:
                        _type = _types[0].getName()
                        
                        if _type == Constants.BINARY_0_1 or _type == Constants.BINARY:
                            _type = "bool";

                        elif _type.startswith(Constants.INTEGER):
                            const =  self._getRelationalConstraints(_type[8:], varName, isArray, sub_indices_vec, domains_with_indices)

                            if const != None:
                                self.additionalConstraints.append(const)

                            _type = "int";

                        else:
                            const =  self._getRelationalConstraints(_type[8:], varName, isArray, sub_indices_vec, domains_with_indices)
                            
                            if const != None:
                                self.additionalConstraints.append(const)

                            _type = "float";

                        if _type.strip() != "":
                            includedVar = True
                            if isArray:
                                varStr += " of var " + _type
                            else:
                                varStr += "var " + _type

                    elif varDecl != None:
                        ins_vec = varDecl.getIn()
                        ins_vec = self._removePreDefinedTypes(map(lambda el: el.attribute.generateCode(self), ins_vec))

                        if ins_vec != None and len(ins_vec) > 0:
                            ins = ins_vec[-1]

                            if ins != "":
                                includedVar = True
                                if isArray:
                                    varStr += " of var " + ins
                                else:
                                    varStr += "var " + ins

                    if not includedVar:
                        if isArray:
                            varStr += " of var float"
                        else:
                            varStr += "var float"

                    if varDecl != None:
                        cnt = ""
                        attr = varDecl.getRelationEqualTo()
                        if attr != None:
                            if isArray:
                                domains = self._getDomainsWithIndices(domains_with_indices)
                                indices = self._getIndices(sub_indices_vec, domains_with_indices)
                                cnt += "constraint forall("+", ".join(domains)+")(" + varName + "["+",".join(indices)+"] = " + attr.attribute.generateCode(self) + ");";
                            else:
                                cnt += "constraint " + varName + " = " + attr.attribute.generateCode(self) + ";";

                            self.additionalConstraints.append(cnt)

                        else:
                            cnt = ""
                            cntAux = ""
                            attr = varDecl.getRelationLessThanOrEqualTo()

                            if attr != None:
                                if isArray:
                                    indices = self._getIndices(sub_indices_vec, domains_with_indices)
                                    cntAux += varName + "["+",".join(indices)+"] <= " + attr.attribute.generateCode(self)
                                else:
                                    cntAux += varName + " <= " + attr.attribute.generateCode(self)

                            attr = varDecl.getRelationGreaterThanOrEqualTo()
                            if attr != None:
                                if cntAux != "":
                                    cntAux += " /\\ "

                                if isArray:
                                    indices = self._getIndices(sub_indices_vec, domains_with_indices)
                                    cntAux += varName + "["+",".join(indices)+"] >= " + attr.attribute.generateCode(self)
                                else:
                                    cntAux += varName + " >= " + attr.attribute.generateCode(self)

                            if cntAux != "":
                                cnt += "constraint " + cntAux + ";"
                                self.additionalConstraints.append(cnt)

                    '''
                    if len(_types) > 0:
                        _type = _types[0].getName()
                        _type = _type if _type != Constants.BINARY_0_1 else Constants.BINARY
                        _type = _type if not _type.startswith(Constants.REALSET) else _type[8:]

                        if _type.strip() != "":
                            varStr += " " + _type

                    if varDecl != None:
                        attr = varDecl.getRelationEqualTo()
                        if attr != None:
                            varStr += ", = " + attr.attribute.generateCode(self)

                        else:
                            attr = varDecl.getRelationLessThanOrEqualTo()
                            if attr != None:
                                varStr += ", <= " + attr.attribute.generateCode(self)

                            attr = varDecl.getRelationGreaterThanOrEqualTo()
                            if attr != None:
                                varStr += ", >= " + attr.attribute.generateCode(self)
                    '''

                    varStr += ": " + varName
                    varStr += ";\n\n"

        return varStr

    def _declareParam(self, _genParameter):
        paramStr = ""
        param = _genParameter.getName()
        domain = None
        _type = None
        isArray = False
        includedType = False

        varDecl = self.genDeclarations.get(_genParameter.getName())

        domain, domains_vec, dependencies_vec, sub_indices_vec = self._getSubIndicesDomainsAndDependencies(_genParameter.getName())
        _types, dim, minVal, maxVal = self._getProperties(_genParameter.getName())

        if domain != None and domain.strip() != "":
            domains = domain.split(",")
            domains = self._getDomains(domains)
            domain = ",".join(domains)
            #logical = self._getLogicalExpressionOfDeclaration(varDecl, param, dependencies_vec, sub_indices_vec)
            paramStr += "array[" + domain + "]"
            isArray = True

        elif minVal != None and maxVal != None:
            paramStr += "array["+str(minVal)+".."+str(maxVal)+"]"
            isArray = True

        
        if not domain and varDecl != None:
            if varDecl.getIndexingExpression() != None:
                domain = varDecl.getIndexingExpression().generateCode(self)
                paramStr += "array[" + domain + "] of "
        

        _types = self._removeTypesThatAreNotDeclarable(_types)
        _types = self._getTypes(_types)

        if len(_types) > 0:
            _type = _types[0].getName()
            if _type == Constants.BINARY_0_1 or _type == Constants.BINARY:
                _type = "bool";
            elif _type.startswith(Constants.INTEGER):
                _type = "int";
            else:
                _type = "float2";

            if _type.strip() != "":
                includedType = True

                if isArray:
                    paramStr += " of " + _type
                else:
                    paramStr += _type

        elif varDecl != None:
            ins_vec = varDecl.getIn()
            ins_vec = self._removePreDefinedTypes(map(lambda el: el.attribute.generateCode(self), ins_vec))
            if ins_vec != None and len(ins_vec) > 0:
                ins = ins_vec[-1]

                if ins != "":
                    includedType = True

                    if isArray:
                        paramStr += " of " + ins
                    else:
                        paramStr += ins

        if not includedType:
            if _genParameter.getIsInteger():
                _type = "int"
            else:
                _type = "float"

            if isArray:
                paramStr += " of " + _type
            else:
                paramStr += _type

        '''
        modifiers = self._getModifiers(_types)

        if len(modifiers) > 0:
            _type = modifiers[0].getName()

            if _type.strip() != "":
                paramStr += " " + _type
        else:
            
            _types = self._getTypes(_types)
            

            if len(_types) > 0:
                _type = _types[0].getName()
                _type = _type if _type != Constants.BINARY_0_1 else Constants.BINARY
                _type = _type if not _type.startswith(Constants.REALSET) else _type[8:]

                if _type.strip() != "":
                    paramStr += " " + _type

        if varDecl != None:
            ins_vec = varDecl.getIn()
            ins_vec = self._removePreDefinedTypes(map(lambda el: el.attribute.generateCode(self), ins_vec))
            if ins_vec != None and len(ins_vec) > 0:
                ins = ",".join(map(lambda el: "in " + el, ins_vec))

                if ins != "":
                    paramStr += ", " + ins

            relations = varDecl.getRelations()
            if relations != None and len(relations) > 0:
                paramStr += ", " + ",".join(map(lambda el: el.op + " " + el.attribute.generateCode(self), relations))

            if varDecl.getDefault() != None:
                default = ", default " + varDecl.getDefault().attribute.generateCode(self)
                paramStr += default

            if varDecl.getValue() != None:
                value = ", := " + varDecl.getValue().attribute.generateCode(self)
                paramStr += value
                self.genValueAssigned.add(GenObj(param))
        '''

        paramStr += ": " + param

        if varDecl != None:
            if varDecl.getValue() != None:
                value = " = " + varDecl.getValue().attribute.generateCode(self)
                paramStr += value
                self.genValueAssigned.add(GenObj(param))

        paramStr += ";\n\n"

        return paramStr

    def _declareSet(self, _genSet):
        name = _genSet.getName()
        setStr = ""
        index2 = ""

        if name in self.tuplesDeclared:
            _tuple = self.tuplesDeclared[name]
            index1 = _tuple["index1"]
            index2 = _tuple["index2"]
            _type  = _tuple["type"]

            setStr += "array["+index1+", "+index2+"] of "+_type+": " + name
        
        else:
            setStr += "enum " + name
        
        '''
        domain = None
        dimen = None

        #varDecl = self.genDeclarations.get(setName)

        domain, domains_vec, dependencies_vec, sub_indices_vec = self._getSubIndicesDomainsAndDependencies(setName)
        _types, dim, minVal, maxVal = self._getProperties(setName)
        
        if domain and domain.strip() != "":
            logical = self._getLogicalExpressionOfDeclaration(varDecl, setName, dependencies_vec, sub_indices_vec)
            setStr += "{" + domain + ("" if logical == None else " : " + logical) + "}"
        elif minVal != None and maxVal != None:
            setStr += "{"+str(minVal)+".."+str(maxVal)+"}"

        if not domain and varDecl != None:
            if varDecl.getIndexingExpression() != None:
                domain = varDecl.getIndexingExpression().generateCode(self)
                setStr += "{" + domain + "}"

        if dim != None and dim > 1:
            setStr += " dimen " + str(dim)

        if varDecl != None:
            subsets = varDecl.getWithin()
            if subsets != None and len(subsets) > 0:
                setStr += ", " + ",".join(map(lambda el: el.op + " " + el.attribute.generateCode(self), subsets))

            ins_vec = varDecl.getIn()
            ins_vec = self._removePreDefinedTypes(map(lambda el: el.attribute.generateCode(self), ins_vec))
            if ins_vec != None and len(ins_vec) > 0:
                ins = ",".join(map(lambda el: "in " + el, ins_vec))

                if ins != "":
                    setStr += ", " + ins

            if varDecl.getDefault() != None:
                default = ", default " + varDecl.getDefault().attribute.generateCode(self)
                setStr += default

            if varDecl.getValue() != None:
                value = ", := " + varDecl.getValue().attribute.generateCode(self)
                setStr += value
                self.genValueAssigned.add(GenObj(setName))
        '''

        setStr += ";\n\n"
        

        return setStr

    def _declareSetsAndParams(self):

        paramSetStr = ""
        if len(self.topological_order) > 0:
            for paramSetIn in self.topological_order:
                _genObj = self.genParameters.get(paramSetIn)

                if _genObj != None:
                    paramSetStr += self._declareParam(_genObj)
                else:
                    _genObj = self.genSets.get(paramSetIn)

                    if _genObj != None:
                        paramSetStr += self._declareSet(_genObj)

        return paramSetStr

    def _declareDataParam(self, _genParameter):
        res = ""

        if not self.genValueAssigned.has(_genParameter.getName()):
            value = ""
            
            if len(self.identifiers[_genParameter.getName()]["sub_indices"]) == 0:
                if _genParameter.getIsSymbolic():
                    value += " ''"
                else:
                    value += " 0"

            res += "param " + _genParameter.getName() + " :=" + value + ";\n\n"

        return res

    def _declareDataSet(self, _genSet):
        res = ""

        if not self.genValueAssigned.has(_genSet.getName()):
            sub_indices = self.identifiers[_genSet.getName()]["sub_indices"]
            if len(sub_indices) > 0:
                dimenIdx = "[" + ",".join(["0"] * len(sub_indices)) + "]"
            else:
                dimenIdx = ""

            res += "set " + _genSet.getName() + dimenIdx + " :=;\n\n"

        return res

    def _declareDataSetsAndParams(self):
        res = ""

        if len(self.topological_order) > 0:
            for paramSetIn in self.topological_order:
                _genObj = self.genParameters.get(paramSetIn)

                if _genObj != None:
                    res += self._declareDataParam(_genObj)
                else:
                    _genObj = self.genSets.get(paramSetIn)

                    if _genObj != None:
                        res += self._declareDataSet(_genObj)

        if res != "":
            res = "data;\n\n" + res + "\n"

        return res

    def _initialize(self):
        self.init()
        graph = self._generateGraph()
        self.topological_order = sort_topologically_stackless(graph)

    def _preModel(self):
        res = ""

        setsAndParams = self._declareSetsAndParams()
        if setsAndParams != "":
            res += setsAndParams

        if len(self.additionalParameters) > 0:
            res += "".join([v for k,v in self.additionalParameters.iteritems()])

        identifiers = self._declareVars()
        if identifiers != "":
            if res != "":
                res += "\n"

            res += identifiers

        if len(self.additionalConstraints) > 0:
            res += "\n" + "\n\n".join(self.additionalConstraints) + "\n"

        return res
    
    def _posModel(self):
        res = "\nsolve;\n\n\n"
        res += self._declareDataSetsAndParams()
        res += "end;"

        return res

    def generateCode_Main(self, node):
        return node.problem.generateCode(self)

    def generateCode_LinearEquations(self, node):
        self._initialize()

        res = node.constraints.generateCode(self) + "\n\nsolve satisfy;\n\n"

        preModel = self._preModel()
        if preModel != "":
            preModel += "\n"

        res = preModel + res

        return res

    def generateCode_LinearProgram(self, node):
        self._initialize()

        res = ""

        if node.constraints:
            res += node.constraints.generateCode(self) + "\n\n"
        
        if node.declarations:
            res += node.declarations.generateCode(self) + "\n\n"

        res += "\n\n" + node.objectives.generateCode(self) + "\n\n"

        preModel = self._preModel()
        if preModel != "":
            preModel += "\n"

        res = preModel + res

        return res

    # Objectives
    def generateCode_Objectives(self, node):
        #self.totalObjectives = len(node.objectives)
        #return "\n\n".join(map(self._getCodeObjective, node.objectives))
        obj = node.objectives[0]
        objStr = "var float: obj = " + obj.generateCode(self)
        objStr += ";\n\nsolve " + obj.type + " obj;\n\n";

        return objStr;

    # Objective Function
    def generateCode_Objective(self, node):
        """
        Generate the code in MathProg for this Objective
        """
        '''
        domain_str = ""
        if node.domain:
            idxExpression = node.domain.generateCode(self)
            if idxExpression:
                domain_str = " {" + idxExpression + "}"
        '''
        self.scope = 0
        self.stmtIndex += 1

        self.scopes[self.stmtIndex] = {}
        self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

        previousParentScope = self.parentScope
        self.parentScope = self.scope

        res = node.linearExpression.generateCode(self)

        self.parentScope = previousParentScope

        return res

    # Constraints
    def generateCode_Constraints(self, node):
        return "\n\n".join(filter(lambda el: el != "" and el != None, map(self._getCodeConstraint, node.constraints)))

    def generateCode_Constraint(self, node):
        self.scope = 0
        self.stmtIndex += 1

        self.scopes[self.stmtIndex] = {}
        self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

        previousParentScope = self.parentScope
        self.parentScope = self.scope

        res = ""
        hasForall = False

        if node.indexingExpression:
            idxExpression = node.indexingExpression.generateCode(self)

            if idxExpression.strip() != "":
                res += "forall(" + idxExpression + ")("
                hasForall = True
            else:
                res += ""
        else:
            res += ""

        res += node.constraintExpression.generateCode(self) + (")" if hasForall else "") + ";"

        self.parentScope = previousParentScope

        return res

    def generateCode_ConstraintExpression2(self, node):
        return node.linearExpression1.generateCode(self) + " " + node.op + " " + node.linearExpression2.generateCode(self)

    def generateCode_ConstraintExpression3(self, node):

        if node.op == ConstraintExpression.LE:
            oppOp = ConstraintExpression.GE
        else:
            oppOp = ConstraintExpression.LE

        res  = node.linearExpression.generateCode(self) + " " + node.op + " " + node.numericExpression2.generateCode(self) + " /\\ "
        res += node.linearExpression.generateCode(self) + " " + oppOp + " " + node.numericExpression1.generateCode(self)

        return res

    # Linear Expression
    def generateCode_ValuedLinearExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_LinearExpressionBetweenParenthesis(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "(" + node.linearExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_LinearExpressionWithArithmeticOperation(self, node):
        return node.expression1.generateCode(self) + " " + node.op + " " + node.expression2.generateCode(self)

    def generateCode_MinusLinearExpression(self, node):
        return "-" + node.linearExpression.generateCode(self)

    def generateCode_IteratedLinearExpression(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        SUM = "sum"

        if node.numericExpression:
            res = SUM + "(" + node.indexingExpression.generateCode(self) + "..(" + node.numericExpression.generateCode(self) + "))("
        else:
            res = SUM + "(" + node.indexingExpression.generateCode(self) + ")("

        res += node.linearExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_ConditionalLinearExpression(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.linearExpression1.generateCode(self)

        if node.linearExpression2:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": previousParentScope}

            res += " else " + node.linearExpression2.generateCode(self)

        res += " endif"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    # Numeric Expression
    def generateCode_NumericExpressionWithFunction(self, node):
        res = str(node.function) + "("

        if node.numericExpression1 != None:
            res += node.numericExpression1.generateCode(self)

        if node.numericExpression2 != None:
            res += ", " + node.numericExpression2.generateCode(self)

        res += ")"

        return res

    def generateCode_ValuedNumericExpression(self, node):
        self.turnStringsIntoInts = True
        res = node.value.generateCode(self)
        self.turnStringsIntoInts = False
        return res

    def generateCode_NumericExpressionBetweenParenthesis(self, node):
        
        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "(" + node.numericExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_NumericExpressionWithArithmeticOperation(self, node):
        res = node.numericExpression1.generateCode(self) + " " + node.op + " "

        if node.op == NumericExpressionWithArithmeticOperation.POW and not (isinstance(node.numericExpression2, ValuedNumericExpression) or isinstance(node.numericExpression2, NumericExpressionBetweenParenthesis)):
            res += "(" + node.numericExpression2.generateCode(self) + ")"
        else:
            res += node.numericExpression2.generateCode(self)

        return res

    def generateCode_MinusNumericExpression(self, node):
        return "-" + node.numericExpression.generateCode(self)

    def generateCode_IteratedNumericExpression(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        if node.supNumericExpression:
            res = str(node.op) + "(" + node.indexingExpression.generateCode(self) + "..(" + node.supNumericExpression.generateCode(self) + "))("
        else:
            res = str(node.op) + "(" + node.indexingExpression.generateCode(self) + ")("

        res += node.numericExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_ConditionalNumericExpression(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.numericExpression1.generateCode(self)

        if node.numericExpression2:
            res += " else " + node.numericExpression2.generateCode(self)

        res += " endif"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    # Symbolic Expression
    def generateCode_SymbolicExpressionWithFunction(self, node):
        res = str(node.function) + "("
        if node.function == SymbolicExpressionWithFunction.SUBSTR:
            res += node.symbolicExpression.generateCode(self) + "," + node.numericExpression1.generateCode(self)
            if node.numericExpression2 != None:
                res += "," + node.numericExpression2.generateCode(self)
        
        elif node.function == SymbolicExpressionWithFunction.TIME2STR:
            res += node.numericExpression1.generateCode(self) + "," + node.symbolicExpression.generateCode(self)

        res += ")"

        return res

    def generateCode_StringSymbolicExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_SymbolicExpressionBetweenParenthesis(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "(" + node.symbolicExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_SymbolicExpressionWithOperation(self, node):
        return node.symbolicExpression1.generateCode(self) + " " + node.op + " " + node.symbolicExpression2.generateCode(self)

    def generateCode_ConditionalSymbolicExpression(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.symbolicExpression1.generateCode(self)

        if node.symbolicExpression2 != None:

            if self.stmtIndex > -1:
                self.scope += 1
                self.scopes[self.stmtIndex][self.scope] = {"parent": previousParentScope}

            res += " else " + node.symbolicExpression2.generateCode(self)

        res += " endif"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    # Indexing Expression
    def generateCode_IndexingExpression(self, node):
        indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, node.entriesIndexingExpression))
        res = ", ".join(indexing)

        if node.logicalExpression:
            res += " where " + node.logicalExpression.generateCode(self)

        return res
    
    # Entry Indexing Expression
    def generateCode_EntryIndexingExpressionWithSet(self, node):
        if isinstance(node.identifier, ValueList):
            values = filter(self.notInTypesThatAreNotDeclarable, node.identifier.getValues())

            if len(values) > 0:
                setExpression = node.setExpression.generateCode(self)
                return ", ".join(map(lambda var: var.generateCode(self) + " " + node.op + " " + setExpression, values))

        elif isinstance(node.identifier, Tuple) or isinstance(node.identifier, TupleList):
            setExpression = node.setExpression.generateCode(self)

            if setExpression in self.tuplesDeclared:

                index1 = self.tuplesDeclared[setExpression]["index1"]
                values = node.identifier.getValues()

                self.replaceNewIndices = False
                idx = values[0].generateCode(self)
                self.replaceNewIndices = True

                if not "new_indices" in self.scopes[self.stmtIndex][self.scope]:
                    self.scopes[self.stmtIndex][self.scope]["new_indices"] = {}

                self.countNewIndices = 0
                self.includeNewIndices = True

                for v in values:
                    self.newIndexExpression = setExpression+"["+idx+","+str(self.countNewIndices)+"]"
                    v.generateCode(self)

                self.countNewIndices = 0
                self.includeNewIndices = False
                
                return idx + " " + node.op + " " + index1

            else:
                return node.identifier.generateCode(self) + " " + node.op + " " + setExpression

        elif self.notInTypesThatAreNotDeclarable(node.identifier):
            return node.identifier.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self)

        return ""

    def generateCode_EntryIndexingExpressionCmp(self, node):
        self.turnStringsIntoInts = True

        if node.op == EntryIndexingExpressionCmp.NEQ:
            op = "!="
        else:
            op = node.op

        res = node.identifier.generateCode(self) + " " + op + " " + node.numericExpression.generateCode(self)

        self.turnStringsIntoInts = False

        return res

    def generateCode_EntryIndexingExpressionEq(self, node):
        self.turnStringsIntoInts = True

        if node.hasSup:
            res = node.identifier.generateCode(self) + " in " + Utils._getInt(node.value.generateCode(self)) # completed in generateCode_IteratedNumericExpression
        else:
            res = node.identifier.generateCode(self) + " in " + node.value.generateCode(self)

        self.turnStringsIntoInts = False

        return res

    # Logical Expression
    def generateCode_LogicalExpression(self, node):
        res = ""
        first = True

        for i in range(len(node.entriesLogicalExpression)):
            conj, code = self._getCodeEntryByKey(node.entriesLogicalExpression[i])

            if code != 0:
                if first:
                    first = False
                    res += code
                else:
                    res += " " + conj + " " + code

        return res

    # Entry Logical Expression
    def generateCode_EntryLogicalExpressionRelational(self, node):
        self.turnStringsIntoInts = True
        if node.op == EntryLogicalExpressionRelational.NEQ:
            op = "!="
        else:
            op = node.op


        res = node.numericExpression1.generateCode(self) + " " + op + " " + node.numericExpression2.generateCode(self)
        self.turnStringsIntoInts = False

        return res

    def generateCode_EntryLogicalExpressionWithSet(self, node):
        if isinstance(node.identifier, ValueList):
            values = filter(self.notInTypesThatAreNotDeclarable, node.identifier.getValues())

            if len(values) > 0:
                setExpression = node.setExpression.generateCode(self)
                return ", ".join(map(lambda var: var.generateCode(self) + " " + node.op + " " + setExpression, values))

        elif isinstance(node.identifier, Tuple) or isinstance(node.identifier, TupleList):
            setExpression = node.setExpression.generateCode(self)

            if setExpression in self.tuplesDeclared:
                index1 = self.tuplesDeclared[setExpression]["index1"]
                values = node.identifier.getValues()
                idx = values[0].generateCode(self)

                if not "new_indices" in self.scopes[self.stmtIndex][self.scope]:
                    self.scopes[self.stmtIndex][self.scope]["new_indices"] = {}

                self.countNewIndices = 0
                self.includeNewIndices = True

                for v in values:
                    self.newIndexExpression = setExpression+"["+idx+","+str(self.countNewIndices)+"]"
                    v.generateCode(self)

                self.countNewIndices = 0
                self.includeNewIndices = False

                return idx + " " + node.op + " " + index1

            else:
                return node.identifier.generateCode(self) + " " + node.op + " " + setExpression

        elif self.notInTypesThatAreNotDeclarable(node.identifier):
            return node.identifier.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self)

        return ""
        '''
        if node.isBinary or node.isInteger or node.isNatural or node.isReal or node.isSymbolic or \
            node.isLogical or node.isDeclaredAsVar or node.isDeclaredAsParam or node.isDeclaredAsSet or \
            isinstance(node.identifier, str):
            return ""
        
        return node.identifier.generateCode(self) + " " + node.op + " " + node.setExpression.generateCode(self)
        '''

    def generateCode_EntryLogicalExpressionWithSetOperation(self, node):
        return node.setExpression1.generateCode(self) + " " + node.op + " " + node.setExpression2.generateCode(self)

    def generateCode_EntryLogicalExpressionIterated(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res =  node.op + "forall(" + node.indexingExpression.generateCode(self) + ")(" +  node.logicalExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_EntryLogicalExpressionBetweenParenthesis(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "(" + node.logicalExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_EntryLogicalExpressionNot(self, node):
        return "not " + node.logicalExpression.generateCode(self)

    def generateCode_EntryLogicalExpressionNumericOrSymbolic(self, node):
        return node.numericOrSymbolicExpression.generateCode(self)

    # Set Expression
    def generateCode_SetExpressionWithValue(self, node):
        if not isinstance(node.value, str):
            return node.value.generateCode(self)
        else:
            return node.value

    def generateCode_SetExpressionWithIndices(self, node):
        var_gen = ""
        if not isinstance(node.identifier, str):
            var_gen = node.identifier.generateCode(self)
        else:
            var_gen = node.identifier

        return  var_gen

    def generateCode_SetExpressionWithOperation(self, node):
        return node.setExpression1.generateCode(self) + " " + node.op + " " + node.setExpression2.generateCode(self)

    def generateCode_SetExpressionBetweenBraces(self, node):
        if node.setExpression != None:
            self.turnStringsIntoInts = True
            setExpression = node.setExpression.generateCode(self)
            self.turnStringsIntoInts = False
        else:
            setExpression = ""

        return "{" + setExpression + "}"

    def generateCode_SetExpressionBetweenParenthesis(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res =  "(" + node.setExpression.generateCode(self) + ")"
        
        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_IteratedSetExpression(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        integrands = ""
        if node.integrands != None:
            if len(node.integrands) == 1:
                integrands += node.integrands[0].generateCode(self)
            else:
                integrands += "(" + ",".join(map(lambda el: el.generateCode(self), node.integrands)) + ")"

        res = "setof {" + node.indexingExpression.generateCode(self) + "} " + integrands

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_ConditionalSetExpression(self, node):
        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.setExpression1.generateCode(self)

        if node.setExpression2:
            if self.stmtIndex > -1:
                self.scope += 1
                self.scopes[self.stmtIndex][self.scope] = {"parent": previousParentScope}

            res += " else " + node.setExpression2.generateCode(self)

        res += " endif"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    # Range
    def generateCode_Range(self, node):
        initValue = node.rangeInit.generateCode(self)
        initValue = Utils._getInt(initValue)

        endValue = node.rangeEnd.generateCode(self)
        endValue = Utils._getInt(endValue)

        res = initValue + ".." + endValue
        if node.by != None:
            res += " by " + node.by.generateCode(self)

        return res

    # Value List
    def generateCode_ValueList(self, node):
        return ",".join(map(self._getCodeValue, node.values))

    # Identifier List
    def generateCode_IdentifierList(self, node):
        return ",".join(map(self._getCodeValue, node.identifiers))

    # Tuple
    def generateCode_Tuple(self, node):
        return "(" + ",".join(map(self._getCodeValue, node.values)) + ")"

    # Tuple List
    def generateCode_TupleList(self, node):
        return ",".join(map(self._getCodeValue, node.values))

    # Value
    def generateCode_Value(self, node):
        return node.value.generateCode(self)

    # Identifier
    def generateCode_Identifier(self, node):
        if isinstance(node.sub_indices, str):
            return ""

        length_sub_indices = len(node.sub_indices)

        if length_sub_indices > 0:
            ident = node.identifier.generateCode(self)
            domains = self._getDomainByIdentifier(ident)
            includedDomains = False

            self.turnStringsIntoInts = True

            if domains != None and domains.strip() != "":
                domains = domains.split(",")
                domains = map(lambda el: el.strip(), domains)

                if len(domains) == length_sub_indices:
                    includedDomains = True
                    for i in range(length_sub_indices):
                        ind = node.sub_indices[i]
                        self.newType = domains[i]

                        ind.generateCode(self)
                    
            if not includedDomains:
                self.newType = "int"
                for i in range(length_sub_indices):
                    ind = node.sub_indices[i]
                    
                    ind.generateCode(self)

                        
            if isinstance(node.sub_indices, list):
                res = ident + "[" + ",".join(map(self._getCodeID, node.sub_indices)) + "]"
            else:
                res = ident + "[" + self._getCodeID(node.sub_indices) + "]"
            
            self.turnStringsIntoInts = False
        
        else:
            res = node.identifier.generateCode(self)
        
        return res

    # Number
    def generateCode_Number(self, node):
        return self.formatNumber(node.number)

    def _getNewIndex(self, ident, stmt, scope):
        if not stmt in self.scopes:
            return None

        if not scope in self.scopes[stmt]:
            return None

        while scope >= 0:
            if "new_indices" in self.scopes[stmt][scope]:
                if ident in self.scopes[stmt][scope]["new_indices"]:
                    return self.scopes[stmt][scope]["new_indices"][ident]

            if not "parent" in self.scopes[stmt][scope]:
                scope = -1
            else:
                scope = self.scopes[stmt][scope]["parent"]

        return None 

    def _setNewIndex(self, ident):
        if self.stmtIndex > -1:
            if not "new_indices" in self.scopes[self.stmtIndex][self.scope]:
                self.scopes[self.stmtIndex][self.scope]["new_indices"] = {}

            if not ident in self.scopes[self.stmtIndex][self.scope]["new_indices"]:
                self.scopes[self.stmtIndex][self.scope]["new_indices"][ident] = self.newIndexExpression
                self.countNewIndices += 1

            else:
                newIndex = self.scopes[self.stmtIndex][self.scope]["new_indices"][ident]
                if newIndex == "int" and self.newIndexExpression != "int":
                    self.scopes[self.stmtIndex][self.scope]["new_indices"][ident] = self.newIndexExpression
                    self.countNewIndices += 1

    # ID
    def generateCode_ID(self, node):
        ident = node.value

        if self.includeNewIndices:
            self._setNewIndex(ident)

        if self.replaceNewIndices:
            new_ident = self._getNewIndex(ident, self.stmtIndex, self.scope)
            if new_ident != None:
                return new_ident

        return ident

    # String
    def generateCode_String(self, node):
        string = "\"" + node.string[1:-1] + "\""

        if self.turnStringsIntoInts:
            param = string[1:-1]

            if not param in self.additionalParameters:
                if not self.newType:
                    self.newType = "int"

                if not param in self.additionalParameters or self.newType != "int":
                    self.additionalParameters[param] = self.newType+": " + param + ";\n\n"

            self.newIndexExpression = param
            self._setNewIndex(string)

            return param

        if self.replaceNewIndices:
            new_ident = self._getNewIndex(string, self.stmtIndex, self.scope)
            if new_ident != None:
                return new_ident

        #if node.string[0] == "\'":
        #node.string[0] = "\""
        #node.string[len(node.string)-1] = "\""

        return string
