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

# Superwas application entry point
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-07-15 15:54:10 +0200 (ma, 15 jul 2013) $
# $Id: superwas.py 460 2013-07-15 13:54:10Z andre $

""" 
General overview of application workings:
----------------------------------------

Entry point for the application:
- Reads properties configuration file.
- Initialise log4j logger object
- Setup Config object and validate property file and setup config objects based on property contents
- Call action method on config object with specified command line parameters
install
	Call create method on config objects
	Save config
uninstall
	Validate property file and setup config objects based on property contents
	Call remove and uninstall method on config objects
	Save config
stop
	Call stop method on config objects
start
	Call start method on config objects
documentation
	Show documentation for configuraton properties of config objects
nagiosStatus
	Output PMI statistics for Nagios to fifo

Error Handling and Logging
--------------------------

For logging a Log4j logger object is created, this is used throughout
the application to log messages at different levels. Log4j is
configured in the log4j.properties file. Default log4j configuration is
to log to stdout on level INFO and to $SUPERWAS_TMP on level debug.

All errors are reported through Exceptions. The exception contains a
message indicating the problem which is logged at level ERROR at the
end of this module. A stack trace is logged at LEVEL DEBUG.

Running SUPERWAS
-------------
Point your classpath to the log4j library, eg.:
export CLASSPATH=/opt/scripts/was/superwas/lib/log4j-1.2.8.jar

Setup environment variables:
SUPERWAS_HOME - This location is used to search the SUPERWAS scripts. If it's
not specified the . (current directory) is assumed, and superwas has to be
started from that directory
SUPERWAS_TMP - Directory where the superwas.log will be written. If it's not
specified /tmp is assumed.

Invoke wsadmin like this:
wsadmin.sh -wsadmin_classpath $CLASSPATH -javaoption \
-DSUPERWAS_TMP=$SUPERWAS_TMP -javaoption -DSUPERWAS_HOME=$SUPERWAS_HOME <ARGUMENTS> \

<ARGUMENTS> are explained by usage method and displayed if superwas is run without arguments.
"""

import org.apache.log4j
import java.lang
import java.util.Properties as jProperties
import java.io.FileInputStream as FileInputStream
import os
import getopt


# Global Log4j logger object used througout the application
logger=None

# For debugging
def retry():
	AdminConfig.reset()
	execfile('superwas.py')

# Get SUPERWAS TMP directory from system props
if java.lang.System.getProperty('SUPERWAS_TMP') is not None:
	superwastmp=java.lang.System.getProperty('SUPERWAS_TMP')
else:
	superwastmp='/tmp'
	java.lang.System.setProperty('SUPERWAS_TMP', superwastmp)
# Get WASSAD scripting directory from system props
if java.lang.System.getProperty('SUPERWAS_HOME') is not None:
	scriptdir=java.lang.System.getProperty('SUPERWAS_HOME')
	sys.path.append(scriptdir)
else:
	scriptdir='.'

# Source submodule
execfile('%s/config.py' % scriptdir)

# Global config object
config=Config()

def usage ():
	"""
	This function prints the commandline options that are supported
	"""
	print
	print "Syntax: -i <PROPERTIESPATH>"
	print "        -[install,uninstall,stop,start,documentation] <CONFIGTYPE>..."
	print "        [-n <NAME>]..."
	print " --install                         Install the specified CONFIGTYPE, use @ for all." 
	print " --uninstall,                      Uninstall the specified CONFIGTYPE." 
	print " --stop,                           Stop the specified CONFIGTYPE." 
	print " --start,                          Start the specified CONFIGTYPE." 
	print " --documentation                   Documentation for the specified CONFIGTYPE." 
	print " --nagiosStats                     Output PMI stats for Nagios to fifo (specified by -o)."
	print " -n, --name=NAME                  Only apply action to named object."
	print " -i, --properties=PROPERTIESPATH  Path to superwas properties file." 
	print " -o, --fifo=FIFOPATH              Path to fifo for nagios stats output, default: /tmp/superwasnagios."
	print " -u, --usage                      Print this help text." 
	print " -d, --dry-run                    Dry run, don't save the configuration."
	print
	print "Multiple actions may be specified by supplying multiple install, uninstall,"
	print "stop, start and documentation arguments. These actions require an argument"
	print "that specify the config type defined in the configuration file to which"
	print "the action applies. To apply to all types specify @."
	print "Optionally a name may be specified to restrict the action by supplying"
	print "the -n argments. The first specified name applies to the first specified"
	print "action, the second name to the second action etc. If a single action is"
	print "specified and no name then the action applies to all defined elements"
	print "in the config file. If multiple actions are specified and for all but"
	print "the last action they apply to all defined elements the special name @"
	print "has to be specified."
	print
	print "Valid CONFIGTYPES:"
	for a in config.getWasConfigTypes():
		print "     %s" % a
	print "To use all specify @."

def main():
	global logger, config

	# Create log4j logger
	logger=org.apache.log4j.Logger.getLogger("superwas")
	org.apache.log4j.PropertyConfigurator.configure("%s/log4j.properties" % scriptdir)

	propfile=""
	actions=[]
	types=[]
	names=[]
	fifo=""
	dryRun=0
	try:
		opts, args = getopt.getopt(sys.argv[0:], "i:n:uo:d", ["properties=","name=", "usage", "fifo=","dry-run","install=", "uninstall=","start=","stop=","documentation=","nagiosStats"])
	except getopt.GetoptError, err:
		print "Invalid syntax : %s" % str(err)
		usage()
		sys.exit(1)

	for o, a in opts:
		if o in ("-i", "--properties"):
			propfile=a
		elif o in ["--install", "--uninstall","--stop","--start","--documentation", "--nagiosStats"]:
			actions.append(o[2:])
			if a=="@":
				types.append("")
			else:
				types.append(a)
		elif o in ("-n", "--name"):
			if a=="@":
				names.append("")		
			else:
				names.append(a)
		elif o in ("-u", "--usage"):
			usage()
			sys.exit(0)
		elif o in ("-o", "--fifo"):
			fifo=a
		elif o in ("-d", "--dry-run"):
			dryRun=1
		else:
			assert 0, "unhandled option"

	if propfile=="":
		print "Option -i/--properties missing"
		usage()
		sys.exit(1)
	if len(actions)==0:
		print "Action Option missing"
		usage()
		sys.exit(1)

	config.setPropFile(propfile)
	config.setFifo(fifo)
	config.setDryRun(dryRun)
	for i in range(0,len(actions)):
		if len(names)>i:
			name=names[i]
		else:
			name=""
		try:
			if i>0: config.validate()
			config.action(types[i], actions[i], name)
			AdminConfig.reset()
		except:
			logger.error(str(sys.exc_info()[1]) + "\n")
			logger.debug(sys.exc_info()[2].dumpStack() + "\n")
			sys.exit(1)

main()
