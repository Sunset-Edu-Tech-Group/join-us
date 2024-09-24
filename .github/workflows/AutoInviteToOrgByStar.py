# Max Base & SunsetMkt
# 2021-06-19 & 2024-09
# https://github.com/BaseMax/AutoInviteToOrgByStar

import json
import os

import requests

# print("Hello, World")

if os.getenv("CI"):
    print("Looks like GitHub Actions!")
else:
    print("Maybe running locally?")

# Do not show your secrets in the logs
# print("Environ:")
# print(os.environ)
# print("Prefix:")
# print(sys.prefix)

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ORG_NAME = os.environ["ORG_NAME"]
TEAM_NAME = os.environ["TEAM_NAME"]

# GITHUB_EVENT_PATH: The path to the file on the runner that
# contains the full event webhook payload.
file = open(os.environ["GITHUB_EVENT_PATH"])
data = json.load(file)

# print("Data:")
# print(data)

USERNAME = data["sender"]["login"]

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

print(f"Checking if @{USERNAME} is already in the team ...")


response = requests.get(
    f"https://api.github.com/orgs/{ORG_NAME}/teams/{TEAM_NAME}/memberships/{USERNAME}",
    headers=headers,
)

if response.status_code == 200:
    print(f"User @{USERNAME} is already in the team.")
    exit(0)
elif response.status_code == 404:
    print(f"User @{USERNAME} is not in the team.")
else:
    print(f"Error: {response.status_code} {response.text}")
    exit(1)

print(f"Inviting @{USERNAME} ...")

response = requests.put(
    f"https://api.github.com/orgs/{ORG_NAME}/teams/{TEAM_NAME}/memberships/{USERNAME}",
    headers=headers,
)

if response.status_code == 200:
    print(f"Invitation sent to @{USERNAME}.")
    exit(0)
else:
    print(f"Error: {response.status_code} {response.text}")
    exit(1)
