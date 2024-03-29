from flask import Flask, render_template, request, jsonify
import json
from BankersAlgorithm import BankersAlgorithm as ba
app = Flask(__name__)


default_config = {'num_proc': 5, 'num_res': 3, 'resources': [10, 5, 7],
                  'allocation': [[0, 1, 0], [2, 0, 0], [3, 0, 2],
                                 [2, 1, 1], [0, 0, 2]],
                  'max': [[7, 5, 3], [3, 2, 2], [9, 0, 2],
                          [2, 2, 2], [4, 3, 3]]}


def bankers_algorithm_factory(config=default_config):
    return ba(config["num_proc"], config["num_res"], config["resources"],
              config["allocation"], config["max"])


b = bankers_algorithm_factory()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/request", methods=["POST"])
def resource_request():
    proc_id = int(request.form["proc_id"])
    resources = list(map(int, request.form.getlist("resource_req[]")))
    try:
        is_safe, safe_sequence, log = b.request(proc_id, resources)
        return jsonify({"is_safe": is_safe,
                        "safe_seq": safe_sequence,
                        "log": log})
    except ValueError as ve:
        return jsonify({"is_safe": False,
                        "safe_seq": [],
                        "log": ["Value Error: " + str(ve)]})


@app.route("/safety", methods=["GET"])
def safety():
    try:
        is_safe, safe_sequence, log = b.safety()
        return jsonify({"is_safe": is_safe,
                        "safe_seq": safe_sequence,
                        "log": log})
    except ValueError as ve:
        return jsonify({"is_safe": False,
                        "safe_seq": [],
                        "log": ["Value Error: " + str(ve)]})


@app.route("/update", methods=["POST"])
def update():
    config = json.loads(request.form["config"])["config"]
    global b
    try:
        b = bankers_algorithm_factory(config)
        return jsonify({"status": "success"})
    except Exception as e:
        b = bankers_algorithm_factory(default_config)
        return jsonify({"status": "error", "error": str(e)})


@app.route("/current")
def current():
    return jsonify({
        'num_proc': b.num_proc,
        'num_res': b.num_res,
        'resources': b.resources,
        'allocation': b.allocation,
        'max': b.maximum
    })


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
