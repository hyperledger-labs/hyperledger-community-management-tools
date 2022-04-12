#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0

import time
import getpass
from jinja2 import Template
import dateutil.parser
from datetime import datetime, timezone
import requests
import argparse


def get_api_results(url, username, password, paginate=False):
    print("Processing URL: %s" % url)
    while True:
        r = requests.get(url, auth=(username, password))

        # This API sometimes returns a 202, so we want to make sure that we get the
        # results before moving on
        if r.status_code == 202:
            time.sleep(1)
            continue

        r.raise_for_status()
        break

    results = r.json()

    if paginate and 'next' in r.links.keys():
      results.extend(get_api_results(r.links['next']['url'], username, password, paginate)) 

    return results


def get_non_archived_repositories_for_org(gh_org, username, password):
    t = Template("https://api.github.com/orgs/{{org}}/repos?per_page=100&page=1")
    url = t.render(org=gh_org)
    results = get_api_results(url, username, password, paginate=True)

    repositories = sorted(set(map(lambda y: y['full_name'], (list(filter(lambda x:x['archived'] == False, results))))))

    return repositories


def get_last_commit_date(gh_repo, username, password):
    t = Template("https://api.github.com/repos/{{repo}}/commits/HEAD")
    url = t.render(repo=gh_repo)
    results = get_api_results(url, username, password)

    return results['commit']['committer']['date']

def list_old_repositories(org, username, password, when, details):
    repos = get_non_archived_repositories_for_org(org, username, password)

    old_repos = []

    for r in repos:
        last_commit_date = dateutil.parser.isoparse(get_last_commit_date(r, username, password))
        if last_commit_date <= when.replace(tzinfo=timezone.utc):
            if details:
                old_repos.append("{},{}".format(last_commit_date, r))
            else:
                old_repos.append(r)

    print("Repos where HEAD commit occurred prior to {}".format(when))
    for r in old_repos:
        print(r)

def main():
    parser = argparse.ArgumentParser(description="List repositories that have not had a commit in a certain time period.")
    parser.add_argument("-u", "--username",
        help="Github username to use for API calls (required)",
        required=True)
    parser.add_argument("-p", "--password",
        help="Github access token to use for API calls",
        required=False)
    parser.add_argument("-o", "--org", help="GitHub organization (required)",
        required=True)
    parser.add_argument("-d", "--details", help="Include last commit date in output",
        default=False, action='store_true')
    parser.add_argument("-w", "--when", help="Include repos with last commit prior to date (required YYYY-mm-dd)",
        required=True, type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    args = parser.parse_args()

    username = args.username
    password = args.password

    if not password:
        password = getpass.getpass("Please enter github access token:")

    list_old_repositories(args.org, username, password, args.when, args.details)


if __name__ == "__main__":
    main()
