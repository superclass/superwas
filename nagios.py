#!/usr/bin/python

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

# Classes to create Nagios statistics from WAS PMI data
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-18 16:38:05 +0100 (vr, 18 jan 2013) $
# $Id: nagios.py 428 2013-01-18 15:38:05Z andre $
class NagiosStatus:
	def __init__(self, code, message, perfdata):
		self.code=code
		self.message=message
		self.perfdata=perfdata

	def getCode(self):
		return self.code

	def getMessage(self):
		return self.message

	def getPerformanceData(self):
		return self.perfdata

class NagiosStat:
	# Nagio Return values
	OK=0 # indicates a service is working properly.
	WARNING=1 # indicates a service is in warning state.
	CRITICAL=2 # indicates a service is in critical state.
	UNKNOWN=3 # indicates a service is in unknown state.
	STATUS=["OK","WARNING","CRITICAL","UNKOWN"]
	def __init__(self):
		self.criticalThreshold=0
		self.warningThreshold=0
		self.statusinput=[]

	def setStatus(self, stats):
		pass

	def setCriticalThreshold(self, critical):
		self.criticalThreshold=int(critical)

	def setWarningThreshold(self, warning):
		self.warningThreshold=int(warning)

class HeapStat(NagiosStat):
	def __init__(self):
		NagiosStat.__init__(self)
		self.current=-1
		self.count=-1
	
	def setCurrentHeapSize(self, current):
		self.current=int(current)

	def setUsedMemory(self, count):
		self.count=int(count)

	def setStatus(self, stats):
		for stat in stats:
			pu=stat.getStatistic('HeapSize')
			if pu is not None: 
				self.setCurrentHeapSize(pu.getCurrent())
			pu=stat.getStatistic('UsedMemory')
			if pu is not None: 
				self.setUsedMemory(pu.getCount())

	def getStatus(self):
		percentage=-1
		status=self.UNKNOWN
		message="HeapStatus unknown"
		if self.criticalThreshold<0 or self.warningThreshold<0:
			logger.debug("Heap stats off, returning OK")
			return NagiosStatus(self.OK, "Heap thresholds unset", "")
		if self.count!=-1 and self.current!=-1:
			if self.count!=0:
				percentage=(float(self.count)/self.current)*100
			else:
				percentage=0
			if percentage>=self.criticalThreshold:
				status=NagiosStat.CRITICAL
				message="CRITICAL heapSize %d/%d" % (percentage,self.criticalThreshold)
			elif percentage>=self.warningThreshold:
				status=NagiosStat.WARNING
				message="WARNING heapSize %d/%d" % (percentage,self.warningThreshold)
			else: 
				status=NagiosStat.OK
				message="OK heapSize %d/%d" % (percentage,self.warningThreshold)
		logger.debug("Heap stats: %s %s" % (status,message))
		return NagiosStatus(status, message,"Heap=%d%%;%d;%d;;;" % (percentage,self.warningThreshold,self.criticalThreshold))

class CPUStat(NagiosStat):
	def __init__(self):
		NagiosStat.__init__(self)
		self.percentage=-1

	def setCPUPercentage(self, percentage):
		self.percentage=int(percentage)

	def getStatus(self):
		status=NagiosStat.UNKNOWN
		message="CPU Usage unknown"
		if self.criticalThreshold<0 or self.warningThreshold<0:
			logger.debug("CPU stats off, returning OK")
			return NagiosStatus(self.OK, "CPU thresholds unset", "")
		if self.percentage!=-1:
			if self.percentage >=self.criticalThreshold:
				status=NagiosStat.CRITICAL
				message="CRITICAL CPU Usage %d/%d" % (self.percentage,self.criticalThreshold)
			elif self.percentage >=self.warningThreshold:
				status=NagiosStat.WARNING
				message="WARNING CPU Usage %d/%d" % (self.percentage,self.warningThreshold)
			else:
				status=NagiosStat.OK	
				message="OK CPU Usage %d/%d" % (self.percentage,self.warningThreshold)
		return NagiosStatus(status, message, "CPU=%d%%;%d;%d;;;" % (self.percentage,self.warningThreshold,self.criticalThreshold))

	def setStatus(self, stats):
		for stat in stats:
			pu=stat.getStatistic('ProcessCpuUsage')
			if pu is not None: 
				self.setCPUPercentage(pu.getCount())

class DataSourceUsageStat(NagiosStat):
	def __init__(self):
		NagiosStat.__init__(self)
		self.percentUsed=-1

	def setPercentUsed(self, percentUsed):
		self.percentUsed=float(percentUsed)

	def setStatus(self, stats):
		for stat in stats:
			pu=stat.getStatistic('PercentUsed')
			if pu is not None: 
				self.setPercentUsed(pu.getMean())

	def getStatus(self):
		status=NagiosStat.UNKNOWN
		message="DataSource connection pool usage unknown"
		if self.criticalThreshold<0 or self.warningThreshold<0:
			logger.debug("DataSource usage stats off, returning OK")
			return NagiosStatus(self.OK, "DataSource usage thresholds unset", "")
		if self.percentUsed!=-1:
			if self.percentUsed >=self.criticalThreshold:
				status=NagiosStat.CRITICAL
				message="CRITICAL DataSource pool usage %d/%d" % (self.percentUsed,self.criticalThreshold)
			elif self.percentUsed >=self.warningThreshold:
				status=NagiosStat.WARNING
				message="WARNING DataSource pool usage %d/%d" % (self.percentUsed,self.warningThreshold)
			else:
				status=NagiosStat.OK	
				message="OK DataSource usage %d/%d" % (self.percentUsed,self.warningThreshold)
		return NagiosStatus(status, message, "DataSourceUsage=%d%%;%d;%d;;;" % (self.percentUsed,self.warningThreshold,self.criticalThreshold))

class DataSourceWaitStat(NagiosStat):
	def __init__(self):
		NagiosStat.__init__(self)
		self.waitTime=-1

	def setWaitTime(self, waitTime):
		self.waitTime=float(waitTime)

	def setStatus(self, stats):
		for stat in stats:
			pu=stat.getStatistic('WaitTime')
			if pu is not None: 
				self.setWaitTime(pu.getMean())

	def getStatus(self):
		status=NagiosStat.UNKNOWN
		message="DataSource connection pool wait time unknown"
		if self.criticalThreshold<0 or self.warningThreshold<0:
			logger.debug("DataSource wait stats off, returning OK")
			return NagiosStatus(self.OK, "DataSource wait time thresholds unset", "")
		if self.waitTime!=-1:
			if self.waitTime >=self.criticalThreshold:
				status=NagiosStat.CRITICAL
				message="CRITICAL DataSource wait time %d/%d" % (self.waitTime,self.criticalThreshold)
			elif self.waitTime >=self.warningThreshold:
				status=NagiosStat.WARNING
				message="WARNING DataSource wait time %d/%d" % (self.waitTime,self.warningThreshold)
			else:
				status=NagiosStat.OK	
				message="OK DataSource wait time %d/%d" % (self.waitTime,self.warningThreshold)
		return NagiosStatus(status, message, "DataSourceWait=%dms;%d;%d;;;" % (self.waitTime,self.warningThreshold,self.criticalThreshold))

class WebContainerConcurrentHungThreadCount(NagiosStat):
	def __init__(self):
		NagiosStat.__init__(self)
		self.hungThreads=-1
		self.maxPoolSize=-1

	def setHungThreads(self, hungThreads):
		self.hungThreads=int(hungThreads)

	def setMaxPoolSize(self, maxpoolsize):
		self.maxPoolSize=int(maxpoolsize)

	def setStatus(self, stats):
		for stat in stats:
			pu=stat.getStatistic('ConcurrentHungThreadCount')
			if pu is not None: 
				self.setHungThreads(pu.getCurrent())
			pu=stat.getStatistic('PoolSize')
			if pu is not None: 
				self.setMaxPoolSize(pu.getUpperBound())

	def getStatus(self):
		status=NagiosStat.UNKNOWN
		message="Webcontainer hung threads unknown"
		if self.criticalThreshold<0 or self.warningThreshold<0:
			logger.debug("Webcontainer hung threads stats off, returning OK")
			return NagiosStatus(self.OK, "WebContainer hung threads thresholds unset", "")
		if self.hungThreads!=-1 and self.maxPoolSize!=-1:
			if self.maxPoolSize!=0:
				percentage=(float(self.hungThreads)/self.maxPoolSize)*100
			else:
				percentage=0
			if percentage >=self.criticalThreshold:
				status=NagiosStat.CRITICAL
				message="CRITICAL Webcontainer hung threads %d/%d" % (percentage,self.criticalThreshold)
			elif percentage >=self.warningThreshold:
				status=NagiosStat.WARNING
				message="WARNING Webcontainer hung threads %d/%d" % (percentage,self.warningThreshold)
			else:
				status=NagiosStat.OK	
				message="OK Webcontainer hung threads %d/%d" % (percentage,self.warningThreshold)
		return NagiosStatus(status, message, "WebContainerConcurrentHungThreadCount=%d%%;%d;%d;;;" % (self.hungThreads,self.warningThreshold,self.criticalThreshold))

class WebContainerActiveStat(NagiosStat):
	def __init__(self):
		NagiosStat.__init__(self)
		self.active=-1
		self.maxPoolSize=-1

	def setActive(self, active):
		self.active=int(active)

	def setMaxPoolSize(self, maxpoolsize):
		self.maxPoolSize=int(maxpoolsize)

	def setStatus(self, stats):
		for stat in stats:
			pu=stat.getStatistic('ActiveCount')
			if pu is not None: 
				self.setActive(pu.getCurrent())
			pu=stat.getStatistic('PoolSize')
			if pu is not None: 
				self.setMaxPoolSize(pu.getUpperBound())

	def getStatus(self):
		status=NagiosStat.UNKNOWN
		message="Webcontainer usage unknown"
		if self.criticalThreshold<0 or self.warningThreshold<0:
			logger.debug("Webcontainer stats off, returning OK")
			return NagiosStatus(self.OK, "WebContainer thresholds unset", "")
		if self.active!=-1 and self.maxPoolSize!=-1:
			if self.maxPoolSize!=0:
				percentage=(float(self.active)/self.maxPoolSize)*100
			else:
				percentage=0
			if percentage >=self.criticalThreshold:
				status=NagiosStat.CRITICAL
				message="CRITICAL Webcontainer usage %d/%d" % (percentage,self.criticalThreshold)
			elif percentage >=self.warningThreshold:
				status=NagiosStat.WARNING
				message="WARNING Webcontainer usage %d/%d" % (percentage,self.warningThreshold)
			else:
				status=NagiosStat.OK	
				message="OK Webcontainer usage %d/%d" % (percentage,self.warningThreshold)
		return NagiosStatus(status, message, "WebContainerActiveStat=%d%%;%d;%d;;;" % (self.active,self.warningThreshold,self.criticalThreshold))

class LiveSessionStat(NagiosStat):
	def __init__(self):
		NagiosStat.__init__(self)
		self.live=-1

	def setLive(self, live):
		self.live=int(live)

	def setStatus(self, stats):
		for stat in stats:
			pu=stat.getStatistic('LiveCount')
			if pu is not None: 
				self.setLive(pu.getCurrent())

	def getStatus(self):
		status=NagiosStat.UNKNOWN
		message="Live sessions unknown"
		if self.criticalThreshold<0 or self.warningThreshold<0:
			logger.debug("Live sessions stats off, returning OK")
			return NagiosStatus(self.OK, "Live sesions thresholds unset", "")
		if self.live!=-1:
			if self.live>=self.criticalThreshold:
				status=NagiosStat.CRITICAL
				message="CRITICAL Live sessions %d/%d" % (self.live,self.criticalThreshold)
			elif self.live >=self.warningThreshold:
				status=NagiosStat.WARNING
				message="WARNING Live sessions %d/%d" % (self.live,self.warningThreshold)
			else:
				status=NagiosStat.OK	
				message="OK Live sessions %d/%d" % (self.live,self.warningThreshold)
		return NagiosStatus(status, message, "LiveSession=%d;%d;%d;;;" % (self.live,self.warningThreshold,self.criticalThreshold))
