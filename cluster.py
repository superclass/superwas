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

# ServerCluster Class
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: cluster.py 424 2013-01-04 15:04:36Z andre $
class ServerCluster(WASConfig, ManagementScopedWASConfig):
	"""
	Class to represent a WAS cluster.

	This can be used to create a cluster and to perform actions on
	an existing cluster.

	For an existing cluster the config ID is fetched when the
	cluster name is set through the setName method.

	The scope of the cluster is a Cell object that needs to be
	provided to the constructor.
	"""
	level=1
	def __init__(self, parent=None):
		"""
		Create a new Cluster object.

		The scope of the cluster is a Cell object that needs to be
		provided to the constructor.
		"""
		WASConfig.__init__(self, parent)
		ManagementScopedWASConfig.__init__(self)
		self.validParents=["Cell"]
		self.__members=[]

	def isRunning(self):
		"""
		Return if the cluster is running. Returns 0 when the
		cluster is not running and 1 when it's running.

		If the cluster does not exit an Exception is raised.
		"""
		cluster=self.getMbean()
		if cluster == '': 
			raise Exception("%s : %s not defined" % (self.getType(),self.getName()))
		state = AdminControl.getAttribute( cluster, "state" )
		logger.debug("Cluster start : %s" % state)
		if ( state == "websphere.cluster.running" ):
			return 1
		else:
			return 0

	def addChild(self, child):
		WASConfig.addChild(self, child)
		if isinstance(child, Server):
			self.__members.append(child)

	def getMembers(self):
		return self.__members
		
	def setName(self, name):
		WASConfig.setName(self, name)

	def validate(self):
		WASConfig.validate(self)	
		self.setManagementScope()

	def remove(self):
		WASConfig.remove(self)
		#ManagementScopedWASConfig.remove(self)

	def setManagementScope(self):
		self.managementScope=ManagementScope()
		self.managementScope.setScopeName("%s:(%s):%s" % (self.getParent().getManagementScope().getScopeName(),"cluster",self.getName()))
		self.managementScope.setScopeType("cluster")
		self.managementScope.setParent(self.getSecurity())
		self.managementScope.validate()
		self.logValue()

	def getMbean(self):
		if self.getConfigID() != "":
			mbean=AdminControl.completeObjectName('cell=%s,type=Cluster,name=%s,*' % (self.getCell().getName(),self.getName()))
			logger.debug(mbean)
			return mbean
		return ""

	def stop(self):
		"""
		Stop the cluster. This method waits a maximum 10
		minutes until the cluster is stopped. If the cluster
		has not stopped in 10 minutes an Exception is raised.

		If the cluster does not exist an Exception is raised.
		"""
		logger.info("Stopping Cluster : %s" % self.getName())
		if self.isRunning(): 
			mBean=self.getMbean()
			AdminControl.invoke(mBean, "stop")
			i=0
			while self.isRunning():
				if i==40: raise Exception("Cluster : %s did not stop in 10 minutes, please check." % self.getName())
				logger.info("Cluster stopping...")
				time.sleep(15)
				i+=1
		else:
			logger.info("Cluster already stopped")
		logger.info("Clusters stopped: %s" % self.getName())

	def start(self):
		"""
		Start the cluster. This method waits a maximum of 15
		minutes until the cluster is started. If the cluster
		has not started in 15 minutes an Exception is raised.

		If the cluster does not exist an Exception is raised.
		"""
		logger.info("Starting Clusters : %s" % self.getName())
		if self.isRunning():
			logger.info("Cluster already started")
		else:
			mBean=self.getMbean()
			AdminControl.invoke(mBean, "start" )
			i=0
			while not self.isRunning():
				if i==60: raise Exception("Cluster : %s did not start in 15 minutes, please check." % self.getName())
				logger.info( "Cluster starting..." )
				time.sleep(15)
				i+=1
		logger.info("Clusters started: %s" % self.getName())

	def create(self):
		"""
		Create the cluster in the WebSphere configuration.
		"""
		WASConfig.create(self)
		self.configID=AdminTask.createCluster('[-clusterConfig [[ %s ]]]' % self.getName())
		self.logCreate()
