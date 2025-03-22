#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@IDE     ：PyCharm
Meta-Llama3.1-8B-Instruct supervised fine-tuning data format
[{
    "prompt":"",
    "message":[{"content":"","role":"system"},{"content":"","role":"user"},{"content":"","role":"assistant"}
    ],
    "prompt_id":""
},
...
]
"""
import hashlib
import random

from utils.util import *

# ******************************parameter***********************************
# **************************************************************************
# **************************************************************************
prompt_system_file = r'../config/prompt_system.txt'
prompt_ddi_file = r'../config/prompt_ddi_wo_opd.txt'

prompt_system = load_txt_get_config(prompt_system_file)
prompt_ddi = load_txt_get_config(prompt_ddi_file)


# ******************************dataset generation**************************
# **************************************************************************
# **************************************************************************
# ##[generate 64-bit prompt hash id]
def prompt_id_generation(prompt):
    # ##
    hash_object = hashlib.sha256(prompt.encode())
    prompt_id = hash_object.hexdigest()
    return prompt_id


# ##[message generation]
def re_message_generation(sentence, answer):
    sys_m = {'content': prompt_system, 'role': 'system'}
    user_m = {'content': prompt_ddi.format(sentence), 'role': 'user'}
    assistant_m = {'content': answer, 'role': 'assistant'}
    return [sys_m, user_m, assistant_m]


# ##
def re_sft_dataset_generation_ddi(src_file, save_folder):
    # ##save file generation
    create_new_dir(save_folder)
    create_new_dir(os.path.join(save_folder, 'data'))
    save_file = os.path.join(os.path.join(save_folder, 'data'), 'train.parquet')

    # ##target format data
    save_data = []
    save_data_no_relation = []
    # ##load json file
    json_data = load_json_data_base(src_file)
    # ##
    for obj in json_data:
        id = obj['id']
        sentence = obj['sentence']
        relation = obj['relation']
        answer = ddi_relation_convert_to_option(relation)
        re_message = re_message_generation(sentence, answer)
        prompt_id = prompt_id_generation(id)
        tmp = {}
        tmp['prompt'] = id
        tmp['messages'] = re_message
        tmp['prompt_id'] = prompt_id
        # print(tmp)
        # exit()
        if relation == 'false':
            save_data_no_relation.append(tmp)
        else:
            save_data.append(tmp)
    save_data += random.sample(save_data_no_relation, 8000)
    random.shuffle(save_data)
    # ##save data
    dict_save_to_parquet(save_data, save_file)
    print('###{},llama3.1 supervised fine-tuning data generation and save to {}.'.format(get_current_time(),
                                                                                         save_file))


if __name__ == '__main__':
    # ##
    src_file = r'../data/DDICorpus/train.json'
    save_folder = r'../data\sft_dataset\ddi-baseline-wo-opd'
    # ##
    re_sft_dataset_generation_ddi(src_file, save_folder)
