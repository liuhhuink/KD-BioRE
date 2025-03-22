#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import json
import xml.etree.ElementTree as ET
from utils.util import *


# ##
def xml_data_parse(file):
    # ##
    count_advise = 0
    count_effect = 0
    count_int = 0
    count_mechanism = 0
    count_no_relation = 0

    # ##
    xml_data = ET.parse(file)
    root = xml_data.getroot()

    # ##
    relation_id_list = []
    sentence_list = []
    relation_list = []
    # ##
    for sentence in root.findall('sentence'):
        # ##
        sentence_id = sentence.attrib.get('id')
        sentence_text = sentence.attrib.get('text')
        # ##
        entity_id_link_entity_type = dict()
        entity_id_link_entity_text = dict()
        entity_id_link_entity_location = dict()
        for entity in sentence.findall('entity'):
            entity_id = entity.attrib.get('id')
            entity_type = entity.attrib.get('type')
            entity_text = entity.attrib.get('text')
            entity_location = entity.attrib.get('charOffset')
            # ##
            if entity_id in entity_id_link_entity_type.keys():
                pass
            else:
                entity_id_link_entity_type.update({entity_id: entity_type})
            # ##
            if entity_id in entity_id_link_entity_text.keys():
                pass
            else:
                entity_id_link_entity_text.update({entity_id: entity_text})
            if entity_id in entity_id_link_entity_location.keys():
                pass
            else:
                entity_id_link_entity_location.update({entity_id: entity_location})
        # ##
        for pair in sentence.findall('pair'):
            pair_id = pair.attrib.get('id')
            e1_id = pair.attrib.get('e1')
            e2_id = pair.attrib.get('e2')
            ddi = pair.attrib.get('ddi')
            if ddi == 'false':
                # ##count of no relation pair
                count_no_relation += 1
                # ##
                relation = 'false'
            else:
                ddi_type = pair.attrib.get('type')
                if ddi_type == 'advise':
                    # ##
                    count_advise += 1
                elif ddi_type == 'effect':
                    # ##
                    count_effect += 1
                elif ddi_type == 'mechanism':
                    # ##
                    count_mechanism += 1
                elif ddi_type == 'int':
                    # ##
                    count_int += 1
                else:
                    print('error relation type', ddi_type, file, sentence_text)
                    exit()
                relation = ddi_type
            # ## entity 1 process
            if ';' in entity_id_link_entity_location[e1_id]:
                e1_location_start = int(entity_id_link_entity_location[e1_id].split(';')[0].split('-')[0])
                e1_location_end = int(entity_id_link_entity_location[e1_id].split(';')[0].split('-')[1])
            else:
                e1_location_start = int(entity_id_link_entity_location[e1_id].split('-')[0])
                e1_location_end = int(entity_id_link_entity_location[e1_id].split('-')[1])

            # ## entity 2 process
            if ';' in entity_id_link_entity_location[e2_id]:
                e2_location_start = int(entity_id_link_entity_location[e2_id].split(';')[0].split('-')[0])
                e2_location_end = int(entity_id_link_entity_location[e2_id].split(';')[0].split('-')[1])
            else:
                e2_location_start = int(entity_id_link_entity_location[e2_id].split('-')[0])
                e2_location_end = int(entity_id_link_entity_location[e2_id].split('-')[1])

            # ##sentence replaced entity with @drug@
            if e1_location_start < e2_location_start:
                new_sentence = (sentence_text[:e1_location_start] +
                                '@DRUG@' + sentence_text[e1_location_end + 1:e2_location_start] +
                                '@DRUG@' + sentence_text[e2_location_end + 1:])
            else:
                new_sentence = (sentence_text[:e2_location_start] +
                                '@DRUG@' + sentence_text[e2_location_end + 1:e1_location_start] +
                                '@DRUG@' + sentence_text[e1_location_end + 1:])
            # ##relation data generation
            relation_id_list.append(pair_id)
            sentence_list.append(new_sentence)
            relation_list.append(relation)

    return count_advise, count_effect, count_mechanism, count_int, count_no_relation, relation_id_list, sentence_list, relation_list


# ##
def ddi_raw_data_processing(xml_folder, save_file):
    # ##
    save_data = []

    # ##
    relation_id_list = []
    sentence_list = []
    relation_list = []

    # ##
    count_advise = 0
    count_effect = 0
    count_int = 0
    count_mechanism = 0
    count_no_relation = 0
    # ##
    files = os.listdir(xml_folder)
    # ##
    for file in files:
        (count_advise_s, count_effect_s, count_mechanism_s, count_int_s, count_no_relation_s,
         relation_id_list_s, sentence_list_s, relation_list_s) = xml_data_parse(os.path.join(xml_folder, file))
        # ##
        count_advise += count_advise_s
        count_effect += count_effect_s
        count_int += count_int_s
        count_mechanism += count_mechanism_s
        count_no_relation += count_no_relation_s

        # ##
        relation_id_list += relation_id_list_s
        sentence_list += sentence_list_s
        relation_list += relation_list_s

    count_relation = count_advise + count_effect + count_int + count_mechanism
    total = count_relation + count_no_relation
    print('total', total)
    print('relation', count_relation)
    print('count mechanism', count_mechanism)
    print('count effect', count_effect)
    print('count advise', count_advise)
    print('count int', count_int)

    print('count no relation', count_no_relation)
    # ##
    for i in range(total):
        # ##
        tmp = {}
        tmp['id'] = relation_id_list[i]
        tmp['sentence'] = sentence_list[i]
        tmp['relation'] = relation_list[i]
        # ##
        save_data.append(tmp)
        # ##
    with open(save_file, 'w', encoding='utf-8') as save_f:
        json.dump(save_data, save_f, ensure_ascii=False, indent=4)
        save_f.close()
    print(
        '###{},dataset ***{}** format transform and save to ***{}***.'.format(get_current_time(), xml_folder,
                                                                              save_file))


if __name__ == '__main__':

    # ##
    xml_folder = fr''
    # ##
    save_file = r''
    # ##
    ddi_raw_data_processing(xml_folder, save_file)