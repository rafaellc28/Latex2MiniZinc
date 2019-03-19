import os
import json

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
from TrueFalse import *
from TopologicalSort import *
from Constants import *
from SymbolTables import *

from GenSets import *
from GenVariables import *
from GenParameters import *
from GenDeclarations import *
from GenBelongsToList import *
from GenBelongsTo import *

from EnumSet import *
from IntegerSet import *
from RealSet import *
from SymbolicSet import *
from LogicalSet import *
from BinarySet import *
from ParameterSet import *
from VariableSet import *
from SetSet import *
from String import *

from LetExpression import *
from PredicateExpression import *
from TestOperationExpression import *
from FunctionExpression import *

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

        self.generateAssertExpression = False

        self.tuples = {}
        self.tuplesDeclared = {}

        self.scopes = {}
        self.scope = 0
        self.parentScope = -1
        self.stmtIndex = -1

        self.countNewIndices = 0
        self.replaceNewIndices = True
        self.getOriginalIndices = False
        self.newIndexExpression = ""
        self.newType = INT
        self.removeAdditionalParameter = False
        self.removeParameterInSetExpressionBetweenBraces = False
        self.array2dIndex1 = None
        self.array2dIndex2 = None

        self.isSetExpressionWithIndices = False

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
        self.extraConstraints = []

        file = os.path.dirname(__file__) + os.sep + "libraries.json"

        self.LIBRARIES = json.load(open(file))

        self.include = {}

        self.isLetExpression = False
        self.isLetExpressionArgument = False
        self.isConstraintInLetExpression = False
        self.isConstraint = False
        self.isWithinOtherExpression = False

    def generateCode(self, node):
        cls = node.__class__
        method_name = 'generateCode_' + cls.__name__
        method = getattr(self, method_name, None)

        if method:
            return method(node)

    def _getDomainByIdentifier(self, ident):
        if ident in self.identifiers:
            res = self.identifiers[ident]
            return res[DOMAIN]

        return None

    def _getDomainsByIdentifier(self, ident):
        if ident in self.identifiers:
            res = self.identifiers[ident]
            return res[DOMAINS]

        return None

    def _getDomainsWithIndicesByIdentifier(self, ident):
        if ident in self.identifiers:
            res = self.identifiers[ident]
            return res[DOMAINS_WITH_INDICES_LIST]

        return None

    def _getSubIndicesDomainsAndDependencies(self, var):
        if var in self.identifiers:
            res = self.identifiers[var]
            return res[DOMAIN], res[DOMAINS], res[DOMAINS_WITH_INDICES_LIST], res[DEPENDENCIES], res[SUB_INDICES], res[STATEMENT]

        return None, [], [], [], None

    def _getProperties(self, var):
        if var in self.identifiers:
            res = self.identifiers[var]
            return res[TYPES], res[DIM], res[MINVAL], res[MAXVAL]

        return None, [], [], []

    def _hasVariable(self, expression):
        dependencies = expression.getDependencies(self)

        for dep in dependencies:
            if self.genVariables.has(dep):
                return True

        return False

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
               (isinstance(obj, SetExpression) and \
               obj.getSymbolName(self).replace(SPACE, EMPTY_STRING) == Constants.BINARY_0_1)

    def _isModifierSet(self, obj):
        obj = self._getIdentifierNode(obj)
        return isinstance(obj, LogicalSet)

    def notInTypesThatAreNotDeclarable(self, value):
        if isinstance(value, Tuple):
            return True
        
        value = value.getSymbol()
        
        return not value.isBinary and not value.isInteger and not value.isNatural and not value.isReal and not value.isSymbolic and not \
        value.isLogical and not value.isEnum and not value.isDeclaredAsVar and not value.isDeclaredAsParam and not value.isDeclaredAsSet and not \
        isinstance(value, str)

    def _removeTypesThatAreNotDeclarable(self, _types):
        return filter(lambda el: not self._isIdentifierType(el.getObj()), _types)

    def _removePreDefinedTypes(self, _types):
        return filter(lambda el: not self._isIdentifierType(el) and not self._isTypeSet(el) and not self._isModifierSet(el), _types)

    def _getTypes(self, _types):
        return filter(lambda el: self._isTypeSet(el.getObj()), _types)

    def _getModifiers(self, _types):
        return filter(lambda el: self._isModifierSet(el.getObj()), _types)

    def _getValueFromNumericExpression(self, expr):
        if isinstance(expr, ValuedNumericExpression):
            return expr.value

        return expr

    def _checkIsSetOperation(self, key):
        for op in self.SET_OPERATIONS:
            op = " " + op + " "
            if op in key:
                return True

        return False

    def _checkIsValuesBetweenBraces(self, setExpression):
        if not setExpression or not (setExpression[0] == BEGIN_SET and setExpression[len(setExpression)-1] == END_SET):
            return False

        setExpression = setExpression[1:-1]
        values = Utils._splitDomain(setExpression, COMMA)

        for value in values:
            if not re.search(REGEX_IDENTIFIER, value) and not re.search(REGEX_BETWEEN_QUOTES, value):
                return False

        return True

    def _checkIsSetBetweenBraces(self, setExpression):
        isAllIdentifiers = self._checkIsValuesBetweenBraces(setExpression)

        if not isAllIdentifiers or not setExpression:
            return False

        return setExpression[0] == BEGIN_SET and setExpression[len(setExpression)-1] == END_SET and not FROM_TO in setExpression and not setExpression == BEGIN_SET + END_SET

    def _checkIsSetExpressionWithTuple(self, setExpression):
        return re.search(REGEX_ARGUMENT_LIST+IN+"\s+", setExpression)

    def _cleanKeyWithSetOperation(self, key):
        key = key.replace(FLOOR+BEGIN_ARGUMENT_LIST, EMPTY_STRING)
        key = key.replace(BEGIN_SET, EMPTY_STRING)
        key = key.replace(END_SET, EMPTY_STRING)
        key = key.replace(BEGIN_ARGUMENT_LIST, EMPTY_STRING)
        key = key.replace(END_ARGUMENT_LIST, EMPTY_STRING)
        key = key.replace(BEGIN_ARRAY, EMPTY_STRING)
        key = key.replace(END_ARRAY, EMPTY_STRING)
        key = key.replace(SUCH_THAT, EMPTY_STRING)
        key = key.replace(COMMA, UNDERLINE)
        key = key.replace(SPACE, UNDERLINE)

        return key

    def _getIndicesFromSetOperation(self, setExpression):
        m = re.findall(REGEX_INDICES_SET_OPERATION, setExpression)
        if m and len(m) > 0:
            indices = []
            for ind in m:
                inds = Utils._splitDomain(ind, COMMA)

                if inds and len(inds) > 0:
                    for i in inds:
                        if not i in indices:
                            indices.append(i)

            return indices

        return None

    def _getSets(self, setExpression):
        sets = []
        dimensions = []
        words = Utils._getWords(setExpression)

        for w in words:
            _genSet = self.genSets.get(w)
            if _genSet != None:
                sets.append(w)
                dimensions.append(_genSet.getDimension())

        return sets, dimensions

    def _isSetForTuple(self, setExpression):
        if not setExpression in self.tuplesDeclared:
            return False

        return not self.tuplesDeclared[setExpression][ISSETWITHINDICES]

    def _processDomainsWithIndices(self, domain_with_indices):

        dummy_indices = []
        for d in domain_with_indices:
            if isinstance(d, str):
                dummy_indices.append(d.split(SPACE+IN+SPACE)[0].strip() if SPACE+IN+SPACE in d else EMPTY_STRING)
            else:
                dummy_indices.append(None)

        new_domain_with_indices = []

        idx = "i"
        count = 0
        
        for i in range(len(domain_with_indices)):
            d = dummy_indices[i]
            
            if d == EMPTY_STRING:
                new_dummy_index = idx+str(count)
                count += 1

                while new_dummy_index in dummy_indices:
                    new_dummy_index = idx+str(count)
                    count += 1

                new_domain_with_indices.append(new_dummy_index + SPACE+IN+SPACE + domain_with_indices[i])

            else:
                new_domain_with_indices.append(domain_with_indices[i])

        return new_domain_with_indices

    # Get the MiniZinc code for a given relational expression
    def _getCodeValue(self, value):
        val = value.generateCode(self)
        return val

    # Get the MiniZinc code for a given sub-indice
    def _getCodeID(self, id_):
        if isinstance(id_, ValuedNumericExpression):
            if isinstance(id_.value, Identifier):
                id_.value.setIsSubIndice(True)

        elif isinstance(id_, Identifier):
            id_.setIsSubIndice(True)

        val = id_.generateCode(self)

        return val

    # Get the MiniZinc code for a given entry
    def _getCodeEntry(self, entry): return entry.generateCode(self)

    # Get the MiniZinc code for a given entry
    def _getCodeEntryByKey(self, entry):
        for key in entry:
            conj = AND if key == ANDLITERAL else OR
            return conj, entry[key].generateCode(self)

    # Get the MiniZinc code for a given objective
    def _getCodeObjective(self, objective):
        self.objectiveNumber += 1
        return objective.generateCode(self)

    # Get the MiniZinc code for a given constraint
    def _getCodeConstraint(self, constraint):
        if isinstance(constraint, Constraint):
            self.constraintNumber += 1

            self.isConstraint = True
            res = CONSTRAINT + SPACE + constraint.generateCode(self)
            self.isConstraint = False

            return res

        elif isinstance(constraint, TestOperationExpression) or isinstance(constraint, PredicateExpression) or \
             isinstance(constraint, LetExpression) or isinstance(constraint, FunctionExpression):

             self.isWithinOtherExpression = True
             res = constraint.generateCode(self)
             self.isWithinOtherExpression = False

             return res

        elif isinstance(constraint, Objective):
            return self._getCodeObjective(constraint)

        return EMPTY_STRING

    def removeInvalidConstraint(self, constraint):
        valid =  constraint != None and constraint.strip() != EMPTY_STRING and constraint.strip() != CONSTRAINT+SPACE+END_STATEMENT

        if valid:
            match = re.search(FORALL+"\(.+\)\(\)", constraint)

            if match:
                valid = False

        return valid

    def formatNumber(self, number):
        return (ZERO if number[0] == PERIOD else EMPTY_STRING) + number

    def _getIndices(self, sub_indices, domains_with_indices, dim, stmt, scope):
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
            indices_ins = [EMPTY_STRING]*len(domains_with_indices)

        indices_ins_res = list(indices_ins)

        count = 0
        for i in range(len(domains_with_indices)):

            if count < dim:
                d = domains_with_indices[i]

                if not isinstance(d, str):
                    setName = d[SET]
                    
                    if setName in self.tuplesDeclared:
                        indices = d[INDICES]
                        index = indices[0]

                        c = 1
                        cs = []
                        for i in indices:
                            if not c in cs:
                                repl = setName + BEGIN_ARRAY+index+COMMA+str(c)+END_ARRAY
                                cs.append(c)
                                c += 1

                                ind = [j for j, v in enumerate(indices_ins) if v == i]
                                for j in ind:
                                    indices_ins_res[j] = repl
                                    count += 1

                                self.newIndexExpression = repl
                                self._setNewIndex(i, stmt, scope)

                else:

                    parts = d.split(" in ")
                    index = parts[0].strip()
                    setName = parts[1].strip()

                    if setName in self.tuplesDeclared:

                        c = 0
                        cs = []
                        
                        dimen = self.tuplesDeclared[setName][DIMEN]
                        indices = range(dimen)
                        
                        size = len(indices_ins)
                        if size < dimen:

                            i = size
                            while i < dimen:
                                indices_ins_res.append(str(i))

                                i += 1

                        repls = []
                        for i in indices_ins:
                            if count < dim:
                                for k in indices:
                                    if not c in cs:
                                        repl = setName + BEGIN_ARRAY+index+COMMA+str(c+1)+END_ARRAY
                                        cs.append(c)
                                        
                                        c += 1
                                        count += 1
                                        repls.append(repl)


                                repl = ", ".join(repls)
                                ind = [j for j, v in enumerate(indices_ins) if v == i]
                                for j in ind:
                                    c2 = 0
                                    for c1 in range(j, len(repls)):
                                        indices_ins_res[c1] = repls[c2]
                                        c2 += 1
                                    
                                self.newIndexExpression = repl
                                self._setNewIndex(i, stmt, scope)

                    else:
                        if SPACE+IN+SPACE in d:
                            indices_ins_res[i] = d.split(SPACE+IN+SPACE)[0].strip()

        return indices_ins_res

    def _getDomainsWithIndices(self, domains_with_indices, dim):
        
        domains = []
        c = 0
        for d in domains_with_indices:
            if c < dim:
                
                if isinstance(d, str):
                    parts = d.split(" in ")
                    index = parts[0].strip()
                    setName = parts[1].strip()
                    
                    if setName in self.tuplesDeclared:
                        index1 = self.tuplesDeclared[setName][INDEX1]
                        domain = index + SPACE+IN+SPACE + index1

                        if not domain in domains:
                            domains.append(domain)
                            c += self.tuplesDeclared[setName][DIMEN]

                    else:
                        if not d in domains:
                            domains.append(d)
                            c += 1

                else:
                    setName = d[SET]
                    
                    if setName in self.tuplesDeclared:
                        index1 = self.tuplesDeclared[setName][INDEX1]
                        indices = d[INDICES]
                        index = indices[0]
                        domain = index + SPACE+IN+SPACE + index1

                        if not domain in domains:
                            domains.append(domain)
                            c += self.tuplesDeclared[setName][DIMEN]

                    else:
                        domains.append(EMPTY_STRING)
                        c += 1

        return domains

    def _getDomains(self, domains, dim):
        res = []
        c = 0
        for d in domains:
            
            if c < dim:
                if d in self.tuplesDeclared:
                    _type = self.tuplesDeclared[d][TYPE]
                    index2 = self.tuplesDeclared[d][INDEX2]
                    size = int(index2[3:])

                    for i in range(size):
                        res.append(INT)
                        c += 1

                elif BEGIN_ARRAY in d:
                    res.append(INT)
                    c += 1

                #elif not FROM_TO in d:
                #    res.append(INT)

                else:
                    res.append(INT)
                    #res.append(d)
                    c += 1

        return res

    def _getRelationalConstraintExpressions(self, attributes, cntAux, cntAux_assert, op, name, sub_indices_vec, domains_with_indices, dim, isArray, isVariable):
        if len(attributes) > 0:
            for attr in attributes:
                cntAux, cntAux_assert = self._getRelationalConstraintExpression(attr, cntAux, cntAux_assert, op, name, sub_indices_vec, domains_with_indices, dim, isArray, isVariable)

        return cntAux, cntAux_assert

    def _getRelationalConstraintExpression(self, attr, cntAux, cntAux_assert, op, name, sub_indices_vec, domains_with_indices, dim, isArray, isVariable):

        if attr != None:
            attribute = attr.attribute.generateCode(self)
            
            if not isVariable:
                self.generateAssertExpression = True
                attribute_assert = attr.attribute.generateCode(self)
                self.generateAssertExpression = False

            if cntAux != EMPTY_STRING:
                cntAux += SPACE+AND+SPACE

            if not isVariable and cntAux_assert != EMPTY_STRING:
                cntAux_assert += SPACE+AND+BACKSPACE+SPACE # backspace must be used to form /\\ and avoid minizinc error

            if isArray:
                stmtIndex = attr.attribute.getSymbolTable().getStatement()
                scope = attr.attribute.getSymbolTable().getScope()

                indices = self._getIndices(sub_indices_vec, domains_with_indices, dim, stmtIndex, scope)
                indices = map(lambda el: el if isinstance(el, str) else el.generateCode(self), indices)
                
                cntAux += name+BEGIN_ARRAY+COMMA.join(indices)+END_ARRAY+SPACE+op+SPACE+attribute

                if not isVariable:
                    indices_assert = map(lambda el: "\\("+el+")", indices)
                    cntAux_assert += name+BEGIN_ARRAY+COMMA.join(indices_assert)+END_ARRAY+SPACE+op+SPACE+attribute_assert
                
            else:
                cntAux += name + SPACE+op+SPACE + attribute

                if not isVariable:
                    cntAux_assert += name + SPACE+op+SPACE + attribute_assert

        return cntAux, cntAux_assert

    def _getRelationalConstraintsFromDeclaration(self, declaration, name, dim, isArray, sub_indices_vec, domains_with_indices, isVariable = False):
        cnt = EMPTY_STRING
        cntAux = EMPTY_STRING
        cntAux_assert = EMPTY_STRING

        attr = declaration.getRelationsEqualTo()
        cntAux, cntAux_assert = self._getRelationalConstraintExpressions(attr, cntAux, cntAux_assert, EQUAL, name, sub_indices_vec, domains_with_indices, dim, isArray, isVariable)

        attr = declaration.getRelationsDifferentFrom()
        cntAux, cntAux_assert = self._getRelationalConstraintExpressions(attr, cntAux, cntAux_assert, NEQ, name, sub_indices_vec, domains_with_indices, dim, isArray, isVariable)

        attr = declaration.getRelationsLessThan()
        cntAux, cntAux_assert = self._getRelationalConstraintExpressions(attr, cntAux, cntAux_assert, LT, name, sub_indices_vec, domains_with_indices, dim, isArray, isVariable)

        attr = declaration.getRelationsLessThanOrEqualTo()
        cntAux, cntAux_assert = self._getRelationalConstraintExpressions(attr, cntAux, cntAux_assert, LE, name, sub_indices_vec, domains_with_indices, dim, isArray, isVariable)

        attr = declaration.getRelationsGreaterThan()
        cntAux, cntAux_assert = self._getRelationalConstraintExpressions(attr, cntAux, cntAux_assert, GT, name, sub_indices_vec, domains_with_indices, dim, isArray, isVariable)

        attr = declaration.getRelationsGreaterThanOrEqualTo()
        cntAux, cntAux_assert = self._getRelationalConstraintExpressions(attr, cntAux, cntAux_assert, GE, name, sub_indices_vec, domains_with_indices, dim, isArray, isVariable)
                    
        if cntAux != EMPTY_STRING:

            if isVariable:
                if isArray:
                    domains = self._getDomainsWithIndices(domains_with_indices, dim)
                    cnt += CONSTRAINT+SPACE+FORALL+BEGIN_ARGUMENT_LIST+(COMMA+SPACE).join(domains)+END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST+cntAux+END_ARGUMENT_LIST+END_STATEMENT

                else:
                    cnt += CONSTRAINT+SPACE+cntAux+END_STATEMENT

                self.additionalConstraints.append(cnt)

            else:

                if isArray:
                    domains = self._getDomainsWithIndices(domains_with_indices, dim)
                    cnt += CONSTRAINT+SPACE+FORALL+BEGIN_ARGUMENT_LIST+(COMMA+SPACE).join(domains)+END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST+ASSERT+BEGIN_ARGUMENT_LIST+cntAux+COMMA+SPACE+QUOTE+ASSERTION+SPACE+cntAux_assert+SPACE+FAILED+QUOTE+END_ARGUMENT_LIST+END_ARGUMENT_LIST+END_STATEMENT

                else:
                    cnt += CONSTRAINT+SPACE+ASSERT+BEGIN_ARGUMENT_LIST+cntAux+COMMA+SPACE+QUOTE+ASSERTION+SPACE+cntAux_assert+SPACE+FAILED+QUOTE+END_ARGUMENT_LIST+END_STATEMENT

                self.additionalConstraints.append(cnt)

    def _getRelationalConstraints(self, _type, name, dim, isArray, sub_indices, domains_with_indices, stmt, scope, isVariable = False):
        rest = _type
        rest = rest.strip()

        if rest != EMPTY_STRING:
            
            var = EMPTY_STRING
            var_assert = EMPTY_STRING
            
            const = EMPTY_STRING
            const_assert = EMPTY_STRING
            
            if isArray:
                indices_ins = self._getIndices(sub_indices, domains_with_indices, dim, stmt, scope)
                indices_ins_assert = map(lambda el: "\\("+el+")", indices_ins)
                
                var = name + BEGIN_ARRAY + COMMA.join(indices_ins) + END_ARRAY

                if not isVariable:
                    var_assert = name+BEGIN_ARRAY+COMMA.join(indices_ins_assert)+END_ARRAY
                
            else:
                var = name
                
            m = re.search(r"("+GT+"|"+GE+")\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?", rest)
            if m:
                rel = EMPTY_STRING
                groups = m.groups(0)
                rel += SPACE + groups[0] + SPACE
                rel += self.formatNumber(groups[1])
                
                if groups[2] != None and groups[2] != 0:
                    rel += groups[2]
                    
                const += var + rel

                if not isVariable:
                    const_assert += var_assert + rel
                
            m = re.search(r"("+LT+"|"+LE+")\s*([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?", rest)
            if m:
                rel = EMPTY_STRING
                groups = m.groups(0)
                rel += SPACE + groups[0] + SPACE
                rel += self.formatNumber(groups[1])
                
                if groups[2] != None and groups[2] != 0:
                    rel += groups[2]
                
                if const != EMPTY_STRING:
                    const += SPACE+AND+SPACE

                    if not isVariable:
                        const_assert += SPACE+AND+SPACE
                    
                const += var + rel

                if not isVariable:
                    const_assert += var_assert + rel
                
            cnt = EMPTY_STRING
            if const:
                
                if isVariable:
                    
                    if isArray:
                        domains = self._getDomainsWithIndices(domains_with_indices, dim)
                        cnt += CONSTRAINT+SPACE+FORALL+BEGIN_ARGUMENT_LIST+(COMMA+SPACE).join(domains)+END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST+const+END_ARGUMENT_LIST+END_STATEMENT
                        
                    else:
                        cnt += CONSTRAINT+SPACE+const+END_STATEMENT
                        
                else:
                    
                    if isArray:
                        
                        domains = self._getDomainsWithIndices(domains_with_indices, dim)
                        cnt += CONSTRAINT+SPACE+FORALL+BEGIN_ARGUMENT_LIST+(COMMA+SPACE).join(domains)+END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST+ASSERT+BEGIN_ARGUMENT_LIST+const+COMMA+SPACE+QUOTE+ASSERTION+SPACE+const_assert+SPACE+FAILED+QUOTE+END_ARGUMENT_LIST+END_ARGUMENT_LIST+END_STATEMENT
                        
                    else:
                        cnt += CONSTRAINT+SPACE+ASSERT+BEGIN_ARGUMENT_LIST+const+COMMA+SPACE+QUOTE+ASSERTION+SPACE+const+SPACE+FAILED+QUOTE+END_ARGUMENT_LIST+END_STATEMENT
                        
                return cnt
                
        return None

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

    def _deleteIndexSet(self, array, name):
        aux = re.search(ARRAY+"\[(.*)\]", array)
        
        if not aux:
            return

        aux = aux.groups(0)[0]
        domains = map(lambda el: el.strip(), aux.split(COMMA))
        index = INDEX_SET_+name

        if index in self.additionalParameters and not index in domains:
            del self.additionalParameters[index]


    def _processDomain(self, domain, domains, domains_with_indices, dim, minVal, maxVal, isVariable = False):

        isArray = False
        array = EMPTY_STRING
        domains_aux = []

        if domain != None and domain.strip() != EMPTY_STRING:

            if isVariable:

                domains0 = self._getDomains(domains, dim)
                for d in domains0:
                    if d in self.tuples:
                        d = INT
                        _tuple = self.tuples[d]
                        dimen = _tuple[DIMEN]

                        if dimen != None:
                            for i in range(dimen):
                                domains_aux.append(d)
                    else:
                        domains_aux.append(d)
                
            else:
                domains_aux = domains
                domains = self._getDomains(domains, dim)
                domain = (COMMA+SPACE).join(domains)
                array = ARRAY + BEGIN_ARRAY + domain + END_ARRAY

            isArray = True
            
        elif minVal != None and len(minVal) > 0 and maxVal != None and len(maxVal) > 0 and Utils._hasAllIndices(minVal, maxVal):
            domainMinMax = []
            for i in range(len(minVal)):
                domainMinMax.append(str(minVal[i])+FROM_TO+str(maxVal[i]))

            domains_aux = self._getDomains(domainMinMax, dim)
            domains = domainMinMax
            domain = (COMMA+SPACE).join(domains)
            array = ARRAY + BEGIN_ARRAY+(COMMA+SPACE).join(domains)+END_ARRAY
            domains_with_indices = self._processDomainsWithIndices(domainMinMax)
            isArray = True

        elif dim > 0:
            domains_aux = [INT]*dim
            domains = self._getDomains(domains_aux, dim)
            domain = (COMMA+SPACE).join(domains)
            array = ARRAY + BEGIN_ARRAY+(COMMA+SPACE).join(domains)+END_ARRAY
            domains_with_indices = self._processDomainsWithIndices(domains_aux)
            isArray = True

        return domain, domains, domains_with_indices, domains_aux, array, isArray

    def _processValueFromDeclaration(self, declaration, name, _type, value, dim, array, isArray, _subIndices, 
            domains, domains_aux, domains_with_indices, stmtIndex, isSet = False):

        arrayFromTuple = False
        deleteTupleIndex = False

        self.removeParameterInSetExpressionBetweenBraces = False

        if declaration.getValue() != None:

            self.turnStringsIntoInts = True
            self.removeAdditionalParameter = True

            indexingExpression = None
            indexingExpression, _subIndicesAux = self._getIndexingExpressionFromDeclaration(declaration, stmtIndex)

            if not indexingExpression:
                indexingExpression = self._getDomainsWithIndicesByIdentifier(name)
                if indexingExpression != None and len(indexingExpression) > 0:
                    indexingExpression = self._getDomainsWithIndices(indexingExpression, dim)
                    indexingExpression = (COMMA+SPACE).join(indexingExpression)

                else:
                    indexingExpression = None

            if isinstance(declaration.getValue().attribute, SymbolicExpression) or isinstance(declaration.getValue().attribute, String):
                self.turnStringsIntoInts = False
                self.removeAdditionalParameter = False
                _type = STRING

            elif isinstance(declaration.getValue().attribute, TrueFalse):
                _type = BOOL

            elif isinstance(declaration.getValue().attribute, SetExpressionBetweenBraces) and not isinstance(declaration.getValue().attribute.setExpression, Range):
                self.removeParameterInSetExpressionBetweenBraces = True

            value = declaration.getValue().attribute.generateCode(self)
            self.removeParameterInSetExpressionBetweenBraces = False
            
            if not isinstance(declaration.getValue().attribute, Array):

                dependencies = declaration.getValue().attribute.getDependencies(self)
                if name in dependencies:
                    
                    cnt = None
                    if isArray:
                        stmtIndex = declaration.getValue().attribute.getSymbolTable().getStatement()
                        scope = declaration.getValue().attribute.getSymbolTable().getScope()

                        indices = map(lambda el: el.generateCode(self), _subIndices)
                        indices = self._getIndices(indices, domains_with_indices, dim, stmtIndex, scope)
                        
                        if indexingExpression:
                            cnt = CONSTRAINT+SPACE+FORALL+BEGIN_ARGUMENT_LIST + indexingExpression + END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST + name + BEGIN_ARRAY + COMMA.join(indices) + END_ARRAY+SPACE+EQUAL+SPACE + value + END_ARGUMENT_LIST+END_STATEMENT;

                    else:
                        cnt = CONSTRAINT+SPACE + name + SPACE+EQUAL+SPACE + value + END_STATEMENT;

                    if cnt:
                        self.additionalConstraints.append(cnt)

                    value = EMPTY_STRING
                    
                else:

                    self.getOriginalIndices = True
                    value2 = declaration.getValue().attribute.generateCode(self)
                    self.getOriginalIndices = False
                    
                    if value2 in self.setsWitOperations:

                        setValue = False
                        if isSet:
                            setValue = self._checkIsSetExpressionWithTuple(value2) or (isArray and not value2.startswith(ARRAY) and not value2.startswith(BEGIN_ARRAY))
                        else:
                            setValue = self._checkIsValuesBetweenBraces(value2)

                        if setValue:
                            value = self.setsWitOperations[value2]
                            self.setsWitOperationsUsed.append(value)
                            
                            if value2 in self.setsWitOperationsIndices:
                                v = self.setsWitOperationsIndices[value2]
                                
                                if v[DIMEN] > 0:
                                    value += BEGIN_ARRAY
                                    inds = []
                                    for i in range(len(v[INDICES])):
                                        inds.append(v[INDICES][i])
                                    value += COMMA.join(inds) + END_ARRAY
                        
                        setType = False
                        if isSet:
                            setType = not self._checkIsSetBetweenBraces(value2) and not self._isSetForTuple(name)
                        else:
                            setType = not self._isSetForTuple(name)

                        if setType:
                            _type = SET_OF_INT
                        
                    self.turnStringsIntoInts = False
                    self.removeAdditionalParameter = False

                    rangeSet = self._getRange(declaration.getValue().attribute)
                    if rangeSet != None:
                        _type = SET_OF_INT
                        value = rangeSet.generateCode(self)

                    elif value.startswith(BEGIN_ARRAY):
                        _type = SET_OF_INT
                    
                    if not (BEGIN_SET in value and isArray) and (not value.startswith(ARRAY) and \
                        (isArray or len(_subIndices) > 0 or BEGIN_ARRAY in value)):
                        
                        if not value.startswith(ARRAY):
                            if indexingExpression != None and indexingExpression.strip() != EMPTY_STRING:
                                value = BEGIN_ARRAY+value+SPACE+SUCH_THAT+SPACE+indexingExpression+END_ARRAY

                            if len(domains) > 0:
                                length_domains = len(domains)
                                indices = []
                                array = ARRAY + BEGIN_ARRAY

                                for i in range(length_domains):
                                    if i < len(domains_aux):
                                        d = domains_aux[i]
                                    else:
                                        d = domains[i]

                                    if domains[i] == INT or (i < len(domains_aux) and domains_aux[i] == INT):
                                        index = INDEX_SET_+name+UNDERLINE+str(i+1)
                                        setExpression = SET_OF_INT + SEP_PARTS_DECLARATION+SPACE+index

                                        if i < len(domains_aux) and FROM_TO in domains_aux[i]:
                                            setExpression += SPACE+ASSIGN+SPACE + domains_aux[i]

                                            if i < len(domains_with_indices) and SPACE+IN+SPACE in domains_with_indices[i]:
                                                pos = domains_with_indices[i].find(SPACE+IN+SPACE)
                                                domains_with_indices[i] = domains_with_indices[i][:pos] + SPACE+IN+SPACE + index

                                        setExpression += END_STATEMENT+BREAKLINE+BREAKLINE

                                        self.additionalParameters[index] = setExpression
                                        indices.append(index)

                                    else:
                                        indices.append(d)
                                
                                self._deleteIndexSet(array, name)
                                isArray = True

                                if _type == ENUM:
                                    _type = INT

                                arrayFromTuple = True
                                deleteTupleIndex = True

                                if isSet:
                                    
                                    if _type != ENUM:
                                        _typeAux = _type + SEP_PARTS_DECLARATION
                                    else:
                                        _typeAux = _type

                                    array += (COMMA+SPACE).join(indices) + END_ARRAY+SPACE + OF + SPACE+_typeAux+SPACE + name

                                else:
                                    array += (COMMA+SPACE).join(indices) + END_ARRAY

                                if not value.startswith(BEGIN_ARRAY):
                                    i = 0
                                    value = BEGIN_ARRAY + value + SPACE+SUCH_THAT+SPACE
                                    for idx in indices:
                                        value += "i"+str(i)+SPACE+IN+SPACE+idx
                                        i += 1
                                    value += END_ARRAY

                                value = ARRAY +str(length_domains)+"d"+BEGIN_ARGUMENT_LIST+(COMMA+SPACE).join(indices)+COMMA+SPACE+value+END_ARGUMENT_LIST

                    self.genValueAssigned.add(GenObj(name))

        return value, _type, array, isArray, arrayFromTuple, deleteTupleIndex

    def _processInDeclaration(self, name, declaration, isArray, isVariable = False):

        _type = EMPTY_STRING

        if declaration != None:
            ins_vec = declaration.getIn()
            ins_vec = self._removePreDefinedTypes(map(lambda el: el.attribute, ins_vec))
            
            if ins_vec != None and len(ins_vec) > 0:
                ins = ins_vec[-1].generateCode(self)

                setExpression = ins_vec[-1]
                ins = setExpression.generateCode(self)

                if isinstance(setExpression, IteratedSetExpression) and setExpression.inferred:
                    if len(ins_vec) > 1:
                        ins = ins_vec[-2].generateCode(self)
                
                if ins != EMPTY_STRING and not self._checkIsSetBetweenBraces(ins) and not (ins == SET_OF_INT and self._isSetForTuple(name)):

                    if isVariable:
                        if isArray:
                            _type += SPACE + OF + SPACE+VAR+SPACE + ins

                        else:
                            _type += VAR + SPACE + ins

                    else:
                        _type += ins

        return _type

    def _processTypeDeclaration(self, name, _types, dim, isArray, sub_indices_vec, domains_with_indices, isVariable = False):
        _type = EMPTY_STRING

        _types = self._removeTypesThatAreNotDeclarable(_types)
        _types = self._getTypes(_types)
        
        if len(_types) > 0:
            _type = _types[0].getObj()

            stmtIndex = _type.getSymbolTable().getStatement()
            scope = _type.getSymbolTable().getScope()
            
            if isinstance(_type, BinarySet):
                _type = BOOL;

            elif isinstance(_type, IntegerSet):

                const =  self._getRelationalConstraints(_type.generateCode(self), name, dim, isArray, sub_indices_vec, domains_with_indices, stmtIndex, scope, isVariable)
                
                if const:
                    self.additionalConstraints.append(const)

                _type = INT;

            elif isinstance(_type, SymbolicSet):
                _type = STRING;

            elif isinstance(_type, RealSet):
                const =  self._getRelationalConstraints(_type.generateCode(self), name, dim, isArray, sub_indices_vec, domains_with_indices, stmtIndex, scope, isVariable)
                
                if const:
                    self.additionalConstraints.append(const)

                _type = FLOAT;

            elif isinstance(_type, EnumSet):
                _type = ENUM;

            if _type.strip() == EMPTY_STRING:
                _type = EMPTY_STRING

        return _type


    def _inferTypeByIndexPositionInAnotherIdentifier(self, name):
        _type = EMPTY_STRING

        if name in self.parameterIsIndexOf:
            valueAux = self.parameterIsIndexOf[name]
            var = valueAux[INDEXOF]
            pos = valueAux[POS]

            setExpression = self._getDomainByIdentifier(var)

            _types = Utils._splitDomain(setExpression, COMMA)
            if pos < len(_types):
                _type_aux = _types[pos]

                if not FROM_TO in _type_aux:
                    _type = _type_aux

        return _type

    def _processTypeFromGenParameter(self, _genParameter):
        _type = EMPTY_STRING

        if _genParameter.getIsInteger():
            _type = INT

        elif _genParameter.getIsSymbolic():
            _type = STRING

        elif _genParameter.getIsLogical():
            _type = BOOL

        else:
            _type = FLOAT

        return _type

    def _getDomainFromIndexingExpressionInDeclaration(self, domain, isArray, array, declaration, stmtIndex):
        indexingExpression, _subIndicesAux = self._getIndexingExpressionFromDeclaration(declaration, stmtIndex)

        if indexingExpression:
            domain = indexingExpression
            isArray = True
            array += ARRAY + BEGIN_ARRAY + domain + END_ARRAY

        return domain, isArray, array

    def _declareVars(self):
        """
        Generate the MiniZinc code for the declaration of variables
        """

        varStr = EMPTY_STRING
        if len(self.genVariables) > 0:
            
            for var in self.genVariables.getAll():
                varStr += self._declareVar(var)

        return varStr

    def _declareVar(self, var):
        """
        Generate the MiniZinc code for the declaration of a variable
        """
        varStr = EMPTY_STRING

        if not self.genParameters.has(var) and not self.genSets.has(var):

            domain = None
            name = var.getName()
            isArray = False
            includedVar = False
            array = EMPTY_STRING
            value = EMPTY_STRING
            
            declaration = self.genDeclarations.get(name)

            domain, domains, domains_with_indices, dependencies_vec, sub_indices_vec, stmtIndex = self._getSubIndicesDomainsAndDependencies(name)
            _types, dim, minVal, maxVal = self._getProperties(name)

            _subIndices = self._getIndicesFromDeclaration(declaration, stmtIndex)

            domain, domains, domains_with_indices, domains_aux, arrayVar, isArray = \
                self._processDomain(domain, domains, domains_with_indices, dim, minVal, maxVal, True)

            if not domain and declaration != None:
                size = len(_subIndices)
                if size > 0:
                    isArray = True
                    domains_aux = [INT]*size
                    domains_with_indices = self._processDomainsWithIndices(domains_aux)

            if isArray:
                
                for i in range(len(domains_aux)):
                    d = domains_aux[i]
                    if d == INT:
                        index = INDEX_SET_+name+UNDERLINE+str(i+1)

                        setExpression = SET_OF_INT + SEP_PARTS_DECLARATION+SPACE+index
                        
                        if i < len(domains):# and (FROM_TO in domains[i] or domains[i] == INT):

                            if domains[i] != INT and not BEGIN_ARRAY in domains[i]:
                                setExpression += SPACE+ASSIGN+SPACE + domains[i]

                            if i < len(domains_with_indices) and SPACE+IN+SPACE in domains_with_indices[i]:
                                
                                pos = domains_with_indices[i].find(SPACE+IN+SPACE)
                                domains_with_indices[i] = domains_with_indices[i][:pos] + SPACE+IN+SPACE + index

                        setExpression += END_STATEMENT+BREAKLINE+BREAKLINE

                        self.additionalParameters[index] = setExpression

                        domains_aux[i] = index

                array  = ARRAY + BEGIN_ARRAY
                array += (COMMA+SPACE).join(domains_aux) + END_ARRAY
                self._deleteIndexSet(array, name)

                varStr += array

            _type = self._processInDeclaration(name, declaration, isArray, True)

            if _type != EMPTY_STRING:
                varStr += _type + SEP_PARTS_DECLARATION
                includedVar = True

            else:
                _typeAux = self._processTypeDeclaration(name, _types, dim, isArray, sub_indices_vec, domains_with_indices, True)

                if _typeAux != EMPTY_STRING:
                    includedVar = True 
                    _type = _typeAux

                    if _type != ENUM:
                        _type = _type + SEP_PARTS_DECLARATION

                    if isArray:
                        varStr += SPACE + OF + SPACE+VAR+SPACE + _type
                    else:
                        varStr += VAR+SPACE + _type

            if not includedVar:
                if isArray:
                    varStr += SPACE + OF + SPACE+VAR+SPACE + FLOAT + SEP_PARTS_DECLARATION
                else:
                    varStr += VAR+SPACE + FLOAT + SEP_PARTS_DECLARATION

            if declaration != None:

                if declaration.getValue() != None:
                    value, _type, array, isArray, arrayFromTuple, deleteTupleIndex = \
                        self._processValueFromDeclaration(declaration, name, _type, value, dim, array, isArray, _subIndices, domains, domains_aux, domains_with_indices, stmtIndex)

                else:
                    self._getRelationalConstraintsFromDeclaration(declaration, name, dim, isArray, sub_indices_vec, domains_with_indices, True)

            if value != EMPTY_STRING and value.strip() != EMPTY_STRING:
                name += SPACE+ASSIGN+SPACE + value.strip()

            varStr += SPACE + name
            varStr += END_STATEMENT+BREAKLINE+BREAKLINE
            
        return varStr

    def _declareParam(self, _genParameter):
        
        name = _genParameter.getName()

        paramStr = EMPTY_STRING
        domain = None
        _type = None
        isArray = False
        includedType = False
        array = EMPTY_STRING
        value = EMPTY_STRING
        
        declaration = self.genDeclarations.get(name)

        domain, domains, domains_with_indices, dependencies_vec, sub_indices_vec, stmtIndex = self._getSubIndicesDomainsAndDependencies(name)
        _types, dim, minVal, maxVal = self._getProperties(name)

        _subIndices = self._getIndicesFromDeclaration(declaration, stmtIndex)

        domain, domains, domains_with_indices, domains_aux, arrayParam, isArray = self._processDomain(domain, domains, domains_with_indices, dim, minVal, maxVal)
        array += arrayParam

        if declaration != None:

            if not domain:
                domain, isArray, array = self._getDomainFromIndexingExpressionInDeclaration(domain, isArray, array, declaration, stmtIndex)
            
            _typeAux = self._processInDeclaration(name, declaration, isArray)

            if _typeAux != EMPTY_STRING:
               includedType = True 
               _type = _typeAux

        if not includedType:

            _typeAux = self._processTypeDeclaration(name, _types, dim, isArray, sub_indices_vec, domains_with_indices)

            if _typeAux != EMPTY_STRING:
               includedType = True 
               _type = _typeAux

        if not includedType:
            _typeAux = self._inferTypeByIndexPositionInAnotherIdentifier(name)

            if _typeAux != EMPTY_STRING:
               includedType = True 
               _type = _typeAux
            
        if not includedType:
            _type = self._processTypeFromGenParameter(_genParameter)

        if _type in self.listSetOfInts:
            _type = INT
            
        if declaration != None:

            if declaration.getValue() != None:            
                value, _type, array, isArray, arrayFromTuple, deleteTupleIndex = self._processValueFromDeclaration(declaration, name, _type, value, dim, array, isArray, _subIndices, domains, domains_aux, domains_with_indices, stmtIndex)
            else:
                self._getRelationalConstraintsFromDeclaration(declaration, name, dim, isArray, _subIndices, domains_with_indices)

        if not _type or _type.strip() == EMPTY_STRING:
            _type = FLOAT

        if _type == SET_OF_INT:
            self.listSetOfInts.append(name)

        if array != EMPTY_STRING:
            paramStr += array
            
            self._deleteIndexSet(array, name)

        # remove { and } from type of the form {n..m}: resulting in n..m
        if _type[0] == BEGIN_SET and _type[-1] == END_SET and FROM_TO in _type:
            _type = _type[1:-1]

        if _type != ENUM:
            _type = _type+SEP_PARTS_DECLARATION

        if isArray:
            paramStr += SPACE + OF + SPACE + _type
        else:
            paramStr += _type

        paramStr += SPACE + name

        if value != EMPTY_STRING:
            paramStr += SPACE+ASSIGN+SPACE + value

        paramStr += END_STATEMENT+BREAKLINE+BREAKLINE

        return paramStr

    def _declareSet(self, _genSet):

        name = _genSet.getName()
        setStr = EMPTY_STRING
        declaration = self.genDeclarations.get(name)
        value = EMPTY_STRING
        isArray = False
        includedType = False
        array = EMPTY_STRING
        deleteTupleIndex = False
        arrayFromTuple = False

        domain, domains, domains_with_indices, dependencies_vec, sub_indices_vec, stmtIndex = self._getSubIndicesDomainsAndDependencies(name)
        _types, dim, minVal, maxVal = self._getProperties(_genSet.getName())
        
        _subIndices = self._getIndicesFromDeclaration(declaration, stmtIndex)
        
        domain, domains, domains_with_indices, domains_aux, arraySet, isArray = self._processDomain(domain, domains, domains_with_indices, dim, minVal, maxVal)
        array += arraySet

        if name in self.tuplesDeclared:
            isArray = True
            _tuple = self.tuplesDeclared[name]
            index1 = _tuple[INDEX1]
            index2 = _tuple[INDEX2]
            _type  = _tuple[TYPE]

            self.array2dIndex1 = index1
            self.array2dIndex2 = index2

        else:
            _type = ENUM

        if declaration != None:
            
            if not domain:
                domain, isArray, array = self._getDomainFromIndexingExpressionInDeclaration(domain, isArray, array, declaration, stmtIndex)

            _typeAux = self._processInDeclaration(name, declaration, isArray)
            
            if _typeAux != EMPTY_STRING:
               includedType = True
               _type = _typeAux

            if not includedType:

                _typeAux = self._processTypeDeclaration(name, _types, dim, isArray, sub_indices_vec, domains_with_indices)

                if _typeAux != EMPTY_STRING:
                   includedType = True 
                   _type = _typeAux

            if not includedType:
                _typeAux = self._inferTypeByIndexPositionInAnotherIdentifier(name)
                
                if _typeAux != EMPTY_STRING:
                   includedType = True 
                   _type = _typeAux

            if _type in self.listSetOfInts:
                _type = INT

            if declaration.getValue() != None:
                value, _type, array, isArray, arrayFromTuple, deleteTupleIndex = \
                    self._processValueFromDeclaration(declaration, name, _type, value, dim, array, isArray, _subIndices, domains, domains_aux, domains_with_indices, stmtIndex, True)
            else:
                self._getRelationalConstraintsFromDeclaration(declaration, name, dim, isArray, _subIndices, domains_with_indices)
                
        if name in self.tuplesDeclared:
            _tuple = self.tuplesDeclared[name]
            index1 = _tuple[INDEX1]

            if deleteTupleIndex:
                del self.additionalParameters[index1]

            else:
                index2 = _tuple[INDEX2]

                if _tuple[REALTYPE]:
                    _type  = _tuple[REALTYPE]

                if _type == ENUM:
                    _type = INT
                    _typeAux = INT + SEP_PARTS_DECLARATION
                else:
                    _typeAux = _type + SEP_PARTS_DECLARATION
                    
                arrayFromTuple = True
                array = ARRAY + BEGIN_ARRAY+index1
                
                if index2 != None:
                    array += COMMA+SPACE+index2
                    
                array += END_ARRAY+SPACE + OF + SPACE+_typeAux+SPACE + name
                
                self.array2dIndex1 = index1
                self.array2dIndex2 = index2
                
        if _type == SET_OF_INT and self._isSetForTuple(name):
            _type = INT

        if array != EMPTY_STRING and _type != ENUM:
            setStr += array
            
            self._deleteIndexSet(array, name)

        if not arrayFromTuple:
            if _type != ENUM:
                _typeAux = _type+SEP_PARTS_DECLARATION
            else:
                _typeAux = _type

            if setStr == EMPTY_STRING:
                setStr += _typeAux + SPACE + name
            else:
                setStr += SPACE + OF + SPACE + _typeAux + SPACE + name

        if value != EMPTY_STRING:
            setStr += SPACE+ASSIGN+SPACE + value

        self.array2dIndex1 = None
        self.array2dIndex2 = None
        
        if _type == ENUM:
            self.listEnums.append(name)

        elif _type == SET_OF_INT:
            self.listSetOfInts.append(name)
            
        setStr += END_STATEMENT+BREAKLINE+BREAKLINE
        
        return setStr

    def _declareSetsAndParams(self):
        paramSetStr = EMPTY_STRING

        for _genObj in self.genSets.getAll():
            paramSetStr += self._declareSet(_genObj)

        for _genObj in self.genParameters.getAll():
            paramSetStr += self._declareParam(_genObj)

        return paramSetStr

    def _declareDataParam(self, _genParameter):
        return EMPTY_STRING

    def _declareDataSet(self, _genSet):
        return EMPTY_STRING

    def _declareDataSetsAndParams(self):
        return EMPTY_STRING

    def _preModel(self):
        res = EMPTY_STRING

        setsAndParams = self._declareSetsAndParams()
        if setsAndParams != EMPTY_STRING:
            res += setsAndParams

        identifiers = self._declareVars()
        if identifiers != EMPTY_STRING:
            if res != EMPTY_STRING:
                res += BREAKLINE

            res += identifiers

        del_list = []
        for key in self.additionalParameters:
            if key in self.setsWitOperationsInv and not key in self.setsWitOperationsUsed:
                del_list.append(key)

        for d in del_list:
            del self.additionalParameters[d]

            index = INDEX_SET_+d
            if index in self.additionalParameters:
                del self.additionalParameters[index]

        if len(self.additionalParameters) > 0:
            res += EMPTY_STRING.join([self.additionalParameters[k] for k in sorted(self.additionalParameters)])

        if len(self.additionalConstraints) > 0:
            res += BREAKLINE + (BREAKLINE+BREAKLINE).join(self.additionalConstraints) + BREAKLINE

        return res
        
    def _posModel(self):
        return EMPTY_STRING

    def generateCode_Main(self, node):
        return node.problem.generateCode(self)

    def generateCode_LinearEquations(self, node):

        constraints = filter(lambda el: isinstance(el, Constraint) or isinstance(el, TestOperationExpression) or \
                                isinstance(el, PredicateExpression) or isinstance(el, LetExpression) or \
                                isinstance(el, FunctionExpression), node.constraints.getConstraints())
        objectives = filter(lambda el: isinstance(el, Objective), node.constraints.getConstraints())

        preModel = self._preModel()
        if preModel != EMPTY_STRING:
            preModel += BREAKLINE

        # check libraries to include
        if len(self.include) > 0:
            preModel += (BREAKLINE+BREAKLINE).join([INCLUDE+" \"" + lb + "\""+END_STATEMENT for (k,lb) in self.include.iteritems()])
            preModel += BREAKLINE+BREAKLINE

        res = (BREAKLINE+BREAKLINE).join(filter(lambda cnt: self.removeInvalidConstraint(cnt), map(lambda el: self._getCodeConstraint(el), constraints))) + BREAKLINE+BREAKLINE

        if len(objectives) > 0:
            obj = objectives[0]
            res += BREAKLINE+BREAKLINE + self._getObjectiveCode(obj) + BREAKLINE+BREAKLINE
        else:
            res += SOLVE+SPACE+SATISFY+END_STATEMENT+BREAKLINE+BREAKLINE

        res = preModel + res

        return res

    def generateCode_LinearProgram(self, node):

        res = EMPTY_STRING

        preModel = self._preModel()
        if preModel != EMPTY_STRING:
            preModel += BREAKLINE

        if node.constraints:
            res += node.constraints.generateCode(self) + BREAKLINE+BREAKLINE
        
        res += BREAKLINE+BREAKLINE + node.objectives.generateCode(self) + BREAKLINE+BREAKLINE

        res = preModel + res

        return res

    # Declarations
    def generateCode_Declarations(self, node):

        declarations = map(lambda el: el.generateCode(self), node.declarations)
        res = (BREAKLINE+BREAKLINE).join(declarations) + BREAKLINE+BREAKLINE

        return res

    def generateCode_Declaration(self, node):
        res = node.declarationExpression.generateCode(self)

        if node.indexingExpression:
            res += BEGIN_SET+ node.indexingExpression.generateCode(self) +END_SET

        return res

    def generateCode_DeclarationExpression(self, node):
        identifiers = []
        for identifier in node.identifiers:
            identifiers.append(identifier.generateCode(self))

        res = (COMMA+SPACE).join(identifiers)

        if node.attributeList and len(node.attributeList) > 0:
            attr = map(lambda el: el.generateCode(self), node.attributeList)
            res += BREAKLINE + (COMMA+SPACE).join(attr)

        return res

    def generateCode_DeclarationAttribute(self, node):
        return node.attribute.generateCode(self)

    # Objectives
    def generateCode_Objectives(self, node):
        obj = node.objectives[0]
        objStr = self._getObjectiveCode(obj)

        return objStr;

    def _getObjectiveCode(self, obj):
        objStr = SOLVE+SPACE + obj.type + SPACE+ obj.linearExpression.generateCode(self) +END_STATEMENT+BREAKLINE+BREAKLINE;

        return objStr;

    # Objective Function
    def generateCode_Objective(self, node):
        """
        Generate the code in MiniZinc for this Objective
        """
        res = self._getObjectiveCode(node)

        return res

    # Constraints
    def generateCode_Constraints(self, node):
        return (BREAKLINE+BREAKLINE).join(filter(lambda el: self.removeInvalidConstraint(el), map(self._getCodeConstraint, node.constraints)))

    def generateCode_Constraint(self, node):
        res = EMPTY_STRING

        if self.isLetExpressionArgument:
            res += CONSTRAINT + SPACE

        hasForall = False

        if node.indexingExpression:
            idxExpression = node.indexingExpression.generateCode(self)

            if idxExpression.strip() != EMPTY_STRING:
                res += FORALL+BEGIN_ARGUMENT_LIST + idxExpression + END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST
                hasForall = True

        res += node.constraintExpression.generateCode(self) + (END_ARGUMENT_LIST if hasForall else EMPTY_STRING)

        if not self.isLetExpressionArgument and not self.isConstraintInLetExpression and not self.isWithinOtherExpression:
            res += END_STATEMENT
        
        return res

    def generateCode_ConstraintExpression2(self, node):
        return node.linearExpression1.generateCode(self) + SPACE + node.op + SPACE + node.linearExpression2.generateCode(self)

    def generateCode_ConstraintExpression3(self, node):

        if node.op == ConstraintExpression.LE:
            oppOp = ConstraintExpression.GE
        else:
            oppOp = ConstraintExpression.LE

        res  = node.linearExpression.generateCode(self) + SPACE + node.op + SPACE + node.numericExpression2.generateCode(self) + SPACE+AND+SPACE
        res += node.linearExpression.generateCode(self) + SPACE + oppOp + SPACE + node.numericExpression1.generateCode(self)

        return res

    def generateCode_LogicalConstraintExpression(self, node):
        res = node.logicalExpression.generateCode(self) + SPACE + node.op + SPACE + node.constraintExpression1.generateCode(self)
        
        if node.constraintExpression2:
            res += SPACE+ELSE+SPACE + node.constraintExpression2.generateCode(self)

        return res

    def generateCode_ConditionalConstraintExpression(self, node):

        res = IF+SPACE + node.logicalExpression.generateCode(self) + SPACE+THEN+SPACE + node.constraintExpression1.generateCode(self)

        if node.constraintExpression2:
            res += SPACE+ELSE+SPACE + node.constraintExpression2.generateCode(self)

        else:
            res += SPACE+ELSE+SPACE+TRUE

        res += SPACE+ENDIF

        return res


    # Linear Expression
    def generateCode_ValuedLinearExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_LinearExpressionBetweenParenthesis(self, node):
        res = BEGIN_ARGUMENT_LIST + node.linearExpression.generateCode(self) + END_ARGUMENT_LIST

        return res

    def generateCode_LinearExpressionWithArithmeticOperation(self, node):
        return node.expression1.generateCode(self) + SPACE + node.op + SPACE + node.expression2.generateCode(self)

    def generateCode_MinusLinearExpression(self, node):
        return MINUS + node.linearExpression.generateCode(self)

    def generateCode_IteratedLinearExpression(self, node):

        self.isWithinOtherExpression = True

        indexingExpression = node.indexingExpression.generateCode(self)
        if isinstance(node.indexingExpression, NumericExpressionWithArithmeticOperation) and not self._hasVariable(node.indexingExpression):
            indexingExpression = FLOOR+BEGIN_ARGUMENT_LIST + indexingExpression + END_ARGUMENT_LIST
            
        if node.numericExpression:
            numericExpression = node.numericExpression.generateCode(self)
            if isinstance(node.numericExpression, NumericExpressionWithArithmeticOperation) and not self._hasVariable(node.numericExpression):
                numericExpression = FLOOR+BEGIN_ARGUMENT_LIST + numericExpression + END_ARGUMENT_LIST
            else:
                numericExpression = BEGIN_ARGUMENT_LIST + numericExpression + END_ARGUMENT_LIST
                
            res = SUM + BEGIN_ARGUMENT_LIST + indexingExpression + FROM_TO + numericExpression + END_ARGUMENT_LIST+END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST
        else:
            res = SUM + BEGIN_ARGUMENT_LIST + indexingExpression + END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST

        res += node.linearExpression.generateCode(self) + END_ARGUMENT_LIST

        self.isWithinOtherExpression = False

        return res

    def generateCode_ConditionalLinearExpression(self, node):

        res = IF+SPACE + node.logicalExpression.generateCode(self)

        if node.linearExpression1:
            res += SPACE+THEN+SPACE + node.linearExpression1.generateCode(self)

            if node.linearExpression2:
                res += SPACE+ELSE+SPACE + node.linearExpression2.generateCode(self)

            res += SPACE+ENDIF

        return res

    def _getNumericFunction(self, function):
        if function == NumericExpressionWithFunction.LOG:
            function = LN
        elif function == TRUNC:
            function = NumericExpressionWithFunction.FLOOR

        return function

    # True or False Expression
    def generateCode_TrueFalse(self, node):
        return node.value

    # LetExpression
    def generateCode_LetExpression(self, node):
        
        self.isLetExpression = True
        self.isLetExpressionArgument = True
        arguments = node.preparedArguments.generateCode(self)
        self.isLetExpressionArgument = False
        
        
        self.isConstraintInLetExpression = True
        res = LET + SPACE + BEGIN_SET + arguments + END_SET + SPACE + IN + \
                BREAKLINE + TAB + node.expression.generateCode(self)
        self.isConstraintInLetExpression = False

        self.isLetExpression = False

        #if self.isConstraint and not isinstance(node.expression, LetExpression):
        #    res += END_STATEMENT

        return res

    # PredicateExpression
    def generateCode_PredicateExpression(self, node):
        res = PREDICATE + SPACE + node.name.generateCode(self) + BEGIN_ARGUMENT_LIST + node.preparedArguments.generateCode(self) + END_ARGUMENT_LIST

        if node.expression:
            res += SPACE + EQUAL + BREAKLINE + TAB + node.expression.generateCode(self)

        res += END_STATEMENT

        return res

    # TestOperationExpression
    def generateCode_TestOperationExpression(self, node):
        res = TEST + SPACE + node.name.generateCode(self) + BEGIN_ARGUMENT_LIST + node.preparedArguments.generateCode(self) + END_ARGUMENT_LIST
        
        if node.expression:
            res += SPACE + EQUAL + BREAKLINE + TAB + node.expression.generateCode(self)

        res += END_STATEMENT

        return res

    # FunctionExpression
    def generateCode_FunctionExpression(self, node):
        var = VAR + SPACE if node.typeIsVariable else EMPTY_STRING
        _type = FLOAT if isinstance(node.type, RealSet) else node.type.generateCode(self)

        res = FUNCTION + SPACE + var + _type + SEP_PARTS_DECLARATION + SPACE + node.name.generateCode(self) + BEGIN_ARGUMENT_LIST + node.preparedArguments.generateCode(self) + END_ARGUMENT_LIST
        
        if node.expression:
            res += SPACE + EQUAL + BREAKLINE + TAB + node.expression.generateCode(self)

        res += END_STATEMENT

        return res

    # Arguments
    def generateCode_Arguments(self, node):
        if self.isLetExpression:
            sep = END_STATEMENT
        else:
            sep = COMMA

        self.extraConstraints = []
        res = (sep+SPACE).join(map(lambda el: el.generateCode(self), node.arguments))

        if len(self.extraConstraints) > 0:
            res += sep + SPACE + (sep+SPACE).join(self.extraConstraints)

        self.extraConstraints = []

        return res

    def _getArgument(self, node, name):
        res = EMPTY_STRING

        if name.sub_indices and len(name.sub_indices) > 0:
            domains = []
            inExpressions = []
            idxParts = None
            logicalExpression = None

            if node.indexingExpression:
                inExpressions = filter(lambda el: (isinstance(el, EntryIndexingExpressionWithSet) and el.op == EntryIndexingExpressionWithSet.IN) or\
                    (isinstance(el, EntryIndexingExpressionEq) and el.op == EntryIndexingExpressionEq.EQ), node.indexingExpression.entriesIndexingExpression)

                if self.isLetExpression:
                    otherExpressions = filter(lambda el: not ((isinstance(el, EntryIndexingExpressionWithSet) and el.op == EntryIndexingExpressionWithSet.IN) or\
                        (isinstance(el, EntryIndexingExpressionEq) and el.op == EntryIndexingExpressionEq.EQ)), node.indexingExpression.entriesIndexingExpression)

                    if len(otherExpressions) > 0:
                        for otherExpression in otherExpressions:
                            extraConstraint = otherExpression.generateCode(self)

                            if not extraConstraint in self.extraConstraints:
                                self.extraConstraints.append(extraConstraint)

                    if node.indexingExpression.logicalExpression:
                        extraConstraint = node.indexingExpression.logicalExpression.generateCode(self)

                        if not extraConstraint in self.extraConstraints:
                            self.extraConstraints.append(extraConstraint)

            for idx in name.sub_indices:
                foundDomain = False

                if len(inExpressions) > 0:
                    subIdx = idx.generateCode(self)

                    for inExpression in inExpressions:

                        if subIdx == inExpression.identifier.generateCode(self):

                            foundDomain = True

                            if isinstance(inExpression, EntryIndexingExpressionWithSet):
                                domains.append(inExpression.setExpression.generateCode(self))
                            else:
                                setExpression = inExpression.value.generateCode(self)

                                if inExpression.supExpression:
                                    setExpression += FROM_TO + inExpression.supExpression.generateCode(self)

                                domains.append(setExpression)

                            break

                if not foundDomain:
                    domains.append(INT)

            res += ARRAY + BEGIN_ARRAY + (COMMA+SPACE).join(domains) + END_ARRAY + SPACE + OF + SPACE

        res += node.argumentType.generateCode(self)
        res += SEP_PARTS_DECLARATION + SPACE


        res += name.generateCodeWithoutIndices(self)

        if node.expression:
            res += SPACE + EQUAL + SPACE + node.expression.generateCode(self)

        return res

    # Argument
    def generateCode_Argument(self, node):
        if self.isLetExpression:
            sep = END_STATEMENT
        else:
            sep = COMMA

        return (sep+SPACE).join(map(lambda name: self._getArgument(node, name), node.names.values))

    # ArgumentType
    def generateCode_ArgumentType(self, node):
        var = VAR + SPACE if node.isVariable else EMPTY_STRING
        _type = FLOAT if isinstance(node.type, SetExpressionWithValue) and \
                         isinstance(node.type.value, RealSet) else node.type.generateCode(self)

        return var + _type

    # Numeric Expression
    def generateCode_NumericExpressionWithFunction(self, node):
        if not isinstance(node.function, str):
            function = node.function.generateCode(self)
        else:
            function = node.function

        function = self._getNumericFunction(function)

        res = function + BEGIN_ARGUMENT_LIST

        if node.numericExpression1 != None:
            numericExpression1 = node.numericExpression1.generateCode(self)
            
            if function == NumericExpressionWithFunction.CARD and numericExpression1 in self.tuplesDeclared:
                _tuple = self.tuplesDeclared[numericExpression1]
                numericExpression1 = _tuple[INDEX1]

            res += numericExpression1

        if node.numericExpression2 != None:
            if function == NumericExpressionWithFunction.ATAN:
                res += DIV
            else:
                res += COMMA+SPACE

            res += node.numericExpression2.generateCode(self)

        res += END_ARGUMENT_LIST

        return res

    def generateCode_FractionalNumericExpression(self, node):
        
        numerator = node.numerator
        if isinstance(node.numerator, ValuedNumericExpression):
            numerator = numerator.value
            
        if not isinstance(numerator, Identifier) and not isinstance(numerator, Number) and not isinstance(numerator, NumericExpressionWithFunction):
            numerator = BEGIN_ARGUMENT_LIST+numerator.generateCode(self)+END_ARGUMENT_LIST
        else:
            numerator = numerator.generateCode(self)
            
        denominator = node.denominator
        if isinstance(denominator, ValuedNumericExpression):
            denominator = denominator.value
            
        if not isinstance(denominator, Identifier) and not isinstance(denominator, Number) and not isinstance(denominator, NumericExpressionWithFunction):
            denominator = BEGIN_ARGUMENT_LIST+denominator.generateCode(self)+END_ARGUMENT_LIST
        else:
            denominator = denominator.generateCode(self)
            
        return numerator+DIV+denominator

    def generateCode_ValuedNumericExpression(self, node):
        self.turnStringsIntoInts = True
        res = node.value.generateCode(self)
        self.turnStringsIntoInts = False
        return res

    def generateCode_NumericExpressionBetweenParenthesis(self, node):
        res = BEGIN_ARGUMENT_LIST + node.numericExpression.generateCode(self) + END_ARGUMENT_LIST

        return res

    def generateCode_NumericExpressionWithArithmeticOperation(self, node):
        res = EMPTY_STRING
        
        numericExpression1 = node.numericExpression1
        if isinstance(numericExpression1, ValuedNumericExpression):
            numericExpression1 = numericExpression1.value
            
        numericExpression2 = node.numericExpression2
        if isinstance(numericExpression2, ValuedNumericExpression):
            numericExpression2 = numericExpression2.value
            
        numericExpressionStr1 = node.numericExpression1.generateCode(self)
        numericExpressionStr2 = node.numericExpression2.generateCode(self)
        
        if node.op == NumericExpressionWithArithmeticOperation.POW:# and not (isinstance(node.numericExpression2, ValuedNumericExpression) or isinstance(node.numericExpression2, NumericExpressionBetweenParenthesis)):
            res += POW+BEGIN_ARGUMENT_LIST + numericExpressionStr1 + COMMA + numericExpressionStr2 + END_ARGUMENT_LIST
            
        elif node.op == NumericExpressionWithArithmeticOperation.QUOT or node.op == NumericExpressionWithArithmeticOperation.MOD:
            
            if not isinstance(numericExpression1, Identifier) and not isinstance(numericExpression1, Number) and not self._hasVariable(numericExpression1):
                numericExpressionStr1 = FLOOR+BEGIN_ARGUMENT_LIST + numericExpressionStr1 + END_ARGUMENT_LIST
                
            if not isinstance(numericExpression2, Identifier) and not isinstance(numericExpression2, Number) and not self._hasVariable(numericExpression2):
                numericExpressionStr2 = FLOOR+BEGIN_ARGUMENT_LIST + numericExpressionStr2 + END_ARGUMENT_LIST
                
            res += numericExpressionStr1 + SPACE + node.op + SPACE + numericExpressionStr2
            
        else:
            res += numericExpressionStr1 + SPACE + node.op + SPACE + numericExpressionStr2
            
        return res
        
    def generateCode_MinusNumericExpression(self, node):
        return MINUS + node.numericExpression.generateCode(self)

    def generateCode_IteratedNumericExpression(self, node):

        indexingExpression = node.indexingExpression.generateCode(self)
        if isinstance(node.indexingExpression, NumericExpressionWithArithmeticOperation) and not self._hasVariable(node.indexingExpression):
            indexingExpression = FLOOR+BEGIN_ARGUMENT_LIST + indexingExpression + END_ARGUMENT_LIST

        if node.supNumericExpression:
            supNumericExpression = node.supNumericExpression.generateCode(self)
            if isinstance(node.supNumericExpression, NumericExpressionWithArithmeticOperation) and not self._hasVariable(node.supNumericExpression):
                supNumericExpression = FLOOR+BEGIN_ARGUMENT_LIST + supNumericExpression + END_ARGUMENT_LIST
            else:
                supNumericExpression = BEGIN_ARGUMENT_LIST + supNumericExpression + END_ARGUMENT_LIST

            res = str(node.op) + BEGIN_ARGUMENT_LIST + indexingExpression + FROM_TO + supNumericExpression + END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST
        else:
            res = str(node.op) + BEGIN_ARGUMENT_LIST + indexingExpression + END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST

        res += node.numericExpression.generateCode(self) + END_ARGUMENT_LIST

        return res

    def generateCode_ConditionalNumericExpression(self, node):

        res = IF+SPACE + node.logicalExpression.generateCode(self) + SPACE+THEN+SPACE + node.numericExpression1.generateCode(self)

        if node.numericExpression2:
            res += SPACE+ELSE+SPACE + node.numericExpression2.generateCode(self)

        else:
            res += SPACE+ELSE+SPACE+ZERO

        res += SPACE+ENDIF

        return res

    # Symbolic Expression

    def generateCode_StringSymbolicExpression(self, node):
        return node.value.generateCode(self)

    def generateCode_SymbolicExpressionBetweenParenthesis(self, node):
        res = BEGIN_ARGUMENT_LIST + node.symbolicExpression.generateCode(self) + END_ARGUMENT_LIST
        return res

    def generateCode_SymbolicExpressionWithOperation(self, node):
        return node.symbolicExpression1.generateCode(self) + SPACE + node.op + SPACE + node.symbolicExpression2.generateCode(self)


    # Expression List
    def generateCode_ExpressionList(self, node):

        indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, node.entriesIndexingExpression))
        res = (COMMA+SPACE).join(indexing)

        if self.array2dIndex2 != None:
            res += COMMA+SPACE+"idx2"+SPACE+IN+SPACE + self.array2dIndex2

        if node.logicalExpression:
            res += SPACE+SUCH_THAT+SPACE + node.logicalExpression.generateCode(self)

        if node.getSymbolTable():

            stmtIndex = node.getSymbolTable().getStatement()
            scope = node.getSymbolTable().getScope()

            if stmtIndex in self.scopes and scope in self.scopes[stmtIndex]:

                if NEWENTRYLOGICALEXPRESSION in self.scopes[stmtIndex][scope] and len(self.scopes[stmtIndex][scope][NEWENTRYLOGICALEXPRESSION]) > 0:
                    if not node.logicalExpression:
                        res += SPACE+WHERE+SPACE
                    else:
                        res += SPACE+AND+SPACE

                    entries = (SPACE+AND+SPACE).join(self.scopes[stmtIndex][scope][NEWENTRYLOGICALEXPRESSION])

                    res += entries

        return res

    # Indexing Expression
    def generateCode_IndexingExpression(self, node):

        indexing = filter(Utils._deleteEmpty, map(self._getCodeEntry, node.entriesIndexingExpression))
        res = (COMMA+SPACE).join(indexing)

        if self.array2dIndex2 != None:
            res += COMMA+SPACE+"idx2"+SPACE+IN+SPACE + self.array2dIndex2

        if node.logicalExpression:
            res += SPACE+WHERE+SPACE + node.logicalExpression.generateCode(self)

            if node.logicalExpression.getSymbolTable():
                stmtIndex = node.logicalExpression.getSymbolTable().getStatement()
                scope = node.logicalExpression.getSymbolTable().getScope()

        if node.getSymbolTable():
            stmtIndex = node.getSymbolTable().getStatement()
            scope = node.getSymbolTable().getScope()

            if stmtIndex in self.scopes and scope in self.scopes[stmtIndex]:
                if NEWENTRYLOGICALEXPRESSION in self.scopes[stmtIndex][scope] and len(self.scopes[stmtIndex][scope][NEWENTRYLOGICALEXPRESSION]) > 0:
                    if not node.logicalExpression:
                        res += SPACE+WHERE+SPACE
                    else:
                        res += SPACE+AND+SPACE

                    entries = (SPACE+AND+SPACE).join(self.scopes[stmtIndex][scope][NEWENTRYLOGICALEXPRESSION])

                    res += entries

        return res
        
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

                setExpression = self._getSetExpression(node)
                varList = COMMA.join(entries)
                res = NOT+BEGIN_ARGUMENT_LIST + varList + SPACE+IN+SPACE + setExpression + END_ARGUMENT_LIST if node.op == EntryIndexingExpressionWithSet.NOTIN else \
                               varList + SPACE + node.op + SPACE + setExpression

                return res

        elif isinstance(node.identifier, Tuple) or isinstance(node.identifier, TupleList):
            setExpression = self._getSetExpression(node)

            if not self.getOriginalIndices and setExpression in self.tuplesDeclared:

                index1 = self.tuplesDeclared[setExpression][INDEX1]
                values = node.identifier.getValues()

                self.replaceNewIndices = False
                idx = values[0].generateCode(self)
                self.replaceNewIndices = True
                
                return idx + SPACE + node.op + SPACE + index1

            else:
                ident = node.identifier.generateCode(self)
                return ident + SPACE + node.op + SPACE + setExpression

        elif self.notInTypesThatAreNotDeclarable(node.identifier):
            ident = node.identifier.generateCode(self)
            setExpression = self._getSetExpression(node)
            res = ident + SPACE + node.op + SPACE + setExpression

            return res

        return EMPTY_STRING

    def generateCode_EntryIndexingExpressionCmp(self, node):
        self.turnStringsIntoInts = True

        if node.op == EntryIndexingExpressionCmp.NEQ:
            op = NEQ
        else:
            op = node.op

        res = node.identifier.generateCode(self) + SPACE + op + SPACE + node.numericExpression.generateCode(self)

        self.turnStringsIntoInts = False

        return res

    def generateCode_EntryIndexingExpressionEq(self, node):
        self.turnStringsIntoInts = True

        if node.hasSup:
            res = node.identifier.generateCode(self) + SPACE+IN+SPACE + Utils._getInt(node.value.generateCode(self)) # completed in generateCode_IteratedNumericExpression

        elif isinstance(node.value, Array):
            res = node.identifier.generateCode(self) + SPACE+IN+SPACE+BEGIN_SET + node.value.value.generateCode(self) + END_SET

        else:
            res = node.identifier.generateCode(self) + SPACE+IN+SPACE + node.value.generateCode(self)

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
                    res += SPACE + conj + SPACE + code

        return res

    # Entry Logical Expression
    def generateCode_EntryLogicalExpressionRelational(self, node):
        self.turnStringsIntoInts = True
        if node.op == EntryLogicalExpressionRelational.NEQ:
            op = NEQ
        else:
            op = node.op


        res = node.numericExpression1.generateCode(self) + SPACE + op + SPACE + node.numericExpression2.generateCode(self)
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

                setExpression = self._getSetExpression(node)
                res = (SPACE+AND+SPACE).join(map(lambda var: NOT+BEGIN_ARGUMENT_LIST + var + SPACE+IN+SPACE + setExpression + END_ARGUMENT_LIST if node.op == EntryLogicalExpressionWithSet.NOTIN else \
                                                var + SPACE + node.op + SPACE + setExpression, entries))

                return res

        elif isinstance(node.identifier, Tuple) or isinstance(node.identifier, TupleList):
            setExpression = self._getSetExpression(node)

            if not self.getOriginalIndices and setExpression in self.tuplesDeclared:
                index1 = self.tuplesDeclared[setExpression][INDEX1]
                values = node.identifier.getValues()
                idx = values[0].generateCode(self)

                return idx + SPACE + node.op + SPACE + index1

            else:
                ident = node.identifier.generateCode(self)
                return ident + SPACE + node.op + SPACE + setExpression
                
        elif self.notInTypesThatAreNotDeclarable(node.identifier):
            ident = node.identifier.generateCode(self)
            setExpression = self._getSetExpression(node)
            res = ident + SPACE + node.op + SPACE + setExpression
            
            return res

        return EMPTY_STRING

    def generateCode_EntryLogicalExpressionWithSetOperation(self, node):
        return node.setExpression1.generateCode(self) + SPACE + node.op + SPACE + node.setExpression2.generateCode(self)

    def generateCode_EntryLogicalExpressionIterated(self, node):
        res =  node.op + BEGIN_ARGUMENT_LIST + node.indexingExpression.generateCode(self) + END_ARGUMENT_LIST+BEGIN_ARGUMENT_LIST +  node.logicalExpression.generateCode(self) + END_ARGUMENT_LIST
        return res

    def generateCode_EntryLogicalExpressionBetweenParenthesis(self, node):
        res = BEGIN_ARGUMENT_LIST + node.logicalExpression.generateCode(self) + END_ARGUMENT_LIST
        return res

    def generateCode_EntryLogicalExpressionNot(self, node):
        return NOT+SPACE + node.logicalExpression.generateCode(self)

    def generateCode_EntryLogicalExpressionNumericOrSymbolic(self, node):
        if isinstance(node.numericOrSymbolicExpression, SymbolicExpression) or isinstance(node.numericOrSymbolicExpression, Identifier):
            return node.numericOrSymbolicExpression.generateCode(self) + SPACE+EQUAL+SPACE+TRUE

        return node.numericOrSymbolicExpression.generateCode(self)

    # Set Expression
    def generateCode_SetExpressionWithValue(self, node):
        if not isinstance(node.value, str):
            return node.value.generateCode(self)
        else:
            return node.value

    def generateCode_SetExpressionWithIndices(self, node):
        self.isSetExpressionWithIndices = True

        var_gen = EMPTY_STRING
        if not isinstance(node.identifier, str):
            var_gen = node.identifier.generateCode(self)
        else:
            var_gen = node.identifier

        self.isSetExpressionWithIndices = False

        return  var_gen

    def generateCode_SetExpressionWithOperation(self, node):
        return node.setExpression1.generateCode(self) + SPACE + node.op + SPACE + node.setExpression2.generateCode(self)

    def generateCode_SetExpressionBetweenBraces(self, node):
        isRange = False

        if node.setExpression != None:
            self.turnStringsIntoInts = True

            if isinstance(node.setExpression, SetExpressionWithValue):
                setExpression = node.setExpression.value
            else:
                setExpression = node.setExpression

            if isinstance(setExpression, Range):
                isRange = True

            setExpression = setExpression.generateCode(self)

            self.turnStringsIntoInts = False

        else:
            setExpression = EMPTY_STRING

        if not isRange:
            setExpression = BEGIN_SET + setExpression + END_SET

        return setExpression

    def generateCode_SetExpressionBetweenParenthesis(self, node):
        res =  BEGIN_ARGUMENT_LIST + node.setExpression.generateCode(self) + END_ARGUMENT_LIST
        return res

    def generateCode_IteratedSetExpression(self, node):
        if node.indexingExpression:
            integrand_str = EMPTY_STRING
            indexingExpression = node.indexingExpression.generateCode(self)

        else:
            integrand_str = SET + SPACE + OF + SPACE
            indexingExpression = None

        isArray2d = False
        if node.integrand != None:
            if not isinstance(node.integrand, Tuple):
                integrand_str += node.integrand.generateCode(self)

            elif self.array2dIndex1 != None and self.array2dIndex2 != None:
                isArray2d = True
                integrand = node.integrand.getValues()

                size = len(integrand)
                integrand_str += ARRAY + "2d"+BEGIN_ARGUMENT_LIST+self.array2dIndex1+COMMA+SPACE+self.array2dIndex2+COMMA+SPACE+BEGIN_ARRAY+IF+SPACE+"idx2"+SPACE+EQUAL+SPACE+"1"+SPACE+THEN+SPACE + integrand[0].generateCode(self)

                for i in range(1,size-1):
                    integrand_str += SPACE+ELSEIF+SPACE+"idx2"+SPACE+EQUAL+SPACE + str(i+1) + SPACE+THEN+SPACE + integrand[0].generateCode(self)

                integrand_str += SPACE+ELSE+SPACE + integrand[size-1].generateCode(self) + SPACE+ENDIF+SPACE

        res = EMPTY_STRING

        if indexingExpression and not isArray2d:
            res += BEGIN_ARRAY

        res += integrand_str

        if indexingExpression:
            res += SUCH_THAT+SPACE + indexingExpression + END_ARRAY

        if isArray2d:
            res += END_ARGUMENT_LIST

        if self.stmtIndex > -1:
            self.parentScope = previousParentScope

        return res

    def generateCode_ConditionalSetExpression(self, node):
        res = IF+SPACE + node.logicalExpression.generateCode(self) + SPACE+THEN+SPACE + node.setExpression1.generateCode(self)

        if node.setExpression2:
            res += SPACE+ELSE+SPACE + node.setExpression2.generateCode(self)

        else:
            res += SPACE+ELSE+SPACE+BEGIN_SET+END_SET

        res += SPACE+ENDIF

        return res

    # Range
    def generateCode_Range(self, node):

        initValue = node.rangeInit.generateCode(self)
        endValue = node.rangeEnd.generateCode(self)

        if isinstance(node.rangeInit, NumericExpressionWithArithmeticOperation) and not self._hasVariable(node.rangeInit):
            initValue = FLOOR+BEGIN_ARGUMENT_LIST+initValue+END_ARGUMENT_LIST

        if isinstance(node.rangeEnd, NumericExpressionWithArithmeticOperation) and not self._hasVariable(node.rangeEnd):
            endValue = FLOOR+BEGIN_ARGUMENT_LIST+endValue+END_ARGUMENT_LIST

        res = initValue + FROM_TO + endValue

        return res

    # Value List
    def generateCode_ValueList(self, node):
        return COMMA.join(map(self._getCodeValue, node.values))

    # Identifier List
    def generateCode_IdentifierList(self, node):
        return COMMA.join(map(self._getCodeValue, node.identifiers))

    # Tuple
    def generateCode_Tuple(self, node):
        return BEGIN_ARGUMENT_LIST + COMMA.join(map(self._getCodeValue, node.values)) + END_ARGUMENT_LIST

    # Tuple List
    def generateCode_TupleList(self, node):
        return COMMA.join(map(self._getCodeValue, node.values))

    # Array
    def generateCode_Array(self, node):
        return BEGIN_ARRAY + COMMA.join(map(self._getCodeValue, node.value)) + END_ARRAY

    # Array with operation
    def generateCode_ArrayWithOperation(self, node):
        return node.array1.generateCode(self) + SPACE + node.op + SPACE + node.array2.generateCode(self)

    # ArrayChoose
    def generateCode_ArrayChoose(self, node):
        return BEGIN_ARRAY + COMMA.join(map(self._getCodeValue, node.value1)) + END_ARRAY+BEGIN_ARRAY + COMMA.join(map(self._getCodeValue, node.value2)) + END_ARRAY

    # Value
    def generateCode_Value(self, node):
        return node.value.generateCode(self)

    # Identifier
    def generateCode_Identifier(self, node):
        if isinstance(node.sub_indices, str):
            return EMPTY_STRING
            
        length_sub_indices = len(node.sub_indices)
        
        if length_sub_indices > 0:
            
            ident = node.identifier.generateCode(self)
            if self.isSetExpressionWithIndices:
                res = ident
                
            else:

                self.countIndicesProcessed += 1
                identProcessing = ident+str(self.countIndicesProcessed)

                self.parentIdentifier = ident
                self.turnStringsIntoInts = True

                if isinstance(node.sub_indices, list):

                    res = ident + BEGIN_ARRAY
                    
                    self.posId[identProcessing] = 0
                    for ind in node.sub_indices:
                        if self.posId[identProcessing] > 0:
                            res += COMMA

                        self.identProcessing = identProcessing

                        self.turnStringsIntoInts = True
                        ind = ind.generateCode(self)
                        self.turnStringsIntoInts = False

                        if self.generateAssertExpression:
                            ind = "\\("+ind+")"

                        res += ind

                        self.posId[identProcessing] += 1
                        
                    res += END_ARRAY
                    del self.posId[identProcessing]

                else:

                    self.identProcessing = identProcessing

                    inds = []
                    res = ident + BEGIN_ARRAY

                    for ind in node.sub_indices:
                        self.turnStringsIntoInts = True
                        ind = self._getCodeID(ind)
                        self.turnStringsIntoInts = False

                        if self.generateAssertExpression:
                            ind = "\\("+ind+")"

                        inds.append(ind)

                    res += COMMA.join(inds) + END_ARRAY

                self.turnStringsIntoInts = False
                self.parentIdentifier = None
                self.identProcessing = None
        
        else:
            res = node.identifier.generateCode(self)
        
        return res

    # Number
    def generateCode_Number(self, node):
        return self.formatNumber(node.number)

    def _getNewIndex(self, ident, symbolTable):
        stmt  = symbolTable.getStatement()
        scope = symbolTable.getScope()

        while scope >= 0:
            if not stmt in self.scopes:
                return None

            if not scope in self.scopes[stmt]:
                return None

            if NEW_INDICES in self.scopes[stmt][scope]:
                if ident in self.scopes[stmt][scope][NEW_INDICES]:
                    new_index = self.scopes[stmt][scope][NEW_INDICES][ident]
                    replaced = True

                    if TO_ENUM + "('"+REALTYPE+"'" in new_index:
                        replaced = False

                        if self.parentIdentifier != None and self.identProcessing != None and self.identProcessing in self.posId:

                            domain = self._getDomainByIdentifier(self.parentIdentifier)
                            
                            if domain != None and domain.strip() != EMPTY_STRING:
                                domains = []
                                domains_aux = Utils._splitDomain(domain, COMMA)
                                
                                for domain in domains_aux:
                                    if domain in self.tuplesDeclared:
                                        dimen  = self.tuplesDeclared[domain][DIMEN]
                                        domain = self.tuplesDeclared[domain][TYPE]
                                        
                                        for i in range(dimen):
                                            domains.append(domain)

                                    else:
                                        domains.append(domain)

                                if len(domains) > 0:
                                    
                                    if self.posId[self.identProcessing] < len(domains):
                                        domain = domains[self.posId[self.identProcessing]]

                                        if domain != INT and domain in self.listEnums:
                                            new_index = new_index.replace("'"+REALTYPE+"'", domain)
                                            replaced = True

                    if not replaced:
                        new_index = ident

                    return new_index

            if not symbolTable.getParent():
                scope = -1
            else:
                scope = symbolTable.getParent().getScope()
                
                if scope == None:
                    scope = -1

            symbolTable = symbolTable.getParent()

        return None 

    def _setNewIndex(self, ident, stmt, scope):
        if not stmt in self.scopes:
            self.scopes[stmt] = {}

        if not scope in self.scopes[stmt]:
            self.scopes[stmt][scope] = {}

        if not NEW_INDICES in self.scopes[stmt][scope]:
            self.scopes[stmt][scope][NEW_INDICES] = {}

        if not ident in self.scopes[stmt][scope][NEW_INDICES]:
            self.scopes[stmt][scope][NEW_INDICES][ident] = self.newIndexExpression
            self.countNewIndices += 1

        else:
            newIndex = self.scopes[stmt][scope][NEW_INDICES][ident]
            if newIndex == INT and self.newIndexExpression != INT:
                self.scopes[stmt][scope][NEW_INDICES][ident] = self.newIndexExpression
                self.countNewIndices += 1

    # ID
    def generateCode_ID(self, node):
        ident = node.value

        if self.removeAdditionalParameter:
            if ident in self.additionalParameters:
                del self.additionalParameters[ident]

        if self.removeParameterInSetExpressionBetweenBraces:
            if self.genParameters.has(ident):
                self.genParameters.remove(ident)
                
        if not node.getSymbolTable():
            return ident

        if self.replaceNewIndices and not self.getOriginalIndices:
            new_ident = self._getNewIndex(ident, node.getSymbolTable())

            if new_ident != None:
                return new_ident

        return ident

    # String
    def generateCode_String(self, node):
        string = "\"" + node.string[1:-1] + "\""

        if not node.getSymbolTable():
            return string

        if self.turnStringsIntoInts:
            param = string[1:-1]

            if self.removeAdditionalParameter:
                if param in self.additionalParameters:
                    del self.additionalParameters[param]

            return param

        if self.replaceNewIndices:
            new_ident = self._getNewIndex(string, node.getSymbolTable())
            if new_ident != None:
                return new_ident

        return string

    # IntegerSet
    def generateCode_IntegerSet(self, node):
        res = INT
        
        firstBound  = None if node.firstBound  == None else node.firstBound.getSymbolName(self)
        secondBound = None if node.secondBound == None else node.secondBound.getSymbolName(self)
        
        if firstBound != None and not Utils._isInfinity(firstBound):
            op = EMPTY_STRING
            if secondBound != None and not Utils._isInfinity(secondBound):
                op += COMMA+SPACE
            else:
                op += SPACE
                
            op += node.firstOp+SPACE
            
            res += op + firstBound
            
        if secondBound != None and not Utils._isInfinity(secondBound):
            op = EMPTY_STRING
            if firstBound != None and not Utils._isInfinity(firstBound):
                op += COMMA+SPACE
            else:
                op += SPACE
                
            op += node.secondOp+SPACE
            
            res += op + secondBound
            
        return res

    # RealSet
    def generateCode_RealSet(self, node):
        res = EMPTY_STRING
        
        firstBound  = None if node.firstBound  == None else node.firstBound.getSymbolName(self)
        secondBound = None if node.secondBound == None else node.secondBound.getSymbolName(self)
        
        if firstBound != None and not Utils._isInfinity(firstBound):
            op = EMPTY_STRING
            if secondBound != None and not Utils._isInfinity(secondBound):
                op += COMMA+SPACE
                
            op += node.firstOp+SPACE
            
            res += op + firstBound
            
        if secondBound != None and not Utils._isInfinity(secondBound):
            op = EMPTY_STRING
            if firstBound != None and not Utils._isInfinity(firstBound):
                op += COMMA+SPACE
                
            op += node.secondOp+SPACE
            
            res += op + secondBound
            
        return res

    # BinarySet
    def generateCode_BinarySet(self, node):
        return BOOL

    # SymbolicSet
    def generateCode_SymbolicSet(self, node):
        return STRING

    # LogicalSet
    def generateCode_LogicalSet(self, node):
        return BOOL

    # EnumSet
    def generateCode_EnumSet(self, node):
        return ENUM

    # ParameterSet
    def generateCode_ParameterSet(self, node):
        return EMPTY_STRING

    # VariableSet
    def generateCode_VariableSet(self, node):
        return EMPTY_STRING

    # SetSet
    def generateCode_SetSet(self, node):
        return EMPTY_STRING
