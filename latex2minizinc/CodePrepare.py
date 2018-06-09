from Utils import *
from ValueList import *
from Tuple import *
from TupleList import *
from Array import *
from Range import *
from Number import *
from NumericExpression import *
from Constants import *


class CodePrepare:

    def __init__(self, codeGenerator = None):
        self.codeGenerator = codeGenerator
        self.isDeclaration = False

    def prepare(self, node):
        cls = node.__class__
        method_name = 'prepare_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    def init(self):
        self.realtype = None
        self.to_enum = False
        self.includeNewIndices = False
        self.lastIdentifier = None


        self.codeGenerator.parameters = map(lambda el: el.getName(), self.codeGenerator.genParameters.getAll())
        self.codeGenerator.sets = map(lambda el: el.getName(), self.codeGenerator.genSets.getAll())
        self.codeGenerator.variables = map(lambda el: el.getName(), self.codeGenerator.genVariables.getAll())

        self.codeGenerator.parameters_and_sets = self.codeGenerator.parameters + self.codeGenerator.sets

        if len(self.codeGenerator.genVariables) > 0:
            for var in self.codeGenerator.genVariables.getAll():
                if not self.codeGenerator.genParameters.has(var) and not self.codeGenerator.genSets.has(var):
                    domain, domains, domain_with_indices_list, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal = self._getSubIndicesDomains(var)
                    self.codeGenerator.identifiers[var.getName()] = {TYPES: _types,
                                                                     DIM: dim,
                                                                     MINVAL: minVal,
                                                                     MAXVAL: maxVal,
                                                                     DOMAIN: domain, 
                                                                     DOMAINS: domains, 
                                                                     DOMAINS_WITH_INDICES_LIST: domain_with_indices_list, 
                                                                     DEPENDENCIES: dependencies, 
                                                                     SUB_INDICES: sub_indices, 
                                                                     STATEMENT: stmtIndex}

        if len(self.codeGenerator.genParameters) > 0:
            for var in self.codeGenerator.genParameters.getAll():
                domain, domains, domain_with_indices_list, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal = self._getSubIndicesDomains(var)
                self.codeGenerator.identifiers[var.getName()] = {TYPES: _types,
                                                                 DIM: dim,
                                                                 MINVAL: minVal,
                                                                 MAXVAL: maxVal,
                                                                 DOMAIN: domain, 
                                                                 DOMAINS: domains, 
                                                                 DOMAINS_WITH_INDICES_LIST: domain_with_indices_list, 
                                                                 DEPENDENCIES: dependencies, 
                                                                 SUB_INDICES: sub_indices, 
                                                                 STATEMENT: stmtIndex}

        if len(self.codeGenerator.genSets) > 0:
            for var in self.codeGenerator.genSets.getAll():
                domain, domains, domain_with_indices_list, dependencies, sub_indices, stmtIndex, _types, dim, minVal, maxVal = self._getSubIndicesDomains(var)
                self.codeGenerator.identifiers[var.getName()] = {TYPES: _types,
                                                                 DIM: dim,
                                                                 MINVAL: minVal,
                                                                 MAXVAL: maxVal,
                                                                 DOMAIN: domain, 
                                                                 DOMAINS: domains, 
                                                                 DOMAINS_WITH_INDICES_LIST: domain_with_indices_list, 
                                                                 DEPENDENCIES: dependencies, 
                                                                 SUB_INDICES: sub_indices, 
                                                                 STATEMENT: stmtIndex}

        self._getTuples()

        '''
        print("Symbol Tables")
        self._printSymbolTables(self.codeGenerator.symbolTables)
        print("")
        
        print("Declarations")
        declarations = self.codeGenerator.symbolTables.getDeclarations()
        self._printSymbolTables(declarations.iteritems())
        print("")
        
        print("Leafs")
        self._printLeafs()
        print("")

        print("Scopes")
        self._printScopes()
        print("")
        '''

    def _printTables(self, tables):
        for dictStmt in tables:
            print("SymbolTable Scope " + str(dictStmt[SCOPE]) + ". Level: " + str(dictStmt["level"]) + ". Leaf: " + str(dictStmt[TABLE].getIsLeaf()) + 
                  ". Parent Scope: " + (str(None) if dictStmt[TABLE].getParent() == None else str(dictStmt[TABLE].getParent().getScope())))

            print("\n".join([str(key) + ": type = " + str(value.getType()) + "; scope = " + str(value.getScope()) + 
                   "; properties = [name: " + str(value.getProperties().getName()) + ", domains: " + 
                   str(map(lambda el: "{" + str(el.getOp()) + " " + el.getName() + ", dependencies: " + str(el.getDependencies()) + "}", value.getProperties().getDomains())) + 
                   ", minVal: " + str(value.getProperties().getMinVal()) + ", maxVal: " + str(value.getProperties().getMaxVal()) + 
                   ", dimension: " + str(value.getProperties().getDimension()) + ", default: " + str(value.getProperties().getDefault()) + 
                   ", attributes: " + str(value.getProperties().getAttributes()) + "]; inferred = " + str(value.getInferred()) + 
                   "; sub_indices = " + str(value.getSubIndices()) + "; isDefined = " + str(value.getIsDefined()) + 
                   "; isInLogicalExpression = " + str(value.getIsInLogicalExpression()) + ";"
                   for key, value in dictStmt[TABLE]]))
            print("")

    def _printStatementSymbolTable(self, statement, tables):
        print("SymbolTable Stmt " + str(statement) + ". Declaration: " + str(tables["isDeclaration"]))
        self._printTables(tables["tables"])


    def _printLeafs(self):
        for stmt, tables in self.codeGenerator.symbolTables:
            print("SymbolTable Stmt " + str(stmt) + ". Declaration: " + str(tables["isDeclaration"]))
            leafs = self.codeGenerator.symbolTables.getLeafs(stmt)
            self._printTables(leafs)

    def _printSymbolTables(self, symbolTables):
        for stmt, tables in symbolTables:
            self._printStatementSymbolTable(stmt, tables)

    def _printScopes(self):
        for stmt, scopes in self.codeGenerator.scopes.iteritems():
            print("Statement: " + str(stmt))

            for scope, value in scopes.iteritems():
                print("Scope: " + str(scope))
                print("Value: " + str(value))

        print("")

    def _getSubIndicesDomainsByTables(self, name, tables, minVal, maxVal, isDeclaration = False, domainsAlreadyComputed = None, skip_outermost_scope = False):

        domain = EMPTY_STRING
        domain_with_indices = EMPTY_STRING
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

        for table in sorted(tables, key=lambda el: el[SCOPE], reverse=True):

            table = table[TABLE]

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

                sub_indices_list = list(t.getSubIndices())
                sub_indices_list.reverse()

                domain = EMPTY_STRING
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
                            domains_with_indices[idx] = {INDICES: _combIndices, SET: _tuple}
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
                                domains_with_indices[ind] = _subIndicesRemaining[i] + SPACE + subIdxDomains[i][0] + SPACE + subIdxDomains[i][1]
                                count[ind] = 1
                                if not _subIndicesRemaining[i] in varNameSubIndices:
                                    varNameSubIndices.append(_subIndicesRemaining[i])

                                dependencies[ind] = subIdxDomains[i][3]

                            else:
                                subIdxDomainsRemaining.append(ind)
                    
                    for idx in domains:
                        if not idx in domainsAlreadyComputed or FROM_TO in domainsAlreadyComputed[idx]:
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
                            _indices = domains_with_indices[key][INDICES]
                            for i in range(key, key+len(_indices)):
                                sub_indices_ret.append(subIndicesAlreadyComputed[i])

                        elif isinstance(subIndicesAlreadyComputed[key], list):
                            for dep in subIndicesAlreadyComputed[key]:
                                sub_indices_ret.append(dep)

                        else:
                            sub_indices_ret.append(subIndicesAlreadyComputed[key])

            domain += (COMMA+SPACE).join(domains_str)
            domain_with_indices = domains_ret

        domain_with_indices = self.codeGenerator._processDomainsWithIndices(domain_with_indices)
        
        return domain, domains_str, domain_with_indices, list(set(dependencies_ret)), sub_indices_ret, minVal, maxVal

    def _setSubIndicesAlreadyComputed(self, idx, subIndicesAlreadyComputed, domains_with_indices, _subIndices):
        if idx in domains_with_indices and isinstance(domains_with_indices[idx], dict):
            _indices = domains_with_indices[idx][INDICES]
            c = 0
            for i in range(idx, idx+len(_indices)):
                subIndicesAlreadyComputed[i] = _indices[c]
                c += 1
        else:
            subIndicesAlreadyComputed[idx]   = _subIndices[idx]

    def _getSubIndicesDomainsByStatements(self, name, statements, minVal, maxVal, isDeclaration = False, domainsAlreadyComputed = None):
        domain = EMPTY_STRING
        domains = []
        domains_with_indices = []
        dependencies = []
        sub_indices = []
        stmtIndex = None
        currStmt = None
        
        for stmt in sorted(statements, reverse=True):

            currStmt = stmt
            
            scopes = self.codeGenerator.symbolTables.getFirstScopeByKey(name, stmt)
            domain, domains, domains_with_indices, dependencies, sub_indices, minVal, maxVal = self._getSubIndicesDomainsByTables(name, scopes, minVal, maxVal, isDeclaration, domainsAlreadyComputed)

            if domain != EMPTY_STRING and (not domainsAlreadyComputed or domains != domainsAlreadyComputed.values()):
                stmtIndex = stmt
                break
            
            leafs = self.codeGenerator.symbolTables.getLeafs(stmt)
            domain, domains, domains_with_indices, dependencies, sub_indices, minVal, maxVal = self._getSubIndicesDomainsByTables(name, leafs, minVal, maxVal, False, domainsAlreadyComputed, True)

            if domain != EMPTY_STRING and (not domainsAlreadyComputed or domains != domainsAlreadyComputed.values()):
                stmtIndex = stmt
                break

        if not stmtIndex:
            stmtIndex = currStmt

        return domain, domains, domains_with_indices, dependencies, sub_indices, stmtIndex, minVal, maxVal

    def _getSubIndicesDomains(self, identifier):
        
        _types, dim, minVal, maxVal = self._getDomain(identifier)
        
        name = identifier.getName()
        declarations = self.codeGenerator.symbolTables.getDeclarationsWhereKeyIsDefined(name)

        domain, domains, domains_with_indices, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, declarations, minVal, maxVal, True)
        
        if domain == EMPTY_STRING:
            statements = self.codeGenerator.symbolTables.getStatementsByKey(name)
            domain, domains, domains_with_indices, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, statements, minVal, maxVal, False)

        if domain == EMPTY_STRING:
            if minVal and maxVal and Utils._hasEqualIndices(minVal, maxVal):
                minMaxVals = self._zipMinMaxVals(minVal, maxVal)
                domain, domains, domains_with_indices, dependencies, sub_indices, stmtIndex, minVal, maxVal = self._getSubIndicesDomainsByStatements(name, declarations, minVal, maxVal, True, minMaxVals)

                if domain == EMPTY_STRING or domains == minMaxVals.values():
                    statements = self.codeGenerator.symbolTables.getStatementsByKey(name)
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

    def _zipMinMaxVals(self, minVal, maxVal):
        minMaxVals = {}

        for idx in minVal:
            if idx in maxVal:
                minMaxVals[idx] = str(minVal[idx])+FROM_TO+str(maxVal[idx])

        return minMaxVals
        
    def _getDomainsByTables(self, name, tables, _types, dim, minVal, maxVal, skip_outermost_scope = False):
        
        for table in sorted(tables, key=lambda el: el[SCOPE], reverse=True):

            table = table[TABLE]

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
            
            scopes = self.codeGenerator.symbolTables.getFirstScopeByKey(name, stmt)
            _types, dim, minVal, maxVal = self._getDomainsByTables(name, scopes, _types, dim, minVal, maxVal, False)

            leafs = self.codeGenerator.symbolTables.getLeafs(stmt)
            _types, dim, minVal, maxVal = self._getDomainsByTables(name, leafs, _types, dim, minVal, maxVal, True)

        return _types, dim, minVal, maxVal

    def _getDomain(self, identifier):
        _types = []
        dim = None
        minVal = None
        maxVal = None

        name = identifier.getName()
        declarations = self.codeGenerator.symbolTables.getDeclarationsWhereKeyIsDefined(name)
        _types, dim, minVal, maxVal = self._getDomainsByStatements(name, declarations, _types, dim, minVal, maxVal)

        statements = self.codeGenerator.symbolTables.getStatementsByKey(name)
        _types, dim, minVal, maxVal = self._getDomainsByStatements(name, statements, _types, dim, minVal, maxVal)

        return _types, dim, minVal, maxVal

    def _addDependencies(self, value, stmtIndex, dependencies):
        names = value.getDependencies(self)

        if names != None and len(names) > 0:
            for name in names:
                if not self.codeGenerator.genBelongsToList.has(GenBelongsTo(name, stmtIndex)):
                    dependencies.append(name)

    def _getDependencies(self, identifier):
        dependencies = []

        decl = self.codeGenerator.genDeclarations.get(identifier.getName())
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

    def _domainIdentifierType(self, domain):
        obj = domain.getObj()
        return self.codeGenerator._isIdentifierType(obj)

    def _domainIsNumberSet(self, domain):
        obj = domain.getObj()
        return self.codeGenerator._isTypeSet(obj)

    def _domainIsModifierSet(self, domain):
        obj = domain.getObj()
        return self.codeGenerator._isModifierSet(obj)

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

    def _checkParameterIsIndexOf(self, indices, name):
        for i in range(len(indices)):
            ind = indices[i]

            if ind in self.codeGenerator.parameters and not ind in self.codeGenerator.parameterIsIndexOf:
                self.codeGenerator.parameterIsIndexOf[ind] = {"indexOf":name, POS:i}

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
                if not set(dependencies).issubset(set(totalIndices+self.codeGenerator.parameters_and_sets)):
                    break

            deps = set(domain.getDependencies())
            deps.discard(set(totalIndices))

            return domain.getOp(), domain.getName(), domain.getObj(), list(deps)

        return None, None, None, None

    def _getDomainSubIndices(self, table, selectedIndices, totalIndices, indicesPosition, minVal, maxVal, isDeclaration = False):
        if not isinstance(selectedIndices, str):
            selectedIndices = COMMA.join(selectedIndices)

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

                        posBy = domain.find(BY) # if a range is inferred as the domain, the by clause is removed

                        if posBy > 0:
                            domain = domain[0:posBy].strip()

                    return op, domain, domainObj, deps, minVal, maxVal

            table = table.getParent()

        if domainAux != None:
            posIn = domainAux.find(SPACE+IN+SPACE)

            if posIn > 0:
                domain = domainAux[0:posIn+4]
            else:
                domain = EMPTY_STRING

            domains = []

            if rangeObjAux:
                
                if 0 in rangeObjAux:

                    if not self._isKeysInDictionary(indicesPosition, maxVal):
                        domains = []

                    else:
                        if isinstance(indicesPosition, list):
                            for idx in indicesPosition:
                                domains.append(rangeObjAux[0].generateCode(self.codeGenerator) + FROM_TO + str(maxVal[idx]))

                        else:
                            domains.append(rangeObjAux[0].generateCode(self.codeGenerator) + FROM_TO + str(maxVal[indicesPosition]))

                elif 1 in rangeObjAux:

                    if not self._isKeysInDictionary(indicesPosition, minVal):
                        domains = []

                    else:
                        if isinstance(indicesPosition, list):
                            for idx in indicesPosition:
                                domains.append(str(minVal[idx]) + FROM_TO + rangeObjAux[1].generateCode(self.codeGenerator))

                        else:
                            domains.append(str(minVal[indicesPosition]) + FROM_TO + rangeObjAux[1].generateCode(self.codeGenerator))

            else:

                if not self._isKeysInDictionary(indicesPosition, minVal) or not self._isKeysInDictionary(indicesPosition, maxVal):
                    domains = []

                else:

                    if isinstance(indicesPosition, list):
                        for idx in indicesPosition:
                            domains.append(str(minVal[idx]) + FROM_TO + str(maxVal[idx]))

                    else:
                        domains.append(str(minVal[indicesPosition]) + FROM_TO + str(maxVal[indicesPosition]))

            if len(domains) > 1:
                domain += BEGIN_SET+(COMMA+SPACE).join(domains)+END_SET

            elif len(domains) > 0:
                domain += domains[0]

            if len(domains) > 0:
                return opAux, domain, None, depsAux, minVal, maxVal

        return None, None, None, None, minVal, maxVal

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
                        keys.append({ORDER:order, IDENTIFIER:key, POS:pos})

                        order += 1

            t = t.getParent()

        return keys

    def _isIndexOf(self, index, table, stmt):
        while table != None:
            keys = self._getKeyForIndex(index, table)
            if len(keys) > 0:
                return keys

            table = table.getParent()

        leafs = self.codeGenerator.symbolTables.getLeafs(stmt)
        for table in sorted(leafs, key=lambda el: el[SCOPE], reverse=True):
            table = table[TABLE]

            while table != None:
                keys = self._getKeyForIndex(index, table)

                if len(keys) > 0:
                    return keys

                table = table.getParent()

        return []

    def _tupleContainIndex(self, index, pos, _tuple):
        for el in _tuple:
            if el[INDEX] == index and el[POS] == pos:
                return True

        return False

    def _addTuple(self, _tuple, stmt, dimen, setWithIndices, index, ident, order, pos = None, higherPriority = False):

        if not _tuple in self.codeGenerator.tuples:
            self.codeGenerator.tuples[_tuple] = {}
        
        if not stmt in self.codeGenerator.tuples[_tuple]:
            self.codeGenerator.tuples[_tuple][stmt] = {DIMEN:dimen, SETWITHINDICES: setWithIndices, IDENTIFIERS: {}}

        elif higherPriority:
            self.codeGenerator.tuples[_tuple][stmt][DIMEN] = dimen
            self.codeGenerator.tuples[_tuple][stmt][SETWITHINDICES] = setWithIndices
            
        if not ident in self.codeGenerator.tuples[_tuple][stmt][IDENTIFIERS]:
            self.codeGenerator.tuples[_tuple][stmt][IDENTIFIERS][ident] = {}

        if not order in self.codeGenerator.tuples[_tuple][stmt][IDENTIFIERS][ident]:
            self.codeGenerator.tuples[_tuple][stmt][IDENTIFIERS][ident][order] = []

        if not self._tupleContainIndex(index, pos, self.codeGenerator.tuples[_tuple][stmt][IDENTIFIERS][ident][order]):
            self.codeGenerator.tuples[_tuple][stmt][IDENTIFIERS][ident][order].append({INDEX: index, POS: pos})

    def _getTuplesByTables(self, tables, stmt):
        for table in sorted(tables, key=lambda el: el[SCOPE], reverse=True):
            scope = table[SCOPE]
            table = table[TABLE]
            
            while table != None:

                for key, value in table:
                    
                    if self.codeGenerator._checkIsSetOperation(key) or self.codeGenerator._checkIsSetBetweenBraces(key):
                        indicesSetOp = self.codeGenerator._getIndicesFromSetOperation(key)

                        dnew = self.codeGenerator._cleanKeyWithSetOperation(key)
                        self.codeGenerator.setsWitOperations[key] = dnew
                        self.codeGenerator.setsWitOperationsInv[dnew] = key

                        if BEGIN_ARRAY in key and SUCH_THAT in key:
                            dimen = 1
                        else:

                            sets, dimensions = self.codeGenerator._getSets(key)
                            if len(sets) > 0:
                                dimen = max(dimensions)
                            else:
                                dimen = 1

                        if indicesSetOp and len(indicesSetOp) > 0:
                            self.codeGenerator.setsWitOperationsIndices[key] = {DIMEN: dimen, INDICES: indicesSetOp}

                        key = dnew

                        self._addTuple(key, stmt, dimen, False, None, None, None, None)

                    elif BEGIN_ARRAY in key and not COMMA in key:

                        parts = key.split(BEGIN_ARRAY)
                        domain = parts[0].strip()
                        domain = self.codeGenerator._cleanKeyWithSetOperation(domain)
                        parts = parts[1].split(END_ARRAY)

                        indices = Utils._splitDomain(parts[0], COMMA)
                        dimen = len(indices)

                        for index in indices:
                            keys = self._isIndexOf(index, table, stmt)

                            if len(keys) > 0:
                                for key in keys:
                                    ident = key[IDENTIFIER]
                                    pos   = key[POS]
                                    order = key[ORDER]

                                    self._addTuple(domain, stmt, dimen, True, index, ident, order, pos)

                    elif COMMA in key:

                        domains = value.getProperties().getDomains()
                        domains.reverse()
                        
                        if len(domains) > 0:
                            indices = key.split(COMMA)
                            dimen = len(indices)

                            for domain in domains:
                                d = domain.getName()

                                if self.codeGenerator._checkIsSetOperation(d) or self.codeGenerator._checkIsSetBetweenBraces(d):

                                    indicesSetOp = self.codeGenerator._getIndicesFromSetOperation(key)
                                    dnew = self.codeGenerator._cleanKeyWithSetOperation(d)
                                    self.codeGenerator.setsWitOperations[d] = dnew
                                    self.codeGenerator.setsWitOperationsInv[dnew] = d

                                    if indicesSetOp and len(indicesSetOp) > 0:
                                        self.codeGenerator.setsWitOperationsIndices[d] = {DIMEN: dimen, INDICES: indicesSetOp}

                                    d = dnew
                                
                                d = self.codeGenerator._cleanKeyWithSetOperation(d)
                                for index in indices:
                                    keys = self._isIndexOf(index, table, stmt)

                                    if len(keys) > 0:
                                        for key in keys:
                                            ident = key[IDENTIFIER]
                                            pos   = key[POS]
                                            order = key[ORDER]

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
        statements = self.codeGenerator.symbolTables.getStatements()
        for stmt in sorted(statements, reverse=True):

            scopes = self.codeGenerator.symbolTables.getFirstScope(stmt)
            self._getTuplesByTables(scopes, stmt)

            leafs = self.codeGenerator.symbolTables.getLeafs(stmt)
            self._getTuplesByTables(leafs, stmt)

        for name in self.codeGenerator.tuples:
            
            index1 = None
            _type = None
            pos = {}
            realtype = None
            sizeTuple = None
            isSetWithIndices = False

            for stmt in sorted(self.codeGenerator.tuples[name], reverse=True):

                setWithIndices = self.codeGenerator.tuples[name][stmt][SETWITHINDICES]
                isSetWithIndices = setWithIndices

                if setWithIndices:
                    realtype = SET_OF_INT

                domainIdent = []
                for ident in self.codeGenerator.tuples[name][stmt][IDENTIFIERS]:
                    
                    for order in sorted(self.codeGenerator.tuples[name][stmt][IDENTIFIERS][ident]):
                        domain = self.codeGenerator._getDomainByIdentifier(ident)
                        sizeTuple = self.codeGenerator.tuples[name][stmt][DIMEN]
                        sizeTupleNotNull = sizeTuple

                        if sizeTuple > 1:
                            index2 = "1"+FROM_TO+str(sizeTuple)
                        else:
                            index2 = None

                        if domain == None or domain.strip() == EMPTY_STRING:
                            sizeTupleNotNull -= 1
                        else:
                            domainIdent.append(domain)

                        if len(domainIdent) > 0:
                            _tuple = self.codeGenerator.tuples[name][stmt][IDENTIFIERS][ident][order]
                            domainIdents = list(domainIdent)
                            
                            if len(domainIdent) == 1:
                                domain = Utils._splitDomain(domainIdent[0], COMMA)
                                domainIdents = domain

                            if len(_tuple) >= sizeTuple:
                                domainIdent = []

                            domains = Utils._stripDomains(domainIdents)
                            if not setWithIndices and all(map(lambda el: el == domains[0], domains)):
                                _type = domains[0]

                            else:
                                size = len(domains)
                                pos = []
                                d = []

                                for t in _tuple:
                                    pos.append(t[POS])

                                for position in pos:
                                    if position != None:
                                        if position >= size:
                                            index1 = None
                                            _type = None
                                            pos = {}
                                            sizeTuple = None

                                            continue

                                        d.append(domains[position])

                                if not setWithIndices and len(d) > 0 and all(map(lambda el: el == d[0], d)):
                                    _type = d[0]

                                else:
                                    index1 = None
                                    _type = None
                                    pos = {}
                                    sizeTuple = None

                                    continue

                        if _type == None or _type == name or _type == ident or _type in self.codeGenerator.tuples or FROM_TO in _type:
                            index1 = None
                            _type = None
                            pos = {}
                            sizeTuple = None

                            continue

                        if _type != None and _type != INT:
                            break

                    if _type != None and _type != INT:
                        break

                if _type != None and _type != INT:
                    break

                index1 = None
                _type = None
                pos = {}
                sizeTuple = None


            if index1 == None and not FROM_TO in name:
                index1 = INDEX_SET_+name
                setint = SET_OF_INT + SEP_PARTS_DECLARATION + SPACE + index1 + END_STATEMENT + BREAKLINE + BREAKLINE

                self.codeGenerator.additionalParameters[index1] = setint

            if _type == None:
                _type = INT

            if realtype != None and not isSetWithIndices:
                aux = realtype
                realtype = _type
                _type = aux

            if realtype == INT:
                realtype = None

            if name in self.codeGenerator.setsWitOperationsInv:
                if index2 != None:
                    self.codeGenerator.additionalParameters[name] = ARRAY + BEGIN_ARRAY + index1 + COMMA + index2 + END_ARRAY + SPACE + OF + SPACE + _type + SEP_PARTS_DECLARATION + SPACE + name + END_STATEMENT + BREAKLINE + BREAKLINE
                else:
                    self.codeGenerator.additionalParameters[name] = ARRAY + BEGIN_ARRAY + index1 + END_ARRAY + SPACE + OF + SPACE + _type + SEP_PARTS_DECLARATION + SPACE + name + END_STATEMENT + BREAKLINE + BREAKLINE

            self.codeGenerator.tuplesDeclared[name] = {INDEX1: index1, INDEX2: index2, TYPE: _type, REALTYPE: realtype, DIMEN: sizeTuple, ISSETWITHINDICES: isSetWithIndices}

    def _initialize(self):
        self.init()

    def _getIdentifier(self, var):
        return var.getSymbol()

    def _getSetExpression(self, node):
        node.setExpression.prepare(self)
        setExpression = node.setExpression.generateCode(self.codeGenerator)

        if setExpression in self.codeGenerator.setsWitOperations:
            setExpression = self.codeGenerator.setsWitOperations[setExpression]

            if not self.isDeclaration:
                self.codeGenerator.setsWitOperationsUsed.append(setExpression)

        return setExpression

    def _checkRealType(self, setExpression, values):
        if not isinstance(values, list):
            values = [values]

        if BEGIN_ARRAY in setExpression:
            setExpression = setExpression.split(BEGIN_ARRAY)[0]

        
        if setExpression in self.codeGenerator.tuplesDeclared:
            
            realtype = self.codeGenerator.tuplesDeclared[setExpression][REALTYPE]
            if realtype != None and realtype != SET_OF_INT:
                self.includeNewIndices = True
                self.to_enum = True
                self.realtype = realtype
                for v in values:
                    v.prepare(self)

                self.includeNewIndices = False
                self.to_enum = False
                self.realtype = None

        elif FROM_TO in setExpression:
            self.includeNewIndices = True
            self.to_enum = True
            self.realtype = "'"+REALTYPE+"'"
            for v in values:
                v.prepare(self)

            self.includeNewIndices = False
            self.to_enum = False
            self.realtype = None

    def _prepareDeclaration(self, declaration):
        declaration.prepare(self)

    def prepare_Main(self, node):
        node.problem.prepare(self)

    def prepare_LinearEquations(self, node):
    	self._initialize()

    	node.constraints.prepare(self)

    def prepare_LinearProgram(self, node):
    	self._initialize()

        node.objectives.prepare(self)
        if node.constraints:
            node.constraints.prepare(self)

    # Declarations
    def prepare_Declarations(self, node):

        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()

        if not stmtIndex in self.codeGenerator.scopes:
            self.codeGenerator.scopes[stmtIndex] = {}
            self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_Declarations"}

        self.isDeclaration = True
    	map(self._prepareDeclaration, node.declarations)
        self.isDeclaration = False

    def prepare_Declaration(self, node):
        node.declarationExpression.prepare(self)

        if node.indexingExpression:
            node.indexingExpression.prepare(self)

    def prepare_DeclarationExpression(self, node):
        for identifier in node.identifiers:
            identifier = self._getIdentifier(identifier)
            identifier.prepare(self)

        map(lambda el: el.prepare(self), node.attributeList)

    def prepare_DeclarationAttribute(self, node):
        return node.attribute.prepare(self)

    # Objectives
    def prepare_Objectives(self, node):
    	map(lambda el: el.prepare(self), node.objectives)

    # Objective Function
    def prepare_Objective(self, node):
        """
        Generate the code in MiniZinc for this Objective
        """
        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()

        if not stmtIndex in self.codeGenerator.scopes:
            self.codeGenerator.scopes[stmtIndex] = {}
            self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_Objective"}

        node.linearExpression.prepare(self)


    # Constraints
    def prepare_Constraints(self, node):
        map(lambda el: el.prepare(self), node.constraints)

    def prepare_Constraint(self, node):
        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()
        
        if not stmtIndex in self.codeGenerator.scopes:
            self.codeGenerator.scopes[stmtIndex] = {}
            self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_Constraint"}
            
        if node.indexingExpression:
            node.indexingExpression.prepare(self)
            
        node.constraintExpression.prepare(self)

    def prepare_ConstraintExpression2(self, node):
        node.linearExpression1.prepare(self)
        node.linearExpression2.prepare(self)

    def prepare_ConstraintExpression3(self, node):

    	node.numericExpression1.prepare(self)
        node.linearExpression.prepare(self)
        node.numericExpression2.prepare(self)
    
    def prepare_LogicalConstraintExpression(self, node):
        node.logicalExpression.prepare(self)
        node.constraintExpression1.prepare(self)

        if node.constraintExpression2:
            node.constraintExpression2.prepare(self)

    def prepare_ConditionalConstraintExpression(self, node):

        node.logicalExpression.prepare(self)

        stmtIndex = node.constraintExpression1.getSymbolTable().getStatement()
        scope = node.constraintExpression1.getSymbolTable().getScope()

        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_ConditionalConstraintExpression1"}

        node.constraintExpression1.prepare(self)

        if node.constraintExpression2:
            stmtIndex = node.constraintExpression2.getSymbolTable().getStatement()
            scope = node.constraintExpression2.getSymbolTable().getScope()

            self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_ConditionalConstraintExpression2"}

            node.constraintExpression2.prepare(self)

    # Linear Expression
    def prepare_ValuedLinearExpression(self, node):
        return node.value.prepare(self)

    def prepare_LinearExpressionBetweenParenthesis(self, node):
        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()

        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_LinearExpressionBetweenParenthesis"}

        node.linearExpression.prepare(self)

    def prepare_LinearExpressionWithArithmeticOperation(self, node):
        node.expression1.prepare(self)
        node.expression2.prepare(self)

    def prepare_MinusLinearExpression(self, node):
        node.linearExpression.prepare(self)

    def prepare_IteratedLinearExpression(self, node):

        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()

        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_IteratedLinearExpression"}

        node.indexingExpression.prepare(self)
        
        if node.numericExpression:
            node.numericExpression.prepare(self)

        node.linearExpression.prepare(self)

    def prepare_ConditionalLinearExpression(self, node):

        node.logicalExpression.prepare(self)

        if node.linearExpression1:
            stmtIndex = node.linearExpression1.getSymbolTable().getStatement()
            scope = node.linearExpression1.getSymbolTable().getScope()

            self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_ConditionalLinearExpression1"}

            node.linearExpression1.prepare(self)

            if node.linearExpression2:

                if node.linearExpression2:
                    stmtIndex = node.linearExpression2.getSymbolTable().getStatement()
                    scope = node.linearExpression2.getSymbolTable().getScope()

                    self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_ConditionalLinearExpression2"}

                node.linearExpression2.prepare(self)

    # True or False Expression
    def prepare_TrueFalse(self, node):
        pass

    # Numeric Expression
    def prepare_NumericExpressionWithFunction(self, node):

        if not isinstance(node.function, str):
            node.function.prepare(self)
            function = node.function.generateCode(self.codeGenerator)
        else:
            function = node.function

        function = self.codeGenerator._getNumericFunction(function)
        
        if function in self.codeGenerator.LIBRARIES and not function in self.codeGenerator.include:
            self.codeGenerator.include[function] = self.codeGenerator.LIBRARIES[function]

        if node.numericExpression1 != None:
            node.numericExpression1.prepare(self)

        if node.numericExpression2 != None:
            node.numericExpression2.prepare(self)

    def prepare_FractionalNumericExpression(self, node):
        
        node.numerator.prepare(self)
        node.denominator.prepare(self)

    def prepare_ValuedNumericExpression(self, node):
        node.value.prepare(self)

    def prepare_NumericExpressionBetweenParenthesis(self, node):

        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()
        
        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_NumericExpressionBetweenParenthesis", CONTEXT: "(" + node.numericExpression.generateCode(self.codeGenerator) + ")"}
        node.numericExpression.prepare(self)

    def prepare_NumericExpressionWithArithmeticOperation(self, node):

        node.numericExpression1.prepare(self)
        node.numericExpression2.prepare(self)
        
    def prepare_MinusNumericExpression(self, node):
        node.numericExpression.prepare(self)

    def prepare_IteratedNumericExpression(self, node):

        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()

        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_IteratedNumericExpression"}

        node.indexingExpression.prepare(self)

        if node.supNumericExpression:
            node.supNumericExpression.prepare(self)

        node.numericExpression.prepare(self)

    def prepare_ConditionalNumericExpression(self, node):

        node.logicalExpression.prepare(self)

        stmtIndex = node.numericExpression1.getSymbolTable().getStatement()
        scope = node.numericExpression1.getSymbolTable().getScope()

        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_ConditionalNumericExpression1"}

        node.numericExpression1.prepare(self)

        if node.numericExpression2:
            stmtIndex = node.numericExpression2.getSymbolTable().getStatement()
            scope = node.numericExpression2.getSymbolTable().getScope()

            self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_ConditionalNumericExpression2"}

            node.numericExpression2.prepare(self)


    # Symbolic Expression
    def prepare_StringSymbolicExpression(self, node):
        node.value.prepare(self)

    def prepare_SymbolicExpressionBetweenParenthesis(self, node):

        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()

        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_SymbolicExpressionBetweenParenthesis"}

        node.symbolicExpression.prepare(self)

    def prepare_SymbolicExpressionWithOperation(self, node):
        node.symbolicExpression1.prepare(self)
        node.symbolicExpression2.prepare(self)

    # Expression List
    def prepare_ExpressionList(self, node):
        map(lambda el: el.prepare(self), node.entriesIndexingExpression)

        if node.logicalExpression:
            node.logicalExpression.prepare(self)

    # Indexing Expression
    def prepare_IndexingExpression(self, node):
        map(lambda el: el.prepare(self), node.entriesIndexingExpression)

        if node.logicalExpression:
            node.logicalExpression.prepare(self)

    # Entry Indexing Expression
    def prepare_EntryIndexingExpressionWithSet(self, node):

        if isinstance(node.identifier, ValueList):
            values = filter(self.codeGenerator.notInTypesThatAreNotDeclarable, node.identifier.getValues())

            if len(values) > 0:
                
                for v in values:
                    self.codeGenerator.replaceNewIndices = False
                    v.prepare(self)
                    v = v.generateCode(self.codeGenerator)
                    self.codeGenerator.replaceNewIndices = True

                    # used to compute new entry logical expresson when set expression is of the type 1..N by D
                    self.lastIdentifier = v
                    setExpression = self._getSetExpression(node)
                    self._checkRealType(setExpression, values)
                    self.lastIdentifier = None

        elif isinstance(node.identifier, Tuple) or isinstance(node.identifier, TupleList):
            setExpression = self._getSetExpression(node)
            
            if not self.codeGenerator.getOriginalIndices and setExpression in self.codeGenerator.tuplesDeclared:

                index1 = self.codeGenerator.tuplesDeclared[setExpression][INDEX1]
                values = node.identifier.getValues()

                self.codeGenerator.replaceNewIndices = False
                values[0].prepare(self)
                idx = values[0].generateCode(self.codeGenerator)
                self.codeGenerator.replaceNewIndices = True

                stmtIndex = node.getSymbolTable().getStatement()
                scope = node.getSymbolTable().getScope()

                if not NEW_INDICES in self.codeGenerator.scopes[stmtIndex][scope]:
                    self.codeGenerator.scopes[stmtIndex][scope][NEW_INDICES] = {}

                self.codeGenerator.countNewIndices = 1
                self.includeNewIndices = True

                for v in values:
                    self.codeGenerator.newIndexExpression = setExpression+BEGIN_ARRAY+idx+COMMA+str(self.codeGenerator.countNewIndices)+END_ARRAY
                    v.prepare(self)

                self.codeGenerator.countNewIndices = 0
                self.includeNewIndices = False

                # used to compute new entry logical expresson when set expression is of the type 1..N by D
                self.lastIdentifier = idx
                node.setExpression.prepare(self)
                self.lastIdentifier = None

            else:
                node.identifier.prepare(self)
                ident = node.identifier.generateCode(self.codeGenerator)

                # used to compute new entry logical expresson when set expression is of the type 1..N by D
                self.lastIdentifier = ident
                node.setExpression.prepare(self)
                self.lastIdentifier = None

        elif self.codeGenerator.notInTypesThatAreNotDeclarable(node.identifier):
            node.identifier.prepare(self)
            ident = node.identifier.generateCode(self.codeGenerator)

            # used to compute new entry logical expresson when set expression is of the type 1..N by D
            self.lastIdentifier = ident
            setExpression = self._getSetExpression(node)
            self._checkRealType(setExpression, node.identifier)
            self.lastIdentifier = None


    def prepare_EntryIndexingExpressionCmp(self, node):
        self.codeGenerator.turnStringsIntoInts = True
        node.identifier.prepare(self)
        node.numericExpression.prepare(self)
        self.codeGenerator.turnStringsIntoInts = False

    def prepare_EntryIndexingExpressionEq(self, node):
        self.codeGenerator.turnStringsIntoInts = True

        if node.hasSup:
            node.identifier.prepare(self)
            node.value.prepare(self)

        elif isinstance(node.value, Array):
            node.identifier.prepare(self)
            node.value.value.prepare(self)

        else:
            node.identifier.prepare(self)
            node.value.prepare(self)

        self.codeGenerator.turnStringsIntoInts = False

    # Get the MiniZinc code for a given entry
    def _getCodeEntryByKey(self, entry):
        for key in entry:
            entry[key].prepare(self)

    # Logical Expression
    def prepare_LogicalExpression(self, node):
        for i in range(len(node.entriesLogicalExpression)):
            self._getCodeEntryByKey(node.entriesLogicalExpression[i])
            
    # Entry Logical Expression
    def prepare_EntryLogicalExpressionRelational(self, node):
        self.codeGenerator.turnStringsIntoInts = True
        node.numericExpression1.prepare(self)
        node.numericExpression2.prepare(self)
        self.codeGenerator.turnStringsIntoInts = False

    def prepare_EntryLogicalExpressionWithSet(self, node):

        if isinstance(node.identifier, ValueList):
            values = filter(self.codeGenerator.notInTypesThatAreNotDeclarable, node.identifier.getValues())

            if len(values) > 0:

                for v in values:
                    self.codeGenerator.replaceNewIndices = False
                    v.prepare(self)
                    v = v.generateCode(self.codeGenerator)
                    self.codeGenerator.replaceNewIndices = True

                    self.lastIdentifier = v
                    setExpression = self._getSetExpression(node)
                    self._checkRealType(setExpression, values)
                    self.lastIdentifier = None

        elif isinstance(node.identifier, Tuple) or isinstance(node.identifier, TupleList):
            setExpression = self._getSetExpression(node)

            if not self.codeGenerator.getOriginalIndices and setExpression in self.codeGenerator.tuplesDeclared:
                index1 = self.codeGenerator.tuplesDeclared[setExpression][INDEX1]
                values = node.identifier.getValues()
                values[0].prepare(self)
                idx = values[0].generateCode(self.codeGenerator)

                stmtIndex = node.getSymbolTable().getStatement()
                scope = node.getSymbolTable().getScope()

                if not NEW_INDICES in self.codeGenerator.scopes[stmtIndex][scope]:
                    self.codeGenerator.scopes[stmtIndex][scope][NEW_INDICES] = {}

                self.codeGenerator.countNewIndices = 1

                for v in values:
                    self.codeGenerator.newIndexExpression = setExpression+BEGIN_ARRAY+idx+COMMA+str(self.codeGenerator.countNewIndices)+END_ARRAY
                    v.prepare(self)

                self.codeGenerator.countNewIndices = 0

                self.lastIdentifier = idx
                node.setExpression.prepare(self)
                self.lastIdentifier = None

            else:
                node.identifier.prepare(self)
                ident = node.identifier.generateCode(self.codeGenerator)

                self.lastIdentifier = ident
                node.setExpression.prepare(self)
                self.lastIdentifier = None

        elif self.codeGenerator.notInTypesThatAreNotDeclarable(node.identifier):
            node.identifier.prepare(self)
            ident = node.identifier.generateCode(self.codeGenerator)
            
            self.lastIdentifier = ident
            setExpression = self._getSetExpression(node)
            self._checkRealType(setExpression, node.identifier)
            self.lastIdentifier = None

    def prepare_EntryLogicalExpressionWithSetOperation(self, node):
        node.setExpression1.prepare(self)
        node.setExpression2.prepare(self)

    def prepare_EntryLogicalExpressionIterated(self, node):

        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()

        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_EntryLogicalExpressionIterated"}

        node.indexingExpression.prepare(self)
        node.logicalExpression.prepare(self)


    def prepare_EntryLogicalExpressionBetweenParenthesis(self, node):

        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()

        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_EntryLogicalExpressionBetweenParenthesis"}

        node.logicalExpression.prepare(self)


    def prepare_EntryLogicalExpressionNot(self, node):
        node.logicalExpression.prepare(self)

    def prepare_EntryLogicalExpressionNumericOrSymbolic(self, node):
        node.numericOrSymbolicExpression.prepare(self)

    # Set Expression
    def prepare_SetExpressionWithValue(self, node):
        node.value.prepare(self)

    def prepare_SetExpressionWithIndices(self, node):
        self.codeGenerator.isSetExpressionWithIndices = True

        if not isinstance(node.identifier, str):
            node.identifier.prepare(self)

        self.codeGenerator.isSetExpressionWithIndices = False

    def prepare_SetExpressionWithOperation(self, node):
        node.setExpression1.prepare(self)
        node.setExpression2.prepare(self)

    def prepare_SetExpressionBetweenBraces(self, node):
        if node.setExpression != None:
            self.codeGenerator.turnStringsIntoInts = True

            node.setExpression.prepare(self)

            self.codeGenerator.turnStringsIntoInts = False


    def prepare_SetExpressionBetweenParenthesis(self, node):
        node.setExpression.prepare(self)

    def prepare_EnumSetExpression(self, node):
        pass

    def prepare_IteratedSetExpression(self, node):

        stmtIndex = node.getSymbolTable().getStatement()
        scope = node.getSymbolTable().getScope()

        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_IteratedSetExpression"}

        if node.indexingExpression:
            node.indexingExpression.prepare(self)

        if node.integrand != None:
            if not isinstance(node.integrand, Tuple):
                node.integrand.prepare(self)

            else:
                integrand = node.integrand.getValues()

                for i in range(1,len(integrand)):
                    integrand[0].prepare(self)


    def prepare_ConditionalSetExpression(self, node):

        node.logicalExpression.prepare(self)
        node.setExpression1.prepare(self)

        stmtIndex = node.setExpression1.getSymbolTable().getStatement()
        scope = node.setExpression1.getSymbolTable().getScope()

        self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_ConditionalSetExpression"}

        if node.setExpression2:

            stmtIndex = node.setExpression2.getSymbolTable().getStatement()
            scope = node.setExpression2.getSymbolTable().getScope()

            self.codeGenerator.scopes[stmtIndex][scope] = {WHERE: "generateCode_ConditionalSetExpression"}

            node.setExpression2.prepare(self)


    # Range
    def prepare_Range(self, node):

        node.rangeInit.prepare(self)
        node.rangeEnd.prepare(self)

        initValue = node.rangeInit.generateCode(self.codeGenerator)
        endValue = node.rangeEnd.generateCode(self.codeGenerator)

        if node.by != None:

            stmtIndex = node.getSymbolTable().getStatement()
            scope = node.getSymbolTable().getScope()

            if not NEWENTRYLOGICALEXPRESSION in self.codeGenerator.scopes[stmtIndex][scope]:
                self.codeGenerator.scopes[stmtIndex][scope][NEWENTRYLOGICALEXPRESSION] = []
            
            if self.lastIdentifier != None:
                newEntry = BEGIN_ARGUMENT_LIST+self.lastIdentifier+MINUS+initValue+END_ARGUMENT_LIST+SPACE+MOD+SPACE + node.by.generateCode(self.codeGenerator) + SPACE+EQUAL+SPACE+"0"
                if not newEntry in self.codeGenerator.scopes[stmtIndex][scope][NEWENTRYLOGICALEXPRESSION]:
                    self.codeGenerator.scopes[stmtIndex][scope][NEWENTRYLOGICALEXPRESSION].append(newEntry)

    # Value List
    def prepare_ValueList(self, node):
        map(lambda el: el.prepare(self), node.values)

    # Identifier List
    def prepare_IdentifierList(self, node):
        map(lambda el: el.prepare(self), node.identifiers)

    # Tuple
    def prepare_Tuple(self, node):
        map(lambda el: el.prepare(self), node.values)

    # Tuple List
    def prepare_TupleList(self, node):
        map(lambda el: el.prepare(self), node.values)

    # Array
    def prepare_Array(self, node):
        map(lambda el: el.prepare(self), node.value)

    # Array with operation
    def prepare_ArrayWithOperation(self, node):
        node.array1.prepare(self)
        node.array2.prepare(self)

    # ArrayChoose
    def prepare_ArrayChoose(self, node):
        map(lambda el: el.prepare(self), node.value1)
        map(lambda el: el.prepare(self), node.value2)

    # Value
    def prepare_Value(self, node):
        node.value.prepare(self)

    # Identifier
    def prepare_Identifier(self, node):
        if isinstance(node.sub_indices, str):
            node.identifier.prepare(self)
            return

        length_sub_indices = len(node.sub_indices)

        if length_sub_indices > 0:

            node.identifier.prepare(self)
            ident = node.identifier.generateCode(self.codeGenerator)

            if not self.codeGenerator.isSetExpressionWithIndices:

                domains = self.codeGenerator._getDomainByIdentifier(ident)
                includedDomains = False

                self.codeGenerator.countIndicesProcessed += 1
                identProcessing = ident+str(self.codeGenerator.countIndicesProcessed)

                self.codeGenerator.parentIdentifier = ident
                self.codeGenerator.turnStringsIntoInts = True

                if domains != None and domains.strip() != EMPTY_STRING:
                    domains = Utils._splitDomain(domains, COMMA)

                    if len(domains) == length_sub_indices:

                        includedDomains = True
                        for i in range(length_sub_indices):
                            ind = node.sub_indices[i]
                            self.codeGenerator.newType = domains[i]

                            self.codeGenerator.turnStringsIntoInts = True
                            ind.prepare(self)
                            self.codeGenerator.turnStringsIntoInts = False
                        
                if not includedDomains:

                    self.codeGenerator.newType = INT
                    for i in range(length_sub_indices):
                        ind = node.sub_indices[i]
                        
                        self.codeGenerator.turnStringsIntoInts = True
                        ind.prepare(self)
                        self.codeGenerator.turnStringsIntoInts = False
                        
                else:

                    inds = []
                    for ind in node.sub_indices:
                        self.codeGenerator.turnStringsIntoInts = True
                        ind.prepare(self)
                        self.codeGenerator.turnStringsIntoInts = False
                    
                self.codeGenerator.turnStringsIntoInts = False
                self.codeGenerator.parentIdentifier = None
                
        else:
            node.identifier.prepare(self)

    # Number
    def prepare_Number(self, node):
        pass

    # ID
    def prepare_ID(self, node):
        
        ident = node.value

        if self.includeNewIndices:
            if self.to_enum:
                self.codeGenerator.newIndexExpression = TO_ENUM + BEGIN_ARGUMENT_LIST+self.realtype+COMMA+ident+END_ARGUMENT_LIST

            stmtIndex = node.getSymbolTable().getStatement()
            scope = node.getSymbolTable().getScope()

            self.codeGenerator._setNewIndex(ident, stmtIndex, scope)

    # String
    def prepare_String(self, node):

        string = "\"" + node.string[1:-1] + "\""

        if self.codeGenerator.turnStringsIntoInts:
            param = string[1:-1]

            if self.codeGenerator.removeAdditionalParameter:
                if param in self.codeGenerator.additionalParameters:
                    del self.codeGenerator.additionalParameters[param]
            else:
                if not param in self.codeGenerator.additionalParameters:
                    if not self.codeGenerator.newType:
                        self.codeGenerator.newType = INT

                    if not param in self.codeGenerator.additionalParameters or self.codeGenerator.newType != INT:
                        self.codeGenerator.additionalParameters[param] = self.codeGenerator.newType+SEP_PARTS_DECLARATION+SPACE + param + END_STATEMENT+BREAKLINE+BREAKLINE

            stmtIndex = node.getSymbolTable().getStatement()
            scope = node.getSymbolTable().getScope()

            self.codeGenerator.newIndexExpression = param
            self.codeGenerator._setNewIndex(string, stmtIndex, scope)

            if self.codeGenerator.genParameters.has(param):
                self.codeGenerator.genParameters.remove(param)

            if self.codeGenerator.genSets.has(param):
                self.codeGenerator.genSets.remove(param)

    # IntegerSet
    def prepare_IntegerSet(self, node):
        pass

    # RealSet
    def prepare_RealSet(self, node):
        pass

    # BinarySet
    def prepare_BinarySet(self, node):
        pass

    # SymbolicSet
    def prepare_SymbolicSet(self, node):
        pass

    # LogicalSet
    def prepare_LogicalSet(self, node):
        pass

    # ParameterSet
    def prepare_ParameterSet(self, node):
        pass

    # VariableSet
    def prepare_VariableSet(self, node):
        pass

    # SetSet
    def prepare_SetSet(self, node):
        pass
