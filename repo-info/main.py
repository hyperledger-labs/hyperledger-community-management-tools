#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0

import getpass
from jinja2 import Template
import json
import requests
import argparse

def query_github_repositories(gh_org, token):
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
                createdAt
                description
                isArchived
                primaryLanguage {
                  name
                }
                stargazerCount
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
                    'createdAt':i['node']['createdAt'],
                    'description': i['node']['description'],
                    'isArchived':i['node']['isArchived'],
                    'primaryLanguage': i['node']['primaryLanguage']['name'] if (i['node']['primaryLanguage'] != None) else 'not specified',
                    'stargazerCount': i['node']['stargazerCount']})

    has_next_page = results['data']['organization']['repositories']['pageInfo']['hasNextPage']
    after_clause =', after:"{}"'.format(results['data']['organization']['repositories']['pageInfo']['endCursor'])
 
  return repos


def print_repo_info(org, token):
  repos = query_github_repositories(org, token)

  print(json.dumps(repos, indent=2))

def main():
  parser = argparse.ArgumentParser(description="Provide information about GitHub repositories within an organization")
  parser.add_argument("-t", "--token",
      help="Github access token to use for API calls",
      required=False)
  parser.add_argument("-o", "--org", help="GitHub organization (required)",
      required=True)
  args = parser.parse_args()

  token = args.token

  if not token:
      token = getpass.getpass("Please enter github access token:")

  print_repo_info(args.org, token)


if __name__ == "__main__":
    main()
