from __future__ import unicode_literals, print_function

import os
from sys import stderr

def make_dir(dir_path_list):
    if not dir_path_list:
        return os.path.realpath('.')
    
    if os.path.isdir(dir_path_list[0]):
        os.chdir(dir_path_list[0])
    else:
        os.mkdir(dir_path_list[0])
        os.chdir(dir_path_list[0])
        
    return make_dir(dir_path_list[1:])

def build_path(dir_path_list, prefix_path=None):
    os.chdir(prefix_path)

    return make_dir(dir_path_list)

'''
project_dir/data/
    2014/
        /<month/
            /<day of filing>/
                minutes.pdf
                log?
                processed_data_files
'''
def minutes_data(date, pre_path='data'):
    home = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    dpl = [pre_path, unicode(date.year), unicode(date.month), unicode(date.day)]

    return build_path(dpl, prefix_path=home)


