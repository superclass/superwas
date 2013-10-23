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

# Virtual Host Classes
#
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: virtualhost.py 424 2013-01-04 15:04:36Z andre $
class HostAlias(WASConfig):
	level=2
	def __init__(self, parent=None):
		"""
		The scope of the Virtual host is a Cell object that
		needs to be provided to the constructor.
		"""
		WASConfig.__init__(self, parent)
		self.man_attributes={'hostname' : "",'port':0}
		self.validParents=["VirtualHost"]

	def setName(self):
		pass
	def getName(self):
		return self.getHostname()

	def setHostname(self, hostname):
		if hostname is not None: self.man_attributes['hostname']=hostname
		self.logValue()
	def getHostname(self):
		return self.man_attributes['hostname']

	def setPort(self, port):
		if port is not None: self.man_attributes['port']=port
		self.logValue()
	def getPort(self):
		return self.man_attributes['port']

	def getKeyAttribute(self):
		return "hostname"

	def setConfigID(self):
		pass

	def getContainmentPath(self):
		return ""

	def create(self):
		WASConfig.create(self)
		self.configID=AdminConfig.create(self.getConfigType(), self.getParent().getConfigID(), Util.dictToList(self.man_attributes))
		self.logCreate()

class VirtualHost(WASConfig):
	"""
	Class to represent a Virtual Host

	Author: Andre van Dijk (SuperClass IT)
	Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $

	$Id: virtualhost.py 424 2013-01-04 15:04:36Z andre $
	"""
	level=1
	def __init__(self, parent=None):
		"""
		The scope of the Virtual host is a Cell object that
		needs to be provided to the constructor.
		"""
		WASConfig.__init__(self, parent)
		self.validParents=["Cell"]

	def remove(self):
		# Remove virtual host
		if self.configID!='':
			logger.info("Removing virtual host : %s" % self.getName())
			AdminConfig.remove(self.configID)

	def create(self):
		WASConfig.create(self)
		self.configID=AdminConfig.create(self.getConfigType(), self.getParent().getConfigID(), Util.dictToList(self.man_attributes))
		self.logCreate()
