from simplexml import dumps
from flask import Flask, request, jsonify, g
from src.estimator import estimator
import time

app = Flask(__name__)


@app.before_request
def before_req():
    g.start = time.time() * 1000


@app.after_request
def after_req(response):
    f = open('log.txt', 'a+')
    req_method = request.method
    req_path = request.path
    res_time = round(time.time() * 1000 - g.start)
    res_status_code = response.status_code

    f.write("{} \t\t {} \t\t {} \t\t {} ms \n".format(req_method, req_path, res_status_code, res_time))
    f.close()
    return response


@app.route('/')
def home():
    return "Hello, Word"


@app.route('/api/v1/on-covid-19', methods=['POST'])
def get_estimation_default():
    req_data = request.get_json()
    res = estimator(req_data)
    return jsonify(res)


@app.route('/api/v1/on-covid-19/json', methods=['POST'])
def get_estimation_json():
    return get_estimation_default()


@app.route('/api/v1/on-covid-19/xml', methods=['POST'])
def get_estimation_xml():
    req_data = request.get_json()
    res = dumps({'response': estimator(req_data)})
    return res


@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
def get_logs():
    f = open('log.txt', 'r')
    contents = f.read()
    f.close()
    return contents


if __name__ == '__main__':
    app.run(debug=True)
