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

# Node class
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: node.py 424 2013-01-04 15:04:36Z andre $
class Node(WASConfig, ManagementScopedWASConfig):
	"""
	Class to represent a Node.

	Author: Andre van Dijk (SuperClass IT)
	Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $

	$Id: node.py 424 2013-01-04 15:04:36Z andre $
	"""
	level=1
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		ManagementScopedWASConfig.__init__(self)
		self.validParents=["Cell"]

	def setName(self, name):
		WASConfig.setName(self, name)

	def validate(self):
		WASConfig.validate(self)
		if self.configID == "": raise Exception("Node %s is not defined" % self.getName())
		logger.debug("Found node : %s" % self.getName())
		self.setManagementScope()

	def create(self):
		pass
	def remove(self):
		pass
