import re

def _flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(_flatten(el))
        else:
            result.append(el)
    return result

class Utils:
    @staticmethod
    def _deleteEmpty(str):
        return str != ""

    @staticmethod
    def _getInt(val):
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    # from http://stackoverflow.com/questions/406121/flattening-a-shallow-list-in-python
    _flatten = staticmethod(_flatten)

    @staticmethod
    def _isInfinity(value):
        return value == "Infinity" or value == "-Infinity"

    @staticmethod
    def _isFromZeroToN(values):
        i = 0
        for idx in values:
            if idx != i:
                return False

            i += 1

        return True

    @staticmethod
    def _hasEqualIndices(minVal, maxVal):
        minValIndices = sorted(minVal.keys())
        maxValIndices = sorted(maxVal.keys())

        return minValIndices == maxValIndices

    @staticmethod
    def _hasAllIndices(minVal, maxVal):
        minValIndices = sorted(minVal.keys())
        maxValIndices = sorted(maxVal.keys())

        if minValIndices != maxValIndices:
            return False

        if not Utils._isFromZeroToN(minValIndices):
            return False

        if not Utils._isFromZeroToN(maxValIndices):
            return False

        return True

    @staticmethod
    def _stripDomains(domains):
        return map(lambda el: el.strip(), domains)

    @staticmethod
    def _splitDomain(domain, SEP):
        return Utils._stripDomains(domain.split(SEP))

    @staticmethod
    def _getWords(expression):
        if isinstance(expression, str):
            return re.sub("[^\w]", " ", expression).split()

        return []
