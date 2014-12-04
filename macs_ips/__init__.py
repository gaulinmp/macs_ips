from flask import Flask

app = Flask(__name__)
app.debug = True
app.secret_key = 'asdlf;na;oeiungt;43o89n332oi3n6lkw34hiagiwuefhniencyra'

import sec_browser_usage.views
