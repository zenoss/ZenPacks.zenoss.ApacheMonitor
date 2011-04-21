###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
from Products.Zuul.infos import ProxyProperty
from zope.interface import implements
from Products.Zuul.infos.template import BasicDataSourceInfo
from ZenPacks.zenoss.ApacheMonitor.interfaces import IApacheMonitorDataSourceInfo


class ApacheMonitorDataSourceInfo(BasicDataSourceInfo):
    implements(IApacheMonitorDataSourceInfo)
    usessh = ProxyProperty('usessh')
    component = ProxyProperty('component')
    eventKey = ProxyProperty('eventKey')
    timeout = ProxyProperty('timeout')
    hostname = ProxyProperty('hostname')
    port = ProxyProperty('port')
    ssl = ProxyProperty('ssl')
    url = ProxyProperty('url')
    ngregex = ProxyProperty('ngregex')
    ngerror = ProxyProperty('ngerror')
    
    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
    


