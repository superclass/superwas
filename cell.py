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

# Cell and Security Class
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: cell.py 424 2013-01-04 15:04:36Z andre $
class Cell(WASConfig, ManagementScopedWASConfig):
	"""
	Class to represent a Cell
	"""
	def __init__(self, parent=None):
		WASConfig.__init__(self,parent)
		ManagementScopedWASConfig.__init__(self)
		self.man_attributes['name']=AdminControl.getCell()
		self.__security=Security()
		self.__security.setConfigID()
		self.__security.setConfigID()
		self.setConfigID()
		self.setManagementScope()

	def setName(self, name):
		pass

	def getCell(self):
		return self

	def getSecurity(self):
		return self.__security

	def getName(self):
		return self.man_attributes['name']

	def getContainmentPath(self):
		return "/Cell:%s/" % self.getName()

	def setManagementScope(self):
		self.managementScope=ManagementScope()
		self.managementScope.setScopeName("(%s):%s" % (self.getConfigType().lower(),self.getName()))
		self.managementScope.setScopeType(self.getConfigType().lower())
		self.managementScope.setParent(self.getSecurity())
		self.managementScope.validate()

	def validate(self):
		pass

	def create(self):
		pass
	def remove(self):
		pass

class Security(WASConfig):
	def __init__(self, parent=None):
		WASConfig.__init__(self,parent)
		self.man_attributes={}

	def getName(self):
		return "Security"

	def getContainmentPath(self):
		return "/Security:/"

	def remove(self):
		pass
	def create(self):
		pass
