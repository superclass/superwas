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
# $Id: jaas.py 424 2013-01-04 15:04:36Z andre $
class JAASAuthData(WASConfig):
	"""
	Class to represent WAS JAAS authentication data.
	"""
	level=1
	def __init__(self, parent=None):
		"""
		Create a new JAASAuthData object.
		"""
		WASConfig.__init__(self, parent)
		self.validParents=["Cell"]
		self.man_attributes={
			'alias':"",
			'userId':""
		}
		self.opt_attributes={
			'password':"",
			'description':""
		}

	def getKeyAttribute(self):
		return "alias"

	def setConfigID(self):
		for i in Util.wslist(AdminConfig.list(self.getConfigType(), self.getSecurity().getConfigID())):
			if i=='': continue
			alias=AdminConfig.showAttribute(i, "alias")
			if alias==self.getName(): self.configID=i
		self.logValue()

	def setAlias(self, alias):
		self.setName(alias)
	def getAlias(self):
		return self.getName()

	def setUserId(self, userId):
		if userId is not None: self.man_attributes['userId']=userId
		self.logValue()
	def getUserId(self):
		return self.man_attributes['userId']

	def setPassword(self, password):
		if password is not None: self.opt_attributes['password']=password
	def getPassword(self):
		return self.opt_attributes['password']

	def setDescription(self, description):
		if description is not None: self.opt_attributes['description']=description
	def getDescription(self):
		return self.opt_attributes['description']

	def create(self):
		WASConfig.create(self)
		self.configID=AdminConfig.create( "JAASAuthData", self.getSecurity().getConfigID(), Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes))
		self.logCreate()
