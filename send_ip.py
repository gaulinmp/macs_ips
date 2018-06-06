#!/usr/bin/env python

import re
import sh
import json
import requests
import socket
    
PASSWORD_FILE = 'macs_ips.password'
SERVER_ROOT = 'http://mgaulin.com/projects/macs_ips'

def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    return s.getsockname()[0]

def url_string():
    _r = []
    comp_name = socket.gethostname().split(".")[0]

    for eth in re.compile(r'\n\b', re.I).split(str(sh.ifconfig())):
        if not eth or eth[0] != 'e':
            continue
        ip = re.findall(r'\binet [^\d]*((?:\d{1,3}\.){3}\d{1,3})', eth, re.I)
        iname = re.findall(r'^[a-z0-9]*', eth, re.I)
        if ip and iname:
            _r.append("comp_name={}_{}&comp_ip={}"
                      .format(comp_name, iname[0], ip[0]))

    #ip_internal = [x.split('inet addr:')[-1].split()[0] for x in sh.ifconfig().split("\n\n") if x.startswith('e')][0]
    try:
        resp = requests.get("https://api.ipify.org?format=json")
        ip_external = json.loads(resp.content.decode('utf-8'))['ip']
        if ip_external:
            _r.append("comp_name={}_external&comp_ip={}".format(comp_name, ip_external))
    except:
        pass
    print(_r)
    return _r

if __name__ == "__main__":
    with open(PASSWORD_FILE, 'r') as fh:
        pword = fh.read().strip()
    for url in url_string():
        full_url = ("{}/secret_write?magic_word={}&{}"
                    .format(SERVER_ROOT, pword, url))
        print(requests.get(full_url).content)
