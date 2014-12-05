#!/usr/bin/env python

import ipgetter
import socket
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    return s.getsockname()[0]

def url_string():
    comp_name = socket.gethostname().split(".")[0]
    ip_internal = get_internal_ip()
    ip_external = ipgetter.myip()
    return ("comp_name={}_internal&comp_ip={}".format(comp_name, ip_internal),
            "comp_name={}_external&comp_ip={}".format(comp_name, ip_external),)

if __name__ == "__main__":
    for url in url_string():
        print(urlopen("http://mgaulin.com/projects/macs_ips/secret_write?{}".format(url)))
