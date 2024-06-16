# Quarterly Reports Generator

This tool generates a markdown containing all the information needed for the past X months about the projects which are part of the labs.

**IMPORTANT!**
The output might look incomplete, as some sections must be filled with the personal opinion of the quarter according to the evaluation of the steward.

## Running
```
% python main.py -h
usage: main.py [-h] [-t token] -o ORG [-d] -w WHEN

List repositories that have not had a commit in a certain time period.

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Github access token to use for API calls
  -o ORG, --org ORG     GitHub organization (default=hyperledger-labs)
  -d, --details         Include last commit date in output
  -w WHEN, --when WHEN  Include repos with last commit prior to date (required
                        YYYY-mm-dd)
```

