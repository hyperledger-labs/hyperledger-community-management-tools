#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0

import getpass
from jinja2 import Template
import os
import datetime
import requests
import argparse

#
# Get the repositories for a given GitHub organization
#
def query_github_repositories(gh_org, token):
  print("Getting repositories for {}".format(gh_org))
  q = Template('''
    {
      organization(login: "{{org}}") {
        repositories(first: 100, orderBy: {field: NAME, direction: ASC}{{after}}) {
          pageInfo {
            endCursor
            hasNextPage
          }
          edges {
            node {
              ... on Repository {
                name
                nameWithOwner
                isArchived
                isPrivate
              }
            }
          }
        }
      }
    }
    ''')

  has_next_page = True
  after_clause = ''
  repos = []
  while has_next_page:
    j = { 'query' : q.render(org=gh_org, after=after_clause) }
    url = 'https://api.github.com/graphql'
    h = {'Authorization': 'token %s' % token}
    r = requests.post(url, json=j, headers=h)
    r.raise_for_status()
 
    results = r.json()

    for i in results['data']['organization']['repositories']['edges']:
      if not i['node']['isArchived'] and not i['node']['isPrivate']:
        name_with_owner = i['node']['nameWithOwner'] 
        repos.append({'name': '[' + i['node']['name'] + '](https://github.com/' + name_with_owner + ')',
                      'license': '![GitHub License](https://img.shields.io/github/license/' + name_with_owner + '?label=%20)',
                      'last_commit': '![GitHub last commit](https://img.shields.io/github/last-commit/' + name_with_owner + '?display_timestamp=committer&label=%20)',
                      'commits': '![GitHub total commit activity](https://img.shields.io/github/commit-activity/t/' + name_with_owner + '?label=%20)',
                      'issues': '![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/' + name_with_owner + '?label=%20)',
                      'PRs': '![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr/' + name_with_owner + '?label=%20)',
                      'score': '![OSSF-Scorecard Score](https://img.shields.io/ossf-scorecard/github.com/' + name_with_owner + '?label=%20)',
                      'stars': '![GitHub Repo stars](https://img.shields.io/github/stars/' + name_with_owner + '?label=%20)',
                      'forks': '![GitHub forks](https://img.shields.io/github/forks/' + name_with_owner + '?label=%20)',
                      'watchers': '![GitHub watchers](https://img.shields.io/github/watchers/' + name_with_owner + '?label=%20)'})

    has_next_page = results['data']['organization']['repositories']['pageInfo']['hasNextPage']
    after_clause =', after:"{}"'.format(results['data']['organization']['repositories']['pageInfo']['endCursor'])
 
  return repos

#
# Get the repository information for an organization and dump it to stdout
#
def dashboard(org, output_file, token):
  repos = query_github_repositories(org, token)

  md = Template('''# {{org}} Dashboard

| Repo | License | Last Commit | Commits | Issues | Pull Requests | OpenSSF Scorecard | Stars | Forks | Watchers |
| :--: | :-----: | :---------: | :-----: | :----: | :-----------: | :---------------: | :---: | :---: | :------: |
{% for r in repos %}| {{r.name}} | {{r.license}} | {{r.last_commit}} | {{r.commits}} | {{r.issues}} | {{r.PRs}} | {{r.score}} | {{r.stars}} | {{r.forks}} | {{r.watchers}} |
{% endfor %}'''
  )

  if (output_file is None):
    path = './output_files'
    if not os.path.exists(path):
      os.mkdir(path)
    now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = org + '-org-dashboard-' + now + '.md'
    output_file = os.path.join(path, filename)

  md.stream(repos=repos, org=org).dump(output_file)


def main():
  parser = argparse.ArgumentParser(description="Provide information about GitHub repositories within an organization")
  parser.add_argument("-t", "--token",
    help="Github access token to use for API calls",
    required=False)
  parser.add_argument("-o", "--org", help="GitHub organization (required)",
    required=True)
  parser.add_argument("-f", "--output-file", help="Where to store file",
    required=False, default=None)
  args = parser.parse_args()

  token = args.token

  if not token:
    token = getpass.getpass("Please enter github access token:")

  dashboard(args.org, args.output_file, token)


if __name__ == "__main__":
  main()
