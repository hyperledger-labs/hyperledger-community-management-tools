# Introduction
This directory contains a Python tool to provide a dashboard showing information about GitHub repositories within an organization (specified with `-o/--org` option).  It utilizes the [GitHub GraphQL API](https://docs.github.com/en/graphql) to get a list of repositories within the organization and [Shields.io](https://shields.io/badges) to create badges.

NOTE: You may need to [add the Shields.io GitHub application](https://img.shields.io/github-auth) if you are running into issues with shields not displaying due to GitHub rate limiting.

# Prerequisites
The tool has the following prerequisites:
- Python 3.9.9 or higher
- Python packages specified in the requirements.txt file (`pip install -r requirements.txt)

# Running
```
% python main.py -h
usage: main.py [-h] [-t token] -o ORG

Create a dashboard of information for the repositories within the specified GitHub organization.

Arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Github access token to use for API calls
  -o ORG, --org ORG     GitHub organization (required)
```
