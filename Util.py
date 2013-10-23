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

# Utility functions
# 
# Author: Andre van Dijk (SuperClass IT)
# Date: $Date: 2013-01-04 16:04:36 +0100 (vr, 04 jan 2013) $
# $Id: Util.py 424 2013-01-04 15:04:36Z andre $
import java.lang.System

def dictToList(dict):
	"""
	Util function to convert dict to list
	"""
	if dict is not None:
		return [["%s" % key , "%s" % value ] for key,value in dict.items()]
	return None

def getNL():
	return java.lang.System.getProperty('line.separator')

def wslist(wslist):
	"""
	Utility function that converts wsadmin strings to a python list
	"""
	out = []
	if (len(wslist) > 0 and wslist[0] == '[' and wslist[ - 1] == ']'):
		tmpList = wslist[1: - 1].split() #splits space-separated lists,
	else:
		tmpList = wslist.split(getNL())
	for item in tmpList:
		item = item.rstrip();     #removes any Windows "\r"
		if (len(item) > 0):
			out.append(item)
	return out
