# How to run the search and analysis jobs using RESTful requests?

### Generating your own Databricks Personal Access Token

Please follow the following steps to generate your Databricks Personal Access Token, and please save it somewhere as there is no way to view the token again later.
1. Log on to Logically's Databricks instance.
2. Go to User Settings for your account (check the top right of the website after logging in, click on the account name -> User Settings in the dropdown).
3. Navigate to Developer -> Access Tokens (manage).
4. Generate your own token and save somewhere.

### Information for all REST API requests

- API endpoint for submitting job runs `URL_SUBMIT_JOB_RUN = "https://mmafc-backend.onrender.com/submit_job_run"`
- API endpoint for fetching run output `URL_FETCH_RUN_OUTPUT = "https://mmafc-backend.onrender.com/get_run_output"`

### Submit search job run request

`SEARCH_JOB_ID = 431843354010410`

To submit a search job using user input, make a POST request at the `URL_SUBMIT_JOB_RUN` endpoint, with the following JSON data.
```
JSON_DATA = {
    "job_id" : str(SEARCH_JOB_ID),
    "notebook_params" : {
        "hashtags_tiktok": <comma separated values>,
        "keywords_tiktok": <comma separated values>,
        "usernames_tiktok": <comma separated values>,
        "urls_tiktok": <comma separated values where each url must be in the form of tiktok.com/@<username>/video/<video_id> >,
        "keywords_yt": <comma separated values>,
        "urls_yt": <comma separated values where each url must be in the form of youtube.com/shorts/<video_id> >,
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "test_flag": "True"
    }
}
```
Please keep the test flag to true while we're testing.

The response returned is as follows:
```
JSON_RESPONSE = {
  "run_id": ...,
  "number_in_job": ...
}
```
The SEARCH_RUN_ID (run_id) must be stored somewhere to fetch search job output, and to submit the search results to the video analysis job.

### Fetch search job run output

To fetch results for the search job, make a GET request at the `URL_FETCH_RUN_OUTPUT` endpoint, with the following params:
`run_id = <SEARCH_RUN_ID>`

Thus, the URL essentially becomes -> `https://mmafc-backend.onrender.com/get_run_output?run_id=<SEARCH_RUN_ID>`.


The response returned is as follows (when the search job has completed ):
```
JSON_RESPONSE = {
  'metadata': {
    'job_id': SEARCH_JOB_ID,
    'run_id': SEARCH_RUN_ID, 
    'creator_user_name': <account authenticated with the personal access token>,
    'number_in_job': ...,
    'original_attempt_run_id': ...,
    'state': {
      'life_cycle_state': 'TERMINATED',
      'result_state': 'SUCCESS',
      'state_message': '',
      'user_cancelled_or_timedout': False
      },
    'task': {...},
    ...
  },
  'notebook_output': {
    'result': {
      'index': {key:value pairs in the form of ROW_NUMBER: <index in dataframe>},
      'search_type': {key:value pairs in the form of ROW_NUMBER: <search type of the result, may be hashtags, usernames, urls or keywords>},
      'search_input': {key:value pairs in the form of ROW_NUMBER: <search input/word of the result>},
      'video_link': {key:value pairs in the form of ROW_NUMBER: <link of the video in the form of https://www.tiktok.com/@<username>/video/<video_id>},
      'username': {key:value pairs in the form of ROW_NUMBER: <username of the account that posted the video>},
      'description': {key:value pairs in the form of ROW_NUMBER: <description of the video as written by the user>},
      'views': {key:value pairs in the form of ROW_NUMBER: <number of views on the video>},
      'likes': {key:value pairs in the form of ROW_NUMBER: <number of likes on the video>},
      'shares': {key:value pairs in the form of ROW_NUMBER: <number of shares on the video>},
      'comments': {key:value pairs in the form of ROW_NUMBER: <number of comments on the video>},
      'creation_time': {key:value pairs in the form of ROW_NUMBER: <creation time of the video>}
    },
    'truncated': ...
  }
}
```
In case the search job is still running, the response returned is as follows:
```
JSON_RESPONSE = {
  'metadata': {
    'job_id': SEARCH_JOB_ID, 
    'run_id': SEARCH_RUN_ID,
    'creator_user_name': <account authenticated with the personal access token>,
    'number_in_job': ...,
    'original_attempt_run_id': ..., 
    'state': {
      'life_cycle_state': 'RUNNING',
      'state_message': 'In run',
      'user_cancelled_or_timedout': False
      }, 
    'task': {...},
    ...
  },
  'notebook_output': {}
}
```
The `"notebook_output"` will contain all the search results based on the given parameters.

### Submit video analysis job run request

`ANALYSIS_JOB_ID = 740795541882406`

To submit a analysis job based on a search run, make a POST request at the `URL_SUBMIT_JOB_RUN` endpoint, with the following JSON data.
```
JSON_DATA = {
    "job_id" : str(ANALYSIS_JOB_ID),
    "notebook_params" : {
        "search_run_id" : str(SEARCH_RUN_ID),
        "test_flag" : "True"
    }
}
```
Please keep the test flag to true while we're testing.

The response returned is as follows:
```
JSON_RESPONSE = {
  "run_id": ...,
  "number_in_job": ...
}
```
The ANALYSIS_RUN_ID (run_id) must be stored somewhere to fetch analysis job output.

### Fetch analysis job run output

To fetch results for the analysis job, make a GET request at the `URL_FETCH_RUN_OUTPUT` endpoint, with the following params:
`run_id = <ANALYSIS_RUN_ID>`

Thus, the URL essentially becomes -> `https://mmafc-backend.onrender.com/get_run_output?run_id=<ANALYSIS_RUN_ID>`.

The response returned is as follows (when the analysis job has completed ):
```
JSON_RESPONSE = {
  'metadata': {
    'job_id': ANALYSIS_JOB_ID,
    'run_id': ANALYSIS_RUN_ID, 
    'creator_user_name': <account authenticated with the personal access token>,
    'number_in_job': ...,
    'original_attempt_run_id': ...,
    'state': {
      'life_cycle_state': 'TERMINATED',
      'result_state': 'SUCCESS',
      'state_message': '',
      'user_cancelled_or_timedout': False
      },
    'task': {...},
    ...
  },
  'notebook_output': {
    'result': {
      'index': {key:value pairs in the form of ROW_NUMBER: <index in dataframe>},
      'search_type': {key:value pairs in the form of ROW_NUMBER: <search type of the result, may be hashtags, usernames, urls or keywords>},
      'search_input': {key:value pairs in the form of ROW_NUMBER: <search input/word of the result>},
      'video_link': {key:value pairs in the form of ROW_NUMBER: <link of the video in the form of https://www.tiktok.com/@<username>/video/<video_id>},
      'username': {key:value pairs in the form of ROW_NUMBER: <username of the account that posted the video>},
      'description': {key:value pairs in the form of ROW_NUMBER: <description of the video as written by the user>},
      'views': {key:value pairs in the form of ROW_NUMBER: <number of views on the video>},
      'likes': {key:value pairs in the form of ROW_NUMBER: <number of likes on the video>},
      'shares': {key:value pairs in the form of ROW_NUMBER: <number of shares on the video>},
      'comments': {key:value pairs in the form of ROW_NUMBER: <number of comments on the video>},
      'creation_time': {key:value pairs in the form of ROW_NUMBER: <creation time of the video>},
      'transcript': {key:value pairs in the form of ROW_NUMBER: <transcript of the audio>},
      'extracted_fcw_claims': {key:value pairs in the form of ROW_NUMBER: <list of FCW claims>},
      'fcw_scores': {key:value pairs in the form of ROW_NUMBER: <list of scores corresponding to FCW claims>},
      'average_fcw_score': {key:value pairs in the form of ROW_NUMBER: <average FCW score from the list in 'fcw_scores'>},
      'maximum_fcw_score': {key:value pairs in the form of ROW_NUMBER: <maximum FCW score from the list in 'fcw_scores'>},
      'sum_fcw_score': {key:value pairs in the form of ROW_NUMBER: <sum of FCW scores from the list in 'fcw_scores'>}
    },
    'truncated': ...
  }
}
```
In case the analysis job is still running, the response returned is as follows:
```
JSON_RESPONSE = {
  'metadata': {
    'job_id': ANALYSIS_JOB_ID, 
    'run_id': ANALYSIS_RUN_ID,
    'creator_user_name': <account authenticated with the personal access token>,
    'number_in_job': ...,
    'original_attempt_run_id': ..., 
    'state': {
      'life_cycle_state': 'RUNNING',
      'state_message': 'In run',
      'user_cancelled_or_timedout': False
      }, 
    'task': {...},
    ...
  },
  'notebook_output': {}
}
```
The `"notebook_output"` will contain all the analysis results.
