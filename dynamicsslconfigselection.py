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

# Dynamic outbound SSL connections
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-08-07 15:03:37 +0200 (wo, 07 aug 2013) $
# $Id: dynamicsslconfigselection.py 464 2013-08-07 13:03:37Z andre $
class DynamicSSLConfigSelection(WASConfig):
	"""# 
# Dynamic outbound SSL connections
#
"""
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name' : "",
			'description':"",
			'sslConfig':"",
			'dynamicSelectionInfo':""
		}
		self.opt_attributes={
			'certificateAlias':"" 
		}

	def getContainmentPath(self):
		return "/%s:%s/" % (self.getConfigType(),self.getName())

	def setDescription(self, description):
		"""# Descriptionifies the JNDI name for the URL."""
		if description is not None: 
			self.man_attributes['description']=description
		self.logValue()
	def getDescription(self):
		return self.man_attributes['description']

	def setDynamicSelectionInfo(self, dynamicSelectionInfo):
		"""# Specifies a dynamicSelectionInfo for the URL."""
		if dynamicSelectionInfo is not None: self.man_attributes['dynamicSelectionInfo']=dynamicSelectionInfo
		self.logValue()
	def getDynamicSelectionInfo(self):
		return self.man_attributes['dynamicSelectionInfo']

	def setCertificateAlias(self, certificateAlias):
		"""# Specifies a collection for classifying or grouping URLs."""
		if certificateAlias is not None: self.opt_attributes['certificateAlias']=certificateAlias
		self.logValue()
	def getCertificateAlias(self):
		return self.opt_attributes['certificateAlias']

	def setSslConfig(self, sslConfig):
		"""# SslConfigifies the JNDI name for the URL."""
		if sslConfig is not None: 
			self.man_attributes['sslConfig']=sslConfig
		self.logValue()
	def getSslConfig(self):
		return self.man_attributes['sslConfig']

	def create(self):
		WASConfig.create(self)
		secID=self.getSecurity().getConfigID()
		sslConfig=""
		for i in Util.wslist(AdminConfig.list('SSLConfig')):
			alias=AdminConfig.showAttribute(i, 'alias')
			if self.getSslConfig()==alias:
				sslConfig=i	
				break
		if sslConfig=="":
			raise Exception('SSL Config not found : %s' % self.getSslConfig())
		self.man_attributes['sslConfig']=sslConfig
		attrs=Util.dictToList(self.man_attributes)
		if self.getCertificateAlias()!="":
			attrs+=Util.dictToList(self.opt_attributes)
		AdminConfig.create(self.getConfigType(), secID, [['managementScope', self.getParent().getManagementScope().getConfigID()]]+attrs)
		self.logCreate()
