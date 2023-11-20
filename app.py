from flask import Flask, request
import requests
import os
app = Flask(__name__)

DB_PERSONAL_ACCESS_TOKEN = os.getenv('db_pat')
HOST_URL = os.getenv('db_url')

HEADERS = {
    "Authorization": f"Bearer {DB_PERSONAL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

RUN_OUTPUT_API_ENDPOINT = HOST_URL+"api/2.0/jobs/runs/get-output"
SUBMIT_JOB_RUN_API_ENDPOINT = HOST_URL+"api/2.0/jobs/run-now"

@app.route('/get_run_output', methods = ['GET'])
def get_run_output_request():
    run_id = request.args['run_id']
    
    data_json = {
        "run_id" : run_id
    }
    
    response = requests.request(method="GET", headers=HEADERS, url=RUN_OUTPUT_API_ENDPOINT, json=data_json)
    return response.json()

@app.route('/submit_job_run', methods = ['POST'])
def submit_job_run_request():
    req_json = request.json
    data_json = {
        "job_id" : req_json['job_id'],
        "notebook_params" : req_json['notebook_input']
    }
    response = requests.request(method="POST", headers=HEADERS, url=SUBMIT_JOB_RUN_API_ENDPOINT, json=data_json)

    return response.json()

@app.route('/')
def hello_world():
    return 'Basic MMAFC Backend'