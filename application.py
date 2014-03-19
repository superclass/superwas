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

# Application Classes
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-08-28 10:24:55 +0200 (wo, 28 aug 2013) $
# $Id: application.py 465 2013-08-28 08:24:55Z andre $
class TaskInfoData:
	def __init__(self, taskInfo):
		self.__taskInfo=taskInfo

	def getKey(self, key):
		if self.__taskInfo.has_key(key):
			return self.__taskInfo[key]
		else:
			logger.debug("Taskinfo key %s missing returning empty" % key)
			return ""

class WebServerTarget(WASConfig):
	level=6
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["Application"]
		self.ref_attributes={
			'webServer':None
		}

	def setWebServer(self, webServer):
		if webServer is not None and isinstance(webServer, WebServer):
			self.ref_attributes['webServer']=webServer
		else:
			raise Exception("Invalid WebServer")
		self.logValue()

	def getWebServer(self):
		return self.ref_attributes['webServer']

	def getWebServerType(self):
		return "WebServer"

	def getConfigType(self):
		return ""

	def setConfigID(self):
		pass

	def getContainmentPath(self):
		return ""

	def create(self):
		pass
	def remove(self):
		pass

class Role(WASConfig):
	level=6
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["Application"]
		self.opt_attributes={
			'user':'',
			'group':'',
			'everyone':'false',
			'allauthuser':'false'
		}

	def setUser(self, user):
		if user is not None: self.opt_attributes['user']=user
		self.logValue()
	def getUser(self):
		return self.opt_attributes['user']

	def setGroup(self, group):
		if group is not None: self.opt_attributes['group']=group
		self.logValue()
	def getGroup(self):
		return self.opt_attributes['group']

	def setEveryone(self, everyone):
		if everyone is not None: self.opt_attributes['everyone']=everyone
		self.logValue()
	def getEveryone(self):
		return self.opt_attributes['everyone']

	def setAllauthuser(self, allauthuser):
		if allauthuser is not None: self.opt_attributes['allauthuser']=allauthuser
		self.logValue()
	def getAllauthuser(self):
		return self.opt_attributes['allauthuser']

	def getOption(self):
		return "-MapRolesToUsers"

	def getMapping(self):
		roleMapping=[[self.getName(),self.getEveryone(),self.getAllauthuser(),self.getUser(),self.getGroup()]]
		logger.debug("Role mapping : %s" % roleMapping)
		return roleMapping

	def getConfigType(self):
		return ""

	def setConfigID(self):
		pass

	def getContainmentPath(self):
		return ""
	def create(self):
		pass
	def remove(self):
		pass

class WebModule(WASConfig):
	level=6
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["Application"]
		self.opt_attributes={
			'contextRoot':'',
			'classLoaderMode':'PARENT_LAST',
		}
		self.ref_attributes={
			'virtualHost':None
		}

	def setContextRoot(self, contextRoot):
		if contextRoot is not None:
			self.opt_attributes['contextRoot']=contextRoot
		self.logValue()
	def getContextRoot(self):
		return self.opt_attributes['contextRoot']

	def setClassLoaderMode(self, classLoaderMode):
		if classLoaderMode is not None:
			self.opt_attributes['classLoaderMode']=classLoaderMode
		self.logValue()
	def getClassLoaderMode(self):
		return self.opt_attributes['classLoaderMode']

	def setVirtualHost(self, virtualHost):
		"""
		Set the VirtualHost to use in application deployement. VirtualHost
		should be a VirtualHost object otherwise an exception is
		raised.
		"""
		if isinstance(virtualHost, VirtualHost):
			self.ref_attributes['virtualHost']=virtualHost
		else:
			raise Exception("VirtualHost parameter is not a VirtualHost object.")
		self.logValue()
	def getVirtualHost(self):
		return self.ref_attributes['virtualHost']
	def getVirtualHostType(self):
		return "VirtualHost"

	def getMapping(self):
		ctxrootattr=[]
		vhostattr=[]
		taskInfoWebMods=self.getParent().getTaskInfoData("MapWebModToVH")
		for tiwm in taskInfoWebMods:
			wmuri=tiwm.getKey('uri')
			wmwar=wmuri.split(',')[0]
			wmname=tiwm.getKey('web module')
			if self.getVirtualHost()!=None:
				vhostattr.append([wmname, wmuri, self.getVirtualHost().getName()])
			if self.getContextRoot()!="":
				if self.getName()==wmname:
					ctxrootattr.append([wmname, wmuri, self.getContextRoot()])
			logger.debug("Virtual host mappings: %s" % vhostattr)
		return [vhostattr, ctxrootattr]

	def getConfigType(self):
		return ""

	def setConfigID(self):
		pass

	def getContainmentPath(self):
		return ""
	def create(self):
		pass
	def remove(self):
		pass

class BaseResourceRef(WASConfig):
	level=6
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["Application"]
		self.man_attributes={
			'module':"",
			'uri':"",
			'jndi':""
		}
		self.opt_attributes={
			'ejb':""
		}

	def setModule(self, module):
		if module is not None:
			self.man_attributes['module']=module
		self.logValue()
	def getModule(self):
		return self.man_attributes['module']

	def setEjb(self, ejb):
		if ejb is not None:
			self.opt_attributes['ejb']=ejb
		self.logValue()
	def getEjb(self):
		return self.opt_attributes['ejb']

	def setJndi(self, jndi):
		if jndi is not None:
			self.man_attributes['jndi']=jndi
		self.logValue()
	def getJndi(self):
		return self.man_attributes['jndi']

	def setUri(self, uri):
		if uri is not None:
			self.man_attributes['uri']=uri
		self.logValue()
	def getUri(self):
		return self.man_attributes['uri']

	def getOption(self):
		return ""

	def getMapping(self):
		return ""

	def getConfigType(self):
		return ""

	def setConfigID(self):
		pass

	def getContainmentPath(self):
		return ""

	def getKeyAttribute(self):
		return "module"
	def create(self):
		pass
	def remove(self):
		pass

class BeanRef(BaseResourceRef):
	def __init__(self, parent=None):
		BaseResourceRef.__init__(self, parent)

	def getOption(self):
		return "-BindJndiForEJBNonMessageBinding"

	def getMapping(self):
		mapping=[]
		for taskInfo in self.getParent().getTaskInfoData("BindJndiForEJBNonMessageBinding"):
			refModule = taskInfo.getKey("ejb module")
			refEjb = taskInfo.getKey("ejb")
			refUri = taskInfoData.getKey("uri")
			if refmodule == self.getModule() and refEjb == self.getEjb() and refUri==self.getUri():
				reftoref = [refModule , refEjb , refUri , self.getJndi()]
				logger.debug("Bind JNDI rule for non Msg EJB : %s" %  reftoref)
				mapping.append(reftoref)
		return mapping

class CmpRef(BaseResourceRef):
	def __init__(self, parent=None):
		BaseResourceRef.__init__(self, parent)

	def getOption(self):
		return "-DataSourceFor20CMPBeans"

	def getMapping(self):
		mapping=[]
		for taskInfo in self.getParent().getTaskInfoData("DataSourceFor20CMPBeans"):
			refModule = taskInfo.getKey("ejb module")
			refEjb = taskInfo.getKey("ejb")
			refUri = taskInfoData.getKey("uri")
			resourceAuth='cmpBinding.container'

			if refModule==self.getModule() and refEjb==self.getEjb() and uri==self.getUri():
				reftoref=[ refModule ,refEjb , refUri , self.getJndi(), resourceAuth, "", "" ]
				logger.debug( "DataSourceFor20CMPBeans rule : %s" %  reftoref )
				mapping.append(reftoref)
		return mapping

class BaseReferenceResourceRef(BaseResourceRef):
	def __init__(self, parent=None):
		BaseResourceRef.__init__(self, parent)
		self.man_attributes['referenceBinding']=""

	def setReferenceBinding(self, referenceBinding):
		if referenceBinding is not None:
			self.man_attributes['referenceBinding']=referenceBinding
		self.logValue()
	def getReferenceBinding(self):
		return self.man_attributes['referenceBinding']

class ResRef(BaseReferenceResourceRef):
	def __init__(self, parent=None):
		BaseReferenceResourceRef.__init__(self, parent)

	def getOption(self):
		return "-MapResRefToEJB"

	def getMapping(self):
		mapping = []
		for taskInfo in self.getParent().getTaskInfoData("MapResRefToEJB"):
			refModule=taskInfo.getKey("module")
			refEjb=taskInfo.getKey("ejb")
			refUri=taskInfo.getKey("uri")
			resRefType=taskInfo.getKey("resource type")
			referenceBinding=taskInfo.getKey("resource reference")
			if refModule==self.getModule() and refEjb==self.getEjb() and referenceBinding==self.getReferenceBinding() and refUri==self.getUri():
				reftoref = [ refModule , refEjb , refUri , referenceBinding, resRefType, self.getJndi(), "", "" ]
				logger.debug("MapResRefToEJB rule : %s" %  reftoref )
				mapping.append(reftoref)
		return mapping

class EjbRef(BaseReferenceResourceRef):
	def __init__(self, parent=None):
		BaseReferenceResourceRef.__init__(self, parent)

	def getOption(self):
		return "-MapEJBRefToEJB"

	def getMapping(self):
		mapping=[]
		for taskInfo in self.getParent().getTaskInfoData("MapEJBRefToEJB"):
			refModule=taskInfo.getKey("module")
			refEjb=taskInfo.getKey("ejb")
			refUri=taskInfo.getKey("uri")
			referenceBinding=taskInfo.getKey("resource reference")
			refClassname=taskInfo.getKey("class")
			if refModule==self.getModule() and refEjb==self.getEjb() and referenceBinding==self.getReferenceBinding() and refUri==self.getUri():
				reftoref = [ refModule , refEjb , refUri , referenceBinding, refClassname, self.getJndi() ]
				logger.debug( "MapEJBRefToEJB rule : %s" %  reftoref )
				mapping.append(reftoref)
		return mapping

class ResEnv(BaseReferenceResourceRef):
	def __init__(self, parent=None):
		BaseReferenceResourceRef.__init__(self, parent)

	def getOption(self):
		return "-MapResEnvRefToRes"

	def getMapping(self):
		mapping=[]
		for taskInfo in self.getParent().getTaskInfoData("MapResEnvRefToRes"):
			refModule=taskInfo.getKey("module")
			refEjb=taskInfo.getKey("ejb")
			refUri=taskInfo.getKey("uri")
			referenceBinding=taskInfo.getKey("resource reference")
			refType = taskInfo.getKey("resource type")
			if refModule==self.getModule() and refEjb==self.getEjb() and referenceBinding==self.getReferenceBinding() and refUri==self.getUri():
				reftoref = [ refModule , refEjb , refUri , referenceBinding, refType, self.getJndi() ]
				logger.debug( "MapResEnvToRes rule : %s" %  reftoref )
				mapping.append(reftoref)
		return mapping

class MesBind(BaseResourceRef):
	def __init__(self, parent=None):
		BaseResourceRef.__init__(self, parent)
		self.man_attributes={
			'module':"",
			'uri':"",
			'listener':""
		}
		self.opt_attributes={
			'ejb':""
		}
	def setListener(self, listener):
		if listener is not None:
			self.man_attributes['listener']=listener
		self.logValue()
	def getListener(self):
		return self.man_attributes['listener']

	def getOption(self):
		return "-BindJndiForEJBMessageBinding"

	def getMapping(self):
		mapping=[]
		for taskInfo in self.getParent().getTaskInfoData("BindJndiForEJBMessageBinding"):
			refModule=taskInfo.getKey("ejb module")
			refEjb=taskInfo.getKey("ejb")
			refUri=taskInfo.getKey("uri")
			if refModule==self.getModule() and refEjb==self.getEjb() and refUri==self.getUri():
				reftoref = [ refModule , refEjb , refUri , self.getListener() ]
				logger.debug( "BindJndiForEJBMessageBinding rule : %s" %  reftoref )
				mapping.append(reftoref)
		return mapping

class MesRef(BaseResourceRef):
	def __init__(self, parent=None):
		BaseResourceRef.__init__(self, parent)
		self.man_attributes={
			'module':"",
			'uri':"",
			'target':""
		}
		self.opt_attributes={
			'ejb':""
		}
	def setTarget(self, target):
		if target is not None:
			self.man_attributes['target']=target
		self.logValue()
	def getTarget(self):
		return self.man_attributes['target']

	def getOption(self):
		return "-MapMessageDestinationRefToEJB"

	def getMapping(self):
		mapping=[]
		for taskInfo in self.getParent().getTaskInfoData("MapMessageDestinationRefToEJB"):
			refModule=taskInfo.getKey("module")
			refEjb=taskInfo.getKey("ejb")
			refUri=taskInfo.getKey("uri")
			refMesDest=taskInfoData['message destination object']

			if refModule==self.getModule() and refEjb==self.getEjb() and refUri==self.getUri() and refMesDest==self.getTarget():
				reftoref=[ refModule , refEjb , refUri , refMesDest, self.getJndi() ]
				logger.debug( "MapMessageDestinationRefToEJB rule : %s" %  reftoref )
				mapping.append(reftoref)
		return mapping

class Application(WASConfig):
	"""
	Class to represent a application (EAR).

	Considering resource references:
	Set the authentication method to None for all resources
	references. Resources will always use the
	authentication of the resource, e.g. datasource or jms
	factory.

	All DataSourceFor20CMPBeans resource authorization are set to
	container managed and login configuration to None. The JNDI
	name is kept as provided (no way to set it with properties).

	All DataSourceFor20EJBModules resource authorization are set to
	container managed and login configuration to None. The JNDI
	name is kept as provided (no way to set it with properties).
	"""
	level=5
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["Server", "ServerCluster"]

		self.man_attributes={
			'name' : "",
			'earFile' : ""
		}
		self.opt_attributes={
			'precompilejsps':'false',
			'classLoaderMode':"PARENT_FIRST",
			'WARClassLoaderPolicy':"MULTIPLE",
			'libraryName':"",
			'dbType':"DB2UDB_V91",
			'dbSchema':"",
			'startupOrder':1
		}
		self.__webServers=[]
		self.__webModules=[]
		self.__roles=[]

		self.__beanref=[]
		self.__resref=[]
		self.__ejbref=[]
		self.__resenv=[]
		self.__mesbind=[]
		self.__mesref=[]
		self.__cmpref=[]

	def addChild(self, child):
		WASConfig.addChild(self, child)
		if isinstance(child, WebServerTarget):
			self.__webServers.append(child)
		if isinstance(child, WebModule):
			self.__webModules.append(child)
		if isinstance(child, Role):
			self.__roles.append(child)
		if isinstance(child, BeanRef):
			self.__beanref.append(child)
		if isinstance(child, ResRef):
			self.__resref.append(child)
		if isinstance(child, EjbRef):
			self.__ejbref.append(child)
		if isinstance(child, ResEnv):
			self.__resenv.append(child)
		if isinstance(child, MesBind):
			self.__mesbind.append(child)
		if isinstance(child, MesRef):
			self.__mesref.append(child)
		if isinstance(child, CmpRef):
			self.__cmpref.append(child)

	def setEarFile(self, earFile):
		if earFile is not None:
			self.man_attributes['earFile']=earFile
		self.logValue()
	def getEarFile(self):
		return self.man_attributes['earFile']

	def setPrecompilejsps(self, precompilejsps):
		if precompilejsps is not None:
			self.opt_attributes['precompilejsps']=precompilejsps
		self.logValue()
	def getPrecompilejsps(self):
		return self.opt_attributes['precompilejsps']

	def setClassLoaderMode(self, classLoaderMode):
		if classLoaderMode is not None:
			self.opt_attributes['classLoaderMode']=classLoaderMode
		self.logValue()
	def getClassLoaderMode(self):
			return self.opt_attributes['classLoaderMode']

	def setWARClassLoaderPolicy(self, WARClassLoaderPolicy):
		if WARClassLoaderPolicy is not None:
			self.opt_attributes['WARClassLoaderPolicy']=WARClassLoaderPolicy
		self.logValue()
	def getWARClassLoaderPolicy(self):
		return self.opt_attributes['WARClassLoaderPolicy']

	def setLibraryName(self, libraryName):
		if libraryName is not None:
			self.opt_attributes['libraryName']=libraryName
		self.logValue()
	def getLibraryName(self):
		return self.opt_attributes['libraryName']

	def setDbSchema(self, dbSchema):
		"""
		Set deployejb.dbschema for the EJBDeploy tool. Needed
		when the db user does not automatically have the right
		schema.
		"""
		if dbSchema is not None:
			self.opt_attributes['dbSchema']=dbSchema
	def getDbSchema(self):
		return self.opt_attributes['dbSchema']

	def setDbType(self, dbType):
		"""
		Set deployejb.dbtype option for the EJBDeploy tool.

		Only these three types are supported: "DB2UDB_V81"
		"DB2UDB_V91", "DB2UDBISERIES_V54", ORACLE_V91 and ORACLE_V10G. Otherwise an
		Exception is raised. DB2UDB_V91 is the default.
		"""
		# Of valid db types supported 
		types=["DB2UDB_V82"
			"DB2UDB_V81",
			"DB2UDB_V91",
			#"DB2EXPRESS_V81",
			#"DB2EXPRESS_V82",
			#"DERBY_V10",
			#"DB2UDBOS390_V7",
			#"DB2UDBOS390_V8",
			#"DB2UDBOS390_NEWFN_V8",
			#"DB2UDBOS390_V9",
			#"DB2UDBISERIES_V53",
			"DB2UDBISERIES_V54"
			#"INFORMIX_V93",
			#"INFORMIX_V94",
			#"INFORMIX_V100",
			#"MSSQLSERVER_2005",
			#"MSSQLSERVER_2000",
			"ORACLE_V9I",
			"ORACLE_V10G",
			#"SQL92",
			#"SQL99",
			#"SYBASE_V1250",
			#"SYBASE_V15"
			]
		if dbType in types:
			self.opt_attributes['dbType']=dbType
	def getDbType(self):
		return self.opt_attributes['dbType']

	def setStartupOrder(self, startupOrder):
		if startupOrder is not None:
			self.opt_attributes['startupOrder']=startupOrder
		self.logValue()

	def getStartupOrder(self):
		return self.opt_attributes['startupOrder']

	def getTaskInfoData(self, taskName):
		"""
		This function makes a collection of value dictionaries from the
		output of taskInfo. The taskInfo data is not structured, but
		still contains some name/value pairs, separated by colon,
		grouped by empty line.
		"""
		rawString = AdminApp.taskInfo(self.getEarFile(),taskName).split(Util.getNL())
		#rawString = AdminApp.taskInfo(self.getEarFile(),taskName).split()
		aDict={}
		taskInfoList=[]
		for aLine in rawString:
			if aLine == "":
				if aDict.has_key('uri'): 
					taskInfoList.append(TaskInfoData(aDict))
				aDict = {}
			else:
				keyValuePair = aLine.split(":")
				if len( keyValuePair ) > 1:
					aDict[keyValuePair[0].strip().lower()] = keyValuePair[1].strip()
		return taskInfoList

	def isRunning(self):
		"""
		This function checks if the application is started.

		return True(1) if started otherwise False(0)

		If the cluster the application is deployed to does not
		exist an Exception is raised.
		"""
		Apps = Util.wslist(AdminControl.queryNames( "type=Application,J2EEName=%s,*" % self.getName() ))
		result = ""
		if (Apps != ['']):
			for App in Apps:
				appname = AdminControl.getAttribute( App, "name" )
				if ( appname == self.getName() ):
					# If the next commando returns empty than the application is stopped
					result = AdminControl.completeObjectName( "type=Application,name=%s,*" % self.getName() )
					break
		if ( result == "" ):
			return 0
		return 1

	def start(self):
		"""
		Attempt to start the application by invoking the start
		operation on the AppManager beans of the AppsServer the
		application is deployed on. This is an asychronous
		operation.

		If the cluster the application is deployed to does not
		exist an Exception is raised.
		"""
		if self.getParent().isRunning():
			if self.isRunning():
				logger.info("Application already running : %s" % self.getName() )
			else:
				logger.info("Starting application : %s" % self.getName() )
				if self.getParent().getConfigType() == "ServerCluster":
					for s in self.getParent().getMembers():
						appMan = s.getAppManagerMbean()
						AdminControl.invoke( appMan, "startApplication", "[\"" + self.getName() + "\"]", "java.lang.String" )
						logger.info( "Application %s start initiated on : %s" % (self.getName(), s.getName()) )
				else:
					appMan = self.getParent().getAppManagerMbean()
					AdminControl.invoke( appMan, "startApplication", "[\"" + self.getName() + "\"]", "java.lang.String" )
					logger.info( "Application %s start initiated on : %s" % (self.getName(), self.getParent().getName()) )
		else:
			logger.info( "%s %s is (partially) stopped, Application %s cannot be started"  % (self.getParent().getConfigType(), self.getParent().getName(), self.getName()))

	def stop(self):
		"""
		Attempt to stop the application by invoking the stop
		operation on the AppManager beans of the AppsServer the
		application is deployed on. This is an asychronous
		operation.
		"""
		if self.getParent().isRunning():
			if not self.isRunning():
				logger.info("Application already stopped : %s" % self.getName() )
			else:
				logger.info("Stopping application : %s" % self.getName() )
				if self.getParent().getConfigType() == "ServerCluster":
					for s in self.getParent().getMembers():
						appMan=s.getAppManagerMbean()
						AdminControl.invoke( appMan, "stopApplication", "[\"" + self.getName() + "\"]", "java.lang.String" )
						logger.info( "Application : %s stop initiated on : %s" % (self.getName(), s.getName() ))
				else:
					appMan=self.getParent().getAppManagerMbean()
					AdminControl.invoke( appMan, "stopApplication", "[\"" + self.getName() + "\"]", "java.lang.String" )
					logger.info( "Application : %s stop initiated on : %s" % (self.getName(), self.getParent().getName() ))

		else:
			logger.info( "%s %s is (partially) stopped, Application %s cannot be stopped"  % (self.getParent().getConfigType(),self.getParent().getName(), self.getName()))

	def remove(self):
		"""
		Uninstall the EAR from WAS.
		"""
		# uninstall application
		apps=Util.wslist(AdminApp.list())
		for a in apps:
			if a==self.getName():
				logger.info("Uninstalling application : %s" % self.getName())
				AdminApp.uninstall(self.getName() )

	def create(self):
		"""
		Install the EAR file in WAS.
		"""
		logger.info("Installing EAR : %s on : %s" % (self.getName(), self.getParent().getName()))

		attributes={
			"-cell" : self.getCell().getName(),
			"-appname" : self.getName(),
			"-deployejb.dbtype" : self.getDbType() 
		}
		if self.getDbSchema()!="": attributes["-deployejb.dbschema"]=self.getDbSchema()

		if self.getParent().getConfigType() == 'ServerCluster':
			attributes["-cluster"] = self.getParent().getName()
			attributes["-target"] = "WebSphere:cell=%s,cluster=%s" % (self.getCell().getName(), self.getParent().getName())
		else:
			attributes["-target"] = "WebSphere:cell=%s,node=%s,server=%s" % (self.getCell().getName(), self.getParent().getNode().getName(), self.getParent().getName())

		for i in self.__webServers:
			attributes["-target"] = "%s+WebSphere:cell=%s,node=%s,server=%s" % (attributes["-target"],self.getCell().getName(),i.getWebServer().getParent().getName(),i.getWebServer().getName())

		if self.getPrecompilejsps()=="true":
			attributes["-preCompileJSPs"]=""
		else:
			attributes["-nopreCompileJSPs"]=""
		# Installing ear file
		logger.info( "Installing : " + self.getName() )
		options = []
		for key in attributes.keys():
			options.append(key)
			value = attributes[key]
			if ( value != '' ):
				options.append(value)

		# Set vhost for all webmodules, and contextroot if specified in property file
		vhostattr=[]
		ctxrootattr=[]
		mapping=[]
		for i in self.__webModules:
			mapping=i.getMapping()
			vhostattr+=mapping[0]
			ctxrootattr+=mapping[1]
		if vhostattr != []:
			options.append("-MapWebModToVH")
			options.append(vhostattr)
		if ctxrootattr!=[]:
			options.append("-CtxRootForWebMod")
			options.append(ctxrootattr)

		for i in [self.__beanref, self.__resref, self.__ejbref,self.__resenv,self.__mesbind,self.__mesref,self.__cmpref,self.__roles]:
			mapping=[]
			for j in i:
				mapping+=j.getMapping()
			if mapping!=[]:
				options.append(j.getOption())
				options.append(mapping)
		logger.debug(options)

		self.configID = AdminApp.install(self.getEarFile(), options )
		logger.info( "EAR installation successfully : %s" % self.getName()  )

		# Set library reference
		if self.getLibraryName()!="":
			AdminConfig.create( "LibraryRef", classloader, [["libraryName", self.getLibraryName()]] )

		# Change classloader modes
		deployments = AdminConfig.getid("/Deployment:%s/" % self.getName()) 
		deployedObject = AdminConfig.showAttribute(deployments, "deployedObject")
		classloader = AdminConfig.showAttribute(deployedObject, "classloader")
		logger.info("setting classloader mode for: %s to : %s" % (self.getName(), self.getClassLoaderMode()))
		AdminConfig.modify(classloader, [["mode", self.getClassLoaderMode()]])
		AdminConfig.modify(deployedObject, [["warClassLoaderPolicy", self.getWARClassLoaderPolicy()]])
		logger.info("setting startup weight for: %s to : %s" % (self.getName(), self.getStartupOrder()))
		AdminConfig.modify(deployedObject, [["startingWeight", self.getStartupOrder()]])

		modules=AdminConfig.showAttribute(deployedObject, 'modules')[1:-1].split()
		for m in modules:
			modName=AdminConfig.showAttribute(m, 'uri')
			for wm in self.__webModules:
				if modName==wm.getName():
					logger.info("Setting classLoaderMode for WebModule: %s to : %s" % (wm.getName(), wm.getClassLoaderMode()))
					AdminConfig.modify(m, [["classloaderMode", wm.getClassLoaderMode()]])
