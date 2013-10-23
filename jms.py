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

# JMS Resources, Queue Connection Factories, Queues and Topics
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: jms.py 424 2013-01-04 15:04:36Z andre $
class JMSProvider(WASConfig):
	"""
	General JMS Provider class
	"""
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name':"",
			'externalInitialContextFactory':"",
			'externalProviderURL':""
		}
		self.opt_attributes={
            'description':"",
			'classpath':"",
			'nativepath':""
		}

	def setDescription(self, description):
		if description is not None: self.opt_attributes['description']=description
		self.logValue()
	def getDescription(self):
		return self.opt_attributes['description']

	def setExternalInitialContextFactory(self, externalInitialContextFactory):
		if externalInitialContextFactory is not None: self.man_attributes['externalInitialContextFactory']=externalInitialContextFactory
		self.logValue()

	def getExternalInitialContextFactory(self):
		return self.man_attributes['externalInitialContextFactory']
		
	def setExternalProviderURL(self, externalProviderURL):
		if externalProviderURL is not None: self.man_attributes['externalProviderURL']=externalProviderURL
		self.logValue()

	def getExternalProviderURL(self):
		return self.man_attributes['externalProviderURL']

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

	def validate(self):
		if self.getName() in ["WebSphere JMS Provider", "WebSphere MQ JMS Provider"]:
			self.wasDefault="true"
		WASConfig.validate(self)

class JMSConnectionFactory(WASConfig):
	"""
	Class to represent a JMS connection factory.

	Note that for a MQ type a MQConnectionFactory is created
	instead of MQQueueConnectionFactory or
	MQTopicConnectionFactory, as stated in the J2EE Message
	Provider Standard v1.0, section 6.1.2. Standard: The Connection
	Factory must be used instead of Queue Connection Factory
	because it supports JMS 1.1 and JMS 1.0.2

	Author: Andre van Dijk (SuperClass IT)
	Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $

	$Id: jms.py 424 2013-01-04 15:04:36Z andre $
	"""
	level=4
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["JMSProvider"]
		# JMS options
		self.man_attributes={
			'name':"",
			'jndiName':""
		}
		self.opt_attributes={
			'description':"",
			'authDataAlias':"",
			'XAEnabled':""
		}

		# Connection pool options
		self.connectionPool={"maxConnections": 10, \
		 "minConnections": 1, \
		 "unusedTimeout": 1800, \
		 "agedTimeout": 0, \
		 "reapTime": 180, \
		 "connectionTimeout": 180, \
		 "purgePolicy": "EntirePool"
		}

	def getOptAttributes(self):
		return self.opt_attributes.keys()+self.connectionPool.keys()

	def setJndiName(self, jndi):
		if jndi is not None:
			self.man_attributes['jndiName']=jndi
		self.logValue()

	def getJndiName(self):
		return self.man_attributes['jndiName']

			#types = { "MQQUEUE":"MQQueueConnectionFactory", \
					  #"MQTOPIC":"MQTopicConnectionFactory", \
					  #"MQCON":"MQConnectionFactory", \
					  #"WASQUEUE":"WASQueueConnectionFactory", \
					  #"WASTOPIC":"WASTopicConnectionFactory"\


	def setDescription(self, description):
		if description is not None:
			self.opt_attributes['description']=description
		self.logValue()
	def getDescription(self):
		return self.opt_attributes['description']

	def setXAEnabled(self, xa):
		"""
		Indicates whether to use XA mode.
		"""
		if xa is not None:
			self.opt_attributes['XAEnabled']=xa
		self.logValue()
	def getXAEnabled(self):
		return self.opt_attributes['XAEnabled']

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

	def setAuthDataAlias(self, authDataAlias): 
		if authDataAlias is not None:
			self.opt_attributes['authDataAlias']=authDataAlias
		self.logValue()
	def getAuthDataAlias(self):
		return self.opt_attributes['authDataAlias']

	def create(self):
		# Abstract class
		pass

class MQConnectionFactory(JMSConnectionFactory):
	def __init__(self, parent=None):
		JMSConnectionFactory.__init__(self, parent)
		self.man_attributes={
			'name': "",
			'jndiName' : "",
			'host' : "",
		}
		self.opt_attributes={
			'description': "",
			'XAEnabled':"true",
			'port' : 0,
			'channel' : "",
			'queueManager' : "",
			'transportType' : "BINDINGS",
			'authDataAlias': ""
		}
		# Session pool options
		self.__sessionPool={
			"minConnections" : 1,
			"maxConnections" : 10,
			"unusedTimeout" : 1800,
			"agedTimeout" : 0,
			"reapTime" : 180,
			"connectionTimeout" : 180,
		    "purgePolicy": "EntirePool"
		}
		self.__ssl={
			'sslType':None,
			'sslConfiguration':None
		}

	def getOptAttributes(self):
		return self.__ssl.keys()+JMSConnectionFactory.getOptAttributes(self)+[ "session%s%s" % (k[0].upper(),k[1:]) for k in self.__sessionPool.keys()]

	def setHost(self, host):
		if host is not None:
			self.man_attributes['host']=host
		self.logValue()
	def getHost(self):
		return self.man_attributes['host']
	def setPort(self, port):
		if port is not None:
			self.opt_attributes['port']=port
		self.logValue()
	def getPort(self):
		return self.opt_attributes['port']
	def setChannel(self, channel):
		if channel is not None:
			self.opt_attributes['channel']=channel
		self.logValue()
	def getChannel(self):
		return self.opt_attributes['channel']
	def setQueueManager(self, queueManager):
		if queueManager is not None:
			self.opt_attributes['queueManager']=queueManager
		self.logValue()
	def getQueueManager(self):
		return self.opt_attributes['queueManager']
	def setTransportType(self, transportType):
		if transportType is not None:
			if transportType not in ['BINDINGS', 'CLIENT', 'DIRECT', 'QUEUED']: raise Exception('JMS transport type should be: BINDINGS|CLIENT|DIRECT|QUEUED')
			self.opt_attributes['transportType']=transportType
		self.logValue()
	def getTransportType(self):
		return self.opt_attributes['transportType']

	def setSessionMinConnections(self, minSessions):
		if minSessions is not None:
			self.__sessionPool['minConnections']=minSessions
		self.logValue()
	def getSessionMinConnections(self):
		return self.__sessionPool['minConnections']
	def setSessionMaxConnections(self, maxSessions):
		if maxSessions is not None:
			self.__sessionPool['maxConnections']=maxSessions
		self.logValue()
	def getSessionMaxConnections(self):
		return self.__sessionPool['maxConnections']
	def setSessionUnusedTimeout(self, sessionUnusedTimeout):
		if sessionUnusedTimeout is not None:
			self.__sessionPool['unusedTimeout']=sessionUnusedTimeout
		self.logValue()
	def getSessionUnusedTimeout(self):
		return self.__sessionPool['unusedTimeout']
	def setSessionAgedTimeout(self, sessionAgedTimeout):
		if sessionAgedTimeout is not None:
			self.__sessionPool['agedTimeout']=sessionAgedTimeout
		self.logValue()
	def getSessionAgedTimeout(self):
		return self.__sessionPool['agedTimeout']
	def setSessionReapTime(self, sessionReapTime):
		if sessionReapTime is not None:
			self.__sessionPool['reapTime']=sessionReapTime
		self.logValue()
	def getSessionReapTime(self):
		return self.__sessionPool['reapTime']
	def setSessionConnectionTimeout(self, connectionTimeout):
		if connectionTimeout is not None:
			self.__sessionPool['connectionTimeout']=connectionTimeout
		self.logValue()
	def getSessionConnectionTimeout(self):
		return self.__sessionPool['connectionTimeout']
	def setSessionPurgePolicy(self, purgePolicy):
		if purgePolicy is not None:
			self.__sessionPool['purgePolicy']=purgePolicy
		self.logValue()
	def getSessionPurgePolicy(self):
		return self.__sessionPool['purgePolicy']

	def setSslType(self, sslType):
		if sslType is not None:
			if sslType not in ['SPECIFIC','CENTRAL']:
				raise Exception("SSLType should be SPECIFIC or CENTRAL")
			else:
				self.__ssl['sslType']=sslType
		self.logValue()
	def getSslType(self):
		return self.__ssl['sslType']
	def setSslConfiguration(self, sslConfiguration):
		if sslConfiguration is not None:
			self.__ssl['sslConfiguration']=sslConfiguration
		self.logValue()
	def getSslConfiguration(self):
		return self.__ssl['sslConfiguration']

	def getStatistics(self):
		servers=AdminControl.queryMBeans('type=Perf,*')	
		for s in servers.toArray():
			j2cfs=AdminControl.queryMBeans('type=Server,node=%s,process=%s,*' % (s.getObjectName().getKeyProperty("node"),s.getObjectName().getKeyProperty("process") ))
			for j in j2cfs.toArray():
				j2cStats=AdminControl.invoke_jmx(s.getObjectName(),'getStatsObject',[j.getObjectName(),java.lang.Boolean('true')],['javax.management.ObjectName','java.lang.Boolean'])
				if j2cStats is not None:
					for i in j2cStats.subCollections():
						if i.getName()=="j2cModule":
							for h in j2cStats.getStats("j2cModule").getSubStats():
								for k in h.getSubStats():
									if k.getName()==self.getJndiName():
										print k.getName()
		WASConfig.getStatistics(self)
		
	def create(self):
		WASConfig.create(self)
		templateList = Util.wslist(AdminConfig.listTemplates( self.getConfigType() ))
		templateToUse = None
		for template in templateList:
			if ( AdminConfig.showAttribute( template, "XAEnabled" )==self.getXAEnabled() ):
				templateToUse = template
				break
		if templateToUse == None: raise Exception("No proper template found for : %s, xa: %s" % (self.getType(),self.getXAEnabled()))
		authOptions=[]
		options=Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes)
		if self.getAuthDataAlias() is not None:
			options.append(["xaRecoveryAuthAlias", self.getAuthDataAlias()])
		if self.getSslType() is not None:
			options.append(["sslType", self.getSslType()])
		if self.getSslConfiguration() is not None:
			options.append(["sslConfiguration", self.getSslConfiguration()])
		logger.debug("jmsOptions : %s" % options)
		self.configID=AdminConfig.createUsingTemplate(self.getConfigType(), self.getParent().getConfigID(), options, templateToUse )
		if self.getAuthDataAlias() is not None:
			AdminConfig.create('MappingModule', self.getConfigID(), [ ['authDataAlias', self.getAuthDataAlias()], ['mappingConfigAlias','DefaultPrincipalMapping']])
		logger.info("Setting connection pool options for %s: %s" % (self.getType(),self.getName()))
		logger.debug("connectionPool : %s" % self.connectionPool)
		connectionPool = AdminConfig.showAttribute( self.getConfigID(), "connectionPool" )
		AdminConfig.modify( connectionPool, Util.dictToList(self.connectionPool) )
		logger.info("Setting session pool options for %s: %s" % (self.getType(),self.getName()))
		logger.debug("sessionPool : %s" % self.__sessionPool)
		sessionPool = AdminConfig.showAttribute( self.getConfigID(), "sessionPool" )
		AdminConfig.modify( sessionPool, Util.dictToList(self.__sessionPool))
		logger.info("Succesfully created %s: %s" % (self.getType(),self.getName()))

class MQQueueConnectionFactory(MQConnectionFactory):
	def __init__(self, parent=None):
		MQConnectionFactory.__init__(self, parent)

class MQTopicConnectionFactory(MQConnectionFactory):
	def __init__(self, parent=None):
		MQConnectionFactory.__init__(self, parent)

class JmsDestination(WASConfig):
	"""
	Class to represent a JMS Destination, either a queue or a topic.

	Author: Andre van Dijk (SuperClass IT)
	$Rev: 424 $
	"""
	level=4
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["JMSProvider"]
		self.man_attributes={
			'name':"",
			'jndiName':""
		}
		self.opt_attributes={
			 "expiry" : "APPLICATION_DEFINED",
			 "persistence" : "APPLICATION_DEFINED",
			 "priority" : "APPLICATION_DEFINED",
			 "specifiedExpiry" : 0,
			 "specifiedPriority" : 0
		}

	def setJndiName(self, jndi):
		if jndi is not None:
			self.man_attributes['jndiName']=jndi
		self.logValue()
	def getJndiName(self):
		return self.man_attributes['jndiName']

	def setExpiry(self, expiry):
		if expiry is not None:
			expiries = ["APPLICATION_DEFINED","SPECIFIED","UNLIMITED"]
			if expiry not in expiries: raise Exception("Illegal JMS Destination expiry: should be APPLICATION_DEFINED, SPECIFIED or UNLIMITED")
			self.opt_attributes['expiry']=expiry
		self.logValue()
	def getExpiry(self):
		return self.opt_attributes['expiry']
	def setPersistence(self, persistence):
		if persistence is not None:
			persistences = ["APPLICATION_DEFINED","SPECIFIED","UNLIMITED"]
			if persistence not in persistences: raise Exception("Illegal JMS Destination persistence: should be APPLICATION_DEFINED, SPECIFIED or UNLIMITED")
			self.opt_attributes['persistence']=persistence
		self.logValue()
	def getPersistence(self):
		return self.opt_attributes['persistence']
	def setPriority(self, priority):
		if priority is not None:
			priorites = ["APPLICATION_DEFINED","SPECIFIED","UNLIMITED"]
			if priority not in priorities: raise Exception("Illegal JMS Destination priority: should be APPLICATION_DEFINED, SPECIFIED or UNLIMITED")
			self.opt_attributes['priority']=priority
		self.logValue()
	def getPriority(self):
		return self.opt_attributes['priority']
	def setSpecifiedExpiry(self, specifiedExpiry):
		if specifiedExpiry is not None:
			self.opt_attributes['specifiedExpiry']=specifiedExpiry
		self.logValue()
	def getSpecifiedExpiry(self):
		return self.opt_attributes['specifiedExpiry']
	def setSpecifiedPriority(self, specifiedPriority):
		if specifiedPriority is not None:
			self.opt_attributes['specifiedPriority']=specifiedPriority
		self.logValue()
	def getSpecifiedPriority(self):
		return self.opt_attributes['specifiedPriority']

	def create(self):
		# Abstract class
		pass

class MQDestination(JmsDestination):
	"""
	Class to represent a MQQueue.

	Author: Andre van Dijk (SuperClass IT)
	$Rev: 424 $
	"""
	def __init__(self, parent=None):
		JmsDestination.__init__(self, parent)
		self.man_attributes={
			'name':"",
			'jndiName':""
		}
		self.opt_attributes.update({
			"targetClient" : "MQ",
			"useNativeEncoding" : "false",
			"decimalEncoding" : "Normal" ,
			"integerEncoding" : "Normal" ,
			"floatingPointEncoding" : "IEEENormal"
		})
	def setCcsid(self, ccsid):
		if ccsid is not None:
			self.opt_attributes['CCSID']=ccsid
			self.logValue()
	def getCcsid(self):
		return self.opt_attributes['CCSID']
	def setTargetClient(self, targetClient):
		if targetClient is not None:
			targetClients = ["MQ","JMS"]
			if targetClient not in targetClients: raise Exception("Illegal JMS Destination targetclient: should be MQ or JMS")
			self.opt_attributes['targetClient']=targetClient
		self.logValue()
	def getTargetClient(self):
		return self.opt_attributes['targetClient']
	def setUseNativeEncoding(self, useNativeEncoding):
		if useNativeEncoding is not None:
			self.opt_attributes['useNativeEncoding']=useNativeEncoding
		self.logValue()
	def getUseNativeEncoding(self):
		return self.opt_attributes['useNativeEncoding']
	def setDecimalEncoding(self, decimalEncoding):
		if decimalEncoding is not None:
			decimalEncodings = ["Normal","Reversed"]
			if decimalEncoding not in decimalEncodings: raise Exception("Illegal JMS Destination decimalEncoding: should be Normal or Reversed")
			self.opt_attributes['decimalEncoding']=decimalEncoding
		self.logValue()
	def getDecimalEncoding(self):
		return self.opt_attributes['decimalEncoding']
	def setIntegerEncoding(self, integerEncoding):
		if integerEncoding is not None:
			integerEncodings = ["Normal","Reversed"]
			if integerEncoding not in integerEncodings: raise Exception("Illegal JMS Destination integerEncoding: should be Normal or Reversed")
			self.opt_attributes['integerEncoding']=integerEncoding
		self.logValue()
	def getIntegerEncoding(self):
		return self.opt_attributes['integerEncoding']
	def setFloatingPointEncoding(self, floatingPointEncoding):
		if floatingPointEncoding is not None:
			floatingPointEncodings = ["IEEENormal","IEEEReversed","S390"]
			if floatingPointEncoding not in floatingPointEncodings: raise Exception("Illegal JMS Destination floatingPointEncoding: should be IEEENormal, IEEEReversed or S390")
			self.opt_attributes['floatingPointEncoding']=floatingPointEncoding
		self.logValue()
	def getFloatingPointEncoding(self):
		return self.opt_attributes['floatingPointEncoding']


	def create(self):
		WASConfig.create(self)
		AdminConfig.create(self.getConfigType(), self.getParent().getConfigID(), Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes) )

class MQQueue(MQDestination):
	"""
	Class to represent a MQTopic.

	Author: Andre van Dijk (SuperClass IT)
	$Rev: 424 $
	"""
	def __init__(self, parent=None):
		MQDestination.__init__(self, parent)
		self.man_attributes.update({
			"baseQueueName" : ""
		})
		self.opt_attributes.update({
			"baseQueueManagerName" : ""
		})
	def setBaseQueueName(self, mqName):
		if mqName is not None:
			self.man_attributes['baseQueueName']=mqName
		self.logValue()
	def getBaseQueueName(self):
		return self.man_attributes['baseQueueName']
	def setBaseQueueManagerName(self, queueManagerName):
		if queueManagerName is not None:
			self.opt_attributes['baseQueueManagerName']=queueManagerName
		self.logValue()
	def getBaseQueueManagerName(self):
		return self.opt_attributes['baseQueueManagerName']

class MQTopic(MQDestination):
	"""
	Class to represent a MQTopic.

	Author: Andre van Dijk (SuperClass IT)
	$Rev: 424 $
	"""
	def __init__(self, parent=None):
		MQDestination.__init__(self, parent)
		self.man_attributes.update({
			"baseTopicName" : ""
		})

	def setBaseTopicName(self, mqName):
		if mqName is not None:
			self.man_attributes['baseTopicName']=mqName
		self.logValue()
	def getBaseTopicName(self):
		return self.man_attributes['baseTopicName']
