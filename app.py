import argparse
import os
from multiprocessing import Manager

import gunicorn.app.base
from flask import Flask, request
from river import compose, linear_model, metrics, preprocessing

metric = metrics.ROCAUC()
model = compose.Pipeline(
    preprocessing.StandardScaler(), linear_model.LogisticRegression()
)
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    json_request = request.json
    x = json_request["x"]
    return str(data["multiprocess_manager"]["model"].predict_one(x)), 200

@app.route("/update_model", methods=["PUT"])
def update_model():
    json_request = request.json
    x, y = json_request["x"], json_request["y"]
    model = data["multiprocess_manager"]["writable_model"]
    y_pred = model.predict_proba_one(x)
    model.learn_one(x, y)

    metric = data["multiprocess_manager"]["metric"]
    metric.update(y, y_pred)

    data["multiprocess_manager"]["metric"] = metric
    data["multiprocess_manager"]["writable_model"] = model
    data["multiprocess_manager"]["read_only_model"] = model
    return str(data["multiprocess_manager"]["metric"]), 200

def initialize():
    global data
    data = {}
    data["main_pid"] = os.getpid()
    manager_dict = Manager().dict()
    manager_dict["read_only_model"] = model
    manager_dict["writable_model"] = model
    manager_dict["metric"] = metric
    data["multiprocess_manager"] = manager_dict

class HttpServer(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    global data
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-workers", type=int, default=5)
    parser.add_argument("--port", type=str, default="8080")
    args = parser.parse_args()
    options = {
        "bind": "%s:%s" % ("0.0.0.0", args.port),
        "workers": args.num_workers,
    }
    initialize()
    HttpServer(app, options).run()