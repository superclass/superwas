# This file is part of Superwas.
# 
# Superwas is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Superwas is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Superwas.  If not, see <http://www.gnu.org/licenses/>.

# Variable classes
#
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: wasvariable.py 424 2013-01-04 15:04:36Z andre $
class WASVariable(WASConfig):
	"""
	Class to represent WAS variables

	Author: Andre van Dijk (SuperClass IT)
	Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $

	$Id: wasvariable.py 424 2013-01-04 15:04:36Z andre $
	"""
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name':""
		}
		self.opt_attributes={
			'value':""
		}
		self.__varMap=""

	def getConfigType(self):
		return "VariableSubstitutionEntry"

	def __setVarMap(self):
		self.__varMap=AdminConfig.getid("%sVariableMap:/" % self.getParent().getContainmentPath())

	def setConfigID(self):
		self.__setVarMap()
		if self.__varMap != "":
			entries=Util.wslist(AdminConfig.list("VariableSubstitutionEntry",self.__varMap))
			for entry in entries:
				if AdminConfig.showAttribute(entry, 'symbolicName')==self.getName():
					self.configID=entry
		self.logValue()

	def setValue(self, value):
		if value is not None:
			self.opt_attributes['value']=value
		self.logValue()
	def getValue(self):
		return self.opt_attributes['value']

	def create(self):
		WASConfig.create(self)
		self.__setVarMap()
		if self.__varMap=="":
			raise Exception("Variable map not found on: %s" % self.getParent().getName())
		self.configID=AdminConfig.create(self.getConfigType(), self.__varMap, Util.dictToList(self.opt_attributes)+[['symbolicName', self.getName()]], "entries")
		self.logCreate()
