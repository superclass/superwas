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

# JAAS aliases
#
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: url.py 424 2013-01-04 15:04:36Z andre $
class URLProvider(WASConfig):
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name':"",
			'streamHandlerClassName':"",
			'protocol':""
		}
		self.opt_attributes={
            'description':"",
            'classpath':""
		}

	def setProtocol(self, protocol):
		if protocol is not None: self.man_attributes['protocol']=protocol
		self.logValue()
	def getProtocol(self):
		return self.man_attributes['protocol']

	def setStreamHandlerClassName(self, streamHandlerClassName):
		if streamHandlerClassName is not None: self.man_attributes['streamHandlerClassName']=streamHandlerClassName
		self.logValue()
	def getStreamHandlerClassName(self):
		return self.man_attributes['streamHandlerClassName']

	def setDescription(self, description):
		if description is not None: self.opt_attributes['description']=description
		self.logValue()
	def getDescription(self):
		return self.opt_attributes['description']

	def setClasspath(self, classpath):
		if classpath is not None: self.opt_attributes['classpath']=classpath
		self.logValue()
	def getClasspath(self):
		return self.opt_attributes['classpath']

	def validate(self):
		# No checks for default Providers, get config ID
		if self.getName() in ["Default URL Provider"]:
			self.wasDefault="true"
		WASConfig.validate(self)

class URL(WASConfig):
	"""# 
#
# Currently only outgoing URL are supported.
#
# Author: Andre van Dijk <andre.van.dijk@superclass.nl>
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
#
# $Id: url.py 424 2013-01-04 15:04:36Z andre $"""
	level=4
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["URLProvider"]
		self.man_attributes={
			'name' : "",
			'jndiName' : "",
			'spec' : ""
		}
		self.opt_attributes={
			'description' : "",
			'category' : ""
		}

	def setSpec(self, spec):
		"""# Specifies the JNDI name for the URL."""
		if spec is not None: self.man_attributes['spec']=spec
		self.logValue()
	def getSpec(self):
		return self.man_attributes['spec']

	def setJndiName(self, jndiName):
		"""# Specifies the JNDI name for the URL."""
		if jndiName is not None: self.man_attributes['jndiName']=jndiName
		self.logValue()
	def getJndiName(self):
		return self.man_attributes['jndiName']

	def setDescription(self, description):
		"""# Specifies a description for the URL."""
		if description is not None: self.opt_attributes['description']=description
		self.logValue()
	def getDescription(self):
		return self.opt_attributes['description']

	def setCategory(self, category):
		"""# Specifies a collection for classifying or grouping URLs."""
		if category is not None: self.opt_attributes['category']=category
		self.logValue()
	def getCategory(self):
		return self.opt_attributes['category']

	def create(self):
		WASConfig.create(self)
		AdminConfig.create(self.getConfigType(), self.getParent().getConfigID(), Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes))
		self.logCreate()
