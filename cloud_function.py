import functions_framework
import issues_brain
from github import Auth, Github
import requests
import json
from github.GithubException import GithubException



brain = issues_brain.create_brain()

@functions_framework.http
def generate_issue(request):
    
    request_json = request.get_json(silent=True)
    access_key = request_json["GIT_KEY"]
    repo = request_json["repo"]
    selected_file = request_json["selected_file"]
    contents = get_contents(GIT_KEY=GIT_KEY, repo=repo, selected_file=selected_file)
    op = split_output(brain.predict_and_parse(contents))
    if len(op)>3:
      title, description, labels, body = op
      response = send_issue(GIT_KEY=GIT_KEY, repo=repo, title=title, description=description, labels=labels, body=body)
    else:
      title, description, lables=op
      response = send_issue(GIT_KEY=GIT_KEY, repo=repo, title=title, description=description, labels=labels)
    
    

    return response

def get_contents(GIT_KEY, repo, selected_file):
  auth = Auth.Token(GIT_KEY)
  g = Github(auth=auth)
  repo = g.get_repo(repo_id)
  contents = repo.get_contents(selected_file).decoded_content.decode("utf-8")
  return contents

def split_output(contents):
  title = ""
  description = ""
  labels=[]
  segments = contents.split("\n")
  seg = [i for i in seg if i.strip()]
  
  for i in seg:
      if i.startswith(' Ti') or i.startswith('Ti'):
          title=i.split(': ', 1)[1]
          seg.remove(i)
      elif i.startswith('De'):
          description = i.split(': ', 1)[1]
          seg.remove(i)
      elif i.startswith('La'):
          labels = i.split(': ')[1].split(', ') 
          seg.remove(i)
  if len(seg)>0:
    return (title, description, labels, seg)
  else:
    return (title, description, labels)


def send_issue(GIT_KEY, repo, title, description, labels, body=""):
  owner = repo.split("/")[0]
  repo_id = repo.split("/")[1]

  headers = {
    'Authorization': f'token {GIT_KEY}',
    'Accept': 'application/vnd.github.v3+json'
    }
  url = f'https://api.github.com/repos/{owner}/{repo_id}/issues'
  issue_data = {
        'title':title,
        'body':description + body,
        'labels':labels
    }
  
  response = requests.post(url, headers=headers, data=json.dumps(issue_data))
  if response.status_code == 201:
        print('New issue created successfully!')
        return response.json()
  else:
        print(f'Error creating issue: {response.status_code}')
        return response.status_code
  



