# Introduction
This directory contains a Python tool to determine GitHub repositories within an organization (specified with `-o/--org` option) where the HEAD commit occurred prior to the date specified with the `-w/--when` option.  

It utilizes the [GitHub repositories API](https://docs.github.com/en/rest/reference/repos#list-organization-repositories) to get a list of repositories within the organization.
```
GET /orgs/{org}/repos
```

For each repository that is not already archived, it then utilizes the [GitHub commits API](https://docs.github.com/en/rest/reference/commits#get-a-commit) to get the HEAD commit and compare its `commit.committer.date` against the date specified on the command line to see if the HEAD commit occurred prior. All repositories that were created before the date on the command line is then output.
```
GET /repos/{owner}/{repo}/commits/{ref}
```

# Prerequisites
The tool has the following prerequisites:
- Python 3.9.9 or higher

# Running
```
% python main.py -h
usage: main.py [-h] -u USERNAME [-p PASSWORD] -o ORG [-d] -w WHEN

List repositories that have not had a commit in a certain time period.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Github username to use for API calls (required)
  -p PASSWORD, --password PASSWORD
                        Github access token to use for API calls
  -o ORG, --org ORG     GitHub organization (required)
  -d, --details         Include last commit date in output
  -w WHEN, --when WHEN  Include repos with last commit prior to date (required
                        YYYY-mm-dd)
```
