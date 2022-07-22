#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0

import getpass
from jinja2 import Template
import os
import json
import datetime
import requests
import argparse

#
# Get the repositories for a given GitHub organization
#
def query_github_repositories(gh_org, token):
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
                    'primaryLanguage': i['node']['primaryLanguage']['name'] if (i['node']['primaryLanguage'] != None) else 'not specified',
                    'stargazerCount': i['node']['stargazerCount']})

    has_next_page = results['data']['organization']['repositories']['pageInfo']['hasNextPage']
    after_clause =', after:"{}"'.format(results['data']['organization']['repositories']['pageInfo']['endCursor'])
 
  return repos

#
# Get the pull requests for a given GitHub org and repository
#
def get_pull_requests(gh_org, gh_repo, token):
  q = Template('''
    {
      repository(name: "{{repo}}", owner: "{{org}}") {
        pullRequests(first: 100, orderBy: {field: CREATED_AT, direction: ASC}{{after}}) {
          nodes {
            author {
              login
            }
            createdAt
            updatedAt
            merged
            number
            participants(first: 100) {
              edges {
                node {
                  login
                }
              }
            }
            state
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
    ''')

  has_next_page = True
  after_clause = ''
  pull_requests = []
  while has_next_page:
    j = { 'query' : q.render(org=gh_org, repo=gh_repo, after=after_clause) }
    url = 'https://api.github.com/graphql'
    h = {'Authorization': 'token %s' % token}
    r = requests.post(url, json=j, headers=h)
    r.raise_for_status()
 
    results = r.json()

    for i in results['data']['repository']['pullRequests']['nodes']:
      pr = {
        'number': i['number'],
        'createdAt': i['createdAt'],
        'updatedAt': i['updatedAt'],
        'author': i['author']['login'] if i['author'] else 'unknown',
        'merged': i['merged'],
        'state': i['state'],
        'participants': []}
      for j in i['participants']['edges']:
        pr['participants'].append(j['node']['login'])

      pull_requests.append(pr)

    has_next_page = results['data']['repository']['pullRequests']['pageInfo']['hasNextPage']
    after_clause =', after:"{}"'.format(results['data']['repository']['pullRequests']['pageInfo']['endCursor'])
 
  return pull_requests

#
# Get the releases for a given GitHub org and repository
#
def get_releases(gh_org, gh_repo, token):
  q = Template(''' { repository(name: "{{repo}}", owner: "{{org}}") {
        releases(first: 100, orderBy: {field: CREATED_AT, direction: ASC}{{after}}) {
          pageInfo {
            endCursor
            hasNextPage
          }
          nodes {
            name
            createdAt
            author {
              login
            }
          }
        }
      }
    }
    ''')

  has_next_page = True
  after_clause = ''
  releases = []
  while has_next_page:
    j = { 'query' : q.render(org=gh_org, repo=gh_repo, after=after_clause) }
    url = 'https://api.github.com/graphql'
    h = {'Authorization': 'token %s' % token}
    r = requests.post(url, json=j, headers=h)
    r.raise_for_status()
 
    results = r.json()

    for i in results['data']['repository']['releases']['nodes']:
      releases.append({
        'name': i['name'],
        'createdAt': i['createdAt'],
        'createdBy': i['author']['login'] if i['author'] else 'unknown'})
    has_next_page = results['data']['repository']['releases']['pageInfo']['hasNextPage']
    after_clause =', after:"{}"'.format(results['data']['repository']['releases']['pageInfo']['endCursor'])
 
  return releases

#
# Get the repository information for an organization and dump it to stdout
#
def print_repo_info(org, token):
  repos = query_github_repositories(org, token)

  for r in repos:
    r['pullRequests'] = get_pull_requests(org, r['name'], token)
    r['releases'] = get_releases(org, r['name'], token)

  if not os.path.exists('output_files'):
    os.mkdir('output_files')
  path = os.path.join('output_files', org)
  if not os.path.exists(path):
    os.mkdir(path)
  now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  filename = path + '/repo-info-' + now + '.json'
  with open(filename, 'w') as outfile:
    json.dump(repos, outfile, sort_keys=True, indent=2)


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
