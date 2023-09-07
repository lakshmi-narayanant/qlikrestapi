import requests
import base64
import urllib3
import json
import os
import pandas as pd

# Disable SSL certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Replace with your actual values
host = "desktop-v5khvpp"
username = "DESKTOP-V5KHVPP\SSLTP11375"
password = "Sight"
server_name = 'replocate'
task_name='ats'
withendpoints = True
def login(host, username, password):
    sessionid = []
    # Construct the URL
    login_url = f"https://{host}/attunityenterprisemanager/api/v1/login"
    # Encode the credentials in base64
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    # Construct the headers
    headers = {"Authorization": f"Basic {encoded_credentials}"}
    # Make the GET request
    response = requests.get(login_url, headers=headers, verify=False)
    # Check if the login was successful
    if response.status_code == 200:
        print("Login successful")
        # Extract session ID from response headers
        session_id = response.headers.get("EnterpriseManager.APISessionID")
        return session_id
    else:
        print(f"Login failed with status code: {response.status_code}")
        return None
def get_server_list(host, session_id):
    # Construct the URL for GetServerList
    server_list_url = f"https://{host}/attunityenterprisemanager/api/v1/servers"
    # Construct the headers using the provided session ID
    headers = { "EnterpriseManager.APISessionID": session_id}
    # Make the GET request for GetServerList
    response = requests.get(server_list_url, headers=headers, verify=False)
    # Check if the request was successful
    if response.status_code == 200:
        print("GetServerList request successful")
        server_info = response.json()
        print(server_info['serverList'][0]['name'])  #
        # Prettify the JSON object with an indentation of 4 spaces
        prettified_server_details = json.dumps(server_info, indent=4)
        return prettified_server_details

        return df
    else:
        print(f"GetServerList request failed with status code: {response.status_code}")
        return None
def get_task_list(host, session_id, server_name):
    # Construct the URL for GetTaskList
    task_list_url = f"https://{host}/attunityenterprisemanager/api/v1/servers/{server_name}/tasks"
    # Construct the headers using the provided session ID
    headers = {"EnterpriseManager.APISessionID": session_id}
    # Make the GET request for GetTaskList
    response = requests.get(task_list_url, headers=headers, verify=False)
    # Check if the request was successful
    if response.status_code == 200:
        print("GetTaskList request successful")
        task_info = response.json()
        task_list = response.json()['taskList']
        prettified_task_list = json.dumps(task_list, indent=4)
        return prettified_task_list
    else:
        print(f"GetTaskList request failed with status code: {response.status_code}")
        return None
def get_task_details(host, session_id, server_name, task_name):
    # Construct the URL for GetTaskDetails
    task_details_url = f"https://{host}/attunityenterprisemanager/api/v1/servers/{server_name}/tasks/{task_name}"
    # Construct the headers using the provided session ID
    headers = {"EnterpriseManager.APISessionID": session_id}
    # Make the GET request for GetTaskDetails
    response = requests.get(task_details_url, headers=headers, verify=False)
    # Check if the request was successful
    if response.status_code == 200:
        print("GetTaskDetails request successful")
        task_details = response.json()
        # Prettify the JSON response
        prettified_task_details = json.dumps(task_details, indent=4)
        return prettified_task_details
    else:
        print(f"GetTaskDetails request failed with status code: {response.status_code}")
        return None
def export_task(host, session_id, server_name, task_name, withendpoints):
    # Construct the URL for ExportTask
    export_task_url = f"https://{host}/attunityenterprisemanager/api/v1/servers/{server_name}/tasks/{task_name}?action=export&withendpoints={withendpoints}"
    # Construct the headers using the provided session ID
    headers = {"EnterpriseManager.APISessionID": session_id}
    # Make the GET request for ExportTask
    response = requests.get(export_task_url, headers=headers, verify=False)
    # Check if the request was successful
    if response.status_code == 200:
        print("ExportTask request successful")
        exported_data_bytes=response.content
        exported_data_str = exported_data_bytes.decode('utf-8')
        exported_data_json = json.loads(exported_data_str)
        current_directory = os.getcwd()
        print(current_directory)
        # Specify the file name
        file_name = 'exported_data.json'
        # Construct the full file path
        file_path = os.path.join(current_directory, file_name)
        # Step 3: Save the JSON data to a file
        with open(file_path, 'w') as json_file:
            json.dump(exported_data_json, json_file,indent=4)
        json_file.close()

    else:
        print(f"ExportTask request failed with status code: {response.status_code}")
        return None
# Replace with the actual server name
# Call the login function
session_id = login(host, username, password)
if session_id:
    print("Session ID:", session_id)
    # Call the get_server_list function
    server_list = get_server_list(host, session_id)
    if server_list:
        print("Server List:", server_list)
        # Call the get_task_list function
        task_list = get_task_list(host, session_id, server_name)
        if task_list:
            print("Task List:", task_list)
            # Now you have the task list, you can process it as needed
            task_details = get_task_details(host, session_id, server_name, task_name)
            if task_details:
                print("Task Details:", task_details)
                # Call the export_task function
                exported_data = export_task(host, session_id, server_name, task_name, withendpoints)
                if exported_data:
                    print("Exported Data:", exported_data)
