# -*- coding: utf-8 -*-

import os
import requests
import tokenization
import grpc

from tensorflow.core.example import example_pb2
from tensorflow.core.framework import tensor_pb2, tensor_shape_pb2, types_pb2
from typing import List
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

import numpy as np


class WeiBoModelRequestRpcAdapter:
  # rpc_server = "localhost:8500"
  rpc_server = "tfs:8500"
  model_name = "ganbert"
  model_signature_name = "serving_default"

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
    self._channel = grpc.insecure_channel(
        WeiBoModelRequestRpcAdapter.rpc_server)
    self._stub = prediction_service_pb2_grpc.PredictionServiceStub(
        self._channel)

  def request_model_results(self, texts: List) -> List[bool]:
    request = predict_pb2.PredictRequest()
    request.model_spec.name = WeiBoModelRequestRpcAdapter.model_name  # specify model name
    request.model_spec.signature_name = WeiBoModelRequestRpcAdapter.model_signature_name  # specify export signature

    serialized_examples = []
    for text in texts:
      serialized_examples.append(self._preprocess_text(text))

    dims = [
        tensor_shape_pb2.TensorShapeProto.Dim(size=len(serialized_examples))
    ]
    tensor_shape_proto = tensor_shape_pb2.TensorShapeProto(dim=dims)
    tensor_proto = tensor_pb2.TensorProto(dtype=types_pb2.DT_STRING,
                                          tensor_shape=tensor_shape_proto,
                                          string_val=serialized_examples)
    # tensor_proto.string_val.extend(serialized_examples)

    request.inputs["examples"].CopyFrom(tensor_proto)
    request_result = self._stub.Predict(request, 600)  # 600 is timeout
    classifier_result = request_result.outputs["probabilities"].float_val
    classifier_result_np = np.reshape(np.asfarray(classifier_result), (-1, 3))

    results = np.argmax(classifier_result_np, axis=1)

    return (results == self.news_index).tolist()

  def _preprocess_text(self, text) -> str:
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

    ex = example_pb2.Example()
    ex.features.feature["input_ids"].int64_list.value.extend(input_ids)
    ex.features.feature["input_mask"].int64_list.value.extend(input_mask)
    ex.features.feature["segment_ids"].int64_list.value.extend(segment_ids)
    ex.features.feature["label_ids"].int64_list.value.append(label_id)
    ex.features.feature["label_mask"].int64_list.value.append(1)

    return ex.SerializeToString()


def main():
  test = "#民族团结党旗红#【生态净土 大美祁连 生态环境保护工作优先发展】"
  test2 = "【#北京入秋#比常年晚6天】据北京市气象局消息，9月15日北京观象台站日平均气温降至20℃，为8月1日以来首次低于22℃，同时连续5天（9月16日-9月20日）滑动平均气温低于22℃，根据《气候季节划分》判断，9月15日为北京今年入秋日，比常年晚6天。北京气象观测代表站（观象台站）入秋时间常年值（19812010年平均）为9月9日。"
  MAX_SEQ_LEN = 128
  weibo_rpc_client = WeiBoModelRequestRpcAdapter(dict_path="./vocab.txt",
                                                 max_seq_length=MAX_SEQ_LEN,
                                                 do_lower_case=True)
  weibo_rpc_client.request_model_results([test, test2])


if __name__ == '__main__':
  main()
