# NOTEWORTHY PRs

The tool will assist in getting the PRs curated for the weekly developer
newsletter sent by Hyperledger. The tool will print list of all PRs from
Hyperledger and Hyperledger Labs into a html file that were raised in
last `X` days. The number of days is configurable, current default is set
to be 7.

Note that the tool expects user to set the GitHub personal access token
with the read access. This is to avoid GitHub from blocking the machine due
to frequent API calls. The tool makes use of
[go-github](https://github.com/google/go-github/) for pulling the data.

## Dependencies

Option GitHub personal access token with read access (this is required
in case of frequent API calls, default rate that GitHub allow is 60).

Set the following environment variable before running the tool

```
export GITHUB_TOKEN=<YOUR LONG PERSONAL ACCESS TOKEN HERE>
```

The tool is written in Go version 1.15, you can also use the docker
container runtime engine to package and run it as a container.
Tool also comes with a `docker-compose` file to make it easy to run
the command with default configuration.

Tested `docker` and `docker-compose` versions

- Docker version 19.03.4
- docker-compose version 1.24.1

## Configuration

The tool can be configured to fetch the PRs from any organization via
the configuration as long as the input `GITHUB_TOKEN` has read access.
Pass the configuration file as below to the tool, find the comments
next to them here

```
# Organizations from where the PRs are to be listed. Each organization
# has to be listed as a list element.
organizations:
  - organization:
      name: "hyperledger"
  - organization:
      name: "hyperledger-labs"
# Number of days since when the PRs are to be queried
days: 7
# File where the output can be saved
filename: "pRs.json"
# File location where the generated fancy html page to be saved
prettyprintfile: "myfile.html"
```

## Environment

The tool accepts following environment variables in addition to
the configuration file.


```
# The html pretty print file path
PRETTY_PRINT_FILE_PATH
# GitHub access token
GITHUB_TOKEN
# Configuration file path
CONFIG_FILE
```

## Run

Prefer to run it as a container, run the following command

```
docker-compose up
```

You may optionally build and run the tool as

```
go build
./noteworthy-prs
```
