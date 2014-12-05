import os
import re
import json
import time
import logging
import datetime

from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.debug = True
app.secret_key = 'apf9s8enpaosen6lkw34hiagiwuefhniencyra'

db_filename = "data.json"

@app.route('/')
def test():
    secret   = request.args.get('magic_word', '')
    if 'please' == secret:
        return "%s" % json.dumps(rw_db())
    return ""

@app.route('/secret_write', methods=['GET', ])
def write():
    name_txt = request.args.get('comp_name', '')
    ip_txt   = request.args.get('comp_ip', '')
    if name_txt and ('dumb' != name_txt): # exists and
        if ip_txt and ('dumb' != ip_txt): # is a string
            return rw_db(name_txt, ip_txt)
    return "ERROR: {}".format(request.args)


def rw_db(key=None, value=None):
    """Either read the database, or pass key:value to write to db."""
    if key: return _w_db(key=key, value=value)
    return _r_db()

def _r_db():
    filename = os.path.join(app.root_path, db_filename)
    try:
        with open(filename) as fh:
            data = fh.read()
    except FileNotFoundError:
        logging.warn("File Not Found: {}".format(filename))
        with open(filename, 'w+') as fh:
            fh.write("{}")
            data = "{}"
    print("Read: {}".format(data))
    try:
        return json.loads(data)
    except ValueError:
        logging.warn("Data read not valie JSON: {}".format(data))
        return {}

def _w_db(key=None, value=None):
    current_db = _r_db()
    current_db[key] = value
    filename = os.path.join(app.root_path, db_filename)
    with open(filename, 'w+') as fh:
            fh.write(json.dumps(current_db))
    print("Wrote: {}".format(current_db))
    return json.dumps(current_db)
