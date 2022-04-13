#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0

import getpass
from jinja2 import Template
import dateutil.parser
from datetime import datetime, timezone
import requests
import argparse

def query_github(gh_org, token):
  q = Template('''
    {
      organization(login: "{{org}}") {
        repositories(first: 100, orderBy: {field: NAME, direction: ASC}{{after}}) {
          totalCount
          pageInfo {
            endCursor
            hasNextPage
          }
          edges {
            node {
              ... on Repository {
                name
                isArchived
                defaultBranchRef {
                  target {
                    ... on Commit {
                      committedDate
                    }
                  }
                }
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
      repos.append({'name':i['node']['name'],
                    'isArchived':i['node']['isArchived'],
                    'committedDate':i['node']['defaultBranchRef']['target']['committedDate']})

    has_next_page = results['data']['organization']['repositories']['pageInfo']['hasNextPage']
    after_clause =', after:"{}"'.format(results['data']['organization']['repositories']['pageInfo']['endCursor'])
 
  return repos


def list_old_repositories(org, token, when, details):
  repos = query_github(org, token)

  print("Repos where HEAD commit occurred prior to {}".format(when))
  for r in repos:
    if not r['isArchived']:
      last_commit_date = dateutil.parser.isoparse(r['committedDate'])
      if last_commit_date <= when.replace(tzinfo=timezone.utc):
          if details:
              print("{},{}".format(last_commit_date, r['name']))
          else:
              print(r['name'])


def main():
  parser = argparse.ArgumentParser(description="List repositories that have not had a commit in a certain time period.")
  parser.add_argument("-t", "--token",
      help="Github access token to use for API calls",
      required=False)
  parser.add_argument("-o", "--org", help="GitHub organization (required)",
      required=True)
  parser.add_argument("-d", "--details", help="Include last commit date in output",
      default=False, action='store_true')
  parser.add_argument("-w", "--when", help="Include repos with last commit prior to date (required YYYY-mm-dd)",
      required=True, type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
  args = parser.parse_args()

  token = args.token

  if not token:
      token = getpass.getpass("Please enter github access token:")

  list_old_repositories(args.org, token, args.when, args.details)


if __name__ == "__main__":
    main()
