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

# Config Class
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-07-15 15:37:37 +0200 (ma, 15 jul 2013) $
# $Id: config.py 458 2013-07-15 13:37:37Z andre $
import java.util.Properties as jProperties
import java.io.FileInputStream as FileInputStream
import java.io.FileOutputStream as FileOutputStream
import Util
import re
import os
import time

# Source sub modules that contain the WasConfig classes
execfile('%s/wasconfig.py' % scriptdir)
execfile('%s/cell.py' % scriptdir)
execfile('%s/cluster.py' % scriptdir)
execfile('%s/server.py' % scriptdir)
execfile('%s/node.py' % scriptdir)
execfile('%s/virtualhost.py' % scriptdir)
execfile('%s/jms.py' % scriptdir)
execfile('%s/namespacebinding.py' % scriptdir)
execfile('%s/wasvariable.py' % scriptdir)
execfile('%s/sharedlibrary.py' % scriptdir)
execfile('%s/workmanager.py' % scriptdir)
execfile('%s/mail.py' % scriptdir)
execfile('%s/url.py' % scriptdir)
execfile('%s/scheduler.py' % scriptdir)
execfile('%s/datasource.py' % scriptdir)
execfile('%s/jaas.py' % scriptdir)
execfile('%s/application.py' % scriptdir)
execfile('%s/nagios.py' % scriptdir)
execfile('%s/objectcache.py' % scriptdir)
execfile('%s/replication.py' % scriptdir)
execfile('%s/dynamicsslconfigselection.py' % scriptdir)
execfile('%s/sslconfig.py' % scriptdir)

class Config:
	"""
	config.py

	The Config class is used for reading the configuration
	property files and setting up the config objects (ServerCluster,
	Application, Server etc.) based on the contents found in
	the property file.

	The validate method validate the mandatory properties of
	the wasconfig objects by calling their validate method.

	Default values for wasconfig objects are loaded from property
	files with the name of each wasconfig class in the defaults
	directory (eg Server.properties). If a values is not found
	in the user provided property file these defaults are used
	otherwise hardcoded defaults are provided in the wasconfig
	objects for non mandatory properties.

	All errors are reported through exceptions. Logging is done
	through the logger object, that is assumed to be setup and
	available before the class is instantiated.
	"""

	def __init__(self):
		""" Initialises the Config object and sets default """
		self.__props=jProperties()
		self.__defaults=jProperties()
		self.__predefs=jProperties()
		self.__dryRun=0
		self.__nagiosFifo="/tmp/superwasnagios"
		self.__wasObjects={
			"Cell":[],
			"Node":[],
			"ServerCluster":[],
			"Server":[],
			"EnvEntry":[],
			"CustomJVMParam":[],
			"CustomSessionParam":[],
			"MessageListener":[],
			"WebServer":[],
			"JAASAuthData":[],
			"VirtualHost":[],
			"HostAlias":[],
			"AS400JDBCProvider":[],
			"AS400XAJDBCProvider":[],
			"ORAJDBCProvider":[],
			"ORAXAJDBCProvider":[],
			"DB2JDBCProvider":[],
			"DB2XAJDBCProvider":[],
			"AS400DataSource":[],
			"DB2DataSource":[],
			"JMSProvider":[],
		    "JMSConnectionFactory":[],
		    "MQQueueConnectionFactory":[],
			"MQTopicConnectionFactory":[],
			"MQQueue":[],
			"MQTopic":[],
			"StringNameSpaceBinding":[],
			"EjbNameSpaceBinding":[],
			"CORBAObjectNameSpaceBinding":[],
			"IndirectLookupNameSpaceBinding":[],
			"MailProvider":[],
			"MailSession":[],
			"URLProvider":[],
			"URL":[],
			"WorkManagerProvider":[],
			"WorkManager":[],
			"SchedulerProvider":[],
			"SchedulerConfiguration":[],
			"WASVariable":[],
			"SharedLibrary":[],
			"Application":[],
			"WebModule":[],
			"WebServerTarget":[],
			"BeanRef":[],
			"ResRef":[],
			"Role":[],
			"CmpRef":[],
			"ResRef":[],
			"EjbRef":[],
			"EjbEnv":[],
			"ResEnv":[],
			"MesBind":[],
			"MesRef":[],
			"CacheProvider":[],
			"ObjectCacheInstance":[],
			"CustomResourceProperty":[],
			"DataReplicationDomain":[],
			"DynamicSSLConfigSelection":[],
			"KeyStore":[],
			"SSLConfig":[],
			"WebContainerProperty":[],
			"PMIModule":[],
		}

	def setPropFile(self, propfile):
		if propfile!="":
			try:
				self.__props.load(FileInputStream(propfile))
				logger.info("Property file %s succesfully loaded." % propfile)
			except:
				raise Exception("Unable to load property file %s, check if file exists and file permissions" % propfile)
			self.__validateAllSections()

	def setFifo(self, fifo):
		if fifo!="": self.__nagiosFifo=fifo
		logger.debug("Nagios fifo : %s" % self.__nagiosFifo)

	def setDryRun(self, dryRun):
		self.__dryRun=dryRun

	def save(self):
		if self.__dryRun==0:
			logger.info("Saving configuration...")
			AdminConfig.save()
			nodes=AdminConfig.list("Node").split()
			for n in nodes:
				nodeName=AdminConfig.showAttribute(n, 'name')
				syncn=AdminControl.completeObjectName('type=NodeSync,node=%s,process=nodeagent,*' % nodeName)
				if syncn!="":
					logger.info("Syncing node : %s" % nodeName)
					syncResult = "false"
					count = 0
					while syncResult != "true" and count < 5:
						logger.info("Syncing node : %s" % nodeName)
						syncResult=AdminControl.invoke(syncn,"sync")
						logger.info("Sync result is : %s" % syncResult)
						count = count + 1
					if syncResult != "true":
						logger.warn("Sync failed!")
		else:
			logger.info("Dry run not saving config...")

	def getWasConfigTypes(self):
		return self.__wasObjects.keys()

	def getOrderedWasConfigTypes(self):
		sl={}
		for i in self.__wasObjects.keys():
			cmd="level=%s.level" % i
			exec cmd
			if sl.has_key(level):
				sl[level].append(i)
			else:
				sl[level]=[i]
		ret=[]
		keys=sl.keys()
		keys.sort()
		for i in keys:
			ret+=sl[i]
		return ret

	def getCell(self):
		return self.getWasObjects('Cell')[0]
			
	def getWasObjects(self, name):
		if self.__wasObjects.has_key(name):
			return self.__wasObjects[name]
	def setWasObjects(self, name, objectList):
		self.__wasObjects[name]=objectList

	def validate(self):
		for i in self.getOrderedWasConfigTypes():
			for o in self.getWasObjects(i):
				o.validate()	

	def __validateAllSections(self):
		"""
		Validate all sections of the property file by calling
		each validate method.
		"""
		logger.info(" -- Validating property file")
		self.setWasObjects("Cell",[Cell()])
		self.setWasObjects("Node",self.__getNodes())
		# Property file with defaults
		self.__defaults=jProperties()
		self.__predefs=jProperties()
		for i in self.getWasConfigTypes():
			if i=="Cell" or i=="Node":
				logger.debug("skipping cell or node")
				continue
			try:
				self.__defaults.load(FileInputStream("%s/defaults/%s.properties" % (scriptdir,i)))
				logger.info("Property defaults succesfully loaded for : %s" % i)
			except:
				logger.debug("Property defaults could not be loaded for : %s" % i)
			try:
				self.__predefs.load(FileInputStream("%s/predefs/%s.properties" % (scriptdir,i)))
				logger.info("Predefs succesfully loaded for : %s" % i)
			except:
				logger.debug("Predefs could not be loaded for : %s" % i)

		for i in self.getOrderedWasConfigTypes():
			if i=="Cell" or i=="Node":
				logger.debug("skipping cell or node")
				continue
			self.setWasObjects(i, self.__parseWasObjects(i))
			if i=="Server":
				# Clone servers
				for i in self.getWasObjects('Server'):
					clone=i.getClone()
					master=None
					if clone!="":
						for m in self.getWasObject('Server'):
							if m.getName()==clone:
								master=m
								break
						if master!=None:
							i.clone(master)
						else:
							raise Exception("Clone should point to a defined master")
		logger.info(" -- Done validating property file")
		for i in self.getWasConfigTypes():
			if i=="Cell" or i=="Node":
				logger.debug("skipping cell or node")
				continue
			predef=self.__parsePreDefWasObjects(i)
			logger.debug("Predef %s : %s" % (i,predef))
			self.__wasObjects[i]+=predef

	def __parsePreDefWasObjects(self, type):
		objlist=[]
		cmd="obj=%s()" % type
		exec cmd
		for s in self.__getSequence(obj.getKey(), obj.getAttributes(), obj.getKeyAttribute(), 1):
			for a in obj.getManAttributes()+obj.getOptAttributes():
				cmd='obj.set%s(s["%s"])' % (a[0].upper()+a[1:], a)
				exec cmd
			for a in obj.getRefAttributes():
				cmd='refType=obj.get%sType()' % (a[0].upper()+a[1:])
				exec cmd
				found=0
				for r in self.__wasObjects[refType]:
					if r.getName()==s[a]:
						cmd='obj.set%s(r)' % (a[0].upper()+a[1:])
						exec cmd
						found=1
						break
				if not found: raise Exception("Reference object not found : %s.%s %s " % (s['_key'],s['_index'],s[a]))
			for a in obj.getDynAttributes():
				obj.setAttribute(a, self.__getProperty(s['_key'],a,s['_index']))
			if s['scope'] in self.getWasConfigTypes():
				for i in self.getWasObjects(s['scope']):
					obj.setParent(i)
					clone=obj.clone()
					clone.validate()
					objlist.append(clone)
			cmd="obj=%s()" % type
			exec cmd
		return objlist

	def __parseWasObjects(self, type):
		objlist=[]
		cmd="obj=%s()" % type
		exec cmd
		for s in self.__getSequence(obj.getKey(), obj.getAttributes(), obj.getKeyAttribute()):
			obj.setParent(self.__getScope(s))
			for a in obj.getManAttributes()+obj.getOptAttributes():
				cmd='obj.set%s(s["%s"])' % (a[0].upper()+a[1:], a)
				exec cmd
			for a in obj.getRefAttributes():
				if s[a] is not None:
					cmd='refType=obj.get%sType()' % (a[0].upper()+a[1:])
					exec cmd
					found=0
					for r in self.__wasObjects[refType]:
						if r.getName()==s[a]:
							cmd='obj.set%s(r)' % (a[0].upper()+a[1:])
							exec cmd
							found=1
							break
					if not found: raise Exception("Reference object not found : %s.%s %s " % (s['_key'],s['_index'], s[a]))
			for a in obj.getDynAttributes():
				obj.setAttribute(a, self.__getProperty(s['_key'],a,s['_index']))
			obj.validate()
			objlist.append(obj)
			cmd="obj=%s()" % type
			exec cmd
		return objlist

	def __getNodes(self):
		nlist=[]
		nodes=Util.wslist(AdminConfig.list("Node"))
		for n in nodes:
			name=AdminConfig.showAttribute(n, 'name')
			# If the node contains a server called dmgr it's the dmgr node
			if AdminConfig.getid('/Node:%s/Server:dmgr/' % name) == '':
				node=Node()
				node.setParent(self.getCell())
			 	node.setName(name)
				node.validate()
				nlist.append(node)
		return nlist

#############################################################################
# Operations
#############################################################################
	def action(self, wasObject, action, name=""):
		if action=="documentation":
			for i in self.getOrderedWasConfigTypes():
				if wasObject=="" or wasObject==i:
					cmd="d=%s()" % i
					exec cmd
					print d.getDocumentation()
			return
		if action=="nagiosStats":
			self.getNagiosStatus()
			return	
		if wasObject=="":
			if action=="uninstall":
				wasConfigs=self.getOrderedWasConfigTypes()
				wasConfigs.reverse()
			else:
				wasConfigs=self.getOrderedWasConfigTypes()
		else:
			if wasObject in self.getWasConfigTypes():
				wasConfigs=[wasObject]	
			else:
				raise Exception("Invalid Config Type : %s" % wasObject)
		for i in wasConfigs:
			d=0
			for a in self.getWasObjects(i):
				if name=="" or name==a.getName():
					if action=="install":
						a.create()
						d=1
					elif action=="uninstall":
						a.remove()
						d=1
					elif action=="stop":
						a.stop()
						d=1
					elif action=="start":
						a.start()
						d=1
					else:
						raise Exception("Invalid action : %s" % action)
			if name!="" and d==0:
				logger.error("%s not found : %s" % (i,name))
		if action in ["install", "uninstall"]: self.save()

	def getServerStats(self, name):
		for a in self.__servers:
			while a.isRunning():	
				a.getStatistics()
				time.sleep(10)

	def getDataSourceStats(self, name):
		for a in self.__datasources:
			a.getStatistics()
			time.sleep(10)	

	def getJMSStats(self, name):
		for a in self.__jmsFactories:
			a.getStatistics()
			time.sleep(10)	

	def getNagiosStatus(self, name=""):
		# os io functions not implented in wsadmin jython, use java equivalents
		while 1:
			try:
				fifo=FileOutputStream(self.__nagiosFifo)
				logger.debug("Opened fifo for output : %s" % self.__nagiosFifo)
				statuslines=[]
				perflines=[]
				code=-1
				statusMessage="WAS-STATUS UNKNOWN"
				try:
					for a in self.getWasObjects('Server') + self.getWasObjects('DB2DataSource') + self.getWasObjects('AS400DataSource'):
						for s in a.getNagiosStatus():
							if (s.getPerformanceData()!=""):
								perflines.append("%s%s" % (a.getContainmentPath(),s.getPerformanceData()))
							statuslines.append("%s %s-%s" % (a.getConfigType(),a.getName(),s.getMessage()))
							if s.getCode()>code: 
								code=s.getCode()
								if code==NagiosStat.OK:
									statusmessage="WAS-OK"
								else:
									statusmessage="WAS-%s" % s.getMessage()
				except:
					logger.error("Error querying PMI state")
					logger.error(str(sys.exc_info()[1]) + "\n")
					logger.debug(sys.exc_info()[2].dumpStack() + "\n")
				if len(perflines) > 0:
					statuslines[-1]="%s|%s" % (statuslines[-1],perflines[0])
				if len(perflines[1:]) > 1:
					statuslines+=perflines[1:]
				if code==-1: code=NagiosStat.UNKNOWN
				fifo.write(java.lang.String("%s\n" % code).getBytes())
				fifo.write(java.lang.String("%s\n" % statusmessage).getBytes())
				for s in statuslines:
					fifo.write(java.lang.String(s).getBytes())
					fifo.write(java.lang.String("\n").getBytes())
				# Send EOT to end the message
				fifo.write(java.lang.String("\004").getBytes())
				fifo.close()
				logger.debug("Closed fifo for output : %s" % self.__nagiosFifo)
			except:
				fifo.close()
				logger.error("Interupted syscall, closed fifo for output : %s" % self.__nagiosFifo)
			time.sleep(1)

	def __getProperty(self, type, attribute, index, predef=0):
		"""
		Returns the property specified.

		Return:
		[type].[index].[attribute]
		"""
		key="%s.%s.%s" % (type, index, attribute)
		if predef:
			ret=self.__predefs.getProperty(str(key))
		else:
			ret=self.__props.getProperty(str(key))
		if ret is None:
			ret=self.__defaults.getProperty("%s.%s" % ((type,attribute)))
		return ret
			
	def __getSequence(self, key, attributes, keyarg, predef=0):
		"""
		Returns a list of dictionaries from the sequenced items
		in the properties file. E.g. server.0., datasource.0.

		The sequence to get is specified by the key parameter,
		eg. server or server.0.envEntry

		The attributes to get is specified by the list attributes. These attributes will be the keys of the dict.

		keyarg specifies which attribute to use as key, ie.
		which attribute will always be present for a sequence,
		typically this is the name attribute.
		"""
		attributes=attributes
		i=0
		ret=[]
		while 1:
			d={}
			p=self.__getProperty(key,keyarg,str(i),predef)
			if p is None:
				break
			d[keyarg]=p
			# Store key + index for usage in error printing
			d['_key']=key
			d['_index']=str(i)
			for attr in attributes:
				if attr==keyarg: continue
				p=self.__getProperty(key,attr,str(i),predef)
				d[attr]=p
			ret.append(d)
			i+=1
		return ret
		
	def __getScope(self, s):
		parent=s['parent']
		scope=s['scope']
		if scope is None and parent is not None:
			raise Exception("Invalid scope for %s.%s missing scope attribute." % (s['_key'],s['_index']))
		if scope is not None and parent is None:
			raise Exception("Invalid parent for %s.%s missing parent attribute." % (s['_key'],s['_index']))
		if scope is None and parent is None: return self.getCell()

		if scope not in self.getWasConfigTypes():
			raise Exception("Invalid scope : %s" % scope)
		for i in self.getWasObjects(scope):
			if i.matchName(parent): return i
		raise Exception("Parent %s : %s not found for %s.%s" %(scope,parent,s['_key'],s['_index']))
