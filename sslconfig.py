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

# SSL Config classes
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-07-23 09:33:12 +0200 (di, 23 jul 2013) $
# $Id: sslconfig.py 463 2013-07-23 07:33:12Z andre $
class SSLConfig(WASConfig):
	level=4
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name' : ""
		}
		self.opt_attributes={
			'clientKeyAlias':"",
			'serverKeyAlias':"",
			'clientAuthentication':"",
			'sslProtocol':"",
			'jsseProvider':"IBMJSSE2",
			'clientAuthenticationSupported':"",
			'securityLevel':"",
			'enabledCiphers':""
		}
		self.ref_attributes={
			'trustStore':None,
			'keyStore':None
		}

	def setConfigID(self):
		for i in Util.wslist(AdminConfig.list(self.getConfigType() , self.getSecurity().getConfigID())):
			if i=='': continue
			alias=AdminConfig.showAttribute(i, "alias")
			if alias==self.getName(): self.configID=i
		self.logValue()

	def getContainmentPath(self):
		return "%s%s:%s/" % (self.getSecurity().getContainmentPath(),self.getConfigType(),self.getName()) 

	def setClientKeyAlias(self, clientKeyAlias):
		if clientKeyAlias is not None:
			self.opt_attributes['clientKeyAlias']=clientKeyAlias
		self.logValue()
	def getClientKeyAlias(self):
		return self.opt_attributes['clientKeyAlias']

	def setServerKeyAlias(self, serverKeyAlias):
		if serverKeyAlias is not None:
			self.opt_attributes['serverKeyAlias']=serverKeyAlias
		self.logValue()
	def getServerKeyAlias(self):
		return self.opt_attributes['serverKeyAlias']

	def setClientAuthentication(self, clientAuthentication):
		if clientAuthentication is not None:
			self.opt_attributes['clientAuthentication']=clientAuthentication
		self.logValue()
	def getClientAuthentication(self):
		return self.opt_attributes['clientAuthentication']

	def setSslProtocol(self, sslProtocol):
		if sslProtocol is not None:
			if sslProtocol in ["SSL_TLS", "SSL", "SSLv2", "SSLv3", "TLS", "TLSv1"]:
				self.opt_attributes['sslProtocol']=sslProtocol
			else:
				raise Exception('sslProtocol should be "SSL_TLS", "SSL", "SSLv2", "SSLv3", "TLS" or "TLSv1"')
		self.logValue()
	def getSslProtocol(self):
		return self.opt_attributes['sslProtocol']

	def setJsseProvider(self, jsseProvider):
		if jsseProvider is not None:
			self.opt_attributes['jsseProvider']=jsseProvider
		self.logValue()
	def getJsseProvider(self):
		return self.opt_attributes['jsseProvider']

	def setClientAuthenticationSupported(self, clientAuthenticationSupported):
		if clientAuthenticationSupported is not None:
			self.opt_attributes['clientAuthenticationSupported']=clientAuthenticationSupported
		self.logValue()
	def getClientAuthenticationSupported(self):
		return self.opt_attributes['clientAuthenticationSupported']

	def setSecurityLevel(self, securityLevel):
		if securityLevel is not None:
			if securityLevel in ["STRONG", "MEDIUM", "WEAK", "CUSTOM"]:
				self.opt_attributes['securityLevel']=securityLevel
			else:
				raise Exception('security level should be "STRONG", "MEDIUM", "WEAK" or "CUSTOM"')
		self.logValue()
	def getSecurityLevel(self):
		return self.opt_attributes['securityLevel']

	def setEnabledCiphers(self, enabledCiphers):
		if enabledCiphers is not None:
			self.opt_attributes['enabledCiphers']=enabledCiphers
			self.opt_attributes['securityLevel']='CUSTOM'
		self.logValue()
	def getEnabledCiphers(self):
		return self.opt_attributes['enabledCiphers']

	def setTrustStore(self, trustStore):
		if trustStore is not None:
			self.ref_attributes['trustStore']=trustStore
		self.logValue()
	def getTrustStore(self):
		return self.ref_attributes['trustStore']
	def getTrustStoreType(self):
		return "KeyStore"

	def setKeyStore(self, keyStore):
		if keyStore is not None:
			self.ref_attributes['keyStore']=keyStore
		self.logValue()
	def getKeyStore(self):
		return self.ref_attributes['keyStore']
	def getKeyStoreType(self):
		return "KeyStore"

	def create(self):
		attrs='[-alias %s' % self.getName()
		for i in self.opt_attributes.keys():
			if self.opt_attributes[i]!="":
				attrs+=" -%s %s" % (i,self.opt_attributes[i])
		if self.getTrustStore()!=None:
			attrs+=" -trustStoreName %s -trustStoreScopeName %s" % (self.getTrustStore().getName(),self.getTrustStore().getParent().getManagementScope().getScopeName())
		if self.getKeyStore()!=None:
			attrs+=" -keyStoreName %s -keyStoreScopeName %s" % (self.getKeyStore().getName(),self.getKeyStore().getParent().getManagementScope().getScopeName())
		attrs+=" -scopeName %s]" % self.getParent().getManagementScope().getScopeName()
		logger.debug(attrs)
		self.configID=AdminTask.createSSLConfig (attrs)
		self.logCreate()

class KeyStore(WASConfig):
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name' : "",
			'keyStoreType' : "",
			'location' : "",
			'password' : "",

		}
		self.opt_attributes={
			'isFileBased' : "true",
			'readOnly' : "false"
		}

	def getContainmentPath(self):
		return "%s%s:%s/" % (self.getSecurity().getContainmentPath(),self.getConfigType(),self.getName()) 

	def setKeyStoreType(self, type):
		if type is not None:
			self.man_attributes['keyStoreType']=type
		self.logValue()
	def getKeyStoreType(self):
		return self.man_attributes['keyStoreType']

	def setLocation(self, location):
		if location is not None:
			self.man_attributes['location']=location
		self.logValue()
	def getLocation(self):
		return self.man_attributes['location']	

	def setPassword(self, password):
		if password is not None:
			self.man_attributes['password']=password
		self.logValue()
	def getPassword(self):
		return self.man_attributes['password']	

	def setIsFileBased(self, isFileBased):
		if isFileBased is not None:
			self.opt_attributes['isFileBased']=isFileBased
		self.logValue()
	def getIsFileBased(self):
		return self.opt_attributes['isFileBased']	

	def setReadOnly(self, readOnly):
		if readOnly is not None:
			self.opt_attributes['readOnly']=readOnly
		self.logValue()
	def getReadOnly(self):
		return self.opt_attributes['readOnly']	

	def create(self):
		self.configID=AdminTask.createKeyStore('[-scopeName %s -keyStoreName %s -keyStoreType %s -keyStoreLocation %s -keyStorePassword %s -keyStorePasswordVerify %s -keyStoreIsFileBased %s -keyStoreReadOnly %s]' % (self.getParent().getManagementScope().getScopeName(),self.getName(),self.getKeyStoreType(),self.getLocation(),self.getPassword(),self.getPassword(),self.getIsFileBased(),self.getReadOnly()))
		self.logCreate()
