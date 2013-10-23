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

# Dynamic Cache classes
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-18 16:38:05 +0100 (vr, 18 jan 2013) $
# $Id: objectcache.py 428 2013-01-18 15:38:05Z andre $
class CacheProvider(WASConfig):
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name':"",
		}

	def validate(self):
		# No checks for default Providers, get config ID
		if self.getName() in ["CacheProvider"]:
			self.wasDefault="true"
		WASConfig.validate(self)

class CustomResourceProperty(WASConfig):
	level=5
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.__j2eepropset=""
		self.opt_attributes={
			'value':"",
			'description':""
		}
		self.validParents=["ObjectCacheInstance", "URL", "MailSession"]

	def getConfigType(self):
		return "J2EEResourceProperty"

	def setValue(self, value):
		self.opt_attributes['value']=value
		self.logValue()

	def getValue(self):
		return self.opt_attributes['value']

	def setDescription(self, description):
		if description!=None:
			self.opt_attributes['description']=description
		self.logValue()

	def getDescription(self):
		return self.opt_attributes['description']

	def __setJ2EEResourcePropertySet(self):
		if self.getParent().getConfigID()!="":
			self.__j2eepropset=AdminConfig.list('J2EEResourcePropertySet',self.getParent().getConfigID())
		else:
			self.__j2eepropset=""

	def setConfigID(self):
		self.__setJ2EEResourcePropertySet()
		if self.__j2eepropset!="":
			ps=Util.wslist(AdminConfig.list(self.getConfigType(), self.__j2eepropset))
			for c in ps:
				if AdminConfig.showAttribute(c, "name" )==self.getName():
					self.configID=c
					break
		else:
			self.configID=""
		self.logValue()

	def create(self):
		WASConfig.create(self)
		self.__setJ2EEResourcePropertySet()
		if self.__j2eepropset=="":
			self.__j2eepropset=AdminConfig.create('J2EEResourcePropertySet',self.getParent().getConfigID(), [])
		self.configID=AdminConfig.create(self.getConfigType(),self.__j2eepropset,Util.dictToList(self.opt_attributes)+Util.dictToList(self.man_attributes), "resourceProperties")
		self.logCreate()

class ObjectCacheInstance(WASConfig):
	"""# 
#
# Currently only outgoing ObjectCache are supported.
#
# Author: Andre van Dijk <andre.van.dijk@superclass.nl>
# Date: $Date: 2013-01-18 16:38:05 +0100 (vr, 18 jan 2013) $
#
# $Id: objectcache.py 428 2013-01-18 15:38:05Z andre $"""
	level=4
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["CacheProvider"]
		self.man_attributes={
			'name':"",
			'jndiName':"",
			'defaultPriority':"1",
			'cacheSize':"2000",
			'enableDiskOffload':""
		}
		self.opt_attributes={
			'description' : "",
			'category' : ""
		}

	def setJndiName(self, jndiName):
		"""# Specifies the JNDI name for the ObjectCache."""
		if jndiName is not None: self.man_attributes['jndiName']=jndiName
		self.logValue()
	def getJndiName(self):
		return self.man_attributes['jndiName']

	def setDefaultPriority(self, defaultPriority):
		"""# Specifies the JNDI name for the ObjectCache."""
		if defaultPriority is not None: self.man_attributes['defaultPriority']=defaultPriority
		self.logValue()
	def getDefaultPriority(self):
		return self.man_attributes['defaultPriority']

	def setCacheSize(self, cacheSize):
		"""# Specifies the JNDI name for the ObjectCache."""
		if cacheSize is not None: self.man_attributes['cacheSize']=cacheSize
		self.logValue()
	def getCacheSize(self):
		return self.man_attributes['cacheSize']

	def setEnableDiskOffload(self, enableDiskOffload):
		"""# Specifies the JNDI name for the ObjectCache."""
		if enableDiskOffload is not None: self.man_attributes['enableDiskOffload']=enableDiskOffload
		self.logValue()
	def getEnableDiskOffload(self):
		return self.man_attributes['enableDiskOffload']

	def setDescription(self, description):
		"""# Specifies a description for the ObjectCache."""
		if description is not None: self.opt_attributes['description']=description
		self.logValue()
	def getDescription(self):
		return self.opt_attributes['description']

	def setCategory(self, category):
		"""# Specifies a collection for classifying or grouping ObjectCaches."""
		if category is not None: self.opt_attributes['category']=category
		self.logValue()
	def getCategory(self):
		return self.opt_attributes['category']

	def create(self):
		WASConfig.create(self)
		self.configID=AdminConfig.create(self.getConfigType(), self.getParent().getConfigID(), Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes))
		self.logCreate()
