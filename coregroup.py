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

# CoreGroup class
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: node.py 424 2013-01-04 15:04:36Z andre $
class CoreGroup(WASConfig):
	"""
	Class to represent a CoreGroup.

	Author: Andre van Dijk (SuperClass IT)
	"""
	level=1
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["Cell"]
		self.man_attributes={
			'name':"",
			'numCoordinators':"1",
			'transportMemorySize':"100"
		}
		self.opt_attributes={
			'description':""
		}

	def setDescription(self, description):
		if description is not None: self.opt_attributes['description']=description
	def getDescription(self):
		return self.opt_attributes['description']

	def setNumCoordinators(self, numCoordinators):
		if numCoordinators is not None: self.man_attributes['numCoordinators']=numCoordinators
	def getNumCoordinators(self):
		return self.man_attributes['numCoordinators']

	def setTransportMemorySize(self, transportMemorySize):
		if transportMemorySize is not None: self.man_attributes['transportMemorySize']=transportMemorySize
	def getTransportMemorySize(self):
		return self.man_attributes['transportMemorySize']

	def validate(self):
		# No checks for default Providers, get config ID
		if self.getName() in ["DefaultCoreGroup"]:
			self.wasDefault="true"
		WASConfig.validate(self)

	def create(self):
		if self.wasDefault=="false":
			self.configID=AdminTask.createCoreGroup('[-coreGroupName %s]' % self.getName())
			self.logCreate()
			if self.configID!="":
				AdminConfig.modify(self.configID,Util.dictToList(self.man_attributes))
				AdminConfig.modify(self.configID,Util.dictToList(self.opt_attributes))
				logger.info("Successfully set the properties on coregroup : %s" % self.getName())
