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

# WASConfig class. Base Class for all Config classes
#
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-02-11 21:23:24 +0100 (ma, 11 feb 2013) $
# $Id: wasconfig.py 445 2013-02-11 20:23:24Z andre $
class WASConfig:
	level=0
	"""
	Super class representing WAS Config object. All other WAS
	Config objects are derrived from this class.

	Author: Andre van Dijk (SuperClass IT)
	Date: $Date: 2013-02-11 21:23:24 +0100 (ma, 11 feb 2013) $

	$Id: wasconfig.py 445 2013-02-11 20:23:24Z andre $
	"""

	def __init__(self, parent=None):
		"""
		Constructor

		Initialise instance variables.

		Set parent if it is provided, the parent is the WASConfig
		object that contains this object.

		Subclasses should extend this constructor to initialise
		their own instance variables.
		"""

		logger.debug("Constructing : %s" % self.getType())

		self.configID=""
		self.parent=""
		self.children=[]
		self.valid="false"

		self.wasDefault="false"

		self.stats=[]
		
		self.man_attributes={'name' : ""}
		self.opt_attributes={}
		# Attributes that will cause a lookup to reference a WAS config object, like MailProtocol etc.
		self.ref_attributes={}
		self.parent_attributes={
			'parent' : "",
			'scope' : ""
		}
		# Normally no dynamic attributes, used by DataSource
		self.dyn_opt_attributes={}
		self.dyn_man_attributes={}
		self.validParents=["Cell", "Node", "Server", "ServerCluster"]

		if parent is not None:
			self.setParent(parent)

	def setConfigID(self):
		"""
		Fetch the WAS config ID from WAS for this WASConfig object if it exists.
		"""
		logger.debug("Getting Config ID : %s" % self.getContainmentPath())
		self.configID=AdminConfig.getid(self.getContainmentPath())
		self.logValue()

	def getConfigID(self):
		"""
		Return the WAS config ID for this WASConfig object if it exists.
		"""
		return self.configID

	def getKey(self):
		"""# Returns the key attribute to be used in the config file"""
		return self.__class__.__name__.lower()

	def getKeyAttribute(self):
		return "name"

	def getAttributes(self):
		"""# Returns all the supported property file attributes for this class """
		return self.getManAttributes() + self.getOptAttributes() + self.getParentAttributes() + self.getDynAttributes() + self.getRefAttributes()

	def getManAttributes(self):
		"""# Returns all the mandatory property file attributes for this class """
		return self.man_attributes.keys()

	def getOptAttributes(self):
		"""# Returns all the optional property file attributes for this class """
		return self.opt_attributes.keys()

	def getDynManAttributes(self):
		return self.dyn_man_attributes.keys() 

	def getDynOptAttributes(self):
		return self.dyn_opt_attributes.keys() 

	def getDynAttributes(self):
		"""# Returns the attributes that need to be set through setAttribute, these attributes are dynamically retrieved from WAS. Used by Datasources."""
		return self.getDynManAttributes() + self.getDynOptAttributes()

	def getParentAttributes(self):
		"""# Returns all the property file attributes to specify scope and parent for this class """
		return self.parent_attributes.keys()

	def getRefAttributes(self):
		"""# Returns all the property file attributes to specify scope and parent for this class """
		return self.ref_attributes.keys()

	def setAttribute(self, attribute, value):
		if value is not None:
			if attribute in self.getDynManAttributes():
				self.dyn_man_attributes[attribute].setValue(value)
			elif attribute in self.getDynOptAttributes():
				self.dyn_opt_attributes[attribute].setValue(value)
			else:
				raise Exception("Attribute invalid : %s" % attribute)
		logger.debug("Attribute : %s value : %s" % (attribute, self.getAttribute(attribute)))
			
	def getAttribute(self, attribute):
		if attribute in self.getDynManAttributes():
			return self.dyn_man_attributes[attribute].getValue()
		elif attribute in self.getDynOptAttributes():
			return self.dyn_opt_attributes[attribute].getValue()
		else:
			raise Exception("Attribute invalid : %s" % attribute)
			
	def getDocumentation(self):
		docstring="##############################################################################\n"
		docstring+="# %s\n#\n%s\n#\n" % (self.__class__.__name__,self.__doc__)
		docstring+="\n# Mandatory Attributes\n#\n"
		for a in self.man_attributes.keys():
			cmd='h=self.set%s.__doc__' % (a[0].upper()+a[1:])
			exec cmd
			if h is None: h=""
			docstring+="# %s:\n%s\n" % (a,h)
			docstring+="%s.0.%s=%s\n\n" % (self.__class__.__name__.lower(),a,self.man_attributes[a])

		docstring+="\n# Optional Attributes\n#\n"
		for a in self.opt_attributes.keys():
			cmd='h=self.set%s.__doc__' % (a[0].upper()+a[1:])
			exec cmd
			if h is None: h=""
			docstring+="# %s:\n%s\n" % (a,h)
			docstring+="%s.0.%s=%s\n\n" % (self.__class__.__name__.lower(),a,self.opt_attributes[a])
		for a in self.ref_attributes.keys():
			cmd='h=self.set%s.__doc__' % (a[0].upper()+a[1:])
			exec cmd
			if h is None: h=""
			docstring+="# %s:\n%s\n" % (a,h)
			docstring+="%s.0.%s=" % (self.__class__.__name__.lower(),a)
			if self.ref_attributes[a]!=None:
				docstring+=self.ref_attributes[a].getName()
			docstring+="\n\n"

		docstring+="\n# Parent Attributes\n#\n"
		docstring+="#Valid parents:\n#"
		for i in self.validParents:
			docstring+=" %s" % i
		docstring+="\n\n"
		
		for a in self.parent_attributes.keys():
			cmd='h=self.set%s.__doc__' % (a[0].upper()+a[1:])
			exec cmd
			if h is None: h=""
			docstring+="# %s:\n%s\n" % (a,h)
			docstring+="%s.0.%s=%s\n\n" % (self.__class__.__name__.lower(),a,self.parent_attributes[a])

		return docstring

	def setName(self, name):
		"""# Set the name of this object and print a log message with the type of the object and the name."""
		self.man_attributes[self.getKeyAttribute()]=name
		self.logValue()

	def getName(self):
		"""
		Return the name of this WASConfig object.
		"""
		return self.man_attributes[self.getKeyAttribute()]

	def getQualifiedName(self):
		if self.getParent().getConfigType()!="Cell":
			return "%s.%s" % (self.getParent().getQualifiedName(),self.getName())
		else:
			return self.getName()

	def getCell(self):
		"""
		Return the cell object. The cell subclass overrides this
		method and returns its self. Other classes should stick
		to the default implementation, which return the cell
		of the parent. So Eventually the cell will
		be returned by the cell object.
		"""
		return self.getParent().getCell()

	def clone(self):
		"""
		Return an new instance of the WASConfig object containing the same value.
		"""
		cmd="c=%s()" % self.getType()
		exec cmd
		for i in self.getAttributes():
			cmd="c.set%s(self.get%s())" % ((i[0].upper()+i[1:]),(i[0].upper()+i[1:]))
			exec cmd
		return c

	def setScope(self, scope):
		"""# Use this to specify the type of the parent object for this object."""
		pass

	def setParent(self, parent):
		"""# Set the parent of this object. Parent should be another WASConfig object. If parent is not an instance of a WASConfig object or not a valid parent for this object an exception is raised. See the list of valid parents."""
		if parent.getType() in self.validParents: 
			self.parent=parent
		else:
			raise Exception('Invalid parent : %s for %s parent has to be %s' % (parent.getType(),self.getType(),self.validParents))
		parent.addChild(self)
		self.logValue()

	def getParent(self):
		return self.parent

	def getScope(self):
		return self.getParent().getType()


	def getContainmentPath(self):
		"""
		Return the containment path for this object. Return
		the containment path of the WASConfig object, each
		object add its own type and name and calls this
		method recursively on its parent until the cell
		object is reached.
		"""
		return "%s%s:%s/" % (self.getParent().getContainmentPath(),self.getConfigType(),self.getName())

	def getSecurity(self):
		return self.getCell().getSecurity()

	def getMbean(self):
		"""
		For an existing WASConfig object return the Mbean. This
		reference can be used to perform operations like stop
		or start. Subclasses should override this method to
		return the appropriate Mbean.
		"""
		if self.getConfigID() != "":
			return AdminConfig.getObjectName(self.getConfigID())
		return ""

	def getStatistics(self):
		"""
		Get PMI statistics
		"""
		logger.debug("%s %s Statistics : %s" % (self.getType(), self.getName(), self.stats))

	def getNagiosStatus(self):
		logger.debug("Getting nagios status for %s : %s" % (self.getType(), self.getName()))

	def getType(self):
		return self.__class__.__name__

	def getConfigType(self):
		"""
		Return the name of the WASConfig object, eg. Cell,
		Server etc.
		"""
		return self.getType()

	def addChild(self, child):
		if isinstance(child, WASConfig):
			self.children.append(child)
		else:
			raise Exception("Child is not a WASConfig object")
		logger.debug("%s : %s added %s child" % (self.getConfigType(),self.getName(),child.getType()))

	def getChildren(self):
		return self.children

	def validate(self):
		"""
		This method check if the object has been setup properly.
		It will check if all the manadatory fields have
		been filled in. If all the attributes have been
		filled in the ConfigID is fetched from WebSphere
		and stored if the corresponding WebSphere object
		can be found.This method should be called
		before calling any of the methods: stop, start,
		isRunning, remove or create. An exception stating
		the missing attribute name will be raised if
		attributes are missing.
		"""
		if self.getParent() == "":
				raise Exception("Missing parent for %s : %s" % (self.getType(), self.getName()))
		if self.wasDefault=="false":
			for i in self.getManAttributes():
				if self.man_attributes[i] == "":
					raise Exception("Missing attribute %s for %s" % (i, self.getType()))
			for i in self.getDynManAttributes():
				if self.getAttribute(i)=="":
					raise Exception("Missing attribute %s for %s" % (i, self.getType()))
		self.setConfigID()
		self.valid="true"
		logger.debug("%s validity : %s" % (self.getType(), self.isValid()))

	def isValid(self):
		return self.valid

	def matchName(self, name):
		if name.find(".") == -1:
			return self.getName()==name
		return self.getQualifiedName()==name

	def stop(self):
		"""
		Perform the stop operation on this WASConfig object.
		Subclasses should provide the appropriate
		implementation for this method.
		"""
		pass

	def start(self):
		"""
		Perform the start operation on this WASConfig object.
		Subclasses should provide the appropriate
		implementation for this method.
		"""
		pass

	def isRunning(self):
		"""
		Return whether the WASConfig object is running in WAS.
		Returns true (1) or false (0)
		"""
		if not self.isValid():
			raise Exception("%s %s is not validated" % (self.getType(), self.getName()))
		if self.getConfigID()=="":
			raise Exception("%s %s is not defined" % (self.getType(), self.getName()))
		mb=self.getMbean()
		if mb != "":
			if AdminControl.getAttribute(mb, "state") == "STARTED": return 1
		return 0

	def remove(self):
		"""
		Remove the WASConfig object from the WAS configuration.
		Subclasses should override with the appropriate
		implementation for this method.
		"""
		if self.wasDefault!="true":
			if self.getConfigID()!="":
				logger.info("Removing %s : %s" % (self.getType(), self.getName()))
				AdminConfig.remove(self.getConfigID())
			self.configID=""

	def create(self):
		"""
		Create the WASConfig object in the WAS configuration.
		Subclasses should provide the appropriate
		implementation for this method.
		"""
		if self.wasDefault=="true":
			logger.debug("Default object getting configID %s : %s" % (self.getType(),self.getName()))
			self.setConfigID()
			if self.getConfigID()=="":
				logger.debug("Default object not found attempting to create : %s : %s" % (self.getType(),self.getName()))
				template=AdminConfig.listTemplates(self.getConfigType(),"default|resources")
				logger.debug("Found template : %s" % template)
				if template=="":
					raise Exception("Failed to find template for : %s : %s" % (self.getType(),self.getName()))
				self.configID=AdminConfig.createUsingTemplate(self.getConfigType(),self.getParent().getConfigID(),Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes),template)
		else:
			logger.info("Creating %s : %s" % (self.getType(),self.getName()))
			if self.getConfigID()!='':
				raise Exception("%s : %s already exists, uninstall first" % (self.getType(),self.getName()))

	def logValue(self):
		"""
		Write a the value of a setter method to the debug
		log. To be called by setter methods.
		"""
		setter=sys._getframe(1).f_code.co_name
		getter=""
		if setter.startswith("set"):
			getter="g" + setter[1:]
		else:
			raise Exception("logValue should be called only by setter methods")
		cmd="val=self.%s()" % getter
		exec cmd
		if isinstance(val, WASConfig): val=val.getName()
		logger.debug("%s.%s : %s" % (self.getType(),setter,val))

	def logCreate(self):
		logger.info("Succesfully created : %s %s on : %s" % (self.getType(),self.getName(),self.getParent().getName()))
		logger.debug("Succesfully created %s : %s" % (self.getType(),self.getConfigID()))

class DynAttribute:
	def __init__(self, name, description, required, value, type):
		self.name=name
		self.description=description
		self.required=required
		self.value=value
		self.type=type

	def getName(self):
		return self.name
	def getDescription(self):
		return self.description
	def getRequired(self):
		return self.required
	def getValue(self):
		return self.value
	def setValue(self, value):
		self.value=value
	def getType(self):
		return self.type

	def getList(self):
		ret=[]
		ret.append(["name", self.getName()])
		ret.append(["type", self.getType()])
		ret.append(["description", self.getDescription()])
		ret.append(["required", self.getRequired()])
		ret.append(["value", self.getValue()])
		return ret


class ManagementScope(WASConfig):
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=['Security']
		self.man_attributes={
			'scopeName' : "",
			'scopeType':""
		}

	def getKeyAttribute(self):
		return "scopeName"

	def setScopeName(self, scopeName):
		if scopeName is not None:
			self.man_attributes['scopeName']=scopeName
		self.logValue()
	def getScopeName(self):
		return self.man_attributes['scopeName']

	def setScopeType(self, scopeType):
		if scopeType is not None:
			self.man_attributes['scopeType']=scopeType
		self.logValue()
	def getScopeType(self):
		return self.man_attributes['scopeType']

	def setConfigID(self):
		for m in Util.wslist(AdminConfig.list('ManagementScope')):
			scopeName=AdminConfig.showAttribute(m, 'scopeName')
			scopeType=AdminConfig.showAttribute(m, 'scopeType')
			if scopeName==self.getScopeName() and scopeType==self.getScopeType():
				self.configID=m
		if self.configID=="":
			try:
				logger.debug("ManagementScope : %s not found, creating..." % self.getScopeName())
				self.configID=AdminConfig.create(self.getConfigType(),self.getParent().getConfigID(),Util.dictToList(self.man_attributes))
			except:
				logger.debug("Could not create ManagementScope : %s ..." % self.getScopeName())
		self.logValue()

	def validate(self):
		self.setConfigID()
		self.valid="true"

	def start(self):
		pass
	def stop(self):
		pass
	def create(self):
		pass

class ManagementScopedWASConfig:
	def __init__(self):
		self.managementScope=None

	def setManagementScope(self):
		self.managementScope=ManagementScope()
		self.managementScope.setScopeName("%s:(%s):%s" % (self.getParent().getManagementScope().getScopeName(),self.getConfigType().lower(),self.getName()))
		self.managementScope.setScopeType(self.getConfigType().lower())
		self.managementScope.setParent(self.getSecurity())
		self.managementScope.validate()
		self.logValue()
	def getManagementScope(self):
		return self.managementScope
	def remove(self):
		self.getManagementScope().remove()
