from Utils import *
from ValueList import *
from Tuple import *
from TupleList import *
from Array import *
from Range import *
from Objectives import *
from Range import *
from Declarations import *
from Constraints import *
from ConstraintExpression import *
from SetExpression import *
from EntryIndexingExpression import *
from EntryLogicalExpression import *
from SymbolicExpression import *
from TopologicalSort import *
from Constants import *
from SymbolTables import *

from GenSets import *
from GenVariables import *
from GenParameters import *
from GenDeclarations import *
from GenBelongsToList import *
from GenBelongsTo import *

from IntegerSet import *
from RealSet import *
from SymbolicSet import *
from LogicalSet import *
from BinarySet import *
from ParameterSet import *
from VariableSet import *
from SetSet import *
from String import *

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
        self.parameterIsIndexOf = {}

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
        self.getOriginalIndices = False
        self.newIndexExpression = ""
        self.newType = "int"
        self.removeAdditionalParameter = False
        self.array2dIndex1 = None
        self.array2dIndex2 = None

        self.checkSetExpressionWithIndexingExpression = False
        self.isSetExpressionWithIndexingExpression = False
        self.isSetExpressionWithIndices = False
        self.to_enum = False
        self.realtype = None

        self.listEnums = []
        self.listSetOfInts = []
        self.parentIdentifier = None
        self.posId = {}
        self.countIndicesProcessed = 0
        self.identProcessing = None

        self.SET_OPERATIONS = [SetExpressionWithOperation.DIFF, SetExpressionWithOperation.SYMDIFF, SetExpressionWithOperation.UNION, \
                               SetExpressionWithOperation.INTER, SetExpressionWithOperation.CROSS]
        self.setsWitOperations = {}
        self.setsWitOperationsIndices = {}
        self.setsWitOperationsUsed = []
        self.setsWitOperationsInv = {}

        self.FUNCTIONS_TO_REMOVE = ["str2time", "gmtime", "Uniform01", "Uniform", "Normal01", "Normal", "Irand224"]

        self.lastIdentifier = None

        self.LIBRARIES = {"alldifferent": "alldifferent.mzn", "cumulative": "globals.mzn"}
        self.include = []

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
                    domain, domains, domain_with_indices_list, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal = self._getSubIndicesDomains(var)
                    self.identifiers[var.getName()] = {"types": _types,
                                                       "dim": dim,
                                                       "minVal": minVal,
                                                       "maxVal": maxVal,
                                                       "domain": domain, 
                                                       "domains": domains, 
                                                       "domains_with_indices_list": domain_with_indices_list, 
                                                       "dependencies": dependencies, 
                                                       "sub_indices": sub_indices, 
                                                       "statement": stmtIndex}

        if len(self.genParameters) > 0:
            for var in self.genParameters.getAll():
                domain, domains, domain_with_indices_list, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal = self._getSubIndicesDomains(var)
                self.identifiers[var.getName()] = {"types": _types,
                                                   "dim": dim,
                                                   "minVal": minVal,
                                                   "maxVal": maxVal,
                                                   "domain": domain, 
                                                   "domains": domains, 
                                                   "domains_with_indices_list": domain_with_indices_list, 
                                                   "dependencies": dependencies, 
                                                   "sub_indices": sub_indices, 
                                                   "statement": stmtIndex}

        if len(self.genSets) > 0:
            for var in self.genSets.getAll():
                domain, domains, domain_with_indices_list, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal = self._getSubIndicesDomains(var)
                self.identifiers[var.getName()] = {"types": _types,
                                                   "dim": dim,
                                                   "minVal": minVal,
                                                   "maxVal": maxVal,
                                                   "domain": domain, 
                                                   "domains": domains, 
                                                   "domains_with_indices_list": domain_with_indices_list, 
                                                   "dependencies": dependencies, 
                                                   "sub_indices": sub_indices, 
                                                   "statement": stmtIndex}

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
                   "; sub_indices = " + str(value.getSubIndices()) + "; isDefined = " + str(value.getIsDefined()) + 
                   "; isInLogicalExpression = " + str(value.getIsInLogicalExpression()) + ";"
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

    def _getLogicalExpressionOfDeclaration(self, declaration, varName, dependencies, sub_indices, stmtIndex):
        if declaration == None or declaration.getIndexingExpression() == None:
            return None

        indexingExpression = declaration.getIndexingExpression()
        if not stmtIndex in indexingExpression:
            return None

        logicalExpression = indexingExpression[stmtIndex].logicalExpression

        if not logicalExpression:
            return None

        logicalExpressionDependencies = set(logicalExpression.getDependencies(self))

        if varName in logicalExpressionDependencies:
            return logicalExpression.generateCode(self)

        if sub_indices and len(logicalExpressionDependencies.intersection(sub_indices)) > 0:
            return logicalExpression.generateCode(self)

        if dependencies and len(logicalExpressionDependencies.intersection(dependencies)) > 0:
            return logicalExpression.generateCode(self)

        return None

    def _getDomainByIdentifier(self, ident):
        if ident in self.identifiers:
            res = self.identifiers[ident]
            return res["domain"]

        return None

    def _getDomainsByIdentifier(self, ident):
        if ident in self.identifiers:
            res = self.identifiers[ident]
            return res["domains"]

        return None

    def _getDomainsWithIndicesByIdentifier(self, ident):
        if ident in self.identifiers:
            res = self.identifiers[ident]
            return res["domains_with_indices_list"]

        return None

    def _getSubIndicesDomainsAndDependencies(self, var):
        if var in self.identifiers:
            res = self.identifiers[var]
            return res["domain"], res["domains"], res["domains_with_indices_list"], res["dependencies"], res["sub_indices"], res["statement"]

        return None, [], [], [], None

    def _getProperties(self, var):
        if var in self.identifiers:
            res = self.identifiers[var]
            return res["types"], res["dim"], res["minVal"], res["maxVal"]

        return None, [], [], []

    def _getKeyForIndex(self, index, table):
        keys = []
        t = table
        order = 0
        while t != None:
            for key, value in t:

                sub_indices_list = list(value.getSubIndices())
                sub_indices_list.reverse()

                for subInd in sub_indices_list:
                    if index in subInd:
                        pos = subInd.index(index)
                        keys.append({"order":order, "identifier":key, "pos":pos})

                        order += 1

            t = t.getParent()

        return keys

    def _isIndexOf(self, index, table, stmt):
        while table != None:
            keys = self._getKeyForIndex(index, table)
            if len(keys) > 0:
                return keys

            table = table.getParent()

        leafs = self.symbolTables.getLeafs(stmt)
        for table in sorted(leafs, key=lambda el: el["scope"], reverse=True):
            table = table["table"]

            while table != None:
                keys = self._getKeyForIndex(index, table)

                if len(keys) > 0:
                    return keys

                table = table.getParent()

        return []

    def _tupleContainIndex(self, index, pos, _tuple):
        for el in _tuple:
            if el["index"] == index and el["pos"] == pos:
                return True

        return False

    def _addTuple(self, _tuple, stmt, dimen, setWithIndices, index, ident, order, pos = None, higherPriority = False):
        if not _tuple in self.tuples:
            self.tuples[_tuple] = {}
        
        if not stmt in self.tuples[_tuple]:
            self.tuples[_tuple][stmt] = {"dimen":dimen, "setWithIndices": setWithIndices, "identifiers": {}}
        elif higherPriority:
            self.tuples[_tuple][stmt]["dimen"] = dimen
            self.tuples[_tuple][stmt]["setWithIndices"] = setWithIndices
            
        if not ident in self.tuples[_tuple][stmt]["identifiers"]:
            self.tuples[_tuple][stmt]["identifiers"][ident] = {}

        if not order in self.tuples[_tuple][stmt]["identifiers"][ident]:
            self.tuples[_tuple][stmt]["identifiers"][ident][order] = []

        if not self._tupleContainIndex(index, pos, self.tuples[_tuple][stmt]["identifiers"][ident][order]):
            self.tuples[_tuple][stmt]["identifiers"][ident][order].append({"index": index, "pos": pos})

    def _checkIsSetOperation(self, key):
        for op in self.SET_OPERATIONS:
            op = " " + op + " "
            if op in key:
                return True

        return False

    def _checkIsValuesBetweenBraces(self, setExpression):
        if not setExpression or not (setExpression[0] == "{" and setExpression[len(setExpression)-1] == "}"):
            return False

        setExpression = setExpression[1:-1]
        values = self._splitDomain(setExpression)
        for value in values:
            if not re.search("^[_a-zA-Z][_a-zA-Z0-9]*$", value) and not re.search('"(?:[^\\\\]|\\\\.)*?(?:"|$)|\'(?:[^\\\\]|\\\\.)*?(?:\'|$)', value):
                return False

        return True

    def _checkIsSetBetweenBraces(self, setExpression):
        isAllIdentifiers = self._checkIsValuesBetweenBraces(setExpression)

        if not isAllIdentifiers or not setExpression:
            return False

        return setExpression[0] == "{" and setExpression[len(setExpression)-1] == "}" and not ".." in setExpression and not setExpression == "{}"

    def _cleanKeyWithSetOperation(self, key):
        key = key.replace("{", "")
        key = key.replace("}", "")
        key = key.replace("(", "")
        key = key.replace(")", "")
        key = key.replace("[", "")
        key = key.replace("]", "")
        key = key.replace("|", "")
        key = key.replace(",", "_")
        key = key.replace(" ", "_")

        return key

    def _getIndicesFromSetOperation(self, setExpression):
        m = re.findall("\[([a-zA-Z0-9][a-zA-Z0-9,]*)\]", setExpression)
        if m and len(m) > 0:
            indices = []
            for ind in m:
                inds = self._splitDomain(ind)

                if inds and len(inds) > 0:
                    for i in inds:
                        if not i in indices:
                            indices.append(i)

            return indices

        return None

    def _getWords(self, expression):
        if isinstance(expression, str):
            return re.sub("[^\w]", " ", expression).split()

        return []

    def _getSets(self, setExpression):
        sets = []
        dimensions = []
        words = self._getWords(setExpression)

        for w in words:
            _genSet = self.genSets.get(w)
            if _genSet != None:
                sets.append(w)
                dimensions.append(_genSet.getDimension())

        return sets, dimensions

    def _getTuplesByTables(self, tables, stmt):
        for table in sorted(tables, key=lambda el: el["scope"], reverse=True):
            scope = table["scope"]
            table = table["table"]
            
            while table != None:

                for key, value in table:

                    if self._checkIsSetOperation(key) or self._checkIsSetBetweenBraces(key):
                        indicesSetOp = self._getIndicesFromSetOperation(key)

                        dnew = self._cleanKeyWithSetOperation(key)
                        self.setsWitOperations[key] = dnew
                        self.setsWitOperationsInv[dnew] = key

                        if "[" in key and "|" in key:
                            dimen = 1
                        else:

                            sets, dimensions = self._getSets(key)
                            if len(sets) > 0:
                                dimen = max(dimensions)
                            else:
                                dimen = 1

                        if indicesSetOp and len(indicesSetOp) > 0:
                            self.setsWitOperationsIndices[key] = {"dimen": dimen, "indices": indicesSetOp}

                        key = dnew

                        self._addTuple(key, stmt, dimen, False, None, None, None, None)

                    elif "[" in key and not "," in key:

                        parts = key.split("[")
                        domain = parts[0].strip()
                        parts = parts[1].split("]")

                        indices = self._splitDomain(parts[0])
                        dimen = len(indices)

                        for index in indices:
                            keys = self._isIndexOf(index, table, stmt)

                            if len(keys) > 0:
                                for key in keys:
                                    ident = key["identifier"]
                                    pos   = key["pos"]
                                    order = key["order"]

                                    self._addTuple(domain, stmt, dimen, True, index, ident, order, pos)

                    elif "," in key:

                        domains = value.getProperties().getDomains()
                        domains.reverse()
                        
                        if len(domains) > 0:
                            indices = key.split(",")
                            dimen = len(indices)

                            for domain in domains:
                                d = domain.getName()

                                if self._checkIsSetOperation(d) or self._checkIsSetBetweenBraces(d):

                                    indicesSetOp = self._getIndicesFromSetOperation(key)
                                    dnew = self._cleanKeyWithSetOperation(d)
                                    self.setsWitOperations[d] = dnew
                                    self.setsWitOperationsInv[dnew] = d

                                    if indicesSetOp and len(indicesSetOp) > 0:
                                        self.setsWitOperationsIndices[d] = {"dimen": dimen, "indices": indicesSetOp}

                                    d = dnew
                                    
                                for index in indices:
                                    keys = self._isIndexOf(index, table, stmt)

                                    if len(keys) > 0:
                                        for key in keys:
                                            ident = key["identifier"]
                                            pos   = key["pos"]
                                            order = key["order"]

                                            self._addTuple(d, stmt, dimen, False, index, ident, order, pos, True)

                                    else:
                                        self._addTuple(d, stmt, dimen, False, index, None, None, None, True)

                    if len(value.getSubIndices()) > 0:

                        sub_indices_list = list(value.getSubIndices())
                        sub_indices_list.reverse()

                        for _subIndices in sub_indices_list:
                            self._checkParameterIsIndexOf(_subIndices, key)

                table = table.getParent()

    def _getTuples(self):
        statements = self.symbolTables.getStatements()
        for stmt in sorted(statements, reverse=True):

            scopes = self.symbolTables.getFirstScope(stmt)
            self._getTuplesByTables(scopes, stmt)

            leafs = self.symbolTables.getLeafs(stmt)
            self._getTuplesByTables(leafs, stmt)

        for name in self.tuples:
            
            index1 = None
            _type = None
            pos = {}
            realtype = None
            sizeTuple = None

            for stmt in sorted(self.tuples[name], reverse=True):

                setWithIndices = self.tuples[name][stmt]["setWithIndices"]
                
                if setWithIndices:
                    realtype = "set of int"

                domainIdent = []
                for ident in self.tuples[name][stmt]["identifiers"]:
                    
                    for order in sorted(self.tuples[name][stmt]["identifiers"][ident]):
                        domain = self._getDomainByIdentifier(ident)
                        sizeTuple = self.tuples[name][stmt]["dimen"]
                        sizeTupleNotNull = sizeTuple

                        if sizeTuple > 1:
                            index2 = "1.."+str(sizeTuple)
                        else:
                            index2 = None

                        if domain == None or domain.strip() == "":
                            sizeTupleNotNull -= 1
                        else:
                            domainIdent.append(domain)

                        if len(domainIdent) > 0:
                            _tuple = self.tuples[name][stmt]["identifiers"][ident][order]
                            domainIdents = list(domainIdent)
                            
                            if len(domainIdent) == 1:
                                domain = self._splitDomain(domainIdent[0])
                                domainIdents = domain

                            if len(_tuple) >= sizeTuple:
                                domainIdent = []

                            domains = self._stripDomains(domainIdents)
                            if all(map(lambda el: el == domains[0], domains)):
                                _type = domains[0]

                            else:
                                size = len(domains)
                                pos = []
                                d = []

                                for t in _tuple:
                                    pos.append(t["pos"])

                                for position in pos:
                                    if position != None:
                                        if position >= size:
                                            index1 = None
                                            _type = None
                                            pos = {}
                                            #realtype = None
                                            sizeTuple = None

                                            continue

                                        d.append(domains[position])

                                if len(d) > 0 and all(map(lambda el: el == d[0], d)):
                                    _type = d[0]

                                else:
                                    index1 = None
                                    _type = None
                                    pos = {}
                                    #realtype = None
                                    sizeTuple = None

                                    continue

                        if _type == None or _type == name or _type == ident or _type in self.tuples or ".." in _type:
                            index1 = None
                            _type = None
                            pos = {}
                            #realtype = None
                            sizeTuple = None

                            continue

                        if _type != None and _type != "int":
                            break

                    if _type != None and _type != "int":
                        break

                if _type != None and _type != "int":
                    break

                index1 = None
                _type = None
                pos = {}
                #realtype = None
                sizeTuple = None


            if index1 == None and not ".." in name:
                index1 = "INDEX_SET_"+name
                setint = "set of int: "+index1+";\n\n"

                self.additionalParameters[index1] = setint

            if _type == None:
                _type = "int"

            if realtype != None:
                aux = realtype
                realtype = _type
                _type = aux

            if realtype == "int":
                realtype = None

            if name in self.setsWitOperationsInv:
                if index2 != None:
                    self.additionalParameters[name] = "array["+index1+","+index2+"] of "+_type+": " + name + ";\n\n";
                else:
                    self.additionalParameters[name] = "array["+index1+"] of "+_type+": " + name + ";\n\n";

            self.tuplesDeclared[name] = {"index1": index1, "index2": index2, "type": _type, "realtype": realtype, "dimen": sizeTuple}

    def _getSetAttribute(self, attribute):
        if isinstance(attribute, SetExpressionWithValue):
            return attribute.value
        else:
            return attribute

    def _isFromZeroToN(self, values):
        i = 0
        for idx in values:
            if idx != i:
                return False

            i += 1

        return True

    def _hasEqualIndices(self, minVal, maxVal):
        minValIndices = sorted(minVal.keys())
        maxValIndices = sorted(maxVal.keys())

        return minValIndices == maxValIndices

    def _hasAllIndices(self, minVal, maxVal):
        minValIndices = sorted(minVal.keys())
        maxValIndices = sorted(maxVal.keys())

        if minValIndices != maxValIndices:
            return False

        if not self._isFromZeroToN(minValIndices):
            return False

        if not self._isFromZeroToN(maxValIndices):
            return False

        return True

    def _zipMinMaxVals(self, minVal, maxVal):
        minMaxVals = {}

        for idx in minVal:
            if idx in maxVal:
                minMaxVals[idx] = str(minVal[idx])+".."+str(maxVal[idx])

        return minMaxVals

    def _getIdentifierNode(self, value):
        if isinstance(value, SetExpressionWithValue):
            value = value.value

        return value

    def _isIdentifierType(self, obj):
        obj = self._getIdentifierNode(obj)
        return isinstance(obj, ParameterSet) or isinstance(obj, SetSet) or isinstance(obj, VariableSet)

    def _isTypeSet(self, obj):
        obj = self._getIdentifierNode(obj)
        return isinstance(obj, BinarySet) or isinstance(obj, IntegerSet) or isinstance(obj, RealSet) or isinstance(obj, SymbolicSet) or \
              (isinstance(obj, SetExpression) and obj.getSymbolName(self).replace(" ", "") == Constants.BINARY_0_1)

    def _isModifierSet(self, obj):
        obj = self._getIdentifierNode(obj)
        return isinstance(obj, LogicalSet)

    def notInTypesThatAreNotDeclarable(self, value):
        if isinstance(value, Tuple):
            return True
        
        value = value.getSymbol()
        
        return not value.isBinary and not value.isInteger and not value.isNatural and not value.isReal and not value.isSymbolic and not \
        value.isLogical and not value.isDeclaredAsVar and not value.isDeclaredAsParam and not value.isDeclaredAsSet and not \
        isinstance(value, str)

    def _removeTypesThatAreNotDeclarable(self, _types):
        return filter(lambda el: not self._isIdentifierType(el.getObj()), _types)

    def _removePreDefinedTypes(self, _types):
        return filter(lambda el: not self._isIdentifierType(el) and not self._isTypeSet(el) and not self._isModifierSet(el), _types)

    def _getTypes(self, _types):
        return filter(lambda el: self._isTypeSet(el.getObj()), _types)

    def _getModifiers(self, _types):
        return filter(lambda el: self._isModifierSet(el.getObj()), _types)

    def _domainIdentifierType(self, domain):
        obj = domain.getObj()
        return self._isIdentifierType(obj)

    def _domainIsNumberSet(self, domain):
        obj = domain.getObj()
        return self._isTypeSet(obj)

    def _domainIsModifierSet(self, domain):
        obj = domain.getObj()
        return self._isModifierSet(obj)

    def _domainIsInvalid(self, domain):
        return self._domainIdentifierType(domain) or self._domainIsNumberSet(domain) or self._domainIsModifierSet(domain)

    def _getNumber(self, numericExpression):
        if isinstance(numericExpression, Number):
            return numericExpression

        if not isinstance(numericExpression, ValuedNumericExpression):
            return None

        value = numericExpression.getValue()
        if isinstance(value, Number):
            return value

        return None

    def _mountValueByIndex(self, indicesPosition, value):
        valueDict = {}

        if isinstance(indicesPosition, list):
            for idx in indicesPosition:
                valueDict[idx] = value
        else:
            valueDict[indicesPosition] = value

        return valueDict

    def _isKeysInDictionary(self, keys, dictionary):
        if isinstance(keys, list):
            for idx in keys:
                if not idx in dictionary:
                    return False

            return True

        else:
            return keys in dictionary

    def _isRangeThatCanBeImproved(self, obj, indicesPosition, minVal, maxVal):
        asc = True
        rangeObj = {}

        if not isinstance(obj, Range):
            return False, asc, rangeObj, minVal, maxVal

        rangeInit = obj.getRangeInit()
        rangeEnd  = obj.getRangeEnd()

        numberInit = self._getNumber(rangeInit)
        numberEnd  = self._getNumber(rangeEnd)

        if not isinstance(numberInit, Number) and not isinstance(numberEnd, Number):
            return False, asc, rangeObj, minVal, maxVal

        if isinstance(numberInit, Number) and isinstance(numberEnd, Number):
            numberInit = int(numberInit.getNumber())
            numberEnd  = int(numberEnd.getNumber())

            minV = numberInit if numberInit < numberEnd  else numberEnd
            maxV = numberEnd  if numberEnd  > numberInit else numberInit

            minValAux = self._mountValueByIndex(indicesPosition, minV)
            minVal = self._setMinVal(minVal, minValAux)

            maxValAux = self._mountValueByIndex(indicesPosition, maxV)
            maxVal = self._setMaxVal(maxVal, maxValAux)

            return True, asc, rangeObj, minVal, maxVal

        by = obj.getBy()

        if by != None:
            numberBy = self._getNumber(by)
            if numberBy == None:
                return False, asc, rangeObj, minVal, maxVal
                
            elif int(numberBy.getNumber()) < 0:
                asc = False

        if isinstance(numberInit, Number):
            numberInit = int(numberInit.getNumber())

            minValAux = self._mountValueByIndex(indicesPosition, numberInit)
            minVal = self._setMinVal(minVal, minValAux)

            maxValAux = self._mountValueByIndex(indicesPosition, numberInit)
            maxVal = self._setMaxVal(maxVal, maxValAux)

        else:

            if not asc:
                rangeObj[1] = obj.getRangeInit()
            else:
                rangeObj[0] = obj.getRangeInit()

        if isinstance(numberEnd, Number):
            numberEnd = int(numberEnd.getNumber())

            minValAux = self._mountValueByIndex(indicesPosition, numberEnd)
            minVal = self._setMinVal(minVal, minValAux)

            maxValAux = self._mountValueByIndex(indicesPosition, numberEnd)
            maxVal = self._setMaxVal(maxVal, maxValAux)

        else:

            if not asc:
                rangeObj[0] = obj.getRangeEnd()
            else:
                rangeObj[1] = obj.getRangeEnd()

        return True, asc, rangeObj, minVal, maxVal

    def _getItemDomain(self, domains, totalIndices):
        size = len(domains)
        if size == 0:
            return None, None, None, None

        while size > 0:
            size -= 1
            domain = domains[size]

            if self._domainIsInvalid(domain):
                continue

            dependencies = list(domain.getDependencies())

            if domain.getName() in dependencies:
                dependencies.remove(domain.getName())

            if len(dependencies) > 0:
                if not set(dependencies).issubset(set(totalIndices+self.parameters_and_sets)):
                    break

            deps = set(domain.getDependencies())
            deps.discard(set(totalIndices))

            return domain.getOp(), domain.getName(), domain.getObj(), list(deps)

        return None, None, None, None

    def _getItemDomain(self, domains, totalIndices):
        size = len(domains)
        if size == 0:
            return None, None, None, None

        while size > 0:
            size -= 1
            domain = domains[size]

            if self._domainIsInvalid(domain):
                continue

            dependencies = list(domain.getDependencies())

            if domain.getName() in dependencies:
                dependencies.remove(domain.getName())

            if len(dependencies) > 0:
                if not set(dependencies).issubset(set(totalIndices+self.parameters_and_sets)):
                    break

            deps = set(domain.getDependencies())
            deps.discard(set(totalIndices))

            return domain.getOp(), domain.getName(), domain.getObj(), list(deps)

        return None, None, None, None

    def _getDomainSubIndices(self, table, selectedIndices, totalIndices, indicesPosition, minVal, maxVal, isDeclaration = False):
        if not isinstance(selectedIndices, str):
            selectedIndices = ",".join(selectedIndices)

        rangeObjAux = {}
        domainAux = None
        opAux = None
        depsAux = None

        while table != None:
            value = table.lookup(selectedIndices)

            if value != None:
                op, domain, domainObj, deps = self._getItemDomain(value.getProperties().getDomains(), totalIndices)
                
                if domain != None:

                    if not isDeclaration:
                        isRangeThatCanBeImproved, asc, rangeObj, minVal, maxVal = self._isRangeThatCanBeImproved(domainObj, indicesPosition, minVal, maxVal)
                        
                        if isRangeThatCanBeImproved:
                            opAux = op
                            depsAux = deps
                            domainAux = domain
                            
                            if not rangeObjAux and rangeObj:
                                rangeObjAux = rangeObj

                            table = table.getParent()
                            continue

                        posBy = domain.find("by") # if a range is inferred as the domain, the by clause is removed

                        if posBy > 0:
                            domain = domain[0:posBy].strip()

                    return op, domain, domainObj, deps, minVal, maxVal

            table = table.getParent()

        if domainAux != None:
            posIn = domainAux.find(" in ")

            if posIn > 0:
                domain = domainAux[0:posIn+4]
            else:
                domain = ""

            domains = []

            if rangeObjAux:
                
                if 0 in rangeObjAux:

                    if not self._isKeysInDictionary(indicesPosition, maxVal):
                        domains = []

                    else:
                        if isinstance(indicesPosition, list):
                            for idx in indicesPosition:
                                domains.append(rangeObjAux[0].generateCode(self) + ".." + str(maxVal[idx]))

                        else:
                            domains.append(rangeObjAux[0].generateCode(self) + ".." + str(maxVal[indicesPosition]))

                elif 1 in rangeObjAux:

                    if not self._isKeysInDictionary(indicesPosition, minVal):
                        domains = []

                    else:
                        if isinstance(indicesPosition, list):
                            for idx in indicesPosition:
                                domains.append(str(minVal[idx]) + ".." + rangeObjAux[1].generateCode(self))

                        else:
                            domains.append(str(minVal[indicesPosition]) + ".." + rangeObjAux[1].generateCode(self))

            else:

                if not self._isKeysInDictionary(indicesPosition, minVal) or not self._isKeysInDictionary(indicesPosition, maxVal):
                    domains = []

                else:

                    if isinstance(indicesPosition, list):
                        for idx in indicesPosition:
                            domains.append(str(minVal[idx]) + ".." + str(maxVal[idx]))

                    else:
                        domains.append(str(minVal[indicesPosition]) + ".." + str(maxVal[indicesPosition]))

            if len(domains) > 1:
                domain += "{"+", ".join(domains)+"}"

            elif len(domains) > 0:
                domain += domains[0]

            if len(domains) > 0:
                return opAux, domain, None, depsAux, minVal, maxVal

        return None, None, None, None, minVal, maxVal

    def _checkParameterIsIndexOf(self, indices, name):
        for i in range(len(indices)):
            ind = indices[i]

            if ind in self.parameters and not ind in self.parameterIsIndexOf:
                self.parameterIsIndexOf[ind] = {"indexOf":name, "pos":i}

    def _getSubIndicesDomainsByTables(self, name, tables, minVal, maxVal, isDeclaration = False, domainsAlreadyComputed = None, skip_outermost_scope = False):

        domain = ""
        domain_with_indices = ""
        dependencies_ret = []
        sub_indices_ret = []
        domains_str = []
        max_length_domain = 0

        countAlreadyComputed = {}
        dependenciesAlreadyComputed = {}
        subIndicesAlreadyComputed = {}
        

        if not domainsAlreadyComputed:
            domainsAlreadyComputed = {}
            domainsWithIndicesAlreadyComputed = {}
        else:
            domainsWithIndicesAlreadyComputed = dict(domainsAlreadyComputed)

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
                    if table != None:
                        table = table.getParent()
                            
                    continue

                #if t.getIsInLogicalExpression():
                #    if table != None:
                #        table = table.getParent()

                #    continue

                sub_indices_list = list(t.getSubIndices())
                sub_indices_list.reverse()

                domain = ""
                domains = {}
                domains_with_indices = {}
                dependencies = {}
                domains_str = []
                count = {}


                for _subIndices in sub_indices_list:

                    max_length_domain = max(max_length_domain, len(_subIndices))

                    totalIndices = list(_subIndices)
                    idx = 0
                    totalSubIndices = len(_subIndices)
                    indices = range(totalSubIndices)
                    indicesBkp = list(indices)
                    _subIndicesRemaining = list(_subIndices)

                    while idx < totalSubIndices:
                        _combIndices = _subIndices[idx:]
                        _indicesPos = indicesBkp[idx:]
                        
                        if len(_combIndices) <= 1:
                            idx += 1
                            continue

                        op, _tuple, _tupleObj, deps, minVal, maxVal = self._getDomainSubIndices(table, _combIndices, totalIndices, _indicesPos, minVal, maxVal, isDeclaration)
                        while _tuple == None and len(_combIndices) > 0:
                            _combIndices = _combIndices[:-1];
                            _indicesPos = _indicesPos[:-1]
                            
                            if len(_combIndices) <= 1:
                                break

                            op, _tuple, _tupleObj, deps, minVal, maxVal = self._getDomainSubIndices(table, _combIndices, totalIndices, _indicesPos, minVal, maxVal, isDeclaration)
                            
                        if _tuple != None:
                            domains[idx] = _tuple
                            domains_with_indices[idx] = {"indices": _combIndices, "set": _tuple}
                            dependencies[idx] = deps
                            count[idx] = len(_combIndices)
                            
                            for i in range(idx, idx+len(_combIndices)):
                                indices.remove(i)

                            idx += len(_combIndices)

                            for _comb in _combIndices:
                                _subIndicesRemaining.remove(_comb)

                        else:
                            idx += 1
                        
                    if len(indices) > 0:
                        indices = sorted(indices)

                        subIdxDomains = [self._getDomainSubIndices(table, _subIndicesRemaining[i], totalIndices, indices[i], minVal, maxVal, isDeclaration) for i in range(len(_subIndicesRemaining))]
                        subIdxDomainsRemaining = []
                        
                        varNameSubIndices = []

                        for i in range(len(subIdxDomains)):
                            ind = indices[i]
                            minVal = subIdxDomains[i][4]
                            maxVal = subIdxDomains[i][5]

                            if subIdxDomains[i][1] != None:
                                domains[ind] = subIdxDomains[i][1]
                                domains_with_indices[ind] = _subIndicesRemaining[i] + " " + subIdxDomains[i][0] + " " + subIdxDomains[i][1]
                                count[ind] = 1
                                if not _subIndicesRemaining[i] in varNameSubIndices:
                                    varNameSubIndices.append(_subIndicesRemaining[i])

                                dependencies[ind] = subIdxDomains[i][3]

                            else:
                                subIdxDomainsRemaining.append(ind)
                    
                    for idx in domains:
                        if not idx in domainsAlreadyComputed or ".." in domainsAlreadyComputed[idx]:
                            domainsAlreadyComputed[idx]      = domains[idx]
                            dependenciesAlreadyComputed[idx] = dependencies[idx]

                            self._setSubIndicesAlreadyComputed(idx, subIndicesAlreadyComputed, domains_with_indices, _subIndices)

                            countAlreadyComputed[idx]   = count[idx]
                            domainsWithIndicesAlreadyComputed[idx] = domains_with_indices[idx]
                        
                        if not idx in domainsWithIndicesAlreadyComputed:
                            domainsWithIndicesAlreadyComputed[idx] = domains_with_indices[idx]

                        if not idx in subIndicesAlreadyComputed:
                            self._setSubIndicesAlreadyComputed(idx, subIndicesAlreadyComputed, domains_with_indices, _subIndices)
                            
                table = table.getParent()
            
        totalCountAlreadyComputed = 0
        for idx in countAlreadyComputed:
            totalCountAlreadyComputed += countAlreadyComputed[idx]

        if totalCountAlreadyComputed == max_length_domain:
            domains_str = []
            domains_ret = []
            dependencies_ret = []
            sub_indices_ret = []

            for key in sorted(domainsAlreadyComputed.iterkeys()):
                if domainsAlreadyComputed[key] != None:
                    domains_str.append(domainsAlreadyComputed[key])

                    if key in domainsWithIndicesAlreadyComputed:
                        domains_ret.append(domainsWithIndicesAlreadyComputed[key])

                    if key in dependenciesAlreadyComputed:
                        if isinstance(dependenciesAlreadyComputed[key], list):
                            for dep in dependenciesAlreadyComputed[key]:
                                dependencies_ret.append(dep)

                        else:
                            dependencies_ret.append(dependenciesAlreadyComputed[key])

                    if key in subIndicesAlreadyComputed:
                        if key in domains_with_indices and isinstance(domains_with_indices[key], dict):
                            _indices = domains_with_indices[key]["indices"]
                            for i in range(key, key+len(_indices)):
                                sub_indices_ret.append(subIndicesAlreadyComputed[i])

                        elif isinstance(subIndicesAlreadyComputed[key], list):
                            for dep in subIndicesAlreadyComputed[key]:
                                sub_indices_ret.append(dep)

                        else:
                            sub_indices_ret.append(subIndicesAlreadyComputed[key])

            domain += ", ".join(domains_str)
            domain_with_indices = domains_ret

        domain_with_indices = self._processDomainsWithIndices(domain_with_indices)
        
        return domain, domains_str, domain_with_indices, list(set(dependencies_ret)), sub_indices_ret, minVal, maxVal

    def _setSubIndicesAlreadyComputed(self, idx, subIndicesAlreadyComputed, domains_with_indices, _subIndices):
        if idx in domains_with_indices and isinstance(domains_with_indices[idx], dict):
            _indices = domains_with_indices[idx]["indices"]
            c = 0
            for i in range(idx, idx+len(_indices)):
                subIndicesAlreadyComputed[i] = _indices[c]
                c += 1
        else:
            subIndicesAlreadyComputed[idx]   = _subIndices[idx]

    def _processDomainsWithIndices(self, domain_with_indices):

        dummy_indices = []
        for d in domain_with_indices:
            if isinstance(d, str):
                dummy_indices.append(d.split(" in ")[0].strip() if " in " in d else "")
            else:
                dummy_indices.append(None)

        new_domain_with_indices = []

        idx = "i"
        count = 0
        
        for i in range(len(domain_with_indices)):
            d = dummy_indices[i]
            
            if d == "":
                new_dummy_index = idx+str(count)
                count += 1

                while new_dummy_index in dummy_indices:
                    new_dummy_index = idx+str(count)
                    count += 1

                new_domain_with_indices.append(new_dummy_index + " in " + domain_with_indices[i])

            else:
                new_domain_with_indices.append(domain_with_indices[i])

        return new_domain_with_indices

    def _getSubIndicesDomainsByStatements(self, name, statements, minVal, maxVal, isDeclaration = False, domainsAlreadyComputed = None):
        domain = ""
        domains = []
        domains_with_indices = []
        dependencies = []
        sub_indices = []
        stmtIndex = None
        currStmt = None
        
        for stmt in sorted(statements, reverse=True):

            currStmt = stmt
            
            scopes = self.symbolTables.getFirstScopeByKey(name, stmt)
            domain, domains, domains_with_indices, dependencies, sub_indices, minVal, maxVal = self._getSubIndicesDomainsByTables(name, scopes, minVal, maxVal, isDeclaration, domainsAlreadyComputed)

            if domain != "" and (not domainsAlreadyComputed or domains != domainsAlreadyComputed.values()):
                stmtIndex = stmt
                break
            
            leafs = self.symbolTables.getLeafs(stmt)
            domain, domains, domains_with_indices, dependencies, sub_indices, minVal, maxVal = self._getSubIndicesDomainsByTables(name, leafs, minVal, maxVal, False, domainsAlreadyComputed, True)

            if domain != "" and (not domainsAlreadyComputed or domains != domainsAlreadyComputed.values()):
                stmtIndex = stmt
                break

        if not stmtIndex:
            stmtIndex = currStmt

        return domain, domains, domains_with_indices, dependencies, sub_indices, stmtIndex, minVal, maxVal

    def _getSubIndicesDomains(self, identifier):
        
        _types, dim, minVal, maxVal = self._getDomain(identifier)
        
        name = identifier.getName()
        declarations = self.symbolTables.getDeclarationsWhereKeyIsDefined(name)

        domain, domains, domains_with_indices, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, declarations, minVal, maxVal, True)
        
        if domain == "":
            statements = self.symbolTables.getStatementsByKey(name)
            domain, domains, domains_with_indices, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, statements, minVal, maxVal, False)

        if domain == "":
            if minVal and maxVal and self._hasEqualIndices(minVal, maxVal):
                minMaxVals = self._zipMinMaxVals(minVal, maxVal)
                domain, domains, domains_with_indices, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, declarations, minVal, maxVal, True, minMaxVals)

                if domain == "" or domains == minMaxVals.values():
                    statements = self.symbolTables.getStatementsByKey(name)
                    domain, domains, domains_with_indices, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, statements, minVal, maxVal, False, minMaxVals)
                
        return domain, domains, domains_with_indices, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal

    def _setMinVal(self, minVal, minValAux):
        if minVal == None:
            minVal = {}

        if minValAux == None or len(minValAux) == 0:
            return minVal
            
        for idx in minValAux:
            if not idx in minVal or minValAux[idx] < minVal[idx]:
                minVal[idx] = minValAux[idx]

        return minVal

    def _setMaxVal(self, maxVal, maxValAux):
        if maxVal == None:
            maxVal = {}
            
        if maxValAux == None or len(maxValAux) == 0:
            return maxVal
            
        for idx in maxValAux:
            if not idx in maxVal or maxValAux[idx] > maxVal[idx]:
                maxVal[idx] = maxValAux[idx]

        return maxVal
        
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
                    if table != None:
                        table = table.getParent()

                    continue

                prop = t.getProperties()
                domains = prop.getDomains()
                domains.reverse()

                for domain in domains:
                    inserted = False
                    for _type in _types:
                        if domain.getName() == _type.getName():
                            inserted = True # last occurrence prevails (it is scanning from bottom to top, right to left)
                            break

                    if not inserted:
                        _types.append(domain)

                if dim == None:
                    
                    if prop.getDimension() != None:
                        dim = prop.getDimension()

                    else:
                        dim = 0

                _sub_indices = t.getSubIndices()

                if _sub_indices:
                    for indices in _sub_indices:
                        dimen = len(indices)

                        if dimen > dim:
                            dim = dimen

                minVal = self._setMinVal(minVal, prop.getMinVal())
                maxVal = self._setMaxVal(maxVal, prop.getMaxVal())

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

    def _addDependencies(self, value, stmtIndex, dependencies):
        names = value.getDependencies(self)

        if names != None and len(names) > 0:
            for name in names:
                if not self.genBelongsToList.has(GenBelongsTo(name, stmtIndex)):
                    dependencies.append(name)

    def _getDependencies(self, identifier):
        dependencies = []

        decl = self.genDeclarations.get(identifier.getName())
        if decl != None:
            value = decl.getValue()
            if value != None:
                self._addDependencies(value.attribute, decl.getStmtIndex(), dependencies)

            value = decl.getDefault()
            if value != None:
                self._addDependencies(value.attribute, decl.getStmtIndex(), dependencies)

            ins = decl.getIn()
            if ins != None and len(ins) > 0:
                for pSet in ins:
                    self._addDependencies(pSet.attribute, decl.getStmtIndex(), dependencies)

            withins = decl.getWithin()
            if withins != None and len(withins) > 0:
                for pSet in withins:
                    self._addDependencies(pSet.attribute, decl.getStmtIndex(), dependencies)

            relations = decl.getRelations()
            if relations != None and len(relations) > 0:
                for pRel in relations:
                    self._addDependencies(pRel.attribute, decl.getStmtIndex(), dependencies)

            idxsExpression = decl.getIndexingExpression()
            _subIndices = decl.getSubIndices()
            for stmtIndex in idxsExpression:
                if idxsExpression[stmtIndex] and stmtIndex in _subIndices and _subIndices[stmtIndex]:
                    idxExpression = idxsExpression[stmtIndex]

                    self._addDependencies(idxExpression, decl.getStmtIndex(), dependencies)

        return dependencies

    def _checkAddDependence(self, graph, name, dep):
        return dep != name and not dep in graph[name] and dep in self.parameters_and_sets

    def _generateGraphAux(self, graph, genObj):
        if len(genObj) > 0:
            for identifier in genObj.getAll():
                
                name = identifier.getName()
                if not name in graph:
                    graph[name] = []
                
                dependencies = self._getDependencies(identifier)

                if len(dependencies) > 0:
                    for dep in dependencies:
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

    def _getValueFromNumericExpression(self, expr):
        if isinstance(expr, ValuedNumericExpression):
            return expr.value

        return expr

    # Get the MathProg code for a given relational expression
    def _getCodeValue(self, value):
        val = value.generateCode(self)
        #if val.replace('.','',1).isdigit():
        #    val = str(int(float(val)))

        return val

    # Get the MathProg code for a given sub-indice
    def _getCodeID(self, id_):
        if isinstance(id_, ValuedNumericExpression):
            if isinstance(id_.value, Identifier):
                id_.value.setIsSubIndice(True)

        elif isinstance(id_, Identifier):
            id_.setIsSubIndice(True)

        val = id_.generateCode(self)
        #if val.replace('.','',1).isdigit():
        #    val = str(int(float(val)))

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

        elif isinstance(constraint, Objective):
            return self._getCodeObjective(constraint)

        return ""

    def removeInvalidConstraint(self, constraint):
        valid =  constraint != None and constraint.strip() != "" and constraint.strip() != "constraint ;"

        if valid:
            match = re.search("forall\(.+\)\(\)", constraint)

            if match:
                valid = False

        return valid

    def _stripDomains(self, domains):
        return map(lambda el: el.strip(), domains)

    def _splitDomain(self, domain):
        return self._stripDomains(domain.split(","))

    def formatNumber(self, number):
        return ("0" if number[0] == "." else "") + number

    def _getIndices(self, sub_indices, domains_with_indices):
        indices_ins = []

        if sub_indices:
            sizeSubIndices = len(sub_indices)

            if sizeSubIndices > 0:

                if sizeSubIndices >= len(domains_with_indices):
                    indices_ins = list(sub_indices)

                else:

                    for i in range(len(domains_with_indices)):

                        if i < sizeSubIndices:
                            indices_ins.append(sub_indices[i])
                        else:
                            indices_ins.append(domains_with_indices[i])

        if len(indices_ins) == 0:
            indices_ins = [""]*len(domains_with_indices)

        for i in range(len(domains_with_indices)):
            d = domains_with_indices[i]

            if not isinstance(d, str):
                setName = d["set"]
                
                if setName in self.tuplesDeclared:
                    index1 = self.tuplesDeclared[setName]["index1"]
                    indices = d["indices"]
                    index = indices[0]

                    c = 1
                    cs = []
                    for i in indices:
                        if not c in cs:
                            repl = setName + "["+index+","+str(c)+"]"
                            cs.append(c)
                            c += 1

                            ind = [j for j, v in enumerate(indices_ins) if v == i]
                            for j in ind:
                                indices_ins[j] = repl

                            self.newIndexExpression = repl
                            self._setNewIndex(i)

            else:
                if " in " in d:
                    indices_ins[i] = d.split(" in ")[0].strip()

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
                    res.append("int")

            elif "[" in d:
                res.append("int")
            #elif not ".." in d:
            #    res.append("int")
            else:
                res.append("int")
                #res.append(d)

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
            if const:
                if isArray:
                    domains = self._getDomainsWithIndices(domains_with_indices)
                    
                    cnt += "constraint forall("+", ".join(domains)+")("+const+");";
                else:
                    cnt += "constraint "+const + ";";

                return cnt

        return None

    def _hasFunctionsToRemove(self, expression):
        words = self._getWords(expression)
        
        for function in self.FUNCTIONS_TO_REMOVE:
            function = function

            if function in words:
                return True

        return False

    def _getIdentifier(self, var):
        if isinstance(var, str):
            return var

        return var.getSymbol()

    def _getRange(self, setExpression):
        if isinstance(setExpression, SetExpressionBetweenBraces):
            setExpression = setExpression.setExpression

        setExpression = self._getIdentifier(setExpression)

        if isinstance(setExpression, Range):
            return setExpression

        return None

    def _getIndexingExpressionFromDeclaration(self, decl, stmtIndex):
        idxsExpression = decl.getIndexingExpression()
        _subIndices = decl.getSubIndices()
        selected = False
        indexingExpression = None
        subIndices = []

        if stmtIndex in idxsExpression and stmtIndex in _subIndices and _subIndices[stmtIndex] and len(_subIndices[stmtIndex]) > 0:
            return idxsExpression[stmtIndex].generateCode(self), _subIndices[stmtIndex]

        for key in sorted(idxsExpression, reverse=True):
            if idxsExpression[key] and key in _subIndices and _subIndices[key] and len(_subIndices[key]) > 0:
                indExpr = idxsExpression[key].generateCode(self)

                if not selected:
                    selected = True

                    indexingExpression = indExpr
                    subIndices = _subIndices[key]
            else:
                idxsExpression[key].generateCode(self)


        return indexingExpression, subIndices

    def _getIndicesFromDeclaration(self, decl, stmtIndex):
        if not decl:
            return []

        _subIndices = decl.getSubIndices()
        
        if stmtIndex in _subIndices and _subIndices[stmtIndex] and len(_subIndices[stmtIndex]) > 0:
            return _subIndices[stmtIndex]
            
        for key in sorted(_subIndices, reverse=True):
            if key in _subIndices and _subIndices[key] and len(_subIndices[key]) > 0:
                return _subIndices[key]
                
        return []


    def _declareVars(self):
        """
        Generate the MathProg code for the declaration of identifiers
        """

        varStr = ""
        if len(self.genVariables) > 0:
            
            for var in self.genVariables.getAll():
                if not self.genParameters.has(var) and not self.genSets.has(var):

                    self.scope = 0
                    self.stmtIndex += 1

                    if not self.stmtIndex in self.scopes:
                        self.scopes[self.stmtIndex] = {}
                        self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "_declareVars"}

                    previousParentScope = self.parentScope
                    self.parentScope = self.scope

                    value = ""
                    domain = None
                    varName = var.getName()
                    _type = None
                    isArray = False
                    includedVar = False
                    
                    varDecl = self.genDeclarations.get(varName)

                    domain, domains, domains_with_indices, dependencies_vec, sub_indices_vec, stmtIndex = self._getSubIndicesDomainsAndDependencies(varName)
                    _types, dim, minVal, maxVal = self._getProperties(varName)

                    _subIndices = self._getIndicesFromDeclaration(varDecl, stmtIndex)

                    domains_aux = []

                    if domain and domain.strip() != "":
                        domains0 = self._getDomains(domains)
                        
                        for d in domains0:
                            if d in self.tuples:
                                d = "int"
                                _tuple = self.tuples[d]
                                dimen = _tuple["dimen"]

                                if dimen != None:
                                    for i in range(dimen):
                                        domains_aux.append(d)
                            else:
                                domains_aux.append(d)
                            
                        isArray = True

                    elif minVal != None and len(minVal) > 0 and maxVal != None and len(maxVal) > 0:
                        if self._hasAllIndices(minVal, maxVal):
                            domainMinMax = []
                            for i in range(len(minVal)):
                                d = str(minVal[i])+".."+str(maxVal[i])
                                domainMinMax.append(d)
                                domains_aux.append(d)
                            
                            domains_aux = self._getDomains(domainMinMax)
                            domain = ", ".join(domains_aux)
                            domains_with_indices = self._processDomainsWithIndices(domainMinMax)
                            domains = domainMinMax
                            isArray = True

                    elif dim > 0:
                            domains_aux = ["int"]*dim
                            domain = ", ".join(domains_aux)
                            domains_with_indices = self._processDomainsWithIndices(domains_aux)
                            domains = domains_aux
                            isArray = True

                    if not domain and varDecl != None:
                        size = len(_subIndices)
                        if size > 0:
                            isArray = True
                            domains_aux = ["int"]*size
                            domains_with_indices = self._processDomainsWithIndices(domains_aux)

                    if isArray:
                        
                        for i in range(len(domains_aux)):
                            d = domains_aux[i]
                            if d == "int":
                                index = "INDEX_SET_"+varName+"_"+str(i+1)

                                setint = "set of int: "+index
                                
                                if i < len(domains) and (".." in domains[i] or domains[i] == "int"):

                                    if domains[i] != "int":
                                        setint += " = " + domains[i]

                                    if i < len(domains_with_indices) and " in " in domains_with_indices[i]:
                                        
                                        pos = domains_with_indices[i].find(" in ")
                                        domains_with_indices[i] = domains_with_indices[i][:pos] + " in " + index

                                setint += ";\n\n"

                                self.additionalParameters[index] = setint

                                domains_aux[i] = index

                        varStr += "array["
                        varStr += ", ".join(domains_aux) + "]"

                    if varDecl != None:
                        ins_vec = varDecl.getIn()
                        ins_vec = self._removePreDefinedTypes(map(lambda el: el.attribute, ins_vec))

                        if ins_vec != None and len(ins_vec) > 0:
                            ins = ins_vec[-1].generateCode(self)
                            
                            if ins != "":
                                includedVar = True
                                if isArray:
                                    varStr += " of var " + ins
                                else:
                                    varStr += "var " + ins

                    if not includedVar:
                        _types = self._removeTypesThatAreNotDeclarable(_types)
                        _types = self._getTypes(_types)
                        
                        if len(_types) > 0:
                            _type = _types[0].getObj()
                            
                            if isinstance(_type, BinarySet):
                                _type = "bool";

                            elif isinstance(_type, IntegerSet):
                                const =  self._getRelationalConstraints(_type.generateCode(self), varName, isArray, sub_indices_vec, domains_with_indices)
                                
                                if const:
                                    self.additionalConstraints.append(const)

                                _type = "int";

                            elif isinstance(_type, SymbolicSet):
                                _type = "string";

                            else:
                                const =  self._getRelationalConstraints(_type.generateCode(self), varName, isArray, sub_indices_vec, domains_with_indices)
                                
                                if const:
                                    self.additionalConstraints.append(const)

                                _type = "float";

                            if _type.strip() != "":
                                includedVar = True
                                if isArray:
                                    varStr += " of var " + _type
                                else:
                                    varStr += "var " + _type

                    if not includedVar:
                        if isArray:
                            varStr += " of var float"
                        else:
                            varStr += "var float"

                    if varDecl != None:

                        if varDecl.getValue() != None:
                            
                            self.newType = varName
                            self.turnStringsIntoInts = True
                            self.removeAdditionalParameter = True
                            self.isSetExpressionWithIndexingExpression = False

                            indexingExpression = None
                            indexingExpression, _subIndicesAux = self._getIndexingExpressionFromDeclaration(varDecl, stmtIndex)

                            if not indexingExpression:
                                indexingExpression = self._getDomainsWithIndicesByIdentifier(varName)
                                if indexingExpression != None and len(indexingExpression) > 0:
                                    indexingExpression = self._getDomainsWithIndices(indexingExpression)
                                    indexingExpression = ", ".join(indexingExpression)

                                else:
                                    indexingExpression = None

                            if isinstance(varDecl.getValue().attribute, SymbolicExpression) or isinstance(varDecl.getValue().attribute, String):
                                self.turnStringsIntoInts = False
                                self.removeAdditionalParameter = False
                                _type = "string"

                            value = varDecl.getValue().attribute.generateCode(self)
                            if not isinstance(varDecl.getValue().attribute, Array):

                                dependencies = varDecl.getValue().attribute.getDependencies(self)
                                if varName in dependencies:
                                    
                                    cnt = None
                                    if isArray:
                                        indices = map(lambda el: el.generateCode(self), _subIndices)
                                        indices = self._getIndices(indices, domains_with_indices)
                                        
                                        if indexingExpression:
                                            cnt = "constraint forall(" + indexingExpression + ")(" + varName + "[" + ",".join(indices) + "] = " + value + ");";

                                    else:
                                        cnt = "constraint " + varName + " = " + value + ";";

                                    if cnt:
                                        self.additionalConstraints.append(cnt)

                                    value = ""
                                    
                                else:
                                    if self._hasFunctionsToRemove(value):
                                        value = ""

                                    else:

                                        self.getOriginalIndices = True
                                        value2 = varDecl.getValue().attribute.generateCode(self)
                                        self.getOriginalIndices = False
                                        
                                        if value2 in self.setsWitOperations and not self._checkIsValuesBetweenBraces(value2):
                                            value = self.setsWitOperations[value2]
                                            self.setsWitOperationsUsed.append(value)
                                            
                                            if value2 in self.setsWitOperationsIndices:
                                                v = self.setsWitOperationsIndices[value2]

                                                if v["dimen"] > 0:
                                                    value += "["
                                                    inds = []
                                                    for i in range(v["dimen"]):
                                                        inds.append(v["indices"][i])
                                                    value += ",".join(inds) + "]"
                                            
                                            _type = "set of int:"
                                            
                                        self.newType = "int"
                                        self.turnStringsIntoInts = False
                                        self.removeAdditionalParameter = False

                                        rangeSet = self._getRange(varDecl.getValue().attribute)
                                        if rangeSet != None:
                                            _type = "set of int:"
                                            value = rangeSet.generateCode(self)

                                        elif value.startswith("["):
                                            _type = "set of int:"
                                        
                                        if "{" in value and (self.isSetExpressionWithIndexingExpression or isArray):
                                            value = ""
                                            self.isSetExpressionWithIndexingExpression = False

                                        elif isArray or len(_subIndices) > 0 or "[" in value:
                                            
                                            if indexingExpression != None and indexingExpression.strip() != "":
                                                value = "["+value+" | "+indexingExpression+"]"

                                                if not value.startswith("array"):
                                                    
                                                    if len(domains) > 0:
                                                        length_domains = len(domains)
                                                        indices = []
                                                        array = "array["

                                                        for i in range(length_domains):
                                                            d = domains[i]
                                                            if d == "int":
                                                                index = "INDEX_SET_"+varName+"_"+str(i+1)
                                                                setint = "set of int: "+index

                                                                if i < len(domains_aux) and ".." in domains_aux[i]:
                                                                    setint += " = " + domains_aux[i]

                                                                    if i < len(domains_with_indices) and " in " in domains_with_indices[i]:
                                                                        pos = domains_with_indices[i].find(" in ")
                                                                        domains_with_indices[i] = domains_with_indices[i][:pos] + " in " + index

                                                                setint += ";\n\n"

                                                                self.additionalParameters[index] = setint
                                                                indices.append(index)

                                                            else:
                                                                indices.append(d)

                                                        array += ", ".join(indices) + "]"
                                                        isArray = True

                                                        value = "array"+str(length_domains)+"d("+", ".join(indices)+", "+value+")"

                                        self.genValueAssigned.add(GenObj(varName))
                        else:

                            cnt = ""
                            attr = varDecl.getRelationEqualTo()
                            if attr != None:

                                indexingExpression, _subIndicesAux = self._getIndexingExpressionFromDeclaration(varDecl, stmtIndex)
                                attribute = attr.attribute.generateCode(self)

                                if not self._hasFunctionsToRemove(attribute):

                                    if isArray:
                                        domains = self._getDomainsWithIndices(domains_with_indices)
                                        indices = self._getIndices(sub_indices_vec, domains_with_indices)
                                        cnt += "constraint forall("+", ".join(domains)+")(" + varName + "["+",".join(indices)+"] = " + attribute + ");";
                                    else:
                                        cnt += "constraint " + varName + " = " + attribute + ";";

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
                                    if isArray:
                                        domains = self._getDomainsWithIndices(domains_with_indices)
                                        cnt += "constraint forall("+", ".join(domains)+")(" + cntAux + ");"
                                    else:
                                        cnt += "constraint " + cntAux + ";"
                                    self.additionalConstraints.append(cnt)

                    if value != "" and value.strip() != "":
                        varName += " = " + value.strip()

                    varStr += ": " + varName
                    varStr += ";\n\n"

                    self.parentScope = previousParentScope

        return varStr

    def _declareParam(self, _genParameter):
        
        self.scope = 0
        self.stmtIndex += 1

        if not self.stmtIndex in self.scopes:
            self.scopes[self.stmtIndex] = {}
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "_declareParam"}

        previousParentScope = self.parentScope
        self.parentScope = self.scope

        paramStr = ""
        param = _genParameter.getName()
        domain = None
        _type = None
        isArray = False
        includedType = False
        array = ""
        
        varDecl = self.genDeclarations.get(_genParameter.getName())

        domain, domains, domains_with_indices, dependencies_vec, sub_indices_vec, stmtIndex = self._getSubIndicesDomainsAndDependencies(param)
        _types, dim, minVal, maxVal = self._getProperties(_genParameter.getName())

        _subIndices = self._getIndicesFromDeclaration(varDecl, stmtIndex)

        if domain != None and domain.strip() != "":
            domains_aux = domains
            domains = self._getDomains(domains)
            domain = ", ".join(domains)
            array += "array[" + domain + "]"
            isArray = True

        elif minVal != None and len(minVal) > 0 and maxVal != None and len(maxVal) > 0:
            if self._hasAllIndices(minVal, maxVal):
                domainMinMax = []
                for i in range(len(minVal)):
                    domainMinMax.append(str(minVal[i])+".."+str(maxVal[i]))

                domains_aux = domainMinMax
                domains = self._getDomains(domainMinMax)
                array += "array["+", ".join(domains)+"]"
                domains_with_indices = self._processDomainsWithIndices(domainMinMax)
                isArray = True

        elif dim > 0:
                domains_aux = ["int"]*dim
                domains = self._getDomains(domains_aux)
                array += "array["+", ".join(domains)+"]"
                domains_with_indices = self._processDomainsWithIndices(domains_aux)
                isArray = True

        if not domain and varDecl != None:
            indexingExpression = None
            indexingExpression, _subIndicesAux = self._getIndexingExpressionFromDeclaration(varDecl, stmtIndex)

            if indexingExpression:
                domain = indexingExpression
                isArray = True
                array += "array[" + domain + "]"

        if varDecl != None:
            
            ins_vec = varDecl.getIn()
            ins_vec = self._removePreDefinedTypes(map(lambda el: el.attribute, ins_vec))
            if ins_vec != None and len(ins_vec) > 0:
                ins = ins_vec[-1].generateCode(self)

                if ins != "":
                    includedType = True
                    _type = ins
        
        if not includedType:
            _types = self._removeTypesThatAreNotDeclarable(_types)
            _types = self._getTypes(_types)
            
            if len(_types) > 0:
                _type = _types[0].getObj()
                
                if isinstance(_type, BinarySet):
                    _type = "bool";

                elif isinstance(_type, IntegerSet):
                    _type = "int";

                elif isinstance(_type, SymbolicSet):
                    _type = "string";

                elif isinstance(_type, RealSet):
                    _type = "float";

                if _type.strip() != "":
                    includedType = True

        if not includedType and param in self.parameterIsIndexOf:
            value = self.parameterIsIndexOf[param]
            var = value["indexOf"]
            pos = value["pos"]

            setExpression = self._getDomainByIdentifier(var)

            _types = self._splitDomain(setExpression)
            if pos < len(_types):
                _type_aux = _types[pos]

                if not ".." in _type_aux:
                    includedType = True
                    _type = _type_aux

        if not includedType:
            if _genParameter.getIsInteger():
                _type = "int"

            elif _genParameter.getIsSymbolic():
                _type = "string"

            elif _genParameter.getIsLogical():
                _type = "bool"

            else:
                _type = "float"

        if _type in self.listSetOfInts:
            _type = "int"

        value = ""
        if varDecl != None:
            if varDecl.getValue() != None:
                
                self.newType = param
                self.turnStringsIntoInts = True
                self.removeAdditionalParameter = True
                self.isSetExpressionWithIndexingExpression = False

                indexingExpression = None
                indexingExpression, _subIndicesAux = self._getIndexingExpressionFromDeclaration(varDecl, stmtIndex)

                if not indexingExpression:
                    indexingExpression = self._getDomainsWithIndicesByIdentifier(param)
                    if indexingExpression != None and len(indexingExpression) > 0:
                        indexingExpression = self._getDomainsWithIndices(indexingExpression)
                        indexingExpression = ", ".join(indexingExpression)

                    else:
                        indexingExpression = None

                if isinstance(varDecl.getValue().attribute, SymbolicExpression) or isinstance(varDecl.getValue().attribute, String):
                    self.turnStringsIntoInts = False
                    self.removeAdditionalParameter = False
                    _type = "string"

                value = varDecl.getValue().attribute.generateCode(self)

                if not isinstance(varDecl.getValue().attribute, Array):

                    dependencies = varDecl.getValue().attribute.getDependencies(self)
                    if param in dependencies:
                        
                        cnt = None
                        if isArray:
                            indices = map(lambda el: el.generateCode(self), _subIndices)
                            indices = self._getIndices(indices, domains_with_indices)
                            
                            if indexingExpression:
                                cnt = "constraint forall(" + indexingExpression + ")(" + param + "[" + ",".join(indices) + "] = " + value + ");";

                        else:
                            cnt = "constraint " + param + " = " + value + ";";

                        if cnt:
                            self.additionalConstraints.append(cnt)

                        value = ""
                        
                    else:
                        if self._hasFunctionsToRemove(value):
                            value = ""

                        else:

                            self.getOriginalIndices = True
                            value2 = varDecl.getValue().attribute.generateCode(self)
                            self.getOriginalIndices = False
                            
                            if value2 in self.setsWitOperations and not self._checkIsValuesBetweenBraces(value2):
                                value = self.setsWitOperations[value2]
                                self.setsWitOperationsUsed.append(value)
                                
                                if value2 in self.setsWitOperationsIndices:
                                    v = self.setsWitOperationsIndices[value2]

                                    if v["dimen"] > 0:
                                        value += "["
                                        inds = []
                                        for i in range(v["dimen"]):
                                            inds.append(v["indices"][i])
                                        value += ",".join(inds) + "]"
                                
                                _type = "set of int:"
                                
                            self.newType = "int"
                            self.turnStringsIntoInts = False
                            self.removeAdditionalParameter = False

                            rangeSet = self._getRange(varDecl.getValue().attribute)
                            if rangeSet != None:
                                _type = "set of int:"
                                value = rangeSet.generateCode(self)

                            elif value.startswith("["):
                                _type = "set of int:"
                            
                            if "{" in value and (self.isSetExpressionWithIndexingExpression or isArray):
                                value = ""
                                self.isSetExpressionWithIndexingExpression = False

                            elif isArray or len(_subIndices) > 0 or "[" in value:
                                
                                if indexingExpression != None and indexingExpression.strip() != "":
                                    value = "["+value+" | "+indexingExpression+"]"

                                    if not value.startswith("array"):
                                        
                                        if len(domains) > 0:
                                            length_domains = len(domains)
                                            indices = []
                                            array = "array["

                                            for i in range(length_domains):
                                                d = domains[i]
                                                if d == "int":
                                                    index = "INDEX_SET_"+param+"_"+str(i+1)
                                                    setint = "set of int: "+index

                                                    if i < len(domains_aux) and ".." in domains_aux[i]:
                                                        setint += " = " + domains_aux[i]

                                                        if i < len(domains_with_indices) and " in " in domains_with_indices[i]:
                                                            pos = domains_with_indices[i].find(" in ")
                                                            domains_with_indices[i] = domains_with_indices[i][:pos] + " in " + index

                                                    setint += ";\n\n"

                                                    self.additionalParameters[index] = setint
                                                    indices.append(index)

                                                else:
                                                    indices.append(d)

                                            array += ", ".join(indices) + "]"
                                            isArray = True

                                            value = "array"+str(length_domains)+"d("+", ".join(indices)+", "+value+")"

                            self.genValueAssigned.add(GenObj(param))

        if not _type or _type.strip() == "":
            _type = "float"

        if _type == "set of int:":
            self.listSetOfInts.append(param)

        if array != "":
            paramStr += array

        if _type[0] == "{" and _type[-1] == "}" and ".." in _type:
            _type = _type[1:-1]

        if _type != "enum" and not _type.endswith(":"):
            _type = _type+":"

        if isArray:
            paramStr += " of " + _type
        else:
            paramStr += _type

        paramStr += " " + param

        if value != "":
            paramStr += " = " + value

        paramStr += ";\n\n"

        self.parentScope = previousParentScope

        return paramStr

    def _declareSet(self, _genSet):

        self.scope = 0
        self.stmtIndex += 1

        if not self.stmtIndex in self.scopes:
            self.scopes[self.stmtIndex] = {}
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "_declareSet"}

        previousParentScope = self.parentScope
        self.parentScope = self.scope

        name = _genSet.getName()
        
        setStr = ""
        index2 = ""
        varDecl = self.genDeclarations.get(name)
        value = ""
        isArray = False
        array = ""
        deleteTupleIndex = False
        arrayFromTuple = False
        domainOriginal = None

        domain, domains, domains_with_indices, dependencies_vec, sub_indices_vec, stmtIndex = self._getSubIndicesDomainsAndDependencies(name)
        _types, dim, minVal, maxVal = self._getProperties(_genSet.getName())
        
        _subIndices = self._getIndicesFromDeclaration(varDecl, stmtIndex)
        
        if domain != None and domain.strip() != "":
            domains_aux = domains
            domains = self._getDomains(domains)
            domainOriginal = domain
            domain = ", ".join(domains)
            array += "array[" + domain + "]"
            isArray = True
            
        elif minVal != None and len(minVal) > 0 and maxVal != None and len(maxVal) > 0:
            if self._hasAllIndices(minVal, maxVal):
                domainMinMax = []
                for i in range(len(minVal)):
                    domainMinMax.append(str(minVal[i])+".."+str(maxVal[i]))

                domains_aux = domainMinMax
                domains = self._getDomains(domainMinMax)
                array += "array["+", ".join(domains)+"]"
                domains_with_indices = self._processDomainsWithIndices(domainMinMax)
                isArray = True

        elif dim > 0:
                domains_aux = ["int"]*dim
                domains = self._getDomains(domains_aux)
                array += "array["+", ".join(domains)+"]"
                domains_with_indices = self._processDomainsWithIndices(domains_aux)
                isArray = True

        if name in self.tuplesDeclared:
            isArray = True
            _tuple = self.tuplesDeclared[name]
            index1 = _tuple["index1"]
            index2 = _tuple["index2"]
            _type  = _tuple["type"]

            if _type != "enum" and not _type.endswith(":"):
                _type = _type+":"

            self.array2dIndex1 = index1
            self.array2dIndex2 = index2

        else:
            _type = "enum"

        if varDecl != None:
            
            if not domain:
                indexingExpression = None
                indexingExpression, _subIndicesAux = self._getIndexingExpressionFromDeclaration(varDecl, stmtIndex)

                if indexingExpression:
                    domain = indexingExpression
                    isArray = True
                    array += "array[" + domain + "]"

            ins_vec = varDecl.getIn()
            ins_vec = self._removePreDefinedTypes(map(lambda el: el.attribute, ins_vec))
            if ins_vec != None and len(ins_vec) > 0:
                ins = ins_vec[-1].generateCode(self)

                if ins != "":
                    _type = ins

            if varDecl.getValue() != None:
                
                _subIndices = []
                if varDecl.getSubIndices():
                    for key in varDecl.getSubIndices():
                        _subIndices = varDecl.getSubIndices()[key]
                        break

                self.newType = name
                self.turnStringsIntoInts = True
                self.removeAdditionalParameter = True
                self.isSetExpressionWithIndexingExpression = False

                indexingExpression = None
                if varDecl.getIndexingExpression():
                    for key in varDecl.getIndexingExpression():
                        indexingExpression = varDecl.getIndexingExpression()[key].generateCode(self)
                        break

                else:

                    indexingExpression = self._getDomainsWithIndicesByIdentifier(name)
                    if indexingExpression != None and len(indexingExpression) > 0:
                        indexingExpression = ", ".join(indexingExpression)
                    else:
                        indexingExpression = None

                value = varDecl.getValue().attribute.generateCode(self)

                dependencies = varDecl.getValue().attribute.getDependencies(self)
                
                if name in dependencies:
                    
                    if isArray:

                        indices = map(lambda el: el.generateCode(self), _subIndices)
                        indices = self._getIndices(indices, domains_with_indices)

                        cnt = "constraint forall(" + indexingExpression + ")(" + name + "[" + ",".join(indices) + "] = " + value + ");";

                    else:

                        cnt = "constraint " + name + " = " + value + ";";

                    self.additionalConstraints.append(cnt)

                    value = ""
                    
                else:

                    if self._hasFunctionsToRemove(value):
                        value = ""

                    else:
                        
                        self.getOriginalIndices = True
                        value2 = varDecl.getValue().attribute.generateCode(self)
                        self.getOriginalIndices = False
                        
                        if value2 in self.setsWitOperations and not self._checkIsValuesBetweenBraces(value2):
                            value = self.setsWitOperations[value2]
                            self.setsWitOperationsUsed.append(value)

                            if value2 in self.setsWitOperationsIndices:
                                v = self.setsWitOperationsIndices[value2]
                                
                                if v["dimen"] > 0:
                                    value += "["
                                    inds = []

                                    for i in range(v["dimen"]):
                                        inds.append(v["indices"][i])

                                    value += ",".join(inds) + "]"

                            
                            _type = "set of int:"

                        self.newType = "int"
                        self.turnStringsIntoInts = False
                        self.removeAdditionalParameter = False

                        rangeSet = self._getRange(varDecl.getValue().attribute)
                        
                        if rangeSet != None:
                            _type = "set of int:"
                            value = rangeSet.generateCode(self)

                        elif value.startswith("["):
                            _type = "set of int:"

                        if "{" in value and (self.isSetExpressionWithIndexingExpression or isArray):
                            value = ""
                            self.isSetExpressionWithIndexingExpression = False

                        elif isArray or len(_subIndices) > 0 or "[" in value:

                            if indexingExpression != None and indexingExpression.strip() != "":
                                value = "["+value+" | "+indexingExpression+"]"

                                if not value.startswith("array"):
                                    domain = self._getDomainByIdentifier(name)
                                    if domain != None and domain.strip() != "":
                                        domains = self._getDomainsByIdentifier(name)
                                        domains_aux = domains
                                        domains = self._getDomains(domains)

                                        if len(domains) > 0:
                                            length_domains = len(domains)
                                            indices = []
                                            array = "array["

                                            for i in range(length_domains):
                                                d = domains[i]
                                                if d == "int":
                                                    index = "INDEX_SET_"+name+"_"+str(i+1)
                                                    setint = "set of int: "+index

                                                    if i < len(domains_aux) and ".." in domains_aux[i]:
                                                        setint += " = " + domains_aux[i]

                                                        if i < len(domains_with_indices) and " in " in domains_with_indices[i]:
                                                            pos = domains_with_indices[i].find(" in ")
                                                            domains_with_indices[i] = domains_with_indices[i][:pos] + " in " + index

                                                    setint += ";\n\n"

                                                    self.additionalParameters[index] = setint
                                                    indices.append(index)

                                                else:
                                                    indices.append(d)

                                            if _type == "enum":
                                                _type = "int:"

                                            arrayFromTuple = True
                                            array += ", ".join(indices) + "] of "+_type+" " + name
                                            deleteTupleIndex = True

                                            value = "array"+str(length_domains)+"d("+", ".join(indices)+", "+value+")"

                        self.genValueAssigned.add(GenObj(name))

        if name in self.tuplesDeclared:
            _tuple = self.tuplesDeclared[name]
            index1 = _tuple["index1"]

            if deleteTupleIndex:
                del self.additionalParameters[index1]

            else:
                index2 = _tuple["index2"]
                _type  = _tuple["type"]
                #if _type.strip() == "" or _type == "int" or _type == "int:" or "{" in _type or "[" in _type or _tuple["type"] == "set of int":

                if _type != "enum" and not _type.endswith(":"):
                    _type = _type+":"

                if _type == "enum":
                    _type = "int:"
                
                arrayFromTuple = True
                array = "array["+index1

                if index2 != None:
                    array += ", "+index2

                array += "] of "+_type+" " + name

                self.array2dIndex1 = index1
                self.array2dIndex2 = index2

                #if domainOriginal and domainOriginal != "int" and not "{" in domainOriginal and not "[" in domainOriginal:
                #    self.additionalParameters[index1] = self.additionalParameters[index1][:-3] + " = " + domainOriginal + ";\n\n"

        if array != "":
            setStr += array

            if _type == "enum":
                _type = "int:"

        if not arrayFromTuple:
            if _type != "enum" and not _type.endswith(":"):
                _type = _type+":"

            if setStr == "":
                setStr += _type + " " + name
            else:
                setStr += " of " + _type + " " + name

        if value != "":
            setStr += " = " + value

        self.array2dIndex1 = None
        self.array2dIndex2 = None

        if _type == "enum":
            self.listEnums.append(name)

        elif _type == "set of int:":
            self.listSetOfInts.append(name)
            
        setStr += ";\n\n"
        
        self.parentScope = previousParentScope

        return setStr

    def _declareSetsAndParams(self):
        paramSetStr = ""

        for _genObj in self.genSets.getAll():
            paramSetStr += self._declareSet(_genObj)

        for _genObj in self.genParameters.getAll():
            paramSetStr += self._declareParam(_genObj)

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

    def _preModel(self):
        res = ""

        setsAndParams = self._declareSetsAndParams()
        if setsAndParams != "":
            res += setsAndParams

        identifiers = self._declareVars()
        if identifiers != "":
            if res != "":
                res += "\n"

            res += identifiers

        del_list = []
        for key in self.additionalParameters:
            if key in self.setsWitOperationsInv and not key in self.setsWitOperationsUsed:
                del_list.append(key)

        for d in del_list:
            del self.additionalParameters[d]

            index = "INDEX_SET_"+d
            if index in self.additionalParameters:
                del self.additionalParameters[index]

        if len(self.additionalParameters) > 0:
            res += "".join([self.additionalParameters[k] for k in sorted(self.additionalParameters)])

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

        constraints = filter(lambda el: isinstance(el, Constraint), node.constraints.getConstraints())
        objectives = filter(lambda el: isinstance(el, Objective), node.constraints.getConstraints())

        node.constraints.generateCode(self)
        map(lambda el: self._getCodeObjective(el), objectives)

        preModel = self._preModel()
        if preModel != "":
            preModel += "\n"

        # check libraries to include
        if len(self.include) > 0:
            preModel += "\n\n".join(map(lambda lb: "include \"" + lb + "\";", self.include))
            preModel += "\n\n"

        res = "\n\n".join(filter(lambda cnt: self.removeInvalidConstraint(cnt), map(lambda el: self._getCodeConstraint(el), constraints))) + "\n\n"

        if len(objectives) > 0:
            obj = objectives[0]
            res += "\n\n" + self._getObjectiveCode(obj) + "\n\n"
        else:
            res += "solve satisfy;\n\n"

        res = preModel + res

        return res

    def generateCode_LinearProgram(self, node):
        self._initialize()

        if node.constraints:
            node.constraints.generateCode(self)

        res = ""

        preModel = self._preModel()
        if preModel != "":
            preModel += "\n"

        if node.constraints:
            res += node.constraints.generateCode(self) + "\n\n"
        
        res += "\n\n" + node.objectives.generateCode(self) + "\n\n"

        res = preModel + res

        return res

    # Declarations
    def generateCode_Declarations(self, node):
        self.scope = 0
        self.stmtIndex += 1

        if not self.stmtIndex in self.scopes:
            self.scopes[self.stmtIndex] = {}
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_Objective"}

        previousParentScope = self.parentScope
        self.parentScope = self.scope

        declarations = map(lambda el: el.generateCode(self), node.declarations)
        res = "\n\n".join(declarations) + "\n\n"

        self.parentScope = previousParentScope

        return res

    def generateCode_Declaration(self, node):
        res = node.declarationExpression.generateCode(self)

        if node.indexingExpression:
            res += "{"+ node.indexingExpression.generateCode(self) +"}"

        return res

    def generateCode_DeclarationExpression(self, node):
        identifiers = []
        for identifier in node.identifiers:
            identifiers.append(identifier.generateCode(self))

        res = ", ".join(identifiers)

        if node.attributeList and len(node.attributeList) > 0:
            attr = map(lambda el: el.generateCode(self), node.attributeList)
            res += "\n" + ", ".join(attr)

        return res

    def generateCode_DeclarationAttribute(self, node):
        return node.attribute.generateCode(self)

    # Objectives
    def generateCode_Objectives(self, node):
        obj = node.objectives[0]
        objStr = self._getObjectiveCode(obj)

        return objStr;

    def _getObjectiveCode(self, obj):
        objStr = "solve " + obj.type + " "+ obj.linearExpression.generateCode(self) +";\n\n";

        return objStr;

    # Objective Function
    def generateCode_Objective(self, node):
        """
        Generate the code in MathProg for this Objective
        """
        self.scope = 0
        self.stmtIndex += 1

        if not self.stmtIndex in self.scopes:
            self.scopes[self.stmtIndex] = {}
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_Objective"}

        previousParentScope = self.parentScope
        self.parentScope = self.scope

        res = self._getObjectiveCode(node)

        self.parentScope = previousParentScope

        return res

    # Constraints
    def generateCode_Constraints(self, node):
        return "\n\n".join(filter(lambda el: self.removeInvalidConstraint(el), map(self._getCodeConstraint, node.constraints)))

    def generateCode_Constraint(self, node):
        self.scope = 0
        self.stmtIndex += 1

        if not self.stmtIndex in self.scopes:
            self.scopes[self.stmtIndex] = {}
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_Constraint"}

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

    def generateCode_LogicalConstraintExpression(self, node):
        res = node.logicalExpression.generateCode(self) + " " + node.op + " " + node.constraintExpression1.generateCode(self)
        
        if node.constraintExpression2:
            res += " else " + node.constraintExpression2.generateCode(self)

        return res

    def generateCode_ConditionalConstraintExpression(self, node):
        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_ConditionalConstraintExpression1"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.constraintExpression1.generateCode(self)

        if node.constraintExpression2:
            if self.stmtIndex > -1:
                self.scope += 1
                self.scopes[self.stmtIndex][self.scope] = {"parent": previousParentScope, "where": "generateCode_ConditionalConstraintExpression2"}

            res += " else " + node.constraintExpression2.generateCode(self)

        else:
            res += " else true"

        res += " endif"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res


    # Linear Expression
    def generateCode_ValuedLinearExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_LinearExpressionBetweenParenthesis(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_LinearExpressionBetweenParenthesis"}

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
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_IteratedLinearExpression"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        SUM = "sum"

        indexingExpression = node.indexingExpression.generateCode(self)
        if isinstance(node.indexingExpression, NumericExpressionWithArithmeticOperation):
            indexingExpression = "floor(" + indexingExpression + ")"
            
        if node.numericExpression:
            numericExpression = node.numericExpression.generateCode(self)
            if isinstance(node.numericExpression, NumericExpressionWithArithmeticOperation):
                numericExpression = "floor(" + numericExpression + ")"
            else:
                numericExpression = "(" + numericExpression + ")"
                
            res = SUM + "(" + indexingExpression + ".." + numericExpression + "))("
        else:
            res = SUM + "(" + indexingExpression + ")("

        res += node.linearExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_ConditionalLinearExpression(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_ConditionalLinearExpression"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "if " + node.logicalExpression.generateCode(self)

        if node.linearExpression1:
            res += " then " + node.linearExpression1.generateCode(self)

            if node.linearExpression2:
                self.scope += 1
                self.scopes[self.stmtIndex][self.scope] = {"parent": previousParentScope}

                res += " else " + node.linearExpression2.generateCode(self)

            res += " endif"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def _getNumericFunction(self, function):
        if function == NumericExpressionWithFunction.LOG:
            function = "ln"
        elif function == "trunc":
            function = NumericExpressionWithFunction.FLOOR

        return function

    # Numeric Expression
    def generateCode_NumericExpressionWithFunction(self, node):
        if not isinstance(node.function, str):
            function = node.function.generateCode(self)
        else:
            function = node.function

        function = self._getNumericFunction(function)

        if function in self.LIBRARIES and not function in self.include:
            self.include.append(self.LIBRARIES[function])

        res = function + "("

        if node.numericExpression1 != None:
            numericExpression1 = node.numericExpression1.generateCode(self)
            
            if function == NumericExpressionWithFunction.CARD and numericExpression1 in self.tuplesDeclared:
                _tuple = self.tuplesDeclared[numericExpression1]
                numericExpression1 = _tuple["index1"]

            res += numericExpression1

        if node.numericExpression2 != None:
            if function == NumericExpressionWithFunction.ATAN:
                res += "/"
            else:
                res += ", "

            res += node.numericExpression2.generateCode(self)

        res += ")"

        return res

    def generateCode_FractionalNumericExpression(self, node):
        
        numerator = node.numerator
        if isinstance(node.numerator, ValuedNumericExpression):
            numerator = numerator.value
            
        if not isinstance(numerator, Identifier) and not isinstance(numerator, Number) and not isinstance(numerator, NumericExpressionWithFunction):
            numerator = "("+numerator.generateCode(self)+")"
        else:
            numerator = numerator.generateCode(self)
            
        denominator = node.denominator
        if isinstance(denominator, ValuedNumericExpression):
            denominator = denominator.value
            
        if not isinstance(denominator, Identifier) and not isinstance(denominator, Number) and not isinstance(denominator, NumericExpressionWithFunction):
            denominator = "("+denominator.generateCode(self)+")"
        else:
            denominator = denominator.generateCode(self)
            
        return numerator+"/"+denominator

    def generateCode_ValuedNumericExpression(self, node):
        self.turnStringsIntoInts = True
        res = node.value.generateCode(self)
        self.turnStringsIntoInts = False
        return res

    def generateCode_NumericExpressionBetweenParenthesis(self, node):
        
        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_NumericExpressionBetweenParenthesis", "context": "(" + node.numericExpression.generateCode(self) + ")"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "(" + node.numericExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_NumericExpressionWithArithmeticOperation(self, node):
        res = ""

        if isinstance(node.numericExpression1, ValuedNumericExpression):
            node.numericExpression1 = node.numericExpression1.value

        if node.op == NumericExpressionWithArithmeticOperation.POW:# and not (isinstance(node.numericExpression2, ValuedNumericExpression) or isinstance(node.numericExpression2, NumericExpressionBetweenParenthesis)):
            res += "pow(" + node.numericExpression1.generateCode(self) + ","+node.numericExpression2.generateCode(self) + ")"

        elif (node.op == NumericExpressionWithArithmeticOperation.QUOT or node.op == NumericExpressionWithArithmeticOperation.MOD) and \
            not isinstance(node.numericExpression1, Identifier) and not isinstance(node.numericExpression1, Number):

            res += "floor(" + node.numericExpression1.generateCode(self) + ") " + node.op + " " + node.numericExpression2.generateCode(self)

        else:
            res += node.numericExpression1.generateCode(self) + " " + node.op + " " + node.numericExpression2.generateCode(self)

        return res

    def generateCode_MinusNumericExpression(self, node):
        return "-" + node.numericExpression.generateCode(self)

    def generateCode_IteratedNumericExpression(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_IteratedNumericExpression"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        indexingExpression = node.indexingExpression.generateCode(self)
        if isinstance(node.indexingExpression, NumericExpressionWithArithmeticOperation):
            indexingExpression = "floor(" + indexingExpression + ")"

        if node.supNumericExpression:
            supNumericExpression = node.supNumericExpression.generateCode(self)
            if isinstance(node.supNumericExpression, NumericExpressionWithArithmeticOperation):
                supNumericExpression = "floor(" + supNumericExpression + ")"
            else:
                supNumericExpression = "(" + supNumericExpression + ")"

            res = str(node.op) + "(" + indexingExpression + ".." + supNumericExpression + ")("
        else:
            res = str(node.op) + "(" + indexingExpression + ")("

        res += node.numericExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_ConditionalNumericExpression(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_ConditionalNumericExpression"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.numericExpression1.generateCode(self)

        if node.numericExpression2:
            res += " else " + node.numericExpression2.generateCode(self)

        else:
            res += " else 0"

        res += " endif"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    # Symbolic Expression

    def generateCode_StringSymbolicExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_SymbolicExpressionBetweenParenthesis(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_SymbolicExpressionBetweenParenthesis"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "(" + node.symbolicExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_SymbolicExpressionWithOperation(self, node):
        return node.symbolicExpression1.generateCode(self) + " " + node.op + " " + node.symbolicExpression2.generateCode(self)


    # Expression List
    def generateCode_ExpressionList(self, node):
        if self.checkSetExpressionWithIndexingExpression:
            self.isSetExpressionWithIndexingExpression = True

        indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, node.entriesIndexingExpression))
        res = ", ".join(indexing)

        if self.array2dIndex2 != None:
            res += ", idx2 in " + self.array2dIndex2

        if node.logicalExpression:
            res += " | " + node.logicalExpression.generateCode(self)

        if self.stmtIndex > -1:
            if "newEntryLogicalExpression" in self.scopes[self.stmtIndex][self.scope] and len(self.scopes[self.stmtIndex][self.scope]["newEntryLogicalExpression"]) > 0:
                if not node.logicalExpression:
                    res += " where "
                else:
                    res += " /\ "

                entries = " /\ ".join(self.scopes[self.stmtIndex][self.scope]["newEntryLogicalExpression"])

                res += entries


        return res

    # Indexing Expression
    def generateCode_IndexingExpression(self, node):
        if self.checkSetExpressionWithIndexingExpression:
            self.isSetExpressionWithIndexingExpression = True

        indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, node.entriesIndexingExpression))
        res = ", ".join(indexing)

        if self.array2dIndex2 != None:
            res += ", idx2 in " + self.array2dIndex2

        if node.logicalExpression:
            res += " where " + node.logicalExpression.generateCode(self)

        if self.stmtIndex > -1:
            if "newEntryLogicalExpression" in self.scopes[self.stmtIndex][self.scope] and len(self.scopes[self.stmtIndex][self.scope]["newEntryLogicalExpression"]) > 0:
                if not node.logicalExpression:
                    res += " where "
                else:
                    res += " /\ "

                entries = " /\ ".join(self.scopes[self.stmtIndex][self.scope]["newEntryLogicalExpression"])

                res += entries


        return res
    
    def _checkRealType(self, setExpression, values):
        if not isinstance(values, list):
            values = [values]

        if "[" in setExpression:
            setExpression = setExpression.split("[")[0]

        if setExpression in self.tuplesDeclared:
            
            realtype = self.tuplesDeclared[setExpression]["realtype"]
            if realtype != None:
                self.includeNewIndices = True
                self.to_enum = True
                self.realtype = realtype
                for v in values:
                    v.generateCode(self)

                self.includeNewIndices = False
                self.to_enum = False
                self.realtype = None

        elif ".." in setExpression:
            self.includeNewIndices = True
            self.to_enum = True
            self.realtype = "'realtype'"
            for v in values:
                v.generateCode(self)

            self.includeNewIndices = False
            self.to_enum = False
            self.realtype = None

    def _getSetExpression(self, node):
        setExpression = node.setExpression.generateCode(self)

        if setExpression in self.setsWitOperations:
            setExpression = self.setsWitOperations[setExpression]
            self.setsWitOperationsUsed.append(setExpression)

        return setExpression

    # Entry Indexing Expression
    def generateCode_EntryIndexingExpressionWithSet(self, node):
        if isinstance(node.identifier, ValueList):
            values = filter(self.notInTypesThatAreNotDeclarable, node.identifier.getValues())

            if len(values) > 0:
                
                entries = []
                for v in values:
                    self.replaceNewIndices = False
                    v = v.generateCode(self)
                    entries.append(v)
                    self.replaceNewIndices = True

                    # used to compute new entry logical expresson when set expression is of the type 1..N by D
                    self.lastIdentifier = v
                    setExpression = self._getSetExpression(node)
                    self._checkRealType(setExpression, values)
                    self.lastIdentifier = None


                res = ", ".join(map(lambda var: "not(" + var + " in " + setExpression + ")" if node.op == EntryIndexingExpressionWithSet.NOTIN else \
                                                var + " " + node.op + " " + setExpression, entries))

                return res

        elif isinstance(node.identifier, Tuple) or isinstance(node.identifier, TupleList):
            setExpression = self._getSetExpression(node)

            if not self.getOriginalIndices and setExpression in self.tuplesDeclared:

                index1 = self.tuplesDeclared[setExpression]["index1"]
                values = node.identifier.getValues()

                self.replaceNewIndices = False
                idx = values[0].generateCode(self)
                self.replaceNewIndices = True

                if not "new_indices" in self.scopes[self.stmtIndex][self.scope]:
                    self.scopes[self.stmtIndex][self.scope]["new_indices"] = {}

                self.countNewIndices = 1
                self.includeNewIndices = True

                for v in values:
                    self.newIndexExpression = setExpression+"["+idx+","+str(self.countNewIndices)+"]"
                    v.generateCode(self)

                self.countNewIndices = 0
                self.includeNewIndices = False

                # used to compute new entry logical expresson when set expression is of the type 1..N by D
                self.lastIdentifier = idx
                node.setExpression.generateCode(self)
                self.lastIdentifier = None
                
                return idx + " " + node.op + " " + index1

            else:
                ident = node.identifier.generateCode(self)

                # used to compute new entry logical expresson when set expression is of the type 1..N by D
                self.lastIdentifier = ident
                node.setExpression.generateCode(self)
                self.lastIdentifier = None

                return ident + " " + node.op + " " + setExpression

        elif self.notInTypesThatAreNotDeclarable(node.identifier):
            ident = node.identifier.generateCode(self)

            #self.replaceNewIndices = False

            # used to compute new entry logical expresson when set expression is of the type 1..N by D
            self.lastIdentifier = ident
            setExpression = self._getSetExpression(node)
            self._checkRealType(setExpression, node.identifier)
            self.lastIdentifier = None

            res = ident + " " + node.op + " " + setExpression
            #self.replaceNewIndices = True

            return res

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

        elif isinstance(node.value, Array):
            res = node.identifier.generateCode(self) + " in {" + node.value.value.generateCode(self) + "}"

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

                
                entries = []
                for v in values:
                    self.replaceNewIndices = False
                    v = v.generateCode(self)
                    entries.append(v)
                    self.replaceNewIndices = True

                    self.lastIdentifier = v
                    setExpression = self._getSetExpression(node)
                    self._checkRealType(setExpression, values)
                    self.lastIdentifier = None

                res = " /\\ ".join(map(lambda var: "not(" + var + " in " + setExpression + ")" if node.op == EntryLogicalExpressionWithSet.NOTIN else \
                                                var + " " + node.op + " " + setExpression, entries))

                return res

        elif isinstance(node.identifier, Tuple) or isinstance(node.identifier, TupleList):
            setExpression = self._getSetExpression(node)

            if not self.getOriginalIndices and setExpression in self.tuplesDeclared:
                index1 = self.tuplesDeclared[setExpression]["index1"]
                values = node.identifier.getValues()
                idx = values[0].generateCode(self)

                if not "new_indices" in self.scopes[self.stmtIndex][self.scope]:
                    self.scopes[self.stmtIndex][self.scope]["new_indices"] = {}

                self.countNewIndices = 1
                #self.includeNewIndices = True

                for v in values:
                    self.newIndexExpression = setExpression+"["+idx+","+str(self.countNewIndices)+"]"
                    v.generateCode(self)

                self.countNewIndices = 0
                #self.includeNewIndices = False

                self.lastIdentifier = idx
                node.setExpression.generateCode(self)
                self.lastIdentifier = None

                return idx + " " + node.op + " " + index1

            else:
                ident = node.identifier.generateCode(self)

                self.lastIdentifier = ident
                node.setExpression.generateCode(self)
                self.lastIdentifier = None

                return ident + " " + node.op + " " + setExpression

        elif self.notInTypesThatAreNotDeclarable(node.identifier):
            ident = node.identifier.generateCode(self)
            
            self.lastIdentifier = ident
            setExpression = self._getSetExpression(node)
            self._checkRealType(setExpression, node.identifier)
            self.lastIdentifier = None

            res = ident + " " + node.op + " " + setExpression

            return res

        return ""

    def generateCode_EntryLogicalExpressionWithSetOperation(self, node):
        return node.setExpression1.generateCode(self) + " " + node.op + " " + node.setExpression2.generateCode(self)

    def generateCode_EntryLogicalExpressionIterated(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_EntryLogicalExpressionIterated"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res =  node.op + "(" + node.indexingExpression.generateCode(self) + ")(" +  node.logicalExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_EntryLogicalExpressionBetweenParenthesis(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_EntryLogicalExpressionBetweenParenthesis"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "(" + node.logicalExpression.generateCode(self) + ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_EntryLogicalExpressionNot(self, node):
        return "not " + node.logicalExpression.generateCode(self)

    def generateCode_EntryLogicalExpressionNumericOrSymbolic(self, node):
        if isinstance(node.numericOrSymbolicExpression, SymbolicExpression) or isinstance(node.numericOrSymbolicExpression, Identifier):
            return node.numericOrSymbolicExpression.generateCode(self) + " = true"

        return node.numericOrSymbolicExpression.generateCode(self)

    # Set Expression
    def generateCode_SetExpressionWithValue(self, node):
        if not isinstance(node.value, str):
            return node.value.generateCode(self)
        else:
            return node.value

    def generateCode_SetExpressionWithIndices(self, node):
        self.isSetExpressionWithIndices = True

        var_gen = ""
        if not isinstance(node.identifier, str):
            var_gen = node.identifier.generateCode(self)
        else:
            var_gen = node.identifier

        self.isSetExpressionWithIndices = False

        return  var_gen

    def generateCode_SetExpressionWithOperation(self, node):
        return node.setExpression1.generateCode(self) + " " + node.op + " " + node.setExpression2.generateCode(self)

    def generateCode_SetExpressionBetweenBraces(self, node):
        isRange = False

        if node.setExpression != None:
            self.checkSetExpressionWithIndexingExpression = True
            self.isSetExpressionWithIndexingExpression = False
            self.turnStringsIntoInts = True

            if isinstance(node.setExpression, SetExpressionWithValue):
                setExpression = node.setExpression.value
            else:
                setExpression = node.setExpression

            if isinstance(setExpression, Range):
                isRange = True

            setExpression = setExpression.generateCode(self)

            self.checkSetExpressionWithIndexingExpression = False
            self.turnStringsIntoInts = False

        else:
            setExpression = ""

        if not isRange:
            setExpression = "{" + setExpression + "}"

        return setExpression

    def generateCode_SetExpressionBetweenParenthesis(self, node):
        res =  "(" + node.setExpression.generateCode(self) + ")"
        return res

    def generateCode_IteratedSetExpression(self, node):

        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_IteratedSetExpression"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        

        if node.indexingExpression:
            integrand_str = ""
            indexingExpression = node.indexingExpression.generateCode(self)
        else:
            integrand_str = "set of "
            indexingExpression = None

        isArray2d = False
        if node.integrand != None:
            if not isinstance(node.integrand, Tuple):
                integrand_str += node.integrand.generateCode(self)

            elif self.array2dIndex1 != None and self.array2dIndex2 != None:
                isArray2d = True
                integrand = node.integrand.getValues()

                size = len(integrand)
                integrand_str += "array2d("+self.array2dIndex1+", "+self.array2dIndex2+", [if idx2 == 1 then " + integrand[0].generateCode(self)

                for i in range(1,size-1):
                    integrand_str += " elseif idx2 == " + str(i+1) + " then " + integrand[0].generateCode(self)

                integrand_str += " else " + integrand[size-1].generateCode(self) + " endif "

        res = ""

        if indexingExpression and not isArray2d:
            res += "["

        res += integrand_str

        if indexingExpression:
            res += "| " + indexingExpression + "]"

        if isArray2d:
            res += ")"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_ConditionalSetExpression(self, node):
        if self.stmtIndex > -1:
            self.scope += 1
            self.scopes[self.stmtIndex][self.scope] = {"parent": self.parentScope, "where": "generateCode_ConditionalSetExpression1"}

            previousParentScope = self.parentScope
            self.parentScope = self.scope

        res = "if " + node.logicalExpression.generateCode(self) + " then " + node.setExpression1.generateCode(self)

        if node.setExpression2:
            if self.stmtIndex > -1:
                self.scope += 1
                self.scopes[self.stmtIndex][self.scope] = {"parent": previousParentScope, "where": "generateCode_ConditionalSetExpression2"}

            res += " else " + node.setExpression2.generateCode(self)

        else:
            res += " else {}"

        res += " endif"

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    # Range
    def generateCode_Range(self, node):
        initValue = node.rangeInit.generateCode(self)
        endValue = node.rangeEnd.generateCode(self)

        if node.by != None:

            if self.stmtIndex > -1:
                if not "newEntryLogicalExpression" in self.scopes[self.stmtIndex][self.scope]:
                    self.scopes[self.stmtIndex][self.scope]["newEntryLogicalExpression"] = []
                    
            if self.lastIdentifier != None:
                newEntry = "("+self.lastIdentifier+"-"+initValue+") mod " + node.by.generateCode(self) + " = 0"
                if not newEntry in self.scopes[self.stmtIndex][self.scope]["newEntryLogicalExpression"]:
                    self.scopes[self.stmtIndex][self.scope]["newEntryLogicalExpression"].append(newEntry)

        if isinstance(node.rangeInit, NumericExpressionWithArithmeticOperation):
            initValue = "floor("+initValue+")"

        if isinstance(node.rangeEnd, NumericExpressionWithArithmeticOperation):
            endValue = "floor("+endValue+")"

        res = initValue + ".." + endValue

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

    # Array
    def generateCode_Array(self, node):
        return "[" + ",".join(map(self._getCodeValue, node.value)) + "]"

    # Array with operation
    def generateCode_ArrayWithOperation(self, node):
        return node.array1.generateCode(self) + " " + node.op + " " + node.array2.generateCode(self)

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
            if self.isSetExpressionWithIndices:
                res = ident
                
            else:

                domains = self._getDomainByIdentifier(ident)
                includedDomains = False

                self.countIndicesProcessed += 1
                identProcessing = ident+str(self.countIndicesProcessed)

                self.parentIdentifier = ident
                self.turnStringsIntoInts = True

                if domains != None and domains.strip() != "":
                    domains = self._splitDomain(domains)

                    if len(domains) == length_sub_indices:

                        includedDomains = True
                        for i in range(length_sub_indices):
                            ind = node.sub_indices[i]
                            self.newType = domains[i]

                            self.turnStringsIntoInts = True
                            ind.generateCode(self)
                            self.turnStringsIntoInts = False
                        
                if not includedDomains:

                    self.newType = "int"
                    for i in range(length_sub_indices):
                        ind = node.sub_indices[i]
                        
                        self.turnStringsIntoInts = True
                        ind.generateCode(self)
                        self.turnStringsIntoInts = False
                        
                if isinstance(node.sub_indices, list):

                    res = ident + "["
                    self.posId[identProcessing] = 0
                    for ind in node.sub_indices:
                        if self.posId[identProcessing] > 0:
                            res += ","

                        self.identProcessing = identProcessing

                        self.turnStringsIntoInts = True
                        res += ind.generateCode(self)
                        self.turnStringsIntoInts = False

                        self.posId[identProcessing] += 1
                        
                    res += "]"
                    del self.posId[identProcessing]

                else:

                    self.posId = 0
                    self.identProcessing = identProcessing

                    inds = []
                    res = ident + "["

                    for ind in node.sub_indices:
                        self.turnStringsIntoInts = True
                        ind = self._getCodeID(ind)
                        inds.append(ind)
                        self.turnStringsIntoInts = False

                    res += ",".join(inds) + "]"

                    self.posId = None
                    
                self.turnStringsIntoInts = False
                self.parentIdentifier = None
                self.identProcessing = None
        
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
                    new_index = self.scopes[stmt][scope]["new_indices"][ident]
                    replaced = True

                    if "to_enum('realtype'" in new_index:
                        replaced = False

                        if self.parentIdentifier != None and self.identProcessing != None and self.identProcessing in self.posId:

                            domain = self._getDomainByIdentifier(self.parentIdentifier)
                            
                            if domain != None and domain.strip() != "":
                                domains = []
                                domains_aux = self._splitDomain(domain)
                                
                                for domain in domains_aux:
                                    if domain in self.tuplesDeclared:
                                        dimen  = self.tuplesDeclared[domain]["dimen"]
                                        domain = self.tuplesDeclared[domain]["type"]
                                        
                                        for i in range(dimen):
                                            domains.append(domain)

                                    else:
                                        domains.append(domain)

                                if len(domains) > 0:
                                    
                                    if self.posId[self.identProcessing] < len(domains):
                                        domain = domains[self.posId[self.identProcessing]]

                                        if domain != "int" and domain in self.listEnums:
                                            new_index = new_index.replace("'realtype'", domain)
                                            replaced = True

                    if not replaced:
                        new_index = ident

                    return new_index

            if not "parent" in self.scopes[stmt][scope]:
                scope = -1
            else:
                scope = self.scopes[stmt][scope]["parent"]

        return None 

    def _setNewIndex(self, ident):
        if self.stmtIndex > -1:
            if not self.scope in self.scopes[self.stmtIndex]:
                self.scopes[self.stmtIndex][self.scope] = {}

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
            if self.to_enum:
                self.newIndexExpression = "to_enum("+self.realtype+","+ident+")"

            self._setNewIndex(ident)

        if self.replaceNewIndices and not self.getOriginalIndices:
            new_ident = self._getNewIndex(ident, self.stmtIndex, self.scope)

            if new_ident != None:
                return new_ident

        return ident

    # String
    def generateCode_String(self, node):
        string = "\"" + node.string[1:-1] + "\""

        if self.turnStringsIntoInts:
            param = string[1:-1]

            if self.removeAdditionalParameter:
                if param in self.additionalParameters:
                    del self.additionalParameters[param]
            else:
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

        return string

    # IntegerSet
    def generateCode_IntegerSet(self, node):
        res = "integer"
        
        firstBound  = None if node.firstBound  == None else node.firstBound.getSymbolName(self)
        secondBound = None if node.secondBound == None else node.secondBound.getSymbolName(self)
        
        if firstBound != None and not Utils._isInfinity(firstBound):
            op = ""
            if secondBound != None and not Utils._isInfinity(secondBound):
                op += ", "
            else:
                op += " "
                
            op += node.firstOp+" "
            
            res += op + firstBound
            
        if secondBound != None and not Utils._isInfinity(secondBound):
            op = ""
            if firstBound != None and not Utils._isInfinity(firstBound):
                op += ", "
            else:
                op += " "
                
            op += node.secondOp+" "
            
            res += op + secondBound
            
        return res

    # RealSet
    def generateCode_RealSet(self, node):
        res = ""
        
        firstBound  = None if node.firstBound  == None else node.firstBound.getSymbolName(self)
        secondBound = None if node.secondBound == None else node.secondBound.getSymbolName(self)
        
        if firstBound != None and not Utils._isInfinity(firstBound):
            op = ""
            if secondBound != None and not Utils._isInfinity(secondBound):
                op += ", "
                
            op += node.firstOp+" "
            
            res += op + firstBound
            
        if secondBound != None and not Utils._isInfinity(secondBound):
            op = ""
            if firstBound != None and not Utils._isInfinity(firstBound):
                op += ", "
                
            op += node.secondOp+" "
            
            res += op + secondBound
            
        return res

    # BinarySet
    def generateCode_BinarySet(self, node):
        return "binary"

    # SymbolicSet
    def generateCode_SymbolicSet(self, node):
        return "string"

    # LogicalSet
    def generateCode_LogicalSet(self, node):
        return "logical"

    # ParameterSet
    def generateCode_ParameterSet(self, node):
        return ""

    # VariableSet
    def generateCode_VariableSet(self, node):
        return ""

    # SetSet
    def generateCode_SetSet(self, node):
        return ""
