from flask import Flask, request, jsonify, make_response
import requests
import os
import json
app = Flask(__name__)

# DB_PERSONAL_ACCESS_TOKEN = os.getenv('db_pat')
# HOST_URL = os.getenv('db_url')
# SEARCH_JOB_ID = os.getenv('db_search_job')
# ANALYSIS_JOB_ID = os.getenv('db_analysis_job')

DB_PERSONAL_ACCESS_TOKEN = "dapi4f28951dddcde2d9fed9c564fdd9d2b9"
HOST_URL = "https://7798644223489409.9.gcp.databricks.com/"
SEARCH_JOB_ID = "431843354010410"
ANALYSIS_JOB_ID = "740795541882406"

HEADERS = {
    "Authorization": f"Bearer {DB_PERSONAL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

RUN_OUTPUT_API_ENDPOINT = HOST_URL+"api/2.0/jobs/runs/get-output"
SUBMIT_JOB_RUN_API_ENDPOINT = HOST_URL+"api/2.0/jobs/run-now"
ALL_RUNS_API_ENDPOINT = HOST_URL+"api/2.1/jobs/runs/list"

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Content-Type", "application/json")
    return response

@app.route('/')
def hello_world():
    return 'Basic MMAFC Backend'

@app.route('/get_all_runs', methods = ['GET'])
def get_all_runs_request():
    search_response = requests.request(method='GET', headers=HEADERS, url=ALL_RUNS_API_ENDPOINT, json={"job_id":SEARCH_JOB_ID, "limit":25})
    analysis_response = requests.request(method='GET', headers=HEADERS, url=ALL_RUNS_API_ENDPOINT, json={"job_id":ANALYSIS_JOB_ID, "limit":25})

    search_run_output = {}
    for run in search_response.json().get('runs', []):
        search_run_output[run['run_id']] = {
            'job_id': run['job_id'],
            'username': "Logically.AI",
            'parameters': run.get('overriding_parameters', {}),
            'start_time': run['start_time'],
            'run_id': run['run_id'],
            'state': run['state']
        }

    analysis_run_output = {}
    for run in analysis_response.json().get('runs', []):
        analysis_run_output[run['run_id']] = {
            'job_id': run['job_id'],
            'username': "Logically.AI",
            'parameters': run.get('overriding_parameters', {}),
            'start_time': run['start_time'],
            'run_id': run['run_id'],
            'state': run['state']
        }

    output = {
        'search_runs': search_run_output,
        'analysis_runs': analysis_run_output
    }
    return _corsify_actual_response(jsonify(output))


@app.route('/get_run_output', methods = ['GET'])
def get_run_output_request():
    run_id = request.args['run_id']
    
    data_json = {
        "run_id" : run_id
    }
    
    response = requests.request(method="GET", headers=HEADERS, url=RUN_OUTPUT_API_ENDPOINT, json=data_json)

    json_resp = response.json()
    if 'notebook_output' in json_resp:
        if 'result' in json_resp['notebook_output']:
            nan = ''
            json_resp['notebook_output']['result'] = eval(json_resp['notebook_output']['result'])
    return _corsify_actual_response(jsonify(json_resp))

@app.route('/submit_job_run', methods = ['POST', "OPTIONS"])
def submit_job_run_request():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        req_json = request.json
        if req_json['job_id'] == '740795541882406':
            analysis_response = requests.request(method='GET', headers=HEADERS, url=ALL_RUNS_API_ENDPOINT, json={"job_id":ANALYSIS_JOB_ID, "limit":25})
            for run in analysis_response.json()['runs']:
                if str(run['overriding_parameters']['notebook_params']['search_run_id']) == str(req_json['notebook_input']['search_run_id']):
                    data_json = {
                        'run_id': run['run_id'],
                        'number_in_jobs': run['run_id']
                    }
                    return _corsify_actual_response(jsonify(data_json))
        data_json = {
            "job_id" : req_json['job_id'],
            "notebook_params" : req_json['notebook_input']
        }
        response = requests.request(method="POST", headers=HEADERS, url=SUBMIT_JOB_RUN_API_ENDPOINT, json=data_json)
        return _corsify_actual_response(jsonify(response.json()))