#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import time
import json
import pandas as pd


# <editor-folder desc='base function'>
# ##
def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


# ##
def create_new_dir(save_dir):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        print('### {} {} .'.format(get_current_time(), save_dir))
    else:
        print('### {} {} .'.format(get_current_time(), save_dir))


# ##
def load_json_data_base(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = f.read()
        json_data = json.loads(data)
        f.close()
        return json_data


# ##
def load_txt_get_config(txt_file):
    # ##
    f = open(txt_file, 'r', encoding='utf-8')
    # ##
    conf = f.read()
    return conf


# ##dict
def dict_save_to_parquet(data_dict, save_file):
    df = pd.DataFrame(data_dict)
    df.to_parquet(save_file, engine='pyarrow')
    print('###{},dict data save to {}.'.format(get_current_time(), save_file))


# </editor-folder>

# <editor-folder desc='DDI'>
# ##
def ddi_relation_convert_to_option(relation):
    answer = ''
    if relation == 'mechanism':
        answer = 'Mechanism'
    elif relation == 'effect':
        answer = 'Effect'
    elif relation == 'advise':
        answer = 'Advise'
    elif relation == 'int':
        answer = 'Interaction'
    elif relation == 'false':
        answer = 'No relation'
    else:
        print('relation error')
        exit()
    return answer


def ddi_option_convert_to_id(option):
    if option == 'Mechanism':
        id = 0
    elif option == 'Effect':
        id = 1
    elif option == 'Advise':
        id = 2
    elif option == 'Interaction':
        id = 3
    elif option == 'No relation':
        id = 4
    else:
        # return 0
        # id=0
        print(option, 'option error')
        exit()
    return id


# </editor-folder>

# <editor-folder desc=''>
# ##
def chemprot_relation_convert_to_option(relation):
    answer = ''
    if relation == 'CPR:3':
        answer = 'Upregulator'
    elif relation == 'CPR:4':
        answer = 'Downregulator'
    elif relation == 'CPR:5':
        answer = 'Agonist'
    elif relation == 'CPR:6':
        answer = 'Antagonist'
    elif relation == 'CPR:9':
        answer = 'Participant'
    else:
        print('relation error')
        exit()
    return answer


# ##
def chemprot_option_convert_to_id(option):
    if option == 'Upregulator':
        id = 0
    elif option == 'Downregulator':
        id = 1
    elif option == 'Agonist':
        id = 2
    elif option == 'Antagonist':
        id = 3
    elif option == 'Participant':
        id = 4
    else:
        # id=0
        print(option, 'option error')
        exit()
    return id

# </editor-folder>
