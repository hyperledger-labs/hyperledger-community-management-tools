# Introduction
This directory contains a Python tool to determine GitHub repositories within an organization (specified with `-o/--org` option) where the HEAD commit occurred prior to the date specified with the `-w/--when` option.  

It utilizes the [GitHub GraphQL API](https://docs.github.com/en/graphql) to get a list of repositories within the organization. It then lists non-archived repos where the last commit was prior to the date specified with the `-w/--when` option.

# Prerequisites
The tool has the following prerequisites:
- Python 3.9.9 or higher

# Running
```
% python main.py -h
usage: main.py [-h] [-t token] -o ORG [-d] -w WHEN

List repositories that have not had a commit in a certain time period.

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Github access token to use for API calls
  -o ORG, --org ORG     GitHub organization (required)
  -d, --details         Include last commit date in output
  -w WHEN, --when WHEN  Include repos with last commit prior to date (required
                        YYYY-mm-dd)
```
