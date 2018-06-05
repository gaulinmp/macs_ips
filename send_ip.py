#!/usr/bin/env python

import sh
import json
import requests
#import ipgetter
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
    ip_internal = [x.split('inet addr:')[-1].split()[0] for x in sh.ifconfig().split("\n\n") if x.startswith('e')][0]
    try:
        resp = requests.get("https://api.ipify.org?format=json")
        ip_external = json.loads(resp.content.decode('utf-8'))['ip']
    except:
        ip_external = None

    _r = ["comp_name={}_internal&comp_ip={}".format(comp_name, ip_internal), ]
    if ip_external:
        _r.append("comp_name={}_external&comp_ip={}".format(comp_name, ip_external))

    return _r

if __name__ == "__main__":
    for url in url_string():
        full_url = "http://mgaulin.com/projects/macs_ips/secret_write?{}".format(url)
        print(full_url)
        print(urlopen(full_url))
