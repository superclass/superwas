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

# WorkManager Classes
#
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: workmanager.py 424 2013-01-04 15:04:36Z andre $
class WorkManagerProvider(WASConfig):
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name':"",
		}
	def validate(self):
		# No checks for default Providers, get config ID
		if self.getName() in ["Default WorkManager Provider"]:
			self.wasDefault="true"
		WASConfig.validate(self)

class WorkManager(WASConfig):
	"""
	Class to represent a Work Manager.

	This can be used to create a scheduler and to perform actions on
	an existing scheduler.

	For an existing scheduler the config ID is fetched when the
	scheduler name is set through the setName method.

	The scope of the scheduler is a cluster object that needs to be
	provided to the constructor.

	Author: Andre van Dijk (SuperClass IT)
	Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $

	$Id: workmanager.py 424 2013-01-04 15:04:36Z andre $
	"""
	level=4
	def __init__(self, parent=None):
		"""
		Create a new WorkManager object.

		"""
		WASConfig.__init__(self, parent)
		self.validParents=["WorkManagerProvider"]
		
		self.man_attributes={
			'name':"",
			'jndiName':"",
			'minThreads':0,
			'maxThreads':2,
			'threadPriority':5,
			'numAlarmThreads':2
		}
		self.opt_attributes={
			'description':"",
			'isGrowable':"true",
			'workTimeout':0,
			'workReqQFullAction':0,
			'category':""
		}

	def getConfigType(self):
		return "WorkManagerInfo"

	def setJndiName(self, jndiName):
		if jndiName is not None: self.man_attributes['jndiName']=jndiName
		self.logValue()
	def getJndiName(self):
		return self.man_attributes['jndiName']

	def setMinThreads(self, minThreads):
		if minThreads is not None: self.man_attributes['minThreads']=minThreads
		self.logValue()
	def getMinThreads(self):
		return self.man_attributes['minThreads']

	def setMaxThreads(self, maxThreads):
		if maxThreads is not None: self.man_attributes['maxThreads']=maxThreads
		self.logValue()
	def getMaxThreads(self):
		return self.man_attributes['maxThreads']

	def setThreadPriority(self, threadPriority):
		if threadPriority is not None: self.man_attributes['threadPriority']=threadPriority
		self.logValue()
	def getThreadPriority(self):
		return self.man_attributes['threadPriority']

	def setNumAlarmThreads(self, numAlarmThreads):
		if numAlarmThreads is not None: self.man_attributes['numAlarmThreads']=numAlarmThreads
		self.logValue()
	def getNumAlarmThreads(self):
		return self.man_attributes['numAlarmThreads']

	def setIsGrowable(self, isGrowable):
		if isGrowable is not None: self.opt_attributes['isGrowable']=isGrowable
		self.logValue()
	def getIsGrowable(self):
		return self.opt_attributes['isGrowable']

	def setDescription(self, description):
		if description is not None: self.opt_attributes['description']=description
		self.logValue()
	def getDescription(self):
		return self.opt_attributes['description']

	def setCategory(self, category):
		if category is not None: self.opt_attributes['category']=category
		self.logValue()
	def getCategory(self):
		return self.opt_attributes['category']

	def setWorkTimeout(self, workTimeout):
		if workTimeout is not None: self.opt_attributes['workTimeout']=workTimeout
		self.logValue()
	def getWorkTimeout(self):
		return self.opt_attributes['workTimeout']

	def setWorkReqQFullAction(self, workReqQFullAction):
		if workReqQFullAction is not None: self.opt_attributes['workReqQFullAction']=workReqQFullAction
		self.logValue()
	def getWorkReqQFullAction(self):
		return self.opt_attributes['workReqQFullAction']

	def create(self):
		WASConfig.create(self)
		AdminConfig.create(self.getConfigType(),self.getParent().getConfigID(), Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes))
		self.logCreate()
