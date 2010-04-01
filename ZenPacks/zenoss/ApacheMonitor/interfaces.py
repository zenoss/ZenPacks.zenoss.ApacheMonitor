###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
from Products.Zuul.interfaces import IBasicDataSourceInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IApacheMonitorDataSourceInfo(IBasicDataSourceInfo):
    component = schema.Text(title=_t(u'Component'))
    eventKey = schema.Text(title=_t(u'Event Key'))
    timeout = schema.Int(title=_t(u'Timeout (seconds)'))
    hostname = schema.Text(title=_t(u'Apache Host'))
    usessh = schema.Bool(title=_t(u'Use SSH'))
    port = schema.Int(title=_t(u'Apache Port'))
    ssl = schema.Bool(title=_t(u'Use HTTPS?'))
    url = schema.Text(title=_t(u'Status URL'))
    ngerror = schema.Text(title=_t(u'Named Group Regex Error'))
    ngregex = schema.TextLine(title=_t(u'Named Group Regex'), xtype='twocolumntextarea')
    
