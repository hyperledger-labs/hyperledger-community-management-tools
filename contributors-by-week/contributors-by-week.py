import requests
import sys
import datetime

repo_contributors = dict()
repo_contributions = dict()
repo_contributions_last_year = dict()
unique_contributors = dict()
total_contributions = 0

# week_id: total_commits
weekly_contributions = dict()

if len(sys.argv) < 2:
   token=raw_input("GitHub Authentication Token: ")
else:
   token=sys.argv[1]
   
# Can be collected through GitHub API but it is easier this way
repos = [
'hyperledger/indy-node',
'hyperledger/indy-sdk',
'hyperledger/indy-plenum',
'hyperledger/indy-hipe',
'hyperledger/indy-crypto',
'hyperledger/indy-anoncreds',
'hyperledger/indy-agent',
'hyperledger/indy-post-install-automation',
'hyperledger/indy-jenkins-pipeline-lib',
'hyperledger/indy-test-automation',
'hyperledger/ursa',
'hyperledger/ursa-rfcs',
'bcgov/von',
'bcgov/von-network',
'bcgov/TheOrgBook',
'bcgov/von-bc-registries-agent',
'bcgov/von-personal-agent',
'bcgov/permitify',
'bcgov/von-connector',
'bcgov/von-ledger-explorer',
'sovrin-foundation/Responsible-Disclosure-Deep-Learning-Fingerprinting-Attack',
'sovrin-foundation/libsovtoken',
'sovrin-foundation/cloudconfigs', 
'sovrin-foundation/saltstack',
'sovrin-foundation/steward-tools',
'sovrin-foundation/token-plugin',
#'sovrin-foundation/sov-docs-conf',
'sovrin-foundation/ledger-monitoring-server',
'sovrin-foundation/jenkins-shared',
'sovrin-foundation/sovrin',
'sovrin-foundation/community-tools',
'sovrin-foundation/aws-codebuild-pipeline-plugin',
'sovrin-foundation/sovrin-packaging',
'sovrin-foundation/connector-app',
'sovrin-foundation/vc-data-model',
'sovrin-foundation/sovrin-sip',
'sovrin-foundation/sovrin-test-automation',
'sovrin-foundation/sshuttle-helper',
'sovrin-foundation/protocol',
'sovrin-foundation/agent-sdk',
'sovrin-foundation/sovrin_bot',
'sovrin-foundation/sovrin-connector-preview',
'sovrin-foundation/pipeline-test',
'sovrin-foundation/ssi-protocol',
'sovrin-foundation/sovrin.org',
'sovrin-foundation/launch',
'sovrin-foundation/old-sovrin',
'sovrin-foundation/sovrin-agent',
'sovrin-foundation/sovrin-client-c',
'sovrin-foundation/rust-curvecp-poc'
#'sovrin-foundation/sovrin-sample-app'
]

username='' #I don't know why the auth requires a username, as it doesn't appear to use it... 

for repo in repos:
    print('Working on {}'.format(repo))

    repo_contributions_last_year[repo] = 0
    repo_contributors[repo] = 0
    repo_contributions[repo] = 0

    # STATS
    stats_url = 'https://api.github.com/repos/{}/stats/commit_activity'.format(repo)

    username=""
    stats_resp = requests.get(url=stats_url, auth=(username,token))

    if not stats_resp.ok:
        print('Rate limit probably reached')
        sys.exit(123)

    stats = stats_resp.json()

    for week in stats:
        repo_contributions_last_year[repo] += week['total']
        week_id = week['week']
        if weekly_contributions.get(week_id):
            weekly_contributions[week_id][0] += week['total']
        else:
            weekly_contributions[week_id] = [week['total'], 0]

    # CONTRIBUTIONS
    contrib_url = 'https://api.github.com/repos/{}/contributors'.format(repo)

    head_resp = requests.head(url=contrib_url, auth=(username,token))

    if not head_resp.ok:
        print('Rate Limit probably reached')
        sys.exit(123)

    link_header = head_resp.headers.get('link')
    if link_header:
        last_page = link_header.split(';')[1][-2:-1]
    else:
        last_page = 1

    for x in range(1, int(last_page)+1):
        params = {'page': x}
        contributors_resp = requests.get(url=contrib_url, params=params, auth=(username,token))
        contributors = contributors_resp.json()

        for contributor in contributors:
            repo_contributors[repo] += 1
            if contributor['login'] not in unique_contributors:
                unique_contributors[contributor['login']] = 0
            total_contributions += contributor['contributions']
            repo_contributions[repo] += contributor['contributions']

    # CONTRIBUTORS
    contrib_stats_url = 'https://api.github.com/repos/{}/stats/contributors'.format(repo)

    contrib_stats_resp = requests.get(url=contrib_stats_url, auth=(username,token))

    if not contrib_stats_resp.ok:
        print('Rate limit probably reached')
        sys.exit(123)

    contrib_stats = contrib_stats_resp.json()
#    print(contrib_stats)
#    for x in contrib_stats:
#        for y in range(0,6):
#            print(x['weeks'][y]['w'])
    #found=false
    for contributor in contrib_stats:
        for contributor_week in sorted(contributor['weeks']):
            #print(contributor_week['w']) 
            for week in sorted(weekly_contributions.keys()):
                if week == contributor_week ['w']:
                    if contributor_week['a']!=0 or contributor_week['d']!=0 or contributor_week['c']!=0:
                        #print(contributor_week['w'])
                        #found=true
                        if unique_contributors[contributor['author']['login']] < week:
                            if unique_contributors[contributor['author']['login']] > 0: 
                                weekly_contributions[unique_contributors[contributor['author']['login']]][1] -= 1  
                                #print("gothere {}".format(weekly_contributions[unique_contributors[contributor['author']['login']]][1]))
                            unique_contributors[contributor['author']['login']] = week
                            weekly_contributions[week][1] += 1
    #print(weekly_contributions)
#    exit(0)
#    for author in stats:
#        repo_contributions_last_year[repo] += week['total']
#        week_id = week['week']
#        if weekly_contributions.get(week_id):
#            weekly_contributions[week_id] += week['total']
#        else:
#            weekly_contributions[week_id] = week['total']


    # Report
print('#############################################################################################')

print('Contributors per repo:')
for repo in repo_contributors:
    print('\tRepo: {}, contributors: {}'.format(repo, repo_contributors[repo]))

print('#############################################################################################')

print('Contributions per repo:')
for repo in repo_contributions:
    print('\tRepo: {}, contributions: {}'.format(repo, repo_contributions[repo]))

print('#############################################################################################')

print('Number of Unique Contributors is: {}'.format(len(unique_contributors.keys())))
print('Unique contributors are: ')
for uc in unique_contributors:
    print('\tUsername: {}'.format(uc))

print('#############################################################################################')

print("Number of Total Commits is: {}".format(total_contributions))

print('#############################################################################################')

print('Contributions per repo in Last Year')
for repo in repo_contributions_last_year:
    print('\tRepo: {}, contributions: {}'.format(repo, repo_contributions_last_year[repo]))

print('#############################################################################################')

print('Weekly contributions | contributors added:')
for week in sorted(weekly_contributions.keys()):
    if weekly_contributions[week][0] != 0:
        print("\t{} | {} | {}".format(datetime.datetime.fromtimestamp(week).strftime('%Y-%m-%d'), weekly_contributions[week][0], weekly_contributions[week][1]))

print('#############################################################################################')
