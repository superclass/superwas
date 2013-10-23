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

# NameSpaceBinding classes
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: namespacebinding.py 424 2013-01-04 15:04:36Z andre $
class BaseNameSpaceBinding(WASConfig):
	"""
	Class to represent a Name Space binding.
	"""
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name' : "",
			'nameInNameSpace' : ""
		}

	def setNameInNameSpace(self, nameInNameSpace):
		if nameInNameSpace!=None:
			self.man_attributes['nameInNameSpace']=nameInNameSpace
		self.logValue()
	def getNameInNameSpace(self):
		return self.man_attributes['nameInNameSpace']

	def create(self):
		WASConfig.create(self)
		AdminConfig.create(self.getConfigType(),self.getParent().getConfigID(),Util.dictToList(self.man_attributes))
		self.logCreate()

class StringNameSpaceBinding(BaseNameSpaceBinding):
	def __init__(self, parent=None):
		BaseNameSpaceBinding.__init__(self, parent)
		self.man_attributes['stringToBind']=""

	def setStringToBind(self, stringToBind):
		if stringToBind!=None:
			self.man_attributes['stringToBind']=stringToBind
		self.logValue()
	def getStringToBind(self):
		return self.man_attributes['stringToBind']

class EjbNameSpaceBinding(BaseNameSpaceBinding):
	def __init__(self, parent=None):
		BaseNameSpaceBinding.__init__(self, parent)
		self.man_attributes['applicationNodeName']=""
		self.man_attributes['applicationServerName']=""
		self.man_attributes['ejbJndiName']=""
		self.man_attributes['bindingLocation']="SERVERCLUSTER"

	def setApplicationServerName(self, applicationServerName):
		if applicationServerName is not None:
			self.man_attributes['applicationServerName']=applicationServerName
		self.logValue()
	def getApplicationServerName(self):
		return self.man_attributes['applicationServerName']

	def setApplicationNodeName(self, applicationNodeName):
		if applicationNodeName is not None:
			self.man_attributes['applicationNodeName']=applicationNodeName
		self.logValue()
	def getApplicationNodeName(self):
		return self.man_attributes['applicationNodeName']

	def setEjbJndiName(self, ejbJndiName):
		if ejbJndiName is not None:
			self.man_attributes['ejbJndiName']=ejbJndiName
		self.logValue()
	def getEjbJndiName(self):
		return self.man_attributes['ejbJndiName']

	def setBindingLocation(self, bindingLocation):
		if bindingLocation is not None:
			self.man_attributes['bindingLocation']=bindingLocation
		self.logValue()
	def getBindingLocation(self):
		return self.man_attributes['bindingLocation']

class CORBAObjectNameSpaceBinding(BaseNameSpaceBinding):
	def __init__(self, parent=None):
		BaseNameSpaceBinding.__init__(self, parent)
		self.man_attributes['jndiName']=""
		self.man_attributes['providerURL']=""

	def setProviderURL(self, providerURL):
		if providerURL is not None:
			self.man_attributes['providerURL']=providerURL
		self.logValue()
	def getProviderURL(self):
		return self.man_attributes['providerURL']

	def setJndiName(self, jndiName):
		if jndiName is not None:
			self.man_attributes['jndiName']=jndiName
		self.logValue()
	def getJndiName(self):
		return self.man_attributes['jndiName']

class IndirectLookupNameSpaceBinding(BaseNameSpaceBinding):
	def __init__(self, parent=None):
		BaseNameSpaceBinding.__init__(self, parent)
		self.man_attributes['corbanameUrl']=""

	def setCorbanameUrl(self, corbanameUrl):
		if corbanameUrl is not None:
			self.man_attributes['corbanameUrl']=corbanameUrl
		self.logValue()
	def getCorbanameUrl(self):
		return self.man_attributes['corbanameUrl']
