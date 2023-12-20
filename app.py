from flask import Flask, request, jsonify, make_response
import requests
import os
import json
app = Flask(__name__)

DB_PERSONAL_ACCESS_TOKEN = os.getenv('db_pat')
HOST_URL = os.getenv('db_url')
SEARCH_JOB_ID = os.getenv('db_search_job')
ANALYSIS_JOB_ID = os.getenv('db_analysis_job')
OLD_SEARCH_JOB_ID = os.getenv('db_old_search_job')
OLD_ANALYSIS_JOB_ID = os.getenv('db_old_analysis_job')

JOB_ID_SWITCH = {
    OLD_SEARCH_JOB_ID: SEARCH_JOB_ID,
    OLD_ANALYSIS_JOB_ID: ANALYSIS_JOB_ID
}

# DB_PERSONAL_ACCESS_TOKEN = "dapi4f28951dddcde2d9fed9c564fdd9d2b9"
# HOST_URL = "https://7798644223489409.9.gcp.databricks.com/"
# SEARCH_JOB_ID = "431843354010410"
# ANALYSIS_JOB_ID = "740795541882406"


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

def get_params_if_run_on_DB(job_params):
    parameters = {'notebook_params': {}}
    for i in job_params:
        parameters['notebook_params'][i['name']] = i['value']
    return parameters

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
            'parameters': run.get('overriding_parameters', get_params_if_run_on_DB(run.get('job_parameters', []))),
            'start_time': run['start_time'],
            'run_id': run['run_id'],
            'state': run['state']
        }

    analysis_run_output = {}
    for run in analysis_response.json().get('runs', []):
        analysis_run_output[run['run_id']] = {
            'job_id': run['job_id'],
            'username': "Logically.AI",
            'parameters': run.get('overriding_parameters', get_params_if_run_on_DB(run.get('job_parameters', []))),
            'start_time': run['start_time'],
            'run_id': run['run_id'],
            'state': run['state']
        }

    output = {
        'search_runs': search_run_output,
        'analysis_runs': analysis_run_output
    }

    # output_1 = {'job_id': 1065336331418383, 'run_id': 26140641423741, 'creator_user_name': 'dhruv.s@logically.ai', 'number_in_job': 26140641423741, 'original_attempt_run_id': 26140641423741, 'state': {'life_cycle_state': 'TERMINATED', 'result_state': 'SUCCESS', 'state_message': '', 'user_cancelled_or_timedout': False}, 'start_time': 1701407807030, 'setup_duration': 0, 'execution_duration': 0, 'cleanup_duration': 0, 'end_time': 1701410873445, 'run_duration': 3066415, 'trigger': 'ONE_TIME', 'run_name': 'MMAFC Short Video Search DEMO', 'run_page_url': 'https://7798644223489409.9.gcp.databricks.com/?o=7798644223489409#job/1065336331418383/run/26140641423741', 'run_type': 'JOB_RUN', 'format': 'MULTI_TASK', 'job_parameters': [{'name': 'end_date', 'default': '', 'value': '2023-11-25'}, {'name': 'hashtags_tiktok', 'default': '', 'value': '#pallywood,#israhell,#IsraelUnderAttack,#IStandWithIsrael,#IsraelPalestineWar,#Israel_under_attack,#IndiaStandsWithIsrael,#hamasattack,#Gaza_Genocide,#Gazabombing,#gazagenocide,#palestinegenocide,#israelpalestineconflict,#gaza_under_attack,#gazaunderattack,#gazaattack,#freegaza,#hamasterrorists,#palestineunderattack,#israelinewnazism,#israelgazawar,#israelterrorists,#hamasmassacre,#gazahospital,#israelfightsback,#gazacity,#zionistterror,#hamasterrorism,#isrealpalestineconflict,#standwithisrael,#irondome,#gazzeunderattack,#hamasisis,#israelatwar,#palestiniangenocide,#istandwithpalestine,#mossad,#palestinalibre,#StopBombingHospitals,#IsrealiNewNazism,#alaqsaflood,#gazabombing,#israeliwarcrimes,#palestinelivesmatter,#freepalaestine,#idf,#indiastandswithisrael,#hamas_is_isis,#hamaswarcrimes,#commandcenter,#indiawithisrael,#iraniansstandwithisrael,#filistin,#palestinewillbefree,#irgcterrorists,#lfi,#sondakika,#Gazzeoluyor,#almayadeen,#israelundefire,#OperationIronSwords,#isrealvspalastine,#israeliairforce,#falestine,#AlAqsaStorm,#AlAqsaCallsArmies,#israeloccupationofpalestine,#ironbeam,#irondomeisrael,#NoOilForIsrael,#hamas_is_isis,#hamas,#israel,#gaza,#palestine,#israelhamaswar,#israelhamas,#freepalestine,#netanyahu,#therealimage,#israelmusicfestival,#crisisactors AND #palestine,#crisisactors AND #gaza,#crisisactors AND #israel,#crisisactors AND #israelpalestine'}, {'name': 'keywords_tiktok', 'default': '', 'value': 'Alshifa,Rocket R9X,alshifahospital,command center,al shifa hospital,tunnels,hostage,October 7,weapons,hollahoax'}, {'name': 'keywords_yt', 'default': '', 'value': 'israel,pallywood'}, {'name': 'run_id', 'default': '', 'value': '{{job.run_id}}'}, {'name': 'start_date', 'default': '', 'value': '2023-11-23'}, {'name': 'test_flag', 'default': '', 'value': 'False'}, {'name': 'urls_tiktok', 'default': '', 'value': ''}, {'name': 'urls_yt', 'default': '', 'value': ''}, {'name': 'usernames_tiktok', 'default': '', 'value': ''}]}
    # output_2 = {'job_id': 431843354010410, 'run_id': 689720909997032, 'creator_user_name': 'dhruv.s@logically.ai', 'number_in_job': 689720909997032, 'original_attempt_run_id': 689720909997032, 'state': {'life_cycle_state': 'TERMINATED', 'result_state': 'SUCCESS', 'state_message': '', 'user_cancelled_or_timedout': False}, 'overriding_parameters': {'notebook_params': {'hashtags_tiktok': 'russia', 'urls_tiktok': '', 'keywords_tiktok': '', 'usernames_tiktok': '', 'start_date': '2023-11-30', 'end_date': '2023-11-30', 'test_flag': 'True', 'keywords_yt': '', 'urls_yt': ''}}, 'start_time': 1701346859059, 'setup_duration': 0, 'execution_duration': 0, 'cleanup_duration': 0, 'end_time': 1701347354104, 'run_duration': 495045, 'trigger': 'ONE_TIME', 'run_name': 'MMAFC Short Video Search', 'run_page_url': 'https://7798644223489409.9.gcp.databricks.com/?o=7798644223489409#job/431843354010410/run/689720909997032', 'run_type': 'JOB_RUN', 'format': 'MULTI_TASK'}

    # print(output_1['job_parameters']) 
    # print(output_2['overriding_parameters'])

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
                if str(run.get('overriding_parameters', get_params_if_run_on_DB(run.get('job_parameters', [])))['notebook_params']['search_run_id']) == str(req_json['notebook_input']['search_run_id']):
                    data_json = {
                        'run_id': run['run_id'],
                        'number_in_jobs': run['run_id']
                    }
                    return _corsify_actual_response(jsonify(data_json))
        data_json = {
            "job_id" : JOB_ID_SWITCH[req_json['job_id']],
            "notebook_params" : req_json['notebook_input']
        }
        response = requests.request(method="POST", headers=HEADERS, url=SUBMIT_JOB_RUN_API_ENDPOINT, json=data_json)
        return _corsify_actual_response(jsonify(response.json()))