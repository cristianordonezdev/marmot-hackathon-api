import requests
 
GITHUB_TOKEN = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIA0d3hIAW5GETRHmU8R1zGHvPBcPRyKwnPtjc1vRUNZM cts\2385305@DESKTOP-V3M201I'

REPO_OWNER = 'DianaErikaArceo'

REPO_NAME = 'Citas'

HEAD_BRANCH = 'feature_branch'

BASE_BRANCH = 'Citas'

PR_TITLE = 'Diana first Pull Request'

PR_BODY = 'Description of the Diana pull request.'
 
url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls'
 
# Headers for the request

headers = {

    'Authorization': f'token {GITHUB_TOKEN}',

    'Accept': 'application/vnd.github.v3+json'

}
 
# Data for the pull request

data = {

    'title': PR_TITLE,

    'head': HEAD_BRANCH,

    'base': BASE_BRANCH,

    'body': PR_BODY

}
 
from requests.exceptions import HTTPError, ConnectionError
 
try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print(response.json())
except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except Exception as err:
    print(f"An error occurred: {err}")
 