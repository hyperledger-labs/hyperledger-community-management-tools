# Introduction
This directory contains a Python tool to provide information about GitHub repositories within an organization (specified with `-o/--org` option).  It utilizes the [GitHub GraphQL API](https://docs.github.com/en/graphql) to get a list of repositories within the organization.

# Prerequisites
The tool has the following prerequisites:
- Python 3.9.9 or higher

# Running
```
% python main.py -h
usage: main.py [-h] [-t token] -o ORG

List details about repositories within the specified organization.

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Github access token to use for API calls
  -o ORG, --org ORG     GitHub organization (required)
```
