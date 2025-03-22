#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from utils.util import *


# ##
def load_chemprot_data_processing(src_file, save_file):
    # #3
    count_3 = 0
    count_4 = 0
    count_5 = 0
    count_6 = 0
    count_9 = 0
    # ##
    save_data = []
    # ##
    json_data = load_json_data_base(src_file)
    for obj in json_data:
        relation = obj['relation']
        if relation == 'CPR:3':
            count_3 += 1
            save_data.append(obj)
        elif relation == 'CPR:4':
            count_4 += 1
            save_data.append(obj)
        elif relation == 'CPR:5':
            count_5 += 1
            save_data.append(obj)
        elif relation == 'CPR:6':
            count_6 += 1
            save_data.append(obj)
        elif relation == 'CPR:9':
            count_9 += 1
            save_data.append(obj)
        elif relation == 'false':
            pass
        else:
            print('error', obj)
            exit()
    # ##
    with open(save_file, 'w', encoding='utf-8') as save_f:
        json.dump(save_data, save_f, ensure_ascii=False, indent=4)
        save_f.close()
    # ##
    print('CPR:3 count', count_3)
    print('CPR:4 count', count_4)
    print('CPR:5 count', count_5)
    print('CPR:6 count', count_6)
    print('CPR:7 count', count_9)


if __name__ == '__main__':
    # ##
    split = 'test'
    # ##
    src_file = fr'D:\LiuHui\2025-biore-dataset\ChemProt\{split}.json'
    save_file = fr'../data/ChemProt/{split}.json'
    # ##
    load_chemprot_data_processing(src_file, save_file)
