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

# DataSource and Driver Classes
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-02-13 10:16:05 +0100 (wo, 13 feb 2013) $
# $Id: datasource.py 446 2013-02-13 09:16:05Z andre $
class JDBCProvider(WASConfig):
	level=3
	"""
	General JDBC Provider class
	"""
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.opt_attributes={
            'description':"",
			'implementationClassName':"",
			'classpath':"",
			'nativepath':"",
			'xa':"false"
		}
		self.__datasourceHelperClassname=""

	def setDescription(self, description):
		if description is not None: self.opt_attributes['description']=description
		self.logValue()

	def getDescription(self):
		return self.opt_attributes['description']

	def setImplementationClassName(self, implementationClassName):
		if implementationClassName is not None: self.opt_attributes['implementationClassName']=implementationClassName
		self.logValue()

	def getImplementationClassName(self):
		return self.opt_attributes['implementationClassName']

	def setClasspath(self, classpath):
		if classpath is not None: self.opt_attributes['classpath']=classpath
		self.logValue()

	def getClasspath(self):
		return self.opt_attributes['classpath']

	def setNativepath(self, nativepath):
		if nativepath is not None: self.opt_attributes['nativepath']=nativepath
		self.logValue()

	def getNativepath(self):
		return self.opt_attributes['nativepath']

	def setDatasourceHelperClassname(self, datasourceHelperClassname):
		if datasourceHelperClassname is not None: self.__datasourceHelperClassname=datasourceHelperClassname
		self.logValue()

	def getDatasourceHelperClassname(self):
		return self.__datasourceHelperClassname

	def setXa(self, xa):
		if xa is not None: self.opt_attributes['xa']=xa
		self.logValue()

	def getXa(self):
		return self.opt_attributes['xa']

	def create(self):
		WASConfig.create(self)
		template=Util.wslist(AdminConfig.listTemplates( 'JDBCProvider', 'User-defined JDBC Provider Only' ))[0]
		logger.debug(template)
		logger.debug(self.opt_attributes)
		self.configID=AdminConfig.createUsingTemplate('JDBCProvider', self.getParent().getConfigID(), Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes), template)
		self.logCreate()


class AS400JDBCProvider(JDBCProvider):
	"""
	AS400 JDBC Driver class
	"""
	def __init__(self, parent=None):
		JDBCProvider.__init__(self, parent)
	   	self.setDescription("Java JDBC Driver for remote DB2 connections on iSeries")
	   	self.setImplementationClassName("com.ibm.as400.access.AS400JDBCXADataSource")
	   	self.setClasspath("${OS400_TOOLBOX_JDBC_DRIVER_PATH}/jt400.jar")
	   	self.setDatasourceHelperClassname("com.ibm.websphere.rsadapter.DB2AS400DataStoreHelper")
		self.setXa("false")

	def getConfigType(self):
		return "JDBCProvider"

class AS400XAJDBCProvider(JDBCProvider):
	"""
	AS400 XS JDBC Driver class
	"""
	def __init__(self, parent=None):
		JDBCProvider.__init__(self, parent)
	   	self.setDescription("Java JDBC Driver for remote DB2 connections on iSeries")
	   	self.setImplementationClassName("com.ibm.as400.access.AS400JDBCXADataSource")
	   	self.setClasspath("${OS400_TOOLBOX_JDBC_DRIVER_PATH}/jt400.jar")
	   	self.setDatasourceHelperClassname("com.ibm.websphere.rsadapter.DB2AS400DataStoreHelper")
		self.setXa("true")

	def getConfigType(self):
		return "JDBCProvider"

class ORAJDBCProvider(JDBCProvider):
	"""
	Oracle JDBC Driver class
	"""
	def __init__(self, parent=None):
		JDBCProvider.__init__(self, parent)
	   	self.setDescription("Oracle JDBC Driver")
	   	self.setImplementationClassName("oracle.jdbc.pool.OracleConnectionPoolDataSource")
	   	self.setClasspath("${ORACLE_JDBC_DRIVER_PATH}/ojdbc14.jar")
	   	self.setDatasourceHelperClassname("com.ibm.websphere.rsadapter.OracleDataStoreHelper")
		self.setXa("false")

	def getConfigType(self):
		return "JDBCProvider"

class ORAXAJDBCProvider(JDBCProvider):
	"""
	Oracle XA JDBC Driver class
	"""
	def __init__(self, parent=None):
		JDBCProvider.__init__(self, parent)
	   	self.setDescription("Oracle JDBC Driver")
	   	self.setImplementationClassName("oracle.jdbc.xa.client.OracleXADataSource")
	   	self.setClasspath("${ORACLE_JDBC_DRIVER_PATH}/ojdbc14.jar")
	   	self.setDatasourceHelperClassname("com.ibm.websphere.rsadapter.OracleDataStoreHelper")
		self.setXa("true")

	def getConfigType(self):
		return "JDBCProvider"

class DB2JDBCProvider(JDBCProvider):
	"""
	DB2 JDBC Driver class
	"""
	def __init__(self, parent=None):
		JDBCProvider.__init__(self, parent)
	   	self.setDescription("DB2 Universal JDBC Driver Provider")
	   	self.setImplementationClassName("com.ibm.db2.jcc.DB2ConnectionPoolDataSource")
	   	self.setClasspath("${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc.jar;" + \
	  		"${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cu.jar;" + \
	  		"${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cisuz.jar")
	   	self.setDatasourceHelperClassname("com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper")
		self.setXa("false")

	def getConfigType(self):
		return "JDBCProvider"

class DB2XAJDBCProvider(JDBCProvider):
	"""
	DB2 XA JDBC Driver class
	"""
	def __init__(self, parent=None):
		JDBCProvider.__init__(self, parent)
	   	self.setDescription("DB2 Universal JDBC Driver Provider (XA)")
	   	self.setImplementationClassName("com.ibm.db2.jcc.DB2XADataSource")
	   	self.setClasspath("${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc.jar;" + \
	  		"${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cu.jar;" + \
	  		"${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cisuz.jar")
	   	self.setDatasourceHelperClassname("com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper")
		self.setXa("true")

	def getConfigType(self):
		return "JDBCProvider"

class DataSource(WASConfig):
	"""
	Class to represent a WAS Datasource.

	Required properties: name, type, value
	Setters provided for these defined options:
	jndi, serverName, databaseName, portNumber, CMP, preTestSQLString
	custom ones cane be added through addProperty method

	Connection pool properties can be set as well.

	Before creating the first datasource a JDBC provider will be
	created, the provider will be reused for subsequent
	datasources. This means the JDBC provider will have the XA
	property as defined for the first datasource. So if the first
	datasource is XA enabled all datasources will be XA enabled
	because a XA enabled provider will be created.

	A data store helper class name is set as defined for the
	appropriate JDBC driver, see Defined JDBC driver properties.

	Author: Andre van Dijk (SuperClass IT)
	Date: $Date: 2013-02-13 10:16:05 +0100 (wo, 13 feb 2013) $

	$Id: datasource.py 446 2013-02-13 09:16:05Z andre $
	"""
	level=4
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["JDBCProvider"]

		self.man_attributes={
			'name':"",
			'jndiName' : "",
			'authDataAlias': ""
		}

		self.opt_attributes={
			'statementCacheSize' : 10,
		}
		self.__thresholds={
			'usageCriticalThreshold':-1,
			'usageWarningThreshold':-1,
			'waitTimeCriticalThreshold':-1,
			'waitTimeWarningThreshold':-1
		}

		self.__cmp='false'
		
		self.connectionPool={
			'minConnections' : 1,
			'maxConnections' : 10,
			'connectionTimeout' : 1800,
			'agedTimeout' : 0,
			'reapTime' : 180,
			'unusedTimeout' : 1800,
			'purgePolicy' : 'EntirePool'
		}
		self.template="User-defined DataSource"

	def getOptAttributes(self):
		return self.opt_attributes.keys() + self.connectionPool.keys() + self.__thresholds.keys()

	def setJndiName(self, jndi):
		if jndi is not None:
			self.man_attributes['jndiName']=jndi
		self.logValue()

	def getJndiName(self):
		return self.man_attributes['jndiName']

	def setAuthDataAlias(self, authDataAlias):
		if authDataAlias is not None:
			self.man_attributes['authDataAlias']=authDataAlias
		self.logValue()

	def getAuthDataAlias(self):
		return self.man_attributes['authDataAlias']

	def setStatementCacheSize(self, statementCacheSize):
		if statementCacheSize is not None:
			self.opt_attributes['statementCacheSize']=statementCacheSize
		self.logValue()

	def getStatementCacheSize(self):
		return self.opt_attributes['statementCacheSize']

	def setCmp(self, cmp):
		if cmp is not None:
			self.__cmp=cmp
		self.logValue()

	def getCmp(self):
		return self.__cmp

	def setMaxConnections(self, maxConnections):
		if maxConnections is not None:
			self.connectionPool['maxConnections']=maxConnections
		self.logValue()
	def getMaxConnections(self):
		return self.connectionPool['maxConnections']
	def setMinConnections(self, minConnections):
		if minConnections is not None:
			self.connectionPool['minConnections']=minConnections
		self.logValue()
	def getMinConnections(self):
		return self.connectionPool['minConnections']
	def setUnusedTimeout(self, unusedTimeout):
		if unusedTimeout is not None:
			self.connectionPool['unusedTimeout']=unusedTimeout
		self.logValue()
	def getUnusedTimeout(self):
		return self.connectionPool['unusedTimeout']
	def setAgedTimeout(self, agedTimeout):
		if agedTimeout is not None:
			self.connectionPool['agedTimeout']=agedTimeout
		self.logValue()
	def getAgedTimeout(self):
		return self.connectionPool['agedTimeout']
	def setReapTime(self, reapTime):
		if reapTime is not None:
			self.connectionPool['reapTime']=reapTime
		self.logValue()
	def getReapTime(self):
		return self.connectionPool['reapTime']
	def setConnectionTimeout(self, connectionTimeout):
		if connectionTimeout is not None:
			self.connectionPool['connectionTimeout']=connectionTimeout
		self.logValue()
	def getConnectionTimeout(self):
		return self.connectionPool['connectionTimeout']
	def setPurgePolicy(self, purgePolicy):
		if purgePolicy is not None:
			self.connectionPool['purgePolicy']=purgePolicy
		self.logValue()
	def getPurgePolicy(self):
		return self.connectionPool['purgePolicy']

	def getTemplate(self):
		logger.debug(self.template)
		pset=AdminConfig.showAttribute(self.template, "propertySet")
		plist=Util.wslist(AdminConfig.showAttribute(pset,"resourceProperties"))
		for p in plist:
			d=DynAttribute(AdminConfig.showAttribute(p, "name"), AdminConfig.showAttribute(p, "description"), AdminConfig.showAttribute(p, "required"), AdminConfig.showAttribute(p, "value"), AdminConfig.showAttribute(p, "type"))
			if d.getRequired()=="false":
				self.dyn_opt_attributes[d.getName()]=d
			else:
				self.dyn_man_attributes[d.getName()]=d

	def getStatistics(self):
		stats=[]
		servers=AdminControl.queryMBeans('type=Perf,*')	

		for s in servers.toArray():
			so=s.getObjectName()
			providers=AdminControl.queryMBeans('WebSphere:type=%s,process=%s,node=%s,name=%s,*' % (self.getParent().getConfigType(),so.getKeyProperty('process'),so.getKeyProperty('node'),self.getParent().getName()))
			for p in providers.toArray():
				provStats=AdminControl.invoke_jmx(so,'getStatsObject',[p.getObjectName(),java.lang.Boolean('true')],['javax.management.ObjectName','java.lang.Boolean'])
				if provStats is not None:
					for i in provStats.getSubStats():
						if i.getName()==self.getJndiName():
							dataSourceStat=DataSourceUsageStat()
							dataSourceStat.setCriticalThreshold(self.getUsageCriticalThreshold())
							dataSourceStat.setWarningThreshold(self.getUsageWarningThreshold())
							dataSourceStat.setStatus([i])
							stats.append(dataSourceStat)
							dataSourceStat=DataSourceWaitStat()
							dataSourceStat.setCriticalThreshold(self.getWaitTimeCriticalThreshold())
							dataSourceStat.setWarningThreshold(self.getWaitTimeCriticalThreshold())
							dataSourceStat.setStatus([i])
							stats.append(dataSourceStat)
		return stats
		#WASConfig.getStatistics(self)

	def setUsageCriticalThreshold(self, usageCriticalThreshold):
		if usageCriticalThreshold is not None: self.__thresholds['usageCriticalThreshold']=usageCriticalThreshold
		self.logValue()

	def getUsageCriticalThreshold(self):
		return self.__thresholds['usageCriticalThreshold']

	def setUsageWarningThreshold(self, usageWarningThreshold):
		if usageWarningThreshold is not None: self.__thresholds['usageWarningThreshold']=usageWarningThreshold
		self.logValue()

	def getUsageWarningThreshold(self):
		return self.__thresholds['usageWarningThreshold']

	def setWaitTimeCriticalThreshold(self, waitTimeCriticalThreshold):
		if waitTimeCriticalThreshold is not None: self.__thresholds['waitTimeCriticalThreshold']=waitTimeCriticalThreshold
		self.logValue()

	def getWaitTimeCriticalThreshold(self):
		return self.__thresholds['waitTimeCriticalThreshold']

	def setWaitTimeWarningThreshold(self, waitTimeWarningThreshold):
		if waitTimeWarningThreshold is not None: self.__thresholds['waitTimeWarningThreshold']=waitTimeWarningThreshold
		self.logValue()

	def getWaitTimeWarningThreshold(self):
		return self.__thresholds['waitTimeWarningThreshold']

	def getNagiosStatus(self):
		WASConfig.getNagiosStatus(self)
		status=[]
		for i in self.getStatistics():
			status.append(i.getStatus())
		return status

	def create(self):
		WASConfig.create(self)

		options=Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes)
		options.append(["xaRecoveryAuthAlias", self.getAuthDataAlias()])
		options.append(["datasourceHelperClassname", self.getParent().getDatasourceHelperClassname()])
		self.configID=AdminConfig.create( "DataSource", self.getParent().getConfigID(),options)
		self.logCreate()
		logger.info("Setting connection pool options for datasource : %s" % self.getName())
		AdminConfig.modify(AdminConfig.showAttribute(self.configID, "connectionPool" ), Util.dictToList(self.connectionPool) )
	
		MappingModuleAttributes = [["authDataAlias", self.man_attributes['authDataAlias']]]
		if ( self.getCmp() == "true" ):
			relationalResourceAdapter = AdminConfig.showAttribute(self.configID, "relationalResourceAdapter" )
			CMPConnectorFactoryAttributes =\
				[\
				 ["name", self.getName() + "_cf" ],\
				 ["cmpDatasource", self.configID],\
				 ["authDataAlias", self.man_attributes['authDataAlias']]
				]
			CMPConnectorFactory = AdminConfig.create( "CMPConnectorFactory",\
	                                                relationalResourceAdapter,\
	                                                CMPConnectorFactoryAttributes )
			AdminConfig.create( "MappingModule", CMPConnectorFactory, MappingModuleAttributes )
	
		# Set CMP authentication. This is the "old" 5.1 way, so
		# all resource references of the application are set to
		# None when the application is deployed. CMP
		# authentication will use the JAAS entry set here.
		MappingModuleAttributes.append(["mappingConfigAlias", "DefaultPrincipalMapping"])
		AdminConfig.create("MappingModule", self.configID, MappingModuleAttributes)

		#Set the properties for the data source.
		dataSourcePropertySet = AdminConfig.create( "J2EEResourcePropertySet", self.configID, [])
		for i in self.getDynManAttributes():
			AdminConfig.create("J2EEResourceProperty", dataSourcePropertySet, self.dyn_man_attributes[i].getList())
		for i in self.getDynOptAttributes():
			AdminConfig.create("J2EEResourceProperty", dataSourcePropertySet, self.dyn_opt_attributes[i].getList())

class AS400DataSource(DataSource):
	def __init__(self, parent=None):
		DataSource.__init__(self, parent)
		self.validParents=["AS400JDBCProvider","AS400XAJDBCProvider"]

	def setParent(self, parent):
		WASConfig.setParent(self, parent)
		# Get the dynamic properties
		if self.getParent().getXa()=="true":
			self.template=AdminConfig.listTemplates('DataSource', 'DB2 UDB for iSeries (Toolbox XA)')
		else:
			self.template=AdminConfig.listTemplates('DataSource', 'DB2 UDB for iSeries (Toolbox)')
		self.getTemplate()

	def getConfigType(self):
		return "DataSource"

class DB2DataSource(DataSource):
	def __init__(self, parent=None):
		DataSource.__init__(self, parent)
		self.validParents=["DB2JDBCProvider","DB2XAJDBCProvider"]

	def setParent(self, parent):
		WASConfig.setParent(self, parent)
		# Get the dynamic properties
		if self.getParent().getXa()=="true":
			self.template=AdminConfig.listTemplates('DataSource', 'DB2 Universal JDBC Driver XA DataSource')
		else:
			self.template=AdminConfig.listTemplates('DataSource', 'DB2 Universal JDBC Driver DataSource')
		self.getTemplate()

	def getConfigType(self):
		return "DataSource"
