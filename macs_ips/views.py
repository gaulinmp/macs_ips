import os
import re
import json
import time
import datetime
import pandas as pd

from flask import render_template, request, url_for

from sec_browser_usage import app

browser_datafile = '/home1/mgaulinc/projects/python/sec_browser_usage/static/browser_output.tsv'
#assert os.path.exists(browser_datafile)


@app.route('/')
def test():
    return render_template('area.html')


@app.route('/json/')
def data_json_route():
    data = pd.read_csv(browser_datafile, sep='\t', index_col=0, parse_dates=True)

    start_date,end_date = min(data.index),max(data.index)
    start_get_ms = request.args.get('start',"%d000"%time.mktime(start_date.timetuple()))
    end_get_ms = request.args.get('end',"%d000"%time.mktime(end_date.timetuple()))

    start_get_date = max(datetime.datetime.fromtimestamp(int(start_get_ms)/1000),start_date)
    end_get_date = min(datetime.datetime.fromtimestamp(int(end_get_ms)/1000),end_date)

    num_obs,num_days = 250.0,end_get_date - start_get_date

    df = data.ix[start_get_date:end_get_date,: \
           ].resample('%dD'%(max(int(num_days.days/num_obs),1)),how='mean')


    hc_obj = []
    colors = ['#0033FF','#33FF00','#CC00FF','#FF9900']
    browsers = ('safari','chrome','firefox','msie')
    for b in browsers:
        hc_obj.append({'name':b,'type':'area'})
        hc_obj[-1]['data']=zip(df[b].index.map(lambda x: time.mktime(x.timetuple())*1000).tolist(),df[b].round(0).values.tolist())
        #hc_obj[-1]['data']=df[b].round(0).values.tolist()
        #hc_obj[-1]['data']=list(df['pct_'+b].values)
        #hc_obj[-1]['pointStart']= ms_start
        hc_obj[-1]['startdatedebug']= str(start_get_date.date())
        hc_obj[-1]['enddatedebug']= str(end_get_date.date())
        #hc_obj[-1]['pointInterval']= ms_diff
        hc_obj[-1]['color']= colors.pop()

    if not request.args.get('start',False):
        totsum = data.ix[:,[i for i,v in enumerate(df.columns.values) if v!='none']].sum(axis=1)
        totsum_json=zip(totsum.index.map(lambda x: time.mktime(x.timetuple())*1000).tolist(),totsum.values.tolist())
        return "%s(%s);"%( \
            request.args.get('callback','afterSetExtremes')\
                          ,json.dumps({'plotdata':hc_obj,'navdata':totsum_json}))

    return "%s(%s);"%( \
        request.args.get('callback','afterSetExtremes')\
        ,json.dumps(hc_obj))



ignoreme = """
    return render_template('index.html',poo=request)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)
"""
