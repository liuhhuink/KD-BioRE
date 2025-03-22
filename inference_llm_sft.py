#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import torch
from utils.util import *
from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# ******************************parameter***********************************
# **************************************************************************
# **************************************************************************
local_model_path = r"../local_models\Meta-Llama-3.1-8B-Instruct"
sft_model_path = r'./checkpoints/Meta-Llama-3.1-8B-Instruct-sft'
prompt_system_file = r'./config/prompt_system.txt'
prompt_ddi_file = r'./config/prompt_ddi_think.txt'

prompt_system = load_txt_get_config(prompt_system_file)
prompt_ddi = load_txt_get_config(prompt_ddi_file)

# ******************************load model and tokenizer********************
# **************************************************************************
# **************************************************************************

device_map = 'auto'

# Configure BitsAndBytes for 4-bit quantization to reduce memory usage
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

# Load the model
base_model = AutoModelForCausalLM.from_pretrained(local_model_path,
                                                  quantization_config=bnb_config,
                                                  device_map=device_map)
model = PeftModel.from_pretrained(base_model, sft_model_path)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(local_model_path, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

torch.backends.cuda.enable_mem_efficient_sdp(True)
torch.backends.cuda.enable_flash_sdp(True)


# ******************************load model and tokenizer********************
# **************************************************************************
# **************************************************************************

# ##
def request_message_generation(prompt_system, prompt_ddi, question):
    """
        :param prompt_system:
        :param prompt_ddi:
        :param question:
        :return:
        [   {"role":"system", "content":""}
            {"role":"user", "content":""},
        ]
        """
    return [{"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_ddi + question}]


# ##
def local_llama_request(message):
    # ##
    input_ids = tokenizer.apply_chat_template(message, add_generation_prompt=True, return_tensors="pt").to(
        model.device)
    # ##
    outputs = model.generate(input_ids, pad_token_id=tokenizer.eos_token_id, max_new_tokens=512,
                             # eos_token_id=terminators, do_sample=True, temperature=0.9, top_p=0.9)
                             eos_token_id=terminators, do_sample=True, temperature=1, top_p=1)
    # top_p=0.9, )
    # ##
    response = outputs[0][input_ids.shape[-1]:]

    return tokenizer.decode(response, skip_special_tokens=True)


# ##
def load_ddi_test_set_do_re(src_file, save_file):
    # ##
    count = 0
    # ##
    save_data = []
    # ##
    json_data = load_json_data_base(src_file)
    # ##
    for data in json_data:
        # ##
        count += 1
        # ##
        id = data['id']
        sentence = data['sentence']
        relation = data['relation']
        # ##
        message = request_message_generation(prompt_system, prompt_ddi, sentence)
        # ##
        answer = local_llama_request(message)
        print('### {},{} result: {}'.format(count, get_current_time(), answer))
        # ##
        tmp = {}
        tmp['id'] = id
        tmp['sentence'] = sentence
        tmp['relation'] = relation
        tmp['result'] = answer
        save_data.append(tmp)
    # ##
    with open(save_file, 'w', encoding='utf-8') as save_f:
        json.dump(save_data, save_f, ensure_ascii=False, indent=4)
        save_f.close()
    print('###{} Relation extraction done, the result save to {}.'.format(get_current_time(), save_file))


if __name__ == '__main__':
    # ##
    src_file_path = r'./data/DDICorpus/test.json'
    save_file_path = r'./data/DDICorpus/test_res.json'
    # ##
    load_ddi_test_set_do_re(src_file_path, save_file_path)
