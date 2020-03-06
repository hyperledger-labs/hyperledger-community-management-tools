# Introduction
This directory contains a Python tool for generating project reports. For each project specified in the configuration file, a HTML file will be generated in the `./html` directory. You can see the format of the output in `templates/report.html`.

It utilizes the [Github statistics API](https://developer.github.com/v3/repos/statistics/) to report on projects and their repositories. Specifically, it uses the "Get contributors list with additions, deletions, and commit counts":
```
GET /repos/:owner/:repo/stats/contributors
```

# Prerequisites
The tool has the following prerequisites:
- Python 2.7.13 or higher

# Running
```
usage: main.py [-h] [--cfg CFG] -u USERNAME -p PASSWORD [-d] [-s]

-h, --help            show this help message and exit
--cfg CFG             Configuration file containing projects and
                      repositories (default=./repos.cfg).
-u USERNAME, --username USERNAME
                      Github username to use for API calls (required)
-p PASSWORD, --password PASSWORD
                      Github access token to use for API calls (required)
-g, --show_ryg        Show the health summary.
-d, --details         Output detailed lists.
-s, --show_contributors
                      Output all contributors.
```

# Configuration File
The tool takes a configuration file of the format:

```
[project-name]
title = Project Title
incubation_date = <Month Day, Year>
active_date = <Month Day, Year>
deprecation_date = <Month Day, Year>
repos = <organization-name>/<repo-name>
        <organization-name>/<repo-name>
        ...
        <organization-name>/<repo-name>
```

It is important that you do not specify https://github.com within the `repos` list. You can specify as many different projects in the configuration file as you wish.

`incubation_date`, `active_date`, and `deprecation_date` are all optional.
