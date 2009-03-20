#!/usr/bin/env python
###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

from optparse import OptionParser
import sys
import httplib
import re

class ZenossApacheStatsPlugin:
    def __init__(self, host, port, ssl, url):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.url = url

    def run(self):
        line_regex = re.compile(r'^([^:]+): (.+)$')
        metrics = {}

        if self.ssl:
            conn = httplib.HTTPSConnection(self.host, self.port)
        else:
            conn = httplib.HTTPConnection(self.host, self.port)
        
        try:
            conn.request('GET', self.url)
            response = conn.getresponse()
            if response.status != 200:
                print 'Server replied: %d %s to action GET %s' % (
                        response.status, response.reason, self.url)
                sys.exit(1)
            
            data = response.read()
            for line in data.split("\n"):
                match = line_regex.search(line)
                if not match: continue
                name, value = match.groups()

                if name == 'Total Accesses':
                    metrics['totalAccesses'] = value
                elif name == 'Total kBytes':
                    metrics['totalKBytes'] = value
                elif name == 'CPULoad':
                    metrics['cpuLoad'] = value
                elif name == 'ReqPerSec':
                    metrics['reqPerSec'] = value
                elif name == 'BytesPerSec':
                    metrics['bytesPerSec'] = value
                elif name == 'BytesPerReq':
                    metrics['bytesPerReq'] = value
                elif name == 'BusyServers' or name == 'BusyWorkers':
                    metrics['busyServers'] = value
                elif name == 'IdleServers' or name == 'IdleWorkers':
                    metrics['idleServers'] = value
                elif name == 'Scoreboard':
                    metrics['slotWaiting'] = 0
                    metrics['slotStartingUp'] = 0
                    metrics['slotReadingRequest'] = 0
                    metrics['slotSendingReply'] = 0
                    metrics['slotKeepAlive'] = 0
                    metrics['slotDNSLookup'] = 0
                    metrics['slotLogging'] = 0
                    metrics['slotGracefullyFinishing'] = 0
                    metrics['slotOpen'] = 0
                    for code in value:
                        if code == '_':
                            metrics['slotWaiting'] += 1
                        elif code == 'S':
                            metrics['slotStartingUp'] += 1
                        elif code == 'R':
                            metrics['slotReadingRequest'] += 1
                        elif code == 'W':
                            metrics['slotSendingReply'] += 1
                        elif code == 'K':
                            metrics['slotKeepAlive'] += 1
                        elif code == 'D':
                            metrics['slotDNSLookup'] += 1
                        elif code == 'L':
                            metrics['slotLogging'] += 1
                        elif code == 'G':
                            metrics['slotGracefullyFinishing'] += 1
                        elif code == '.':
                            metrics['slotOpen'] += 1

        except SystemExit:
            sys.exit(1)
        except Exception, e:
            print str(e)
            sys.exit(1)

        if not metrics:
            print "no metrics were returned"
            sys.exit(1)
        
        print "STATUS OK|%s" % (' '.join([ "%s=%s" % (m[0],m[1]) \
            for m in metrics.items() ]))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--host', dest='host',
        help='Hostname of Apache server')
    parser.add_option('-p', '--port', dest='port',
        type='int', default=80,
        help='Port of Apache server')
    parser.add_option('-s', '--ssl', dest='ssl',
        action='store_true', default=False,
        help='Use HTTPS for the connection')
    parser.add_option('-u', '--url', dest='url',
        default='/server-status?auto',
        help='Relative URL of server status page')
    options, args = parser.parse_args()

    if not options.host:
        print "You must specify the host parameter."
        sys.exit(1)

    cmd = ZenossApacheStatsPlugin(
        options.host, options.port, options.ssl, options.url)
    cmd.run()
