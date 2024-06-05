import requests
import json
import issues_modular
def create_issues(ACCESS_TOKEN,OWNER,REPO,title,body,labels):
    headers = {
    'Authorization': f'token {ACCESS_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/issues'

    # Define the issue data
    issue_data = {
        'title':title,
        'body':body,
        'labels':labels
    }

    # Send the POST request to create the new issue
    response = requests.post(url, headers=headers, data=json.dumps(issue_data))

    # Check the response status code
    if response.status_code == 201:
        print('New issue created successfully!')
        print(response.json())
    else:
        print(f'Error creating issue: {response.status_code}')
        print(response.text)

# Replace these with your GitHub access token and repository information
ACCESS_TOKEN = ''
OWNER = ''
REPO = ''
CODE = ''''''
issues_modular.predict(CODE)



body='The new issue raised is confirmed'
title='Title-1'
labels=['bug', 'high-priority']
create_issues(ACCESS_TOKEN,OWNER,REPO,title,body,labels)