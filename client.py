# -*- coding: utf-8 -*-
import json
import os
import requests
import tokenization

endpoints = "http://localhost:8501/v1/models/ganbert:predict"
headers = {"content-type": "application-json"}

# tokenizer = tokenization.FullTokenizer(
#     vocab_file="/home/path/to/bert/vocabfile/vocab.txt", do_lower_case=True)
tokenizer = tokenization.FullTokenizer(
    vocab_file="/home/peter/projects/ganbert/chinese_L-12_H-768_A-12/vocab.txt",
    do_lower_case=True)

example = "#民族团结党旗红#【生态净土 大美祁连 生态环境保护工作优先发展】"
token_a = tokenizer.tokenize(example)
tokens = []
segments_ids = []
tokens.append("[CLS]")
segment_ids = []
segment_ids.append(0)
for token in token_a:
  tokens.append(token)
  segment_ids.append(0)
tokens.append('[SEP]')
segment_ids.append(0)
input_ids = tokenizer.convert_tokens_to_ids(tokens)
input_mask = [1] * len(input_ids)
max_seq_length = 128
while len(input_ids) < max_seq_length:
  input_ids.append(0)
  input_mask.append(0)
  segment_ids.append(0)

label_id = 0
instances = [{
    "input_ids": input_ids,
    "input_mask": input_mask,
    "segment_ids": segment_ids,
    "label_ids": label_id,
    "label_mask": [1]
}]
data = json.dumps({"signature_name": "serving_default", "instances": instances})
response = requests.post(endpoints, data=data, headers=headers)
print("response text: ", response.text)
prediction = json.loads(response.text)['predictions']
print(prediction)
