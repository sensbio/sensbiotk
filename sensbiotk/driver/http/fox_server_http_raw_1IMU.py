# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 19:06:44 2015

@author: bsijober
"""

import time
import BaseHTTPServer
import numpy as np
from sensbiotk.driver import fox_dongle as fdongle

HOST_NAME = 'localhost' 
PORT_NUMBER = 8000 


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response()
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        print(str(s.path))
        if foxdongle.is_running():
            data = foxdongle.read()
            if len(data) != 0:
#                print(str(data))
                data = data[2:12]
                s.wfile.write(str(data[0]) +' '+ str(data[1]) +' '+
                    str(data[2]) +' '+ str(data[3]) +' '+ str(data[4]) +' '+
                    str(data[5]) +' '+ str(data[6]) +' '+ str(data[7]) +' '+
                    str(data[8]))
            
        
         

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)

    # instanciates dongle
    foxdongle = fdongle.FoxDongle() 
    init = False
    while not init:
        # handle dongle initialization
        if foxdongle.init_dongle():
            init = True
            print 'Device is connected to %s.' % (foxdongle.line())    
    
    # inits server
    try:
        httpd.serve_forever()
        
                    
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)