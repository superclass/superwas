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

# Server Classes
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-07-22 21:15:08 +0200 (ma, 22 jul 2013) $
# $Id: server.py 462 2013-07-22 19:15:08Z andre $
class WebServer(WASConfig):
	level=2
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["Node"]

	def getConfigType(self):
		return "Server"

	def create(self):
		pass
	def remove(self):
		pass

class EnvEntry(WASConfig):
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.__procDef=""
		self.opt_attributes={
			'value':"",
			'description':""
		}
		self.validParents=["Server"]

	def getConfigType(self):
		return "Property"

	def setValue(self, value):
		self.opt_attributes['value']=value
		self.logValue()

	def getValue(self):
		return self.opt_attributes['value']

	def setDescription(self, description):
		self.opt_attributes['description']=description
		self.logValue()

	def getDescription(self):
		return self.opt_attributes['description']

	def __setProcDef(self):
		if self.getParent().getConfigID()!="":
			self.__procDef=AdminConfig.list('JavaProcessDef',self.getParent().getConfigID())
		else:
			self.__procDef=""

	def setConfigID(self):
		self.__setProcDef()
		if self.__procDef != "":
			envs=Util.wslist(AdminConfig.list(self.getConfigType(), self.__procDef))
			for e in envs:
				if AdminConfig.showAttribute( e, "name" )==self.getName():
					self.configID=e
					break
		else:
			self.configID=""
		self.logValue()

	def create(self):
		WASConfig.create(self)
		self.__setProcDef()
		if self.__procDef=="":
			raise Exception("Process definition not found on: %s" % self.getParent().getName())
		self.configID=AdminConfig.create(self.getConfigType(), self.__procDef, Util.dictToList(self.opt_attributes)+Util.dictToList(self.man_attributes), "environment")
		self.logCreate()

class Property(WASConfig):
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.opt_attributes={
			'value':"",
			'description':""
		}
		self.validParents=["Server"]

	def setValue(self, value):
		self.opt_attributes['value']=value
		self.logValue()

	def getValue(self):
		return self.opt_attributes['value']

	def setDescription(self, description):
		if description is not None:
			self.opt_attributes['description']=description
		self.logValue()

	def getDescription(self):
		return self.opt_attributes['description']

class CustomJVMParam(Property):
	level=3
	def __init__(self, parent=None):
		Property.__init__(self, parent)
		self.__jvm=""

	def getConfigType(self):
		return "Property"

	def __setJVM(self):
		pid=self.getParent().getConfigID()
		if pid!="":
			self.__jvm=AdminConfig.list('JavaVirtualMachine', self.getParent().getConfigID() )
		else:
			self.__jvm=""

	def setConfigID(self):
		self.__setJVM()
		if self.__jvm!="":
			cjp=Util.wslist(AdminConfig.list(self.getConfigType(), self.__jvm))
			for c in cjp:
				if AdminConfig.showAttribute( c, "name" )==self.getName():
					self.configID=c
					break
		else:
			self.configID=""
		self.logValue()

	def create(self):
		WASConfig.create(self)
		self.__setJVM()
		if self.__jvm=="":
			raise Exception("JVM not found in : %s" % self.getParent().getName())
		self.configID=AdminConfig.create(self.getConfigType(), self.__jvm, Util.dictToList(self.opt_attributes)+Util.dictToList(self.man_attributes), "systemProperties")
		self.logCreate()

class CustomSessionParam(Property):
	level=3
	def __init__(self, parent=None):
		Property.__init__(self, parent)
		self.__smID=""

	def getConfigType(self):
		return "Property"

	def __setSM(self):
		pid=self.getParent().getConfigID()
		if pid!="":
			wcID=AdminConfig.list('WebContainer', self.getParent().getConfigID())
			self.__smID=AdminConfig.list('SessionManager', wcID)
		else:
			self.__smID=""

	def setConfigID(self):
		self.__setSM()
		if self.__smID!="":
			csp=Util.wslist(AdminConfig.list(self.getConfigType(), self.__smID))
			for c in csp:
				if AdminConfig.showAttribute( c, "name" )==self.getName():
					self.configID=c
					break
		else:
			self.configID=""
		self.logValue()

	def create(self):
		WASConfig.create(self)
		self.__setSM()
		if self.__smID=="":
			raise Exception("Sesion Manager not found in : %s" % self.getParent().getName())
		self.configID=AdminConfig.create(self.getConfigType(), self.__smID, Util.dictToList(self.opt_attributes)+Util.dictToList(self.man_attributes), "properties")
		self.logCreate()

class WebContainerProperty(Property):
	level=3
	def __init__(self, parent=None):
		Property.__init__(self, parent)
		self.__wc=""

	def getConfigType(self):
		return "Property"

	def __setWC(self):
		pid=self.getParent().getConfigID()
		if pid!="":
			self.__wc=AdminConfig.list('WebContainer', self.getParent().getConfigID() )
		else:
			self.__wc=""

	def setConfigID(self):
		self.__setWC()
		if self.__wc!="":
			cjp=Util.wslist(AdminConfig.list(self.getConfigType(), self.__wc))
			for c in cjp:
				if AdminConfig.showAttribute( c, "name" )==self.getName():
					self.configID=c
					break
		else:
			self.configID=""
		self.logValue()

	def create(self):
		WASConfig.create(self)
		self.__setWC()
		if self.__wc=="":
			raise Exception("WebContainer not found in : %s" % self.getParent().getName())
		self.configID=AdminConfig.create(self.getConfigType(), self.__wc, Util.dictToList(self.opt_attributes)+Util.dictToList(self.man_attributes))
		self.logCreate()

class MessageListener(WASConfig):
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.__messageListenerService=""
		self.man_attributes={
			'name':"",
			'connectionFactoryJNDIName':"",
			'destinationJNDIName':""
		}
		self.opt_attributes={
			'maxMessages':1,
			'maxRetries':0,
			'maxSessions':1
		}
		self.__state={
			'initialState':'START'
		}
		self.validParents=["Server"]

	def getOptAttributes(self):
		return self.opt_attributes.keys() + self.__state.keys()
	
	def setConnectionFactoryJNDIName(self, connectionFactoryJNDIName):
		if connectionFactoryJNDIName is not None:
			self.man_attributes['connectionFactoryJNDIName']=connectionFactoryJNDIName
		self.logValue()

	def getConnectionFactoryJNDIName(self):
		return self.man_attributes['connectionFactoryJNDIName']

	def setDestinationJNDIName(self, destinationJNDIName):
		if destinationJNDIName is not None:
			self.man_attributes['destinationJNDIName']=destinationJNDIName
		self.logValue()

	def getDestinationJNDIName(self):
		return self.man_attributes['destinationJNDIName']

	def setMaxMessages(self, maxMessages):
		if maxMessages is not None:
			if maxMessages.isdigit():
				self.opt_attributes['maxMessages']=maxMessages
			else:
				raise Exception("maxMessages should be a number")
		self.logValue()

	def getMaxMessages(self):
		return self.opt_attributes['maxMessages']

	def setMaxRetries(self, maxRetries):
		if maxRetries is not None:
			if maxRetries.isdigit():
				self.opt_attributes['maxRetries']=maxRetries
			else:
				raise Exception("maxRetries should be a number")
		self.logValue()

	def getMaxRetries(self):
		return self.opt_attributes['maxRetries']

	def setMaxSessions(self, maxSessions):
		if maxSessions is not None:
			if maxSessions.isdigit():
				self.opt_attributes['maxSessions']=maxSessions
			else:
				raise Exception("maxSessions should be a number")
		self.logValue()

	def getMaxSessions(self):
		return self.opt_attributes['maxSessions']

	def setInitialState(self, initialState):
		if initialState is not None:
			if initialState in ["START","STOP"]:
				self.__state['initialState']=initialState
			else:
				raise Exception("State should be START or STOP")
		self.logValue()

	def getInitialState(self):
		return self.__state['initialState']

	def __setMLS(self):
		pid=self.getParent().getConfigID()
		if pid!="":
			self.__messageListenerService = AdminConfig.list( "MessageListenerService", self.getParent().getConfigID() )
		else:
			self.__messageListenerService=""

	def setConfigID(self):
		self.__setMLS
		if self.__messageListenerService != "":
			ports=Util.wslist(AdminConfig.list("ListenerPort", self.__messageListenerService))
			for p in ports:
				if AdminConfig.showAttribute( p, "name" )==self.getName():
					self.configID=p
					break
		else:
			self.configID=""
		self.logValue()

	def create(self):
		WASConfig.create(self)
		self.__setMLS()
		if self.__messageListenerService != "":
			lp=AdminConfig.create("ListenerPort", self.__messageListenerService, Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes))
			if lp=="": raise Exception("Error creating listener port %s on %s" % (self.getName(),self.getParent().getName()))
			self.configID=AdminConfig.create( "StateManageable", lp, Util.dictToList(self.__state) )
			self.logCreate()
		else:
			raise Exception("Message listener service not found on : %s" % self.getParent().getName())

class PMIModule(WASConfig):
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["Server"]
		self.man_attributes={
			'name':""
		}
		self.opt_attributes={
			'stats':""
		}
		self.__pmiService=""

	def setStats(self, stats):
		if stats is not None:
			self.opt_attributes['stats']=stats
		self.logValue()
	def getStats(self):
		return self.opt_attributes['stats']

	def setConfigID(self):
		pass

	def __setPS(self):
		pid=self.getParent().getConfigID()
		if pid!="":
			self.__pmiService=AdminConfig.list( "PMIService", self.getParent().getConfigID() )
		else:
			self.__pmiService=""

	def create(self):
		logger.info("Modifying PMI Module : %s" % self.getName())
		self.__setPS()
		if self.__pmiService!="":
			pm=AdminConfig.list('PMIModule',self.__pmiService)
			pms=Util.wslist(AdminConfig.showAttribute(pm, 'pmimodules'))
			for m in pms:
				if AdminConfig.showAttribute(m, 'moduleName')==self.getName():
					AdminConfig.modify(m, [['enable', self.getStats()]])
					logger.info("Modified PMI Module : %s" % self.getName())
		else:
			raise Exception("PMI service not found on : %s" % self.getParent().getName())

	def remove(self):
		pass

class Server(WASConfig, ManagementScopedWASConfig):
	level=2
	"""# Use this class to create Application Servers."""
	def __init__(self, parent=None):
		"""
		Initialize variables and set default values. Takes
		scope, the object that contains this server, as an
		argument.
		"""
		WASConfig.__init__(self, parent)
		ManagementScopedWASConfig.__init__(self)
		self.ref_attributes['node']=None
		self.validParents=["Node", "ServerCluster"]
		self.man_attributes={
			'name':""
		}
		self.opt_attributes={
			'noSecurePort':"false",
			'securePortSSLConfig':"",
			'dataReplicationDomain':"",
			'weight':2,
			'vhost':None,
			'clone':"",
			'heapWarningThreshold':-1,
			'heapCriticalThreshold':-1,
			'cpuWarningThreshold':-1,
			'cpuCriticalThreshold':-1,
			'webContainerActiveWarningThreshold':-1,
			'webContainerActiveCriticalThreshold':-1,
			'webContainerHungThreadWarningThreshold':-1,
			'webContainerHungThreadCriticalThreshold':-1,
			'liveSessionsWarningThreshold':-1,
			'liveSessionsCriticalThreshold':-1,
			'enableNscaLogs':"false", 
			'accessLogFormat':"COMMON",
			'enableAccessLogging':"false",
			'enableErrorLogging':"false",
			'errorLogLevel':"WARNING",
			'pmiStatisticSet':'none',
		}
		self.__startPort={
			'startPort':0
		}

		self.__nscaAccessLog={
			'filePath':"${SERVER_LOG_ROOT}/http_access.log",
			'maximumBackupFiles':1,
			'maximumSize':500
		}
		self.__nscaErrorLog={
			'filePath':"${SERVER_LOG_ROOT}/http_error.log",
			'maximumBackupFiles':1,
			'maximumSize':500
		}

		self.__httpAccessList=[
			'addressExcludeList',
			'addressIncludeList',
			'hostNameExcludeList',
			'hostNameIncludeList'
		]

		self.__httpAddressExcludeList=[]
		self.__httpAddressIncludeList=[]
		self.__httpHostNameExcludeList=[]
		self.__httpHostNameIncludeList=[]

		self.__httpsAccessList={
			'addressExcludeList':"",
			'addressIncludeList':"",
			'hostNameExcludeList':"",
			'hostNameIncludeList':""
		}

		""" Holds JVM attributes """
		self.__jvmAttr={}
		# Initialize jvmAttribute defaults
		self.__jvmAttr['verboseModeClass']="false"
		self.__jvmAttr['classpath']=""
		self.__jvmAttr['initialHeapSize']=256
		self.__jvmAttr['maximumHeapSize']=768
		self.__jvmAttr['bootClasspath']=""
		self.__jvmAttr['verboseModeGarbageCollection']="false"
		self.__jvmAttr['runHProf']="false"
		self.__jvmAttr['hprofArguments']=""
		self.__jvmAttr['debugMode']="false"
		self.__jvmAttr['debugArgs']=""
		self.__jvmAttr['genericJvmArguments']=""
		self.__jvmAttr['verboseModeJNI']="false"

		""" Holds Process Execution attributes """
		self.__procExec={}
		self.__procExec['umask']="022"
		
		""" Holds Process Definition attributes """
		self.__procDef={}
		self.__procDef['workingDirectory']="${USER_INSTALL_ROOT}"

		""" Holds IO Redirect attributes """
		self.__ioRedirect={}
		self.__ioRedirect['stdoutFilename']="${SERVER_LOG_ROOT}/native_stdout.log"
		self.__ioRedirect['stderrFilename']="${SERVER_LOG_ROOT}/native_stderr.log"

		""" Holds Monitoring Policy attributes """
		self.__monPol={}
		self.__monPol['maximumStartupAttempts']=3
		self.__monPol['pingInterval']=60
		self.__monPol['pingTimeout']=300
		self.__monPol['autoRestart']="true"
		self.__monPol['nodeRestartState']="RUNNING"

		# Web Container settings
		self.__webContainerThreadPool={
			'inactivityTimeout':3500,
			'isGrowable':"false",
			'maximumSize':50,
			'minimumSize':10
		}
		self.__webContainer={
			'enableServletCaching':"false"
		}
		# Session manager settings
		self.__sessionMan={
			'sessionTimeout':30,
			'enableSecurityIntegration':"true",
			'enableCookies':"true"
		}
		# Cookie  settings
		self.__cookie={
			'name':"JSESSIONID",
			'domain':"",
			'maximumAge': -1,
			'path':"/",
			'secure':"false"
		}

		self.__webserverPluginSettings={
			'ConnectTimeout':5,
			'ExtendedHandshake':'false',
			'MaxConnections':-1,
			'Role':'PRIMARY',
			'ServerIOTimeout':60,
			'WaitForContinue':'false'
		}

		# PMI defaults
		self.__pmi={
			'enable' : "false",
			'initialSpecLevel' : "beanModule=N:cacheModule=N:connectionPoolModule=N:j2cModule=N:jvmRuntimeModule=N:orbPerfModule=N:servletSessionsModule=N:systemModule=N:threadPoolModule=N:transactionModule=N:webAppModule=N:webServicesModule=N:wlmModule=N:wsgwModule=N",
			'statisticSet' : "none",
		}
	
	def getAppManagerMbean(self):
		return AdminControl.queryNames( "type=ApplicationManager,process=%s,node=%s,*" % (self.getName(), self.getNode().getName()))

	def getOptAttributes(self):
		return self.__startPort.keys()+self.opt_attributes.keys() + self.__jvmAttr.keys() + self.__procExec.keys() + self.__procDef.keys() + self.__ioRedirect.keys() + [ "webContainerThreadPool%s%s" % (k[0].upper(),k[1:]) for k in self.__webContainerThreadPool.keys()] + self.__webContainer.keys() + self.__sessionMan.keys() + [ "pmi%s%s" % (k[0].upper(),k[1:]) for k in self.__pmi.keys()] + ["pluginSettings%s%s" % (k[0].upper(),k[1:]) for k in self.__webserverPluginSettings.keys()] + ["errorLog%s%s" % (k[0].upper(),k[1:]) for k in self.__nscaErrorLog.keys()] + ["accessLog%s%s" % (k[0].upper(),k[1:]) for k in self.__nscaAccessLog.keys()] + ["https%s%s" % (k[0].upper(),k[1:]) for k in self.__httpsAccessList.keys()] + ["cookie%s%s" % (k[0].upper(),k[1:]) for k in self.__cookie.keys()] + ["http%s%s" % (k[0].upper(),k[1:]) for k in self.__httpAccessList]

	def setParent(self, parent):
		"""# Set the parent of this object. Parent should be another WASConfig object. If parent is not an instance of a WASConfig object or not a valid parent for this object an exception is raised. See the list of valid parents."""
		WASConfig.setParent(self, parent)
		if parent.getConfigType=="Node": self.setNode(parent)

	def remove(self):
		WASConfig.remove(self)
		#ManagementScopedWASConfig.remove(self)

	def setManagementScope(self):
		self.managementScope=ManagementScope()
		self.managementScope.setScopeName("%s:(%s):%s" % (self.getNode().getManagementScope().getScopeName(),self.getConfigType().lower(),self.getName()))
		self.managementScope.setScopeType(self.getConfigType().lower())
		self.managementScope.setParent(self.getSecurity())
		self.managementScope.validate()
		self.logValue()

	def getContainmentPath(self):
		return "%s%s:%s/" % (self.getNode().getContainmentPath(),self.getConfigType(),self.getName())
		
	def validate(self):
		if self.getNode()=="":
			raise Exception("Specify node %s for %s" % (i, self.getConfigType()))
		WASConfig.validate(self)
		self.setManagementScope()
		
	def setNode(self, node):
		"""Specifies the Node that containes the AppServer. Only needs to be specified for AppServers that are cluster members, otherwise the Node is specified by the parent attribute."""
		if node is not None:
			self.ref_attributes['node']=node
			self.logValue()

	def getNode(self):
		return self.ref_attributes['node']
	def getNodeType(self):
		return "Node"

	def setDataReplicationDomain(self, dataReplicationDomain):
		"""Specifies the DataReplicationDomain that containes the AppServer. Only needs to be specified for AppServers that are cluster members, otherwise the DataReplicationDomain is specified by the parent attribute."""
		if dataReplicationDomain is not None:
			self.opt_attributes['dataReplicationDomain']=dataReplicationDomain
			self.logValue()
	def getDataReplicationDomain(self):
		return self.opt_attributes['dataReplicationDomain']

	def setClone(self, master):
		"""# Sets the name of the master server from which all settings will be copied."""
		if master is not None:self.opt_attributes['clone']=master
		self.logValue()

	def getClone(self):
		"""
		Gets the name of the master server from which all settings will be copied.
		"""
		return self.opt_attributes['clone']

	def setStartPort(self, startPort):
		"""# Specifies the starting port for the appserver. If not specified or 0 the highest available port will be automatically determined."""
		if startPort is not None:
			self.__startPort['startPort']=startPort
		self.logValue()
	def getStartPort(self):
		return int(self.__startPort['startPort'])

	def setNoSecurePort(self, noSecurePort):
		"""# noSecurePort - Specifies wether to remove the HTTPS transport chains. Defaults to false (keep the HTTPs chains)."""
		if noSecurePort is not None:
			self.opt_attributes['noSecurePort']=noSecurePort
		self.logValue()

	def getNoSecurePort(self):
		return self.opt_attributes['noSecurePort']

	def setSecurePortSSLConfig(self, securePortSSLConfig):
		if securePortSSLConfig is not None:
			self.opt_attributes['securePortSSLConfig']=securePortSSLConfig
		self.logValue()
	def getSecurePortSSLConfig(self):
		return self.opt_attributes['securePortSSLConfig']

	def setWeight(self, weight):
		"""# Set the cluster number weight. The weight should be an integer between 0 and 20. 0 means the server acts as a backup server only."""
		if weight is not None:
			if weight.isdigit():
				if int(weight)<0 and int(weight)>20:
					raise Exception("Weight should be number between 0 and 20")
			else:
				raise Exception("Weight should be number between 0 and 20")
			self.opt_attributes['weight']=weight
		self.logValue()

	def getWeight(self):
		return self.opt_attributes['weight']

	def setVerboseModeJNI(self, verboseModeJNI):
		"""# Specifies whether to use verbose debug output for native method invocation. The default is not to enable verbose Java Native Interface (JNI) activity."""
		if verboseModeJNI is not None: self.__jvmAttr['verboseModeJNI']=verboseModeJNI
		self.logValue()

	def getVerboseModeJNI(self):
		return self.__jvmAttr['verboseModeJNI']


	def setVerboseModeClass(self, verboseModeClass):
		"""# Specifies whether to use verbose debug output for class loading. The default is to not enable verbose class loading."""
		if verboseModeClass is not None: self.__jvmAttr['verboseModeClass']=verboseModeClass
		self.logValue()

	def getVerboseModeClass(self):
		return self.__jvmAttr['verboseModeClass']

	def setClasspath(self, classpath):
		"""# If you need to add a classpath to this field, enter each classpath entry into a separate table row. You do not have to add a colon or semicolon at the end of each entry."""
		if classpath is not None: self.__jvmAttr['classpath']=classpath
		self.logValue()

	def getClasspath(self):
		return self.__jvmAttr['classpath']

	def setInitialHeapSize(self, initialHeapSize):
		"""# Specifies, in megabytes, the initial heap size available to the JVM code. If this field is left blank, the default value 256 is used."""
		if initialHeapSize is not None: self.__jvmAttr['initialHeapSize']=initialHeapSize
		self.logValue()

	def getInitialHeapSize(self):
		return self.__jvmAttr['initialHeapSize']

	def setMaximumHeapSize(self, maximumHeapSize):
		"""# Specifies, in megabytes, the maximum heap size that is available to the JVM code. If this field is left blank, the default value 768 used."""
		if maximumHeapSize is not None: self.__jvmAttr['maximumHeapSize']=maximumHeapSize
		self.logValue()

	def getMaximumHeapSize(self):
		return self.__jvmAttr['maximumHeapSize']

	def setVerboseModeGarbageCollection(self, verboseModeGarbageCollection):
		"""# Specifies whether to use verbose debug output for garbage collection. The default is not to enable verbose garbage collection."""
		if verboseModeGarbageCollection is not None: self.__jvmAttr['verboseModeGarbageCollection']=verboseModeGarbageCollection
		self.logValue()

	def getVerboseModeGarbageCollection(self):
		return self.__jvmAttr['verboseModeGarbageCollection']

	def setRunHProf(self, runHProf):
		"""# Specifies whether to use HProf profiler support. To use another profiler, specify the custom profiler settings using the HProf Arguments setting. The default is not to enable HProf profiler support."""
		if runHProf is not None: self.__jvmAttr['runHProf']=runHProf
		self.logValue()

	def getRunHProf(self):
		return self.__jvmAttr['runHProf']

	def setHprofArguments(self, hprofArguments):
		"""# Specifies command-line profiler arguments to pass to the JVM code that starts the application server process. You can specify arguments when HProf profiler support is enabled."""
		if hprofArguments is not None: self.__jvmAttr['hprofArguments']=hprofArguments
		self.logValue()

	def getHprofArguments(self):
		return self.__jvmAttr['hprofArguments']

	def setBootClasspath(self, bootclasspath):
		"""# Specifies the booth classpath."""
		if bootclasspath is not None: self.__jvmAttr['bootClasspath']=bootclasspath
		self.logValue()

	def getBootClasspath(self):
		return self.__jvmAttr['bootClasspath']

	def setDebugMode(self, debugMode):
		"""# Specifies whether to run the JVM in debug mode. The default is to not enable debug mode support."""
		if debugMode is not None: self.__jvmAttr['debugMode']=debugMode
		self.logValue()

	def getDebugMode(self):
		return self.__jvmAttr['debugMode']

	def setDebugArgs(self, debugArgs):
		"""# Specifies command-line debug arguments to pass to the JVM code that starts the application server process."""
		if debugArgs is not None: self.__jvmAttr['debugArgs']=debugArgs
		self.logValue()

	def getDebugArgs(self):
		return self.__jvmAttr['debugArgs']

	def setGenericJvmArguments(self, genericJvmArguments):
		"""# Specifies command-line arguments to pass to the Java virtual machine code that starts the application server process."""
		if genericJvmArguments is not None: self.__jvmAttr['genericJvmArguments']=genericJvmArguments
		self.logValue()

	def getGenericJvmArguments(self):
		return self.__jvmAttr['genericJvmArguments']

	def setWorkingDirectory(self, workingDirectory):
		"""# Specifies the file system directory that the process uses as its current working directory. Defaults to ${USER_INSTALL_ROOT}."""
		if workingDirectory is not None: self.__procDef['workingDirectory']=workingDirectory
		self.logValue()

	def getWorkingDirectory(self):
		return self.__procDef['workingDirectory']

	def setUmask(self, umask):
		"""# Specifies the user mask under which the process runs (the # file-mode permission mask). Default is 022."""
		if umask is not None: self.__procExec['umask']=umask
		self.logValue()

	def getUmask(self):
		return self.__procExec['umask']

	def setStdoutFilename(self, stdoutFilename):
		"""# Specifies the file to which the standard output stream is directed. Defaults to ${SERVER_LOG_ROOT}/native_stdout.log."""
		if stdoutFilename is not None: self.__ioRedirect['stdoutFilename']=stdoutFilename
		self.logValue()

	def getStdoutFilename(self):
		return self.__ioRedirect['stdoutFilename']

	def setStderrFilename(self, stderrFilename):
		"""# Specifies the file to which the standard error stream is directed. Defaults to ${SERVER_LOG_ROOT}/native_stderr.log."""
		if stderrFilename is not None: self.__ioRedirect['stderrFilename']=stderrFilename
		self.logValue()

	def getStderrFilename(self):
		return self.__ioRedirect['stderrFilename']

	def setMaximumStartupAttempts(self, maximumStartupAttempts):
		"""# Specifies the maximum number of times to attempt to start the application server before giving up. Defaults to 3."""
		if maximumStartupAttempts is not None: self.__monPol['maximumStartupAttempts']=maximumStartupAttempts
		self.logValue()

	def setPingInterval(self, pingInterval):
		"""# in seconds the frequency of communication attempts between the parent process, such as the node agent, and the process it has spawned,	such as an application server. Defaults to 60."""
		if pingInterval is not None: self.__monPol['pingInterval']=pingInterval
		self.logValue()

	def getPingInterval(self):
		return self.__monPol['pingInterval']

	def setPingTimeout(self, pingTimeout):
		"""# When a parent process is spawning a child process, such as when a process manager spawns a server, the parent process pings the child process to see whether the child was spawned successfully. This value specifies the number of seconds that the parent process should wait (after pinging the child process) before assuming that the child process failed. Defaults to 300."""
		if pingTimeout is not None: self.__monPol['pingTimeout']=pingTimeout
		logger.debug("PingTimeout : %s" % self.__monPol['pingTimeout'])

	def getPingTimeout(self):
		return self.__monPol['pingTimeout']

	def setAutoRestart(self, autoRestart):
		"""# Specifies whether the process should restart automatically if it fails."""
		if autoRestart is not None: self.__monPol['autoRestart']=autoRestart
		self.logValue()

	def getAutoRestart(self):
		return self.__monPol['autoRestart']

	def setNodeRestartState(self, nodeRestartState):
		"""# The setting only applies for the Network Deployment product. It specifies the desired behavior of the servers after the node completely shuts down and restarts. Defaults to RUNNING. Valid values are RUNNING, STOPPED and PREVIOUS."""
		if nodeRestartState is not None:
			if nodeRestartState in [ "RUNNING", "PREVIOUS", "STOPPED" ]:
				self.__monPol['nodeRestartState']=nodeRestartState
			else:
				raise Exception("nodeRestart state should be RUNNING, PREVIOUS or STOPPED")
		self.logValue()

	def getNodeRestartState(self):
		return self.__monPol['nodeRestartState']

	def setEnableServletCaching(self, enableServletCaching):
		"""
		enableServletCaching - Specifies that if a servlet is
		invoked once and it generates output to be cached, a cache
		entry is created containing not only the output, but also
		side effects of the invocation. These side effects can
		include calls to other servlets or JavaServer Pages (JSP)
		files, as well as metadata about the entry, including
		timeout and entry priority information. Defaults to false.
		"""
		if enableServletCaching is not None: self.__webContainer['enableServletCaching']=enableServletCaching
		self.logValue()

	def getEnableServletCaching(self):
		return self.__webContainer['enableServletCaching']

	def setSessionTimeout(self, sessionTimeout):
		"""
		sessionTimeout - Specifies how long a session can go
		unused before it is no longer valid. Specify the value
		in minutes greater than or equal to two. Defaults to 30.
		"""
		if sessionTimeout is not None: self.__sessionMan['sessionTimeout']=sessionTimeout
		self.logValue()

	def setEnableSecurityIntegration(self, enableSecurityIntegration):
		if enableSecurityIntegration is not None: self.__sessionMan['enableSecurityIntegration']=enableSecurityIntegration
		self.logValue()

	def getEnableSecurityIntegration(self):
		return self.__sessionMan['enableSecurityIntegration']

	def setEnableCookies(self, enableCookies):
		if enableCookies is not None: self.__sessionMan['enableCookies']=enableCookies
		self.logValue()

	def getEnableCookies(self):
		return self.__sessionMan['enableCookies']

	def getSessionTimeout(self):
		return self.__sessionMan['sessionTimeout']

	def setCookieDomain(self, domain):
		if domain is not None:
			self.__cookie['domain']=domain
	def getCookieDomain(self ):
			return self.__cookie['domain']
	def setCookieName(self, name):
		if name is not None:
			self.__cookie['name']=name
	def getCookieName(self ):
			return self.__cookie['name']
	def setCookieMaximumAge(self,maximumAge):
		if maximumAge is not None:
			self.__cookie['maximumAge']=maximumAge
	def getCookieMaximumAge(self):
			return self.__cookie['maximumAge']
	def setCookiePath(self,path):
		if path is not None:
			self.__cookie['path']=path
	def getCookiePath(self):
		return self.__cookie['path']
	def setCookieSecure(self,secure):
		if secure is not None:
			self.__cookie['secure']=secure
	def getCookieSecure(self):
		return self.__cookie['secure']

	def setWebContainerThreadPoolInactivityTimeout(self, webContainerThreadPoolInactivityTimeout):
		"""# Specifies the number of milliseconds of inactivity that should elapse before a thread is reclaimed. A value of 0 indicates not to wait and a negative value (less than 0) means to wait forever. Defaults to 3500."""
		if webContainerThreadPoolInactivityTimeout is not None: self.__webContainerThreadPool['inactivityTimeout']=webContainerThreadPoolInactivityTimeout
		self.logValue()

	def getWebContainerThreadPoolInactivityTimeout(self):
		return self.__webContainerThreadPool['inactivityTimeout']

	def setWebContainerThreadPoolIsGrowable(self, webContainerThreadPoolIsGrowable):
		"""# Specifies whether the number of threads can increase beyond the maximum size configured for the thread pool. Defaults to false."""
		if webContainerThreadPoolIsGrowable is not None: self.__webContainerThreadPool['isGrowable']=webContainerThreadPoolIsGrowable
		self.logValue()

	def getWebContainerThreadPoolIsGrowable(self):
		return self.__webContainerThreadPool['isGrowable']

	def setWebContainerThreadPoolMaximumSize(self, webContainerThreadPoolMaximumSize):
		"""# Specifies the maximum number of threads to maintain in the default thread pool. Defaults to 50."""
		if webContainerThreadPoolMaximumSize is not None: self.__webContainerThreadPool['maximumSize']=webContainerThreadPoolMaximumSize
		self.logValue()

	def getWebContainerThreadPoolMaximumSize(self):
		return self.__webContainerThreadPool['maximumSize']

	def setWebContainerThreadPoolMinimumSize(self, webContainerThreadPoolMinimumSize):
		"""# Specifies the minimum number of threads to allow in the pool. Defaults to 10."""
		if webContainerThreadPoolMinimumSize is not None: self.__webContainerThreadPool['minimumSize']=webContainerThreadPoolMinimumSize
		self.logValue()

	def getWebContainerThreadPoolMinimumSize(self):
		return self.__webContainerThreadPool['minimumSize']

	def setVhost(self, vhost):
		"""# Specifies the default virtualhost to use."""
		self.opt_attributes['vhost']=vhost
		self.logValue()

	def getVhost(self):
		return self.opt_attributes['vhost']

	def setPluginSettingsConnectTimeout(self,connectTimeout):
		if connectTimeout is not None:
			self.__webserverPluginSettings['ConnectTimeout']=connectTimeout
		self.logValue()
	def getPluginSettingsConnectTimeout(self):
		return self.__webserverPluginSettings['ConnectTimeout']

	def setPluginSettingsExtendedHandshake(self, extendedHandshake):
		if extendedHandshake is not None:
			self.__webserverPluginSettings['ExtendedHandshake']=extendedHandshake
		self.logValue()
	def getPluginSettingsExtendedHandshake(self):
		return self.__webserverPluginSettings['ExtendedHandshake']

	def setPluginSettingsMaxConnections(self, maxConnections):
		if maxConnections is not None:
			self.__webserverPluginSettings['MaxConnections']=maxConnections
		self.logValue()
	def getPluginSettingsMaxConnections(self):
		return self.__webserverPluginSettings['MaxConnections']
		
	def setPluginSettingsRole(self,role):
		if role is not None and role in ['BACKUP','PIMARY']:
			self.__webserverPluginSettings['Role']=role
		self.logValue()
	def getPluginSettingsRole(self):
		return self.__webserverPluginSettings['Role']
	def setPluginSettingsServerIOTimeout(self, serverIOTimeout):
		if serverIOTimeout is not None:
			self.__webserverPluginSettings['ServerIOTimeout']=serverIOTimeout
		self.logValue()
	def getPluginSettingsServerIOTimeout(self):
		return self.__webserverPluginSettings['ServerIOTimeout']
	def setPluginSettingsWaitForContinue(self, waitForContinue):
		if waitForContinue is not None:
			self.__webserverPluginSettings['WaitForContinue']=waitForContinue
		self.logValue()
	def getPluginSettingsWaitForContinue(self):
		return self.__webserverPluginSettings['WaitForContinue']

	def setPmiEnable(self, pmiEnable):
		"""# Specifies the enable PMI."""
		if pmiEnable is not None:
			self.__pmi['enable']=pmiEnable
		self.logValue()

	def getPmiEnable(self):
		return self.__pmi['enable']

	def setPmiInitialSpecLevel(self, pmiInitialSpecLevel):
		"""# Specifies the initial PMI spec level."""
		self.__pmi['initialSpecLevel']=pmiInitialSpecLevel 
		self.logValue()

	def getPmiInitialSpecLevel(self):
		return self.__pmi['initialSpecLevel']

	def setPmiStatisticSet(self, statisticSet):
		if statisticSet is not None:
			self.__pmi['statisticSet']=statisticSet
		self.logValue()
	def getPmiStatisticSet(self):
		return self.__pmi['statisticSet']

	def setEnableNscaLogs(self, enableNscaLogs):
		if enableNscaLogs is not None:
			self.opt_attributes['enableNscaLogs']=enableNscaLogs
		self.logValue()
	def getEnableNscaLogs(self):
		return self.opt_attributes['enableNscaLogs']

	def setAccessLogFormat(self, accessLogFormat):
		if accessLogFormat is not None:
			self.opt_attributes['accessLogFormat']=accessLogFormat
		self.logValue()
	def getAccessLogFormat(self):
		return self.opt_attributes['accessLogFormat']

	def setEnableAccessLogging(self, enableAccessLogging):
		if enableAccessLogging is not None:
			self.opt_attributes['enableAccessLogging']=enableAccessLogging
		self.logValue()
	def getEnableAccessLogging(self):
		return self.opt_attributes['enableAccessLogging']

	def setEnableErrorLogging(self, enableErrorLogging):
		if enableErrorLogging is not None:
			self.opt_attributes['enableErrorLogging']=enableErrorLogging
		self.logValue()
	def getEnableErrorLogging(self):
		return self.opt_attributes['enableErrorLogging']

	def setErrorLogLevel(self, errorLogLevel):
		if errorLogLevel is not None:
			self.opt_attributes['errorLogLevel']=errorLogLevel
		self.logValue()
	def getErrorLogLevel(self):
		return self.opt_attributes['errorLogLevel']

	def setAccessLogFilePath(self, filePath):
		if filePath is not None:
			self.__nscaAccessLog['filePath']=filePath
		self.logValue()
	def getAccessLogFilePath(self):
		return self.__nscaAccessLog['filePath']

	def setAccessLogMaximumBackupFiles(self, maximumBackupFiles):
		if maximumBackupFiles is not None:
			self.__nscaAccessLog['maximumBackupFiles']=maximumBackupFiles
		self.logValue()
	def getAccessLogMaximumBackupFiles(self):
		return self.__nscaAccessLog['maximumBackupFiles']

	def setAccessLogMaximumSize(self, maximumSize):
		if maximumSize is not None:
			self.__nscaAccessLog['maximumSize']=maximumSize
		self.logValue()
	def getAccessLogMaximumSize(self):
		return self.__nscaAccessLog['maximumSize']

	def setErrorLogMaximumBackupFiles(self, maximumBackupFiles):
		if maximumBackupFiles is not None:
			self.__nscaErrorLog['maximumBackupFiles']=maximumBackupFiles
		self.logValue()
	def getErrorLogMaximumBackupFiles(self):
		return self.__nscaErrorLog['maximumBackupFiles']

	def setErrorLogMaximumSize(self, maximumSize):
		if maximumSize is not None:
			self.__nscaErrorLog['maximumSize']=maximumSize
		self.logValue()
	def getErrorLogMaximumSize(self):
		return self.__nscaErrorLog['maximumSize']

	def setErrorLogFilePath(self, filePath):
		if filePath is not None:
			self.__nscaErrorLog['filePath']=filePath
		self.logValue()
	def getErrorLogFilePath(self):
		return self.__nscaErrorLog['filePath']

	def setHttpAddressExcludeList(self, addressExcludeList):
		if addressExcludeList is not None:
			for i in addressExcludeList.split(","):
				self.__httpAddressExcludeList.append(i)
		self.logValue()
	def getHttpAddressExcludeList(self):
		return self.__httpAddressExcludeList

	def setHttpAddressIncludeList(self, addressIncludeList):
		if addressIncludeList is not None:
			for i in addressIncludeList.split(","):
				self.__httpAddressIncludeList.append(i)
		self.logValue()
	def getHttpAddressIncludeList(self):
		return self.__httpAddressIncludeList

	def setHttpHostNameExcludeList(self, hostNameExcludeList):
		if hostNameExcludeList is not None:
			for i in hostNameExcludeList.split(","):
				self.__httpHostNameExcludeList.append(i)
		self.logValue()
	def getHttpHostNameExcludeList(self):
		return self.__httpHostNameExcludeList

	def setHttpHostNameIncludeList(self, hostNameIncludeList):
		if hostNameIncludeList is not None:
			for i in hostNameIncludeList.split(","):
				self.__httpHostNameIncludeList.append(i)
		self.logValue()
	def getHttpHostNameIncludeList(self):
		return self.__httpHostNameIncludeList

	def setHttpsAddressExcludeList(self, addressExcludeList):
		if addressExcludeList is not None:
			self.__httpsAccessList['addressExcludeList']=addressExcludeList
		self.logValue()
	def getHttpsAddressExcludeList(self):
		return self.__httpsAccessList['addressExcludeList']

	def setHttpsAddressIncludeList(self, addressIncludeList):
		if addressIncludeList is not None:
			self.__httpsAccessList['addressIncludeList']=addressIncludeList
		self.logValue()
	def getHttpsAddressIncludeList(self):
		return self.__httpsAccessList['addressIncludeList']

	def setHttpsHostNameExcludeList(self, hostNameExcludeList):
		if hostNameExcludeList is not None:
			self.__httpsAccessList['hostNameExcludeList']=hostNameExcludeList
		self.logValue()
	def getHttpsHostNameExcludeList(self):
		return self.__httpsAccessList['hostNameExcludeList']

	def setHttpsHostNameIncludeList(self, hostNameIncludeList):
		if hostNameIncludeList is not None:
			self.__httpsAccessList['hostNameIncludeList']=hostNameIncludeList
		self.logValue()
	def getHttpsHostNameIncludeList(self):
		return self.__httpsAccessList['hostNameIncludeList']

	def __modifyLogFiles(self):
		"""
		This function modifies the WAS logging settings (stream parameters).
		"""
		serverID=self.configID
		streamParams = \
		[\
		["baseHour", 1], \
		["formatWrites", "true"], \
		["maxNumberOfBackupFiles", 90], \
		["messageFormatKind", "BASIC"], \
		["rolloverPeriod", 24], \
		["rolloverSize", 1], \
		["rolloverType", "TIME"], \
		["suppressStackTrace", "false"], \
		["suppressWrites", "false"]\
		]
		outputStreamParams = streamParams
		outputStreamParams.append( ["fileName", "${SERVER_LOG_ROOT}/SystemOut.log"] )
		outputStreamRedirect = AdminConfig.showAttribute( serverID, "outputStreamRedirect" )
		if ( (outputStreamRedirect == "") ) : raise Exception("outputStreamRedirect is empty, before calling AdminConfig.modify.")
		AdminConfig.modify( outputStreamRedirect, outputStreamParams )
		errorStreamParams = streamParams
		errorStreamParams.append( ["fileName", "${SERVER_LOG_ROOT}/SystemErr.log"] )
		errorStreamRedirect = AdminConfig.showAttribute( serverID, "errorStreamRedirect" )
		if ( (errorStreamRedirect == "") ) : raise Exception("errorStreamRedirect is empty, before calling AdminConfig.modify.")
		AdminConfig.modify( errorStreamRedirect, errorStreamParams )
		# Activity log
		RASLoggingService = AdminConfig.list( "RASLoggingService", serverID )
		serviceLogId = AdminConfig.showAttribute( RASLoggingService, "serviceLog" )
		if ( (serviceLogId == "") ) : raise Exception("sericeLogId is empty, before calling AdminConfig.modify.")
		AdminConfig.modify( serviceLogId, \
						  [\
						   ["name", "${SERVER_LOG_ROOT}/activity.log"], \
						   ["size", 10], \
						   ["enabled", "true"]\
						  ] )

	def __findStartPort(self):
		"""
		Find the highest BOOTSTRAP port in use. BOOTSTRAP port is the second
		port set so add 18 to return value.

		@return new highest start port or -1 if nothing found
		"""
		maxstartport=-1
		seList = Util.wslist(AdminConfig.list('ServerEntry',self.getNode().getConfigID()))

		for se in seList:
			if len(se) == 0: continue
			name=AdminConfig.showAttribute(se, "serverName")
			if name==self.getName(): continue
			specialEndpointString = AdminConfig.showAttribute( se, "specialEndpoints" )
			specialEndpointList = Util.wslist( specialEndpointString )
			for specialEndpoint in specialEndpointList:
				endPointName = AdminConfig.showAttribute( specialEndpoint, "endPointName" )
				endPoint=None
				if name=="nodeagent" and endPointName=="BOOTSTRAP_ADDRESS":
					endPoint = AdminConfig.showAttribute( specialEndpoint, "endPoint" )
				elif endPointName=="WC_defaulthost":
					endPoint = AdminConfig.showAttribute( specialEndpoint, "endPoint" )
				if endPoint is not None:
					bsport=AdminConfig.showAttribute(endPoint, 'port')
					if bsport > maxstartport:
						maxstartport=bsport
		maxstartport=int(maxstartport)+20
		logger.debug("Found startport for %s: %s" % (self.getName(), str(maxstartport)))
		return maxstartport

	def __changeAndRemovePorts(self):
		"""
		This function modifies the ports for the specified server id on the specified node.
		The ports are numbered starting at the number specified by startPort.
		It also removes the wc_adminhost and wc_adminhost_secure ports.
		The following ports are modified:
		"BOOTSTRAP_ADDRESS", "WC_defaulthost", "WC_defaulthost_secure", "SOAP_CONNECTOR_ADDRESS", "DCS_UNICAST_ADDRESS",
		"ORB_LISTENER_ADDRESS", "SAS_SSL_SERVERAUTH_LISTENER_ADDRESS","CSIV2_SSL_MUTUALAUTH_LISTENER_ADDRESS","CSIV2_SSL_SERVERAUTH_LISTENER_AD
		DRESS",
		"SIB_ENDPOINT_ADDRESS","SIB_ENDPOINT_SECURE_ADDRESS","SIB_MQ_ENDPOINT_ADDRESS","SIB_MQ_ENDPOINT_SECURE_ADDRESS","SIP_DEFAULTHOST",
		"SIP_DEFAULTHOST_SECURE", "SAS_SSL_SERVERAUTHLISTENER"
		"""
		node=self.getNode()
		nodeID=self.getNode().getConfigID()
		startPort=self.getStartPort()
		if startPort==0: startPort=self.__findStartPort()
		changePortDict = \
		{\
		"WC_defaulthost" : 0,\
		"WC_defaulthost_secure" : 1,\
		"BOOTSTRAP_ADDRESS" : 2, \
		"SOAP_CONNECTOR_ADDRESS" : 3, \
		"DCS_UNICAST_ADDRESS" : 4, \
		"ORB_LISTENER_ADDRESS" : 5, \
		"SAS_SSL_SERVERAUTH_LISTENER_ADDRESS" : 6, \
		"CSIV2_SSL_MUTUALAUTH_LISTENER_ADDRESS" : 7, \
		"CSIV2_SSL_SERVERAUTH_LISTENER_ADDRESS" : 8, \
		"SIB_ENDPOINT_ADDRESS" : 9, \
		"SIB_ENDPOINT_SECURE_ADDRESS": 10, \
		"SIB_MQ_ENDPOINT_ADDRESS": 11, \
		"SIB_MQ_ENDPOINT_SECURE_ADDRESS": 12, \
		"SIP_DEFAULTHOST" : 13, \
		"SIP_DEFAULTHOST_SECURE" : 14, \
		"IPC_CONNECTOR_ADDRESS" : 15, \
		}

		# Remove admin chains
		adminChainNameList = ["WCInboundAdmin", "WCInboundAdminSecure" ]
		removePortList = ["WC_adminhost", "WC_adminhost_secure"]
		if self.getNoSecurePort()=="true":
			logger.debug("Removing secure port")
			removePortList.append("WC_defaulthost_secure")
			del changePortDict["WC_defaulthost_secure"]
			adminChainNameList.append("WCInboundDefaultSecure")
			adminChainNameList.append("HttpQueueInboundDefaultSecure")
		serverEntryList = Util.wslist(AdminConfig.list( "ServerEntry", nodeID ))
		name = self.getName()
		logger.info("Change ports on server : %s" % name)
		serverEntryID = None
		for anID in serverEntryList:
			serverName = AdminConfig.showAttribute( anID, "serverName" )
			if ( serverName == name ):
				serverEntryID = anID
				break
		if ( serverEntryID == None ):
			raise Exception( "Server:no serverEntry matching name : " + name + " found" )
		specialEndpointString = AdminConfig.showAttribute( serverEntryID, "specialEndpoints" )
		specialEndpointList = Util.wslist( specialEndpointString )
		changePortDictKeys = changePortDict.keys()
		for specialEndpoint in specialEndpointList:
			endPointName = AdminConfig.showAttribute( specialEndpoint, "endPointName" )
			if ( endPointName in changePortDictKeys ):
				endPoint = AdminConfig.showAttribute( specialEndpoint, "endPoint" )
				offset = startPort + changePortDict[endPointName]
				host=["host", AdminConfig.showAttribute(endPoint,"host")]
				port = ["port", str( offset )]
				if ( (endPoint == "") ) : raise Exception("endPoint is empty, before calling AdminConfig.modify.")
				AdminConfig.modify( endPoint, [host, port] )
			elif (endPointName in removePortList):
				if ( (specialEndpoint == "") ) : raise Exception("specialEndpoint is empty, before calling AdminConfig.remove.")
				AdminConfig.remove(specialEndpoint)
		# Get list of all chains in server
		chainList = Util.wslist(AdminConfig.list( "Chain", self.configID ))
		for chain in chainList:
			if AdminConfig.showAttribute(chain, "name" ) in adminChainNameList:
				AdminTask.deleteChain( chain, "[-deleteChannels true]" )
		logger.info("Succesfully removed admin chains on %s" % self.getName())

	def getStatistics(self):
		stats=[]
		if self.isRunning():
			serverJVM=AdminControl.completeObjectName('type=JVM,process=%s,node=%s,cell=%s,*' % (self.getName(),self.getNode().getName(),self.getCell().getName()))	
			if serverJVM=="": raise Exception("Could not get JVM mbean for : %s" % self.getName())
			serverJVMO=AdminControl.makeObjectName(serverJVM)
			perf=AdminControl.completeObjectName('type=Perf,process=%s,node=%s,cell=%s,*' % (self.getName(),self.getNode().getName(),self.getCell().getName()))	
			if perf=="": raise Exception("PMI not enabled for : %s" % self.getName())
			perfO=AdminControl.makeObjectName(perf)
			s=AdminControl.invoke_jmx(perfO,'getStatsObject',[serverJVMO,java.lang.Boolean('false')],['javax.management.ObjectName','java.lang.Boolean'])
			if s is not None:
				serverStat=HeapStat()
				serverStat.setCriticalThreshold(self.getHeapCriticalThreshold())
				serverStat.setWarningThreshold(self.getHeapWarningThreshold())
				serverStat.setStatus([s])
				stats.append(serverStat)
				serverStat=CPUStat()
				serverStat.setCriticalThreshold(self.getCpuCriticalThreshold())
				serverStat.setWarningThreshold(self.getCpuWarningThreshold())
				serverStat.setStatus([s])
				stats.append(serverStat)

			serverO=AdminControl.makeObjectName(self.getMbean())
			substats=AdminControl.invoke_jmx(perfO,'getStatsObject',[serverO,java.lang.Boolean('true')],['javax.management.ObjectName','java.lang.Boolean'])
			# WebContainer statistics
			if substats is not None:
				s=substats.getStats('threadPoolModule').getStats('WebContainer')
				if s is not None:
					webContainerStat=WebContainerActiveStat()
					webContainerStat.setCriticalThreshold(self.getWebContainerActiveCriticalThreshold())
					webContainerStat.setWarningThreshold(self.getWebContainerActiveWarningThreshold())
					webContainerStat.setStatus([s])
					stats.append(webContainerStat)
					webContainerStat=WebContainerConcurrentHungThreadCount()
					webContainerStat.setCriticalThreshold(self.getWebContainerHungThreadCriticalThreshold())
					webContainerStat.setWarningThreshold(self.getWebContainerHungThreadWarningThreshold())
					webContainerStat.setStatus([s])
					stats.append(webContainerStat)
				
				s=substats.getStats('servletSessionsModule')
				if s is not None:
					sessionStat=LiveSessionStat()
					sessionStat.setCriticalThreshold(self.getLiveSessionsCriticalThreshold())
					sessionStat.setWarningThreshold(self.getLiveSessionsWarningThreshold())
					sessionStat.setStatus([s])
					stats.append(sessionStat)
		return stats
			#WASConfig.getStatistics(self)

	def setHeapWarningThreshold(self, warningThreshold):
		"""# Specifies Nagios monitoring warning threshold for the heap usage in percent."""
		if warningThreshold is not None: self.opt_attributes['heapWarningThreshold']=warningThreshold
		self.logValue()

	def getHeapWarningThreshold(self):
		return self.opt_attributes['heapWarningThreshold']

	def setHeapCriticalThreshold(self, criticalThreshold):
		"""# Specifies Nagios monitoring critical threshold for the heap usage in percent."""
		if criticalThreshold is not None: self.opt_attributes['heapCriticalThreshold']=criticalThreshold
		self.logValue()

	def getHeapCriticalThreshold(self):
		return self.opt_attributes['heapCriticalThreshold']

	def setCpuWarningThreshold(self, warningThreshold):
		"""# Specifies Nagios monitoring warning threshold for the cpu usage in percent."""
		if warningThreshold is not None: self.opt_attributes['cpuWarningThreshold']=warningThreshold
		self.logValue()

	def getCpuWarningThreshold(self):
		return self.opt_attributes['cpuWarningThreshold']

	def setCpuCriticalThreshold(self, criticalThreshold):
		"""# Specifies Nagios monitoring critical threshold for the cpu usage in percent."""
		if criticalThreshold is not None: self.opt_attributes['cpuCriticalThreshold']=criticalThreshold
		self.logValue()

	def getCpuCriticalThreshold(self):
		return self.opt_attributes['cpuCriticalThreshold']

	def setWebContainerActiveWarningThreshold(self, warningThreshold):
		"""# Specifies Nagios monitoring warning threshold for the web container usage in percent."""
		if warningThreshold is not None: self.opt_attributes['webContainerActiveWarningThreshold']=warningThreshold
		self.logValue()

	def getWebContainerActiveWarningThreshold(self):
		return self.opt_attributes['webContainerActiveWarningThreshold']

	def setWebContainerActiveCriticalThreshold(self, criticalThreshold):
		"""# Specifies Nagios monitoring critical threshold for the web container usage in percent."""
		if criticalThreshold is not None: self.opt_attributes['webContainerActiveCriticalThreshold']=criticalThreshold
		self.logValue()

	def getWebContainerActiveCriticalThreshold(self):
		return self.opt_attributes['webContainerActiveCriticalThreshold']

	def setWebContainerHungThreadWarningThreshold(self, warningThreshold):
		"""# Specifies Nagios monitoring hung thread warning threshold for the web container usage in percent."""
		if warningThreshold is not None: self.opt_attributes['webContainerHungThreadWarningThreshold']=warningThreshold
		self.logValue()

	def getWebContainerHungThreadWarningThreshold(self):
		return self.opt_attributes['webContainerHungThreadWarningThreshold']

	def setWebContainerHungThreadCriticalThreshold(self, criticalThreshold):
		"""# Specifies Nagios monitoring hung thread critical threshold for the web container usage in percent."""
		if criticalThreshold is not None: self.opt_attributes['webContainerHungThreadCriticalThreshold']=criticalThreshold
		self.logValue()

	def getWebContainerHungThreadCriticalThreshold(self):
		return self.opt_attributes['webContainerHungThreadCriticalThreshold']

	def setLiveSessionsWarningThreshold(self, warningThreshold):
		"""# Specifies Nagios monitoring live sesion thread warning threshold in absolute numbers."""
		if warningThreshold is not None: self.opt_attributes['liveSessionsWarningThreshold']=warningThreshold
		self.logValue()

	def getLiveSessionsWarningThreshold(self):
		return self.opt_attributes['liveSessionsWarningThreshold']

	def setLiveSessionsCriticalThreshold(self, criticalThreshold):
		"""# Specifies Nagios monitoring live sesion thread critical threshold in absolute numbers."""
		if criticalThreshold is not None: self.opt_attributes['liveSessionsCriticalThreshold']=criticalThreshold
		self.logValue()

	def getLiveSessionsCriticalThreshold(self):
		return self.opt_attributes['liveSessionsCriticalThreshold']

	def getNagiosStatus(self):
		WASConfig.getNagiosStatus(self)
		status=[]
		for i in self.getStatistics():
			status.append(i.getStatus())
		return status

	def stop(self):
		logger.info("Stopping Server : %s" % self.getName())
		if self.isRunning(): 
			AdminControl.stopServer(self.getName(), self.getNode().getName())
		else:
			logger.info("Server already stopped")
		logger.info("Server stopped: %s" % self.getName())

	def start(self):
		logger.info("Starting Server : %s" % self.getName())
		if not self.isRunning(): 
			AdminControl.startServer(self.getName(), self.getNode().getName())
		else:
			logger.info("Server already started")
		logger.info("Server started: %s" % self.getName())

	def create(self):
		""" 
		Create the appserver in WAS
		"""
		WASConfig.create(self)

		if self.getParent().getConfigType() == "ServerCluster":
			# Create cluster member
			if AdminConfig.createClusterMember(self.getParent().getConfigID(), self.getNode().getConfigID(), '[[memberName %s] [weight %s]]' % (self.getName(), self.getWeight())) != "":
				logger.info("Succesfully created cluster member server %s" % self.getName())
			else:
				raise Exception("Error creating server %s" % self.getName())
		else:
			if AdminConfig.create("Server", self.getParent().getConfigID(), '[[name %s]]' % self.getName()) != "":
				self.logCreate()
			else:
				raise Exception("Error creating server %s" % self.getName())
		self.configID=AdminConfig.getid(self.getContainmentPath())
		if self.configID=='': raise Exception("Failed to get server ID from configuration")
		logger.debug("Got serverID: %s" % self.configID)

		# Change the location of the logfiles
		self.__modifyLogFiles()
		self.__changeAndRemovePorts()

		# Setup JVM properties server
		jvmId = AdminConfig.list('JavaVirtualMachine', self.getConfigID() )
		logger.debug("Setting JVM attributes: %s" % Util.dictToList(self.__jvmAttr))
		AdminConfig.modify(jvmId, Util.dictToList(self.__jvmAttr))

		procExecId = AdminConfig.list('ProcessExecution', self.getConfigID() )
		logger.debug("Setting ProcessExecution attributes: %s" % Util.dictToList(self.__procExec))
		AdminConfig.modify(procExecId, Util.dictToList(self.__procExec))

		ioRedirectId = AdminConfig.list('OutputRedirect', self.getConfigID() )
		logger.debug("Setting OutputRedirect attributes: %s" % Util.dictToList(self.__ioRedirect))
		AdminConfig.modify(ioRedirectId, Util.dictToList(self.__ioRedirect))

		monPolId = AdminConfig.list('MonitoringPolicy', self.getConfigID() )
		logger.debug("Setting MonitoringPolicy attributes: %s" % Util.dictToList(self.__monPol))
		AdminConfig.modify(monPolId, Util.dictToList(self.__monPol))

		procDefId = AdminConfig.list('JavaProcessDef', self.getConfigID() )
		logger.debug("Setting ProcessDefinition attributes: %s" % Util.dictToList(self.__procDef))
		AdminConfig.modify(procDefId, Util.dictToList(self.__procDef))

		# Modify WebContainer
		wcID=AdminConfig.list('WebContainer', self.getConfigID())
		if self.getVhost() is not None:
			AdminConfig.modify( wcID, [ ["enableServletCaching", self.getEnableServletCaching()],["defaultVirtualHostName", self.getVhost() ]])
		logger.info("Succesfully set the web container properties on server %s " % (self.getName()))

		# Modify NSCA logging
		if self.getEnableNscaLogs()!="false":
			hals=AdminConfig.list('HTTPAccessLoggingService',self.getConfigID())
			AdminConfig.modify(hals,[ 
				['enable',self.getEnableNscaLogs()],
				['accessLogFormat',self.getAccessLogFormat()],
				['enableAccessLogging',self.getEnableAccessLogging()],
				['enableErrorLogging',self.getEnableErrorLogging()],
				['errorLogLevel',self.getErrorLogLevel()]
				])
			httpErrorLog=AdminConfig.showAttribute(hals, 'errorLog')
			httpAccessLog=AdminConfig.showAttribute(hals, 'accessLog')
			AdminConfig.modify(httpErrorLog,Util.dictToList(self.__nscaErrorLog))
			AdminConfig.modify(httpAccessLog,Util.dictToList(self.__nscaAccessLog))
			logger.info("Succesfully configured NCSA Logging settings")

		chains=Util.wslist(AdminConfig.list('Chain',self.getConfigID()))
		if self.getNoSecurePort()=="false" and self.getSecurePortSSLConfig()!="":
			for i in chains:
				if AdminConfig.showAttribute(i, 'name')=="HttpQueueInboundDefaultSecure":
					for j in Util.wslist(AdminConfig.showAttribute(i,'transportChannels')):
						if AdminConfig.getObjectType(j)=="SSLInboundChannel":
							AdminConfig.modify(j, [['sslConfigAlias', self.getSecurePortSSLConfig()]])
							logger.info("Succesfully set SSL Transport Channel SSL Config")
					break

		for i in chains:
			if AdminConfig.showAttribute(i, 'name')=="HttpQueueInboundDefault":
				for j in Util.wslist(AdminConfig.showAttribute(i,'transportChannels')):
					if AdminConfig.getObjectType(j)=="TCPInboundChannel":
						for h in self.__httpAccessList:
							cmd='accessList=self.getHttp%s()' % (h[0].upper()+h[1:])
							exec cmd
							for a in accessList:
								AdminConfig.modify(j, [[h, a ]])
								logger.info("Succesfully set HTTP TCP Access List : %s" % h)
					break
			if AdminConfig.showAttribute(i, 'name')=="HttpQueueInboundDefaultSecure":
				for j in Util.wslist(AdminConfig.showAttribute(i,'transportChannels')):
					if AdminConfig.getObjectType(j)=="TCPInboundChannel":
						AdminConfig.modify(j, Util.dictToList(self.__httpsAccessList))
						logger.info("Succesfully set HTTPS TCP Access List")
					break

		# Modify Session Manager
		smID=AdminConfig.list('SessionManager', wcID)
		AdminConfig.modify(smID, [["enableSecurityIntegration", self.getEnableSecurityIntegration()]])
		AdminConfig.modify(smID, [["enableCookies", self.getCookies()]])
		tpID=AdminConfig.list('TuningParams', smID)
		AdminConfig.modify(tpID, [['invalidationTimeout', self.getSessionTimeout()]])
		logger.info("Succesfully set the session timeout on server %s to : %s" % (self.getName(), self.getSessionTimeout()))

		cookieID=AdminConfig.list('Cookie',wcID)
		AdminConfig.modify(cookieID, Util.dictToList(self.__cookie))
		logger.info("Succesfully modified cookie settings on server %s" % self.getName())

		if self.getDataReplicationDomain() != "":
			AdminConfig.modify(smID, [["sessionPersistenceMode", "DATA_REPLICATION"]])
			AdminConfig.create('DRSSettings', smID, [['messageBrokerDomainName', self.getDataReplicationDomain()]])
			logger.info("Succesfully configured the session replication domain %s on : %s" % (self.getDataReplicationDomain(), self.getName()))

		# Modify Thread Pool settings
		pools=Util.wslist(AdminConfig.list('ThreadPool', self.configID))
		thpID=""
		# Get the webcontainer ThreadPool
		if len(pools) > 0:
			for p in pools:
				if AdminConfig.showAttribute(p, "name") == "WebContainer":
					thpID=p
					break
		else:
			raise Exception("ThreadPools are missing, an error occured creating the server")
		if thpID=="": raise Exception("WebContainer threadpool is missing on %s", self.getName())
		AdminConfig.modify(thpID, Util.dictToList(self.__webContainerThreadPool))
		logger.info("Succesfully modified webContainer attributes on %s" % self.getName())
		
		# Modify WebServerPluginSettings
		plugincfg=AdminConfig.list('WebserverPluginSettings', self.configID)
		AdminConfig.modify(plugincfg, Util.dictToList(self.__webserverPluginSettings))
		logger.info("Succesfully set the web server plugin properties on server %s " % (self.getName()))

		# Modify PMI data
		pmiServiceRoot = Util.wslist(AdminConfig.list( "PMIService", self.configID ))[0]
		logger.debug("Setting PMI attributes: %s" % Util.dictToList(self.__pmi))
		if ( (pmiServiceRoot == "") ) : raise Exception("pmiServiceRoot is empty, before calling AdminConfig.modify.")
		AdminConfig.modify( pmiServiceRoot, Util.dictToList(self.__pmi) )

	def clone(self):
		"""
		Return a clone of the server object. This method is
		onessecary since Jython copy functions copy.copy and
		copy.deepcopy are not sufficient. Name, node and scope
		are not set as it is expected that these will be
		changed by the caller.
		"""
		logger.debug("Cloning server : %s" % self.getName())
		clone=Server(self.scope)
		clone.setName(self.getName())
		clone.setNode(self.getNode())
		clone.setNoSecurePort(self.getNoSecurePort())
		clone.setWeight(self.getWeight())
		clone.setVhost(self.getVhost())
		clone.setVerboseModeClass(self.setVerboseModeClass())
		clone.setClasspath(self.setClasspath())
		clone.setInitialHeapSize(self.setInitialHeapSize())
		clone.setMaximumHeapSize(self.setMaximumHeapSize())
		clone.setBootClasspath(self.setBootClasspath())
		clone.setVerboseModeGarbageCollection(self.setVerboseModeGarbageCollection())
		clone.setRunHProf(self.setRunHProf())
		clone.setHprofArguments(self.setHprofArguments())
		clone.setDebugMode(self.setDebugMode())
		clone.setDebugArgs(self.setDebugArgs())
		clone.setGenericJvmArguments(self.setGenericJvmArguments())
		clone.setVerboseModeJNI(self.setVerboseModeJNI())
		clone.setUmask(self.getUmask()())
		clone.setWorkingDirectory(self.getWorkingDirectory()())
		clone.setStdoutFilename(self.setStdoutFilename())
		clone.setStderrFilename(self.setStderrFilename())
		clone.setMaximumStartupAttempts(self.setMaximumStartupAttempts())
		clone.setPingInterval(self.setPingInterval())
		clone.setPingTimeout(self.setPingTimeout())
		clone.setAutoRestart(self.setAutoRestart())
		clone.setNodeRestartState(self.setNodeRestartState())
		clone.setWebContainerThreadPoolInactivityTimeout(self.setWebContainerThreadPoolInactivityTimeout())
		clone.setWebContainerThreadPoolIsGrowable(self.setWebContainerThreadPoolIsGrowable())
		clone.setWebContainerThreadPoolMaximumSize(self.setWebContainerThreadPoolMaximumSize())
		clone.setWebContainerThreadPoolMinimumSize(self.setWebContainerThreadPoolMinimumSize())
		clone.setWebContainerThreadPoolEnableServletCaching(self.setWebContainerThreadPoolEnableServletCaching())
		clone.setSessionTimeout(self.setSessionTimeout())
		clone.setEnableSecurityIntegration(self.setEnableSecurityIntegration())
		clone.setPmiEnabled(self.setPmiEnabled())
		clone.setPmiInitialSpecLevel(self.setPmiInitialSpecLevel())

		for i in self.getChildren():
			n=i.clone()
			n.setParent(clone)
			n.validate()

		return clone
