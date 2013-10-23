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

# Shared Library Classes
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: sharedlibrary.py 424 2013-01-04 15:04:36Z andre $
class SharedLibrary(WASConfig):
	"""
	Class to represent a Shared Library.
	"""
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.opt_attributes={
			'classpath':"",
			'nativePath':""
		}

	def getConfigType():
		"Library"	

	def setClasspath(self, classpath):
		if classpath is not None:
			self.opt_attributes['classpath']=classpath
		self.logCreate()
	def getClasspath(self):
		return self.opt_attributes['classpath']

	def setNativePath(self, nativePath):
		if nativePath is not None:
			self.opt_attributes['nativePath']=nativePath
		self.logCreate()
	def getNativePath(self):
		return self.opt_attributes['nativePath']
		
	def create(self):
		WASConfig.create(self)
		AdminConfig.create(self.getConfigType(),self.getParent().getConfigID(), Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes))
		self.logCreate()
