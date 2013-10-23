superwas
========

SuperWas Jython scripting library for IBM WebSphere Application Server.

What is it?
-----------
Superwas is a Jython scripting library to be used with IBM WebSphere
Application Server. It allows you to define your servers, applications
and resources in a property file. This enables automatic and
consistent deployments. It allows you to quickly install or uninstall
server, resources and applications and enables consistency between
different environments like test and production environments. Because
it's command line oriented it enables scripted and scheduled
deployments. The property files used as input are plain text files
which are easy to maintain using a versioning tool, also this enables
convenient comparison of environments. Besides installation and
deinstallation of servers, resources and applications it also allows
starting and stopping for objects that support it (e.g. Application
Servers and Applications). Superwas also provides monitoring support
for Nagios (a well known infrastructure monitoring tool) of certain
WebSphere PMI data: it writes monitoring data to a fifo from which
it can be read by a Nagios plugin (which is part of the Superwas
distribution).

How does it work
----------------
Superwas uses the wsadmin command line tool to interface with
WebSphere Application Server. Superwas written with an Object
Oriented approach allowing for easy extending and reuse.

The basic mode of operation is:
superwas reads the configuration file and validates it. Subsequently
it tries to execute the operations specified (eg install, uninstall,
stop or start). Multiple operations can be specified, allowing for
uninstall and install in one run.

Besides the main user provided configuration file superwas uses
property files for defaults and for predefined objects, in the
defaults and predefs directory respectivlely. Defaults specify
default values for WebSphere objects, e.g. the heap size of an
application server, defaults are overridden by user supplied values
in the main configuration file. If neither the main configuration
value nor a default is provided a hardcoded default will be uses,
mandatory properties never have hardcoded defaults. Predefined
objects may be specified, it allows you to create for instance
variables for each application servers you define.

Besides the basic operations install, uninstall, stop and start it
has options to output documentation (lists all the supported
properties) and to output Nagios monitoring to a fifo. In the Nagios
monitoring mode it reads the configuration file and checks the
monitoring thresholds defined with the PMI data from websphere, the
output is written to a fifo in a format suitable for the Nagios
Plugin. It then blocks until the data is read from the fifo by the
Nagios Plugin. Upon which the process is reitterated, essential
this allows Nagios to control the polling interval.

Supported WAS resources
-----------------------
A list of supported WAS resources is output it superwas is invoked
without arguments. Most frequently used resources are supported.
To get the supported properties of all resources invoke superwas
with the documentatation argument.

Supported WAS Versions
----------------------
Superwas should support WAS versions 6.1, 7.0 and 8.0. It has been
developped and tested only on WAS 7.0 Network Deployment.

Invoking SuperWas WebSphere Application Scripting
-------------------------------------------------
Superwas is invoked with the superwas command. This command assumes
that the WebSphere wsadmin.sh command is accessible. Make sure that
the directory that contains wsadmin.sh is in the PATH environment
variable. Make sure that wsadmin.sh is able to connect to WebSphere,
e.g. setup soap.client.properties with the correct login information.

Logging information is written by default to the log directory in
the users home directory, make sure the directory exists.

To get usage information invoke superwas without arguments or with
the -u argument..

Usage Examples
--------------
Install all resources specified in config file:
superwas -i myconfig.properties --install @

Uninstall all resources specified in config file:
superwas -i myconfig.properties --uninstall @

Uninstall then install all resources specified in config file:
superwas -i myconfig.properties --uninstall @ --install @

Install only DB2 Datasources specified in config file:
superwas -i myconfig.properties --install DB2DataSource

Uninstall then install only DB2 Datasources specified in config file:
superwas -i myconfig.properties --uninstall DB2DataSource --install DB2DataSource

Install only named applications:
superwas -i myconfig.properties --install Application -n application1 --install Application -n application2

Stop Servers:
superwas -i myconfig.properties --stop Server

Stop named server:
superwas -i myconfig.properties --stop Server -n server1

Get documentation for properties:
superwas -i myconfig.properties --documentation

Start Nagios monitoring writing to fifo /var/lib/superwasnagios
superwas -i myconfig.properties --nagiosStats -o /var/lib/superwasnagios

