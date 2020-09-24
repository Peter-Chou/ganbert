import os
from flask import Flask, jsonify, request
from weibo_client import WeiBoModelRequestAdapter

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask(__name__)

TOO_SHORT_THRESHOLD = 30

MAX_SEQ_LEN = 128

weibo_client = WeiBoModelRequestAdapter(dict_path="./vocab.txt",
                                        max_seq_length=MAX_SEQ_LEN,
                                        do_lower_case=True)


@app.route("/v1/weibo/newsClassify", methods=["POST"])
def classify_trash_news():
  response = dict()
  try:
    texts = request.json.get('texts')
    text_length = len(texts)
    if text_length == 0:
      raise Exception("texts must have at least one text.")
    is_news_results = [True] * text_length

    index_list = []
    text_list = []
    for idx, text in enumerate(texts):
      if is_trash_by_rules(text):
        is_news_results[idx] = False
      else:
        index_list.append(idx)
        text_list.append(text)

    if len(text_list) > 0:
      model_results = weibo_client.request_model_results(text_list)
      for idx, model_result in zip(index_list, model_results):
        is_news_results[idx] = model_result

    response["code"] = 1
    response["msg"] = "success"
    response["is_news"] = is_news_results
  except Exception as e:
    response["code"] = "0"
    response["msg"] = "fail"
    response["Error"] = e.args
  finally:
    response_json = jsonify(response)
    return response_json


def is_trash_by_rules(text):
  if _is_too_short(text):
    return True

  return False


def _is_too_short(text):
  if len(text) < TOO_SHORT_THRESHOLD:
    return True
  return False


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=9004, debug=True, threaded=False)
  # app.run(host="0.0.0.0", port=9004, debug=False, threaded=True)
