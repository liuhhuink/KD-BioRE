#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import torch
from utils.util import *
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer,BitsAndBytesConfig

# ##########################################################################
# ##local model weight path
model_path = r'../local_models\Meta-Llama-3.1-8B-Instruct'
# ##local system prompt and user prompt
prompt_system_file = r'./config/prompt_system.txt'
prompt_ddi_file = r'./config/prompt_ddi_llm.txt'

prompt_system = load_txt_get_config(prompt_system_file)
prompt_ddi = load_txt_get_config(prompt_ddi_file)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

# ##########################################################################
# Load fine-tuned model
model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=model_path,
    device_map="auto",
    torch_dtype=torch.float16
)

tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_path)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model.resize_token_embeddings(len(tokenizer))

# Create chat pipeline
chat_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto"
)


# ##########################################################################
# ##request local deployment large language models
def request_local_llm(message):
    output = chat_pipeline(
        message,
        max_new_tokens=256,
        temperature=0.7,
        do_sample=True,
        eos_token_id=tokenizer.eos_token_id
    )
    # print(output[0]['generated_text'])
    return output[0]['generated_text'][2]['content']


# ##generate message for local llm request
def request_message_generation(sentence):
    """
        :param sentence:
        :return:
        [   {"role":"system", "content":""}
            {"role":"user", "content":""},
        ]
        """
    return [{"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_ddi.format(sentence)}]


# ##load test dataset request llm
def load_data_request_local_llm(src_file, save_file):
    """
    :param src_file:
    :param save_file:
    :return:
    """
    # ##
    save_data = []
    # ##
    json_data = load_json_data_base(src_file)
    count = 0
    for obj in json_data:
        count += 1
        sentence = obj['sentence']
        # ##
        message = request_message_generation(sentence)
        # ##
        result = request_local_llm(message)
        print('### {},{} result: {}'.format(count, get_current_time(), result))
        # ##
        tmp = {}
        # tmp['count'] = obj['count']
        tmp['id'] = obj['id']
        tmp['sentence'] = sentence
        tmp['relation'] = obj['relation']
        tmp['result'] = result
        # ##
        save_data.append(tmp)
    # ##save data
    with open(save_file, 'w', encoding='utf-8') as save_f:
        json.dump(save_data, save_f, ensure_ascii=False, indent=4)
        save_f.close()
    print('###{} Relation extraction done, the result save to {}.'.format(get_current_time(), save_file))


if __name__ == '__main__':
    # ##
    src_file_path = r'./data/DDICorpus/test.json'
    save_file_path = r'./data/DDICorpus/test_res.json'
    # ##
    load_data_request_local_llm(src_file_path, save_file_path)
