# -*- coding: utf-8 -*-
import json
import os
from weibo_processor import WeiBoProcessor
import requests
import tokenization
import numpy as np

MAX_SEQ_LEN = 128

EXAMPLE = "#民族团结党旗红#【生态净土 大美祁连 生态环境保护工作优先发展】"  # trash
EXAMPLE_2 = "【#字节跳动针对三方合作中的不实传言做出回应# 】21日上午，字节跳动针对与甲骨文及沃尔玛的三方合作中存在的不实传言进行回应，声明TikTok Global是字节跳动持股100%的子公司，并称目前的合作方案中不涉及任何算法和技术的转让。至于50亿美金教育基金的设立，公司也是从新闻中第一次听说。"  # trash


class WeiBoRequestAdapter:
  endpoints = "http://localhost:8501/v1/models/ganbert:predict"
  headers = {"content-type": "application-json"}

  def __init__(self,
               dict_path,
               max_seq_length,
               do_lower_case=True,
               news_index=2,
               too_short_threshold=30):
    self.tokenizer = tokenization.FullTokenizer(vocab_file=dict_path,
                                                do_lower_case=do_lower_case)
    self.max_seq_len = max_seq_length
    self.news_index = news_index
    self.too_short_threshold = too_short_threshold

  def request_model_results(self, texts):
    instances = []
    for text in texts:
      instances.append(self._preprocess_text(text))

    data = json.dumps({
        "signature_name": "serving_default",
        "instances": instances
    })

    response = requests.post(WeiBoRequestAdapter.endpoints,
                             data=data,
                             headers=WeiBoRequestAdapter.headers)
    prediction = json.loads(response.text)['predictions']
    prediction = np.asfarray(prediction)
    print(type(prediction))
    print(prediction)
    results = np.argmax(prediction, axis=1)
    print("results index: ", results == self.news_index)

  def _is_too_short(self, text):
    if len(text) < self.too_short_threshold:
      return True

  def _preprocess_text(self, text):
    text = tokenization.convert_to_unicode(text)
    tokens_a = self.tokenizer.tokenize(text)
    if len(tokens_a) > self.max_seq_len - 2:
      tokens_a = tokens_a[0:(self.max_seq_len - 2)]

    tokens = []
    segment_ids = []
    tokens.append("[CLS]")
    segment_ids.append(0)

    for token in tokens_a:
      tokens.append(token)
      segment_ids.append(0)
    tokens.append("[SEP]")
    segment_ids.append(0)

    label_id = 0
    input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
    input_mask = [1] * len(input_ids)

    while len(input_ids) < self.max_seq_len:
      input_ids.append(0)
      input_mask.append(0)
      segment_ids.append(0)

    assert len(input_ids) == self.max_seq_len
    assert len(input_mask) == self.max_seq_len
    assert len(segment_ids) == self.max_seq_len
    return {
        "input_ids": input_ids,
        "input_mask": input_mask,
        "segment_ids": segment_ids,
        "label_ids": label_id,
        "label_mask": [1]
    }


def main():
  weibo_client = WeiBoRequestAdapter(dict_path="./vocab.txt",
                                     max_seq_length=MAX_SEQ_LEN,
                                     do_lower_case=True)
  weibo_client.request_model_results([EXAMPLE, EXAMPLE_2])


if __name__ == '__main__':
  main()
