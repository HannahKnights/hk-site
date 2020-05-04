"""
Helper functions related to app configuration and set-up
"""

from conf.globals import *
from conf.bottle import TEMPLATE_PATH

def include_abs_path_in_templates(file_path):
    """
    Makes sure the absolute path is added to the bottle
    template files global
    """
    template_path = get_abs_path(file_path, 'views')
    TEMPLATE_PATH.insert(0, template_path)

def get_abs_path(file_path, relative_path):
    """
    Takes the path, as passed in from base.py and creates absolute paths
    """
    import os
    dir_path = os.path.dirname(file_path)
    abs_path = os.path.join(dir_path, relative_path)
    return abs_path
