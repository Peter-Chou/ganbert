import os
from flask import Flask, jsonify, request

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask(__name__)


@app.route("/v1/weibo/newsClassify", methods=["POST"])
def classify_trash_news():
  return dict()


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=9004, debug=False, threaded=True)
