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

# Replication Domain Classes
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: replication.py 424 2013-01-04 15:04:36Z andre $
class DataReplicationDomain(WASConfig):
	"""# 
# DataReplication Domain
#
"""
	level=1
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["Cell"]
		self.man_attributes={
			'name' : "",
			'encryptionType':"" #ENUM(DES, TRIPLE_DES, NONE)
		}
		self.opt_attributes={
			'numberOfReplicas':0,
			'requestTimeout':5
		}

	def setEncryptionType(self, encryptionType):
		"""# EncryptionTypeifies the JNDI name for the URL."""
		if encryptionType is not None and encryptionType in ['DES', 'TRIPLE_DES', 'NONE']:
			self.man_attributes['encryptionType']=encryptionType
		self.logValue()
	def getEncryptionType(self):
		return self.man_attributes['encryptionType']

	def setNumberOfReplicas(self, numberOfReplicas):
		"""# Specifies a numberOfReplicas for the URL."""
		if numberOfReplicas is not None: self.opt_attributes['numberOfReplicas']=numberOfReplicas
		self.logValue()
	def getNumberOfReplicas(self):
		return self.opt_attributes['numberOfReplicas']

	def setRequestTimeout(self, requestTimeout):
		"""# Specifies a collection for classifying or grouping URLs."""
		if requestTimeout is not None: self.opt_attributes['requestTimeout']=requestTimeout
		self.logValue()
	def getRequestTimeout(self):
		return self.opt_attributes['requestTimeout']

	def create(self):
		WASConfig.create(self)
		rDomain=AdminConfig.create(self.getConfigType(), self.getParent().getConfigID(), [["name", self.getName()]]) 
		AdminConfig.create("DataReplication", rDomain, [['encryptionType', self.getEncryptionType()]] + Util.dictToList(self.opt_attributes))
		self.logCreate()
