ApacheMonitor
-------------

ApacheMonitor provides a method for pulling performance metrics from the Apache
HTTP Server (http://httpd.apache.org/) directly into Zenoss without requiring
the use of an agent. This is accomplished by utilizing the standard mod_status
module that comes with version 1 and 2 of the HTTP server.

The following metrics will be collected and graphed for the Apache HTTP Server.

    * Requests per Second
    * Throughput (Bytes/sec & Bytes/request)
    * CPU Utilization of the HTTP server and all worker processes/threads
    * Slot Usage (Open, Waiting, Reading Request, Sending Reply, Keep-Alive,
                  DNS Lookup and Logging)


Follow these steps to setup your HTTP server so that it will allow Zenoss to
access the server status.

    1. On the Apache server, find your httpd.conf file. This is normally
       located in /etc/httpd/httpd.conf or /etc/httpd/conf/httpd.conf. Other
       locations are possible depending on your operating system and setup.

    2. Turn the ExtendedStatus option on in the httpd.conf file. This option
       will typically be commented out. You can enable it by uncommenting it.

        #ExtendedStatus on

        ... becomes ...

        ExtendedStatus on

    3. Enable the /server-status location in the httpd.conf file. This is
       another option that typically already exists but is commented out.

        #<Location /server-status>
        #    SetHandler server-status
        #    Order deny,allow
        #    Deny from all
        #    Allow from .example.com
        #</Location>

        ... becomes ...

        <Location /server-status>
            SetHandler server-status
            Order deny,allow
            Deny from all
            Allow from zenoss.yourdomain.com
        </Location>

    4. Save the httpd.conf file with these changes then restart httpd. This can
       normally be accomplished with following command.

        apachectl restart


Once your Apache HTTP Server is configured to allow Zenoss to access the
extended status, you can add Apache monitoring to the device within Zenoss
by simply binding the Apache template to the device.

    1. Navigate to the device in the Zenoss web interface.
    2. Click the device menu, choose More then Templates.
    3. Click the templates menu, choose Bind Templates.
    4. Ctrl-click the Apache template from /Devices/Server to choose it.
    5. Click OK.

You will now be collecting the Apache HTTP Server metrics from this device.

