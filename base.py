from conf.bottle import Bottle as _Bottle, run as _run, static_file as _static_file, \
    template as _template, error, abort, response, \
    ConfigDict, TEMPLATE_PATH
from conf.helpers import include_abs_path_in_templates, get_abs_path, get_work_html_list

import os
import json as _json

# create app instance and update the config
app = _Bottle()
conf = ConfigDict()
additional_conf_items = conf.load_module('config')
app.config.update(additional_conf_items)

# add additional abs path to global TEMPLATE_PATH
root_path = os.path.abspath(__file__)
include_abs_path_in_templates(root_path)

# set additional params
debug_mode = app.config.get('DEBUG', False)

"""
    [Add any relevant notes that might help understand the contents of the app]
"""

# resources
# ---------

@app.route('/static/<filepath:path>')
def server_static(filepath):
    root_path = os.path.abspath(__file__)
    static_folder = get_abs_path(root_path, 'static')
    return _static_file(filepath, root = static_folder)

# public
# ------

@app.route('/')
def take_me_home():
    work_list_html = get_work_html_list(verbose = debug_mode)
    return _template('home', work_list_html = work_list_html)


# archive
# -------

# 20122017
@app.route('/archive/20122017')
def archive_20122017():
    return _template('20122017', is_cv = False)

@app.route('/archive/20122017/cv')
def archive_20122017():
    return _template('20122017', is_cv = True)


# error handling
# --------------

@app.error(404)
def error_404(error):
    return 'Nothing here, sorry'

@app.error(500)
def error_500(error):
    return 'Oops, sorry something went wrong'

# run the app
if app.config.get('IS_PRODUCTION'):
    # this is relevant for heroku deployment...
    _run(app, host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
else:
    _run(app, host='localhost', port=8082, debug=True)
