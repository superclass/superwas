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

# Server Classes
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: mail.py 424 2013-01-04 15:04:36Z andre $
class MailProvider(WASConfig):
	level=3
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.man_attributes={
			'name':"Built-in Mail Provider"
		}
		self.opt_attributes={
            'description':"The built-in mail provider"
		}

	def setDescription(self, description):
		if description is not None: self.opt_attributes['description']=description
		self.logValue()
	def getDescription(self):
		return self.opt_attributes['description']

	def validate(self):
		# No checks for default Providers, get config ID
		if self.getName() in ["Built-in Mail Provider"]:
			self.wasDefault="true"
		WASConfig.validate(self)

class MailSession(WASConfig):
	"""# Use this class to create mail sessions, which are collections of
# properties that define how your application sends mail and accesses the
# mail store. To create a useful mail session, an outgoing or incoming
# server and protocol must be provided. A MailSession needs a Mail Provider,
# as a Parent, normally this wil be the  Default Mail Provider. 
#
"""
	level=4
	def __init__(self, parent=None):
		WASConfig.__init__(self, parent)
		self.validParents=["MailProvider"]
		self.man_attributes={
			'name' : "",
			'jndiName' : ""
		}
		self.opt_attributes={
			'description' : "",
			'category' : "",
			'mailTransportHost' : "",
			'strict' : "true",
			'mailTransportProtocol' : "smtp"
		}

	def setJndiName(self, jndiName):
		"""# Specifies the JNDI name for the MailSession."""
		if jndiName is not None: self.man_attributes['jndiName']=jndiName
		self.logValue()
	def getJndiName(self):
		return self.man_attributes['jndiName']

	def setDescription(self, description):
		"""# Specifies a description for the MailSession."""
		if description is not None: self.opt_attributes['description']=description
		self.logValue()
	def getDescription(self):
		return self.opt_attributes['description']

	def setCategory(self, category):
		"""# Specifies a collection for classifying or grouping sessions."""
		if category is not None: self.opt_attributes['category']=category
		self.logValue()
	def getCategory(self):
		return self.opt_attributes['category']

	def setMailTransportHost(self, mailTransportHost):
		"""# Specifies the outgoing transport host for the MailSession."""
		if mailTransportHost is not None: self.opt_attributes['mailTransportHost']=mailTransportHost
		self.logValue()
	def getMailTransportHost(self):
		return self.opt_attributes['mailTransportHost']

	def setStrict(self, strict):
		"""# Specifies whether the recipient addresses must be parsed in strict
#compliance with RFC 822"""
		if strict is not None: self.opt_attributes['strict']=strict
		self.logValue()
	def getStrict(self):
		return self.opt_attributes['strict']

	def setMailTransportProtocol(self, mailTransportProtocol):
		"""# Specifies the outgoing transport protocol, valid values are: smtp, smtps."""
		if mailTransportProtocol in ["smtp","smtps","pop3","pop3s","imap","imaps"]: self.opt_attributes['mailTransportProtocol']=mailTransportProtocol
		self.logValue()
	def getMailTransportProtocol(self):
		return self.opt_attributes['mailTransportProtocol']

	def create(self):
		WASConfig.create(self)
		pprovs=Util.wslist(AdminConfig.list("ProtocolProvider", self.getParent().getConfigID()))
		found=0
		for pprov in pprovs:
			if AdminConfig.showAttribute(pprov, 'protocol') == self.getMailTransportProtocol():
				self.opt_attributes['mailTransportProtocol']=pprov
				found=1
				break
		if found==0: raise Exception("MailTransportProtocol not found : %s" % self.getMailTransportProtocol())
		self.configID=AdminConfig.create(self.getConfigType(),self.getParent().getConfigID(), Util.dictToList(self.man_attributes)+Util.dictToList(self.opt_attributes))
		self.logCreate()
