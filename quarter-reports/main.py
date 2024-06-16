#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0

import getpass
from jinja2 import Template
from datetime import datetime
import requests
import os
import argparse


def get_quarter(month):
  """
  Function to get the quarter for the month given.
  """

  result = ''
  match month:
    case '01'|'02'|'03':
      result = 'Q1'
    case '04'|'05'|'06':
      result = 'Q2'
    case '07'|'08'|'09':
      result = 'Q3'
    case '10'|'11'|'12':
        result = 'Q4'

  return result


def api_call_get_activity_data(gh_org, token):
  """
  Function to get the data for the 'Activity during quarter' section according to the date given.
  """

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
                isArchived
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
    repos = repos + results['data']['organization']['repositories']['edges']
    has_next_page = results['data']['organization']['repositories']['pageInfo']['hasNextPage']
    after_clause =', after:"{}"'.format(results['data']['organization']['repositories']['pageInfo']['endCursor'])

  archived_counter = 0
  for i in repos:
    if i['node']['isArchived'] == True:
      archived_counter+=1
  return len(repos), archived_counter, len(repos)-archived_counter


def query_github_repositories(gh_org, token, when):
  """
  Function to get detailed data about the active/archived labs according to the date given.
  """

  print(f"Getting repositories for {gh_org}")
  q = Template('''
    {
      search(type: REPOSITORY,query:"pushed:>{{date}}, org:{{org}}", first: 100)
      {
        pageInfo {
          endCursor
          hasNextPage
        }
        edges {
          node {
            ... on Repository {
              name
              nameWithOwner
              createdAt
              description
              isArchived
              isPrivate
            }
          }
        }
      }
    }
    ''')

  has_next_page = True
  after_clause = ''
  old_repos, new_repos, repos_archived = [],[],[]
  while has_next_page:
    j = { 'query' : q.render(org=gh_org, after=after_clause, date=str(when)[0:10]) }
    url = 'https://api.github.com/graphql'
    h = {'Authorization': 'token %s' % token}
    r = requests.post(url, json=j, headers=h)
    r.raise_for_status()

    results = r.json()

    for i in results['data']['search']['edges']:
      if not i['node']['isArchived'] and not i['node']['isPrivate']:
        if str(i['node']['createdAt'][0:10]) >= str(when)[0:10]:
          name_with_owner = i['node']['nameWithOwner']
          new_repos.append({'name': '[' + i['node']['name'] + '](https://github.com/' + name_with_owner + ')',
                        'last_commit': '![GitHub last commit](https://img.shields.io/github/last-commit/' + name_with_owner + '?display_timestamp=committer&label=%20)',
                        'description': i['node']['description'],
                        'createdAt': i['node']['createdAt'][0:10],
                        'commits': '![GitHub total commit activity](https://img.shields.io/github/commit-activity/t/' + name_with_owner + '?label=%20)',
                        'issues': '![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/' + name_with_owner + '?label=%20)',
                        'PRs': '![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr/' + name_with_owner + '?label=%20)'})
        else:
          name_with_owner = i['node']['nameWithOwner']
          old_repos.append({'name': '[' + i['node']['name'] + '](https://github.com/' + name_with_owner + ')',
                        'last_commit': '![GitHub last commit](https://img.shields.io/github/last-commit/' + name_with_owner + '?display_timestamp=committer&label=%20)',
                        'description': i['node']['description'],
                        'createdAt': i['node']['createdAt'][0:10],
                        'commits': '![GitHub total commit activity](https://img.shields.io/github/commit-activity/t/' + name_with_owner + '?label=%20)',
                        'issues': '![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/' + name_with_owner + '?label=%20)',
                        'PRs': '![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr/' + name_with_owner + '?label=%20)'})
      elif i['node']['isArchived']:
        name_with_owner = i['node']['nameWithOwner']
        repos_archived.append({'name': '[' + i['node']['name'] + '](https://github.com/' + name_with_owner + ')',
                      'last_commit': '![GitHub last commit](https://img.shields.io/github/last-commit/' + name_with_owner + '?display_timestamp=committer&label=%20)',
                      'description': i['node']['description'],
                      'createdAt': i['node']['createdAt'][0:10]})

    has_next_page = results['data']['search']['pageInfo']['hasNextPage']
    after_clause =', after:"{}"'.format(results['data']['search']['pageInfo']['endCursor'])

  return new_repos, old_repos, repos_archived


def generate_md(org, output_file, token, when):
  """
  Function to write on a markdown file all the data retrieved from a specific org by a given date.
  """

  new_repos, old_repos, archived_repos = query_github_repositories(org, token, when)
  year = str(when)[0:4]
  month = str(when)[5:7]
  quarter = get_quarter(month)
  total, archived, active = api_call_get_activity_data(org,token)
  md = Template(f'''# {quarter} {year} Hyperledger Labs Update

## Overall Health

## Activity during the quarter
- Total Labs: {total}
- Total Labs archived: {archived}
- Active Labs: {active}
- Labs archived in {quarter}: {len(archived_repos)}
- Labs proposed: *To Fill*
- Labs proposals accepted: *To Fill*
- Labs proposals in process: *To Fill*
- Labs Proposals Out of Scope/Withdrawn: *To Fill*
- Labs graduated to project: *To Fill*
'''
'''

## Details of the active labs for the quarter

| <div style="width:150px">Lab Name</div> | <div style="width:450px">Description</div> | Created | Last Commit | Commits | Issues | Pull Requests |
| :-------------------------------------: | :----------------------------------------: | :-----: | :---------: | :-----: | :----: | :-----------: |
{% for x in old_repos %}| <div style="width:150px">{{x.name}}</div> | <div style="width:450px">{{x.description}}</div> | {{x.createdAt}} | {{x.last_commit}} | {{x.commits}} | {{x.issues}} | {{x.PRs}} |
{% endfor %}'''

'''


## Details of the new labs for the quarter
| <div style="width:150px">Lab Name</div> | <div style="width:450px">Description</div> | Created | Last Commit | Pull Requests |
| :-------------------------------------: | :----------------------------------------: | :-----: | :---------: | :-----------: |
{% for x in new_repos %}| <div style="width:150px">{{x.name}}</div> |  <div style="width:450px">{{x.description}}</div> | {{x.createdAt}} | {{x.last_commit}} | | {{x.PRs}} |
{% endfor %}'''


'''


## Details of the archived labs for the quarter
| <div style="width:150px">Lab Name</div> | <div style="width:450px">Description</div> | Created | Last Commit |
| :-------------------------------------: | :----------------------------------------: | :-----: | :---------: |
{% for x in archived_repos %}| <div style="width:150px">{{x.name}}</div> |  <div style="width:450px">{{x.description}}</div> | {{x.createdAt}} | {{x.last_commit}} |
{% endfor %}'''
)


  if (output_file is None):
    print("Generating markdown with the information retrieved...")
    path = './output_files'
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = org + '-quarter-report-' + now + '.md'
    if not os.path.exists(path):
      os.mkdir(path)
    output_file = os.path.join(path, filename)

  md.stream(old_repos=old_repos, new_repos=new_repos, org=org, archived_repos=archived_repos).dump(output_file)
  print(f"Markdown {output_file} ready")

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--token",
      help="Github access token to use for API calls",
      required=False)
  parser.add_argument("-o", "--org", help="GitHub organization (default=hyperledger-labs)",
      default="hyperledger-labs")
  parser.add_argument("-d", "--details", help="Include last commit date in output",
      default=False, action='store_true')
  parser.add_argument("-w", "--when", help="Include repos with last commit prior to date (required YYYY-mm-dd)",
      required=True, type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
  parser.add_argument("-f", "--output-file", help="Where to store file",
    required=False, default=None)
  args = parser.parse_args()


  token = args.token

  if not token:
      token = getpass.getpass("Please enter github access token:")

  generate_md(args.org, args.output_file, token, args.when)

if __name__ == "__main__":
    main()
