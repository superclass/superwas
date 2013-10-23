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

# Scheduler Classes
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: scheduler.py 424 2013-01-04 15:04:36Z andre $
class SchedulerProvider(WASConfig):
	level=3	
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name':"",
		}
		self.opt_attributes={
            'description':"",
		}

	def setDescription(self, description):
		if description is not None: self.opt_attributes['description']=description
		self.logValue()
	def getDescription(self):
		return self.opt_attributes['description']

	def validate(self):
		# No checks for default Providers, get config ID
		if self.getName() in ["Scheduler Provider"]:
			self.wasDefault="true"
		WASConfig.validate(self)

class SchedulerConfiguration(WASConfig):
	"""
	Class to represent a WAS scheduler.

	This can be used to create a scheduler and to perform actions on
	an existing scheduler.

	For an existing scheduler the config ID is fetched when the
	scheduler name is set through the setName method.

	The scope of the scheduler is a cluster object that needs to be
	provided to the constructor.
	"""
	level=4
	def __init__(self, parent=None):
		"""
		Create a new Scheduler object. Scope 

		The scope of the scheduler is a Cell object that needs to be
		provided to the constructor.
		"""
		WASConfig.__init__(self, parent)
		self.validParents=["URLProvider"]
		self.man_attributes={
			'name':"",
			'jndiName':"",
			'datasourceAlias':"",
			'datasourceJNDIName':"",
			'tablePrefix':""
		}
		self.opt_attributes={
			'pollInterval':30,
			'useAdminRoles':"false",
			'workManagerInfoJNDIName':"wm/default"
		}

	def setJndiName(self, jndiName):
		if jndiName is not None: self.man_attributes['jndiName']=jndiName
		self.logValue()
	def getJndiName(self):
		return self.man_attributes['jndiName']

	def setDatasourceAlias(self, datasourceAlias):
		if datasourceAlias is not None: self.man_attributes['datasourceAlias']=datasourceAlias
		self.logValue()
	def getDatasourceAlias(self):
		return self.man_attributes['datasourceAlias']

	def setDatasourceJNDIName(self, datasourceJNDIName):
		if datasourceJNDIName is not None: self.man_attributes['datasourceJNDIName']=datasourceJNDIName
		self.logValue()
	def getDatasourceJNDIName(self):
		return self.man_attributes['datasourceJNDIName']

	def setTablePrefix(self, tablePrefix):
		if tablePrefix is not None: self.man_attributes['tablePrefix']=tablePrefix
		self.logValue()
	def getTablePrefix(self):
		return self.man_attributes['tablePrefix']

	def setPollInterval(self, pollInterval):
		if pollInterval is not None: self.opt_attributes['pollInterval']=pollInterval
	def getPollInterval(self):
		return self.opt_attributes['pollInterval']

	def setUseAdminRoles(self, useAdminRoles):
		if useAdminRoles is not None: self.opt_attributes['useAdminRoles']=useAdminRoles
	def getUseAdminRoles(self):
		return self.opt_attributes['useAdminRoles']

	def setWorkManagerInfoJNDIName(self, workManagerInfoJNDIName):
		if workManagerInfoJNDIName is not None: self.opt_attributes['workManagerInfoJNDIName']=workManagerInfoJNDIName
	def getWorkManagerInfoJNDIName(self):
		return self.opt_attributes['workManagerInfoJNDIName']

	def create(self):
		WASConfig.create(self)
		AdminConfig.create(self.getConfigType(),self.getParent().getConfigID(), Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes))
		self.logCreate()

	def stop(self):
		pass
	def start(self):
		pass
