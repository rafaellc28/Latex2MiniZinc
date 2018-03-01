from GenObj import *

class GenVariable(GenObj):
	def __init__(self, name, isSymbolic = False, isInteger = False, isLogical = False, _type = None, certainty = True, isDeclaredAsVar = False):
		super(GenVariable, self).__init__(name)
		self.isSymbolic = isSymbolic
		self.isInteger = isInteger
		self.isLogical = isLogical
		self.type = _type
		self.certainty = certainty
		self.isDeclaredAsVar = isDeclaredAsVar

	def getIsSymbolic(self):
		return self.isSymbolic
	
	def setIsSymbolic(self, isSymbolic):
		self.isSymbolic = isSymbolic

	def getIsInteger(self):
		return self.isInteger
	
	def setIsInteger(self, isInteger):
		self.isInteger = isInteger

	def getIsLogical(self):
		return self.isLogical
	
	def setIsLogical(self, isLogical):
		self.isLogical = isLogical
		
	def getType(self):
		return self.type

	def setType(self, _type):
		self.type = _type
	
	def getCertainty(self):
		return self.certainty

	def setCertainty(self, certainty):
		self.certainty = certainty

	def getIsDeclaredAsVar(self):
		return self.isDeclaredAsVar

	def setIsDeclaredAsVar(self, isDeclaredAsVar):
		self.isDeclaredAsVar = isDeclaredAsVar
