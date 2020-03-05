#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0

from __future__ import division

import os
import time
import getpass
from jinja2 import Environment, FileSystemLoader, Template
import datetime
import dateutil.relativedelta
import requests
import json
from configparser import ConfigParser, ExtendedInterpolation
import argparse
import collections


PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape = False,
    loader = FileSystemLoader(
               os.path.join(PATH, 'templates')),
    trim_blocks = False)


# Used to format the date from a Unix timestamp to a string
# - value : The Unix timestamp
# - format : The format to use for output
def datetimeformat(value, format='%Y-%b-%d'):
    return datetime.datetime.fromtimestamp(value).strftime(format)


def render_template(template_filename, context):
    env = TEMPLATE_ENVIRONMENT
    env.filters['datetimeformat'] = datetimeformat
    return env.get_template(template_filename).render(context)


# Get a dictionary of contributors who have contributed some percentage of the
# total commits.
# - contributors - The parsed contributor statistics
# - percentage - The percentage of the total commits for which to find
#                contributors
def get_contributors_who_contributed(contributors, percentage):
    total_commits = sum(contributors[item]["total_commits"] for item in contributors)
    sorted_contributors = collections.OrderedDict(sorted(contributors.items(), key=lambda t:t[1]["total_commits"], reverse=True))

    commits = 0
    rc = {}

    for c in sorted_contributors:
        commits = commits + sorted_contributors[c]["total_commits"]
        if commits > (total_commits * percentage):
            break;
        else:
            rc[c] = sorted_contributors[c]

    return rc


# Return Red/Yellow/Green for the retention field
# - retention_rate - The retention rate value
# - level_of_engagement - The level of engagement value
def calculate_retention_color(retention_rate, level_of_engagement):
    rc = "grey"
    if (retention_rate < .34): # Red
        if (level_of_engagement > .66): # Green
            rc = "yellow"
        else:
            rc = "red"
    elif (retention_rate >= .34 and retention_rate <= .66): # Yellow
        if (level_of_engagement < .34): # Red
            rc = "red"
        else:
            rc = "yellow"
    else: #Green
        if (level_of_engagement > .66): # Green
            rc = "green"
        else:
            rc = "yellow"

    return rc


# Return Red/Yellow/Green for diversity field
# - regular_contributor_percent - The percentage of regular contributors
def calculate_diversity_color(regular_contributor_percent):
    rc = "yellow"

    if (regular_contributor_percent < .34):
        rc = "red"
    elif (regular_contributor_percent > .66):
        rc = "green"

    return rc


def get_summary(contributors):
    summary = {}
    summary["total_commits"] = 0
    summary["first_commit"] = None
    summary["last_commit"] = None
    summary["total_additions"] = 0
    summary["total_deletions"] = 0
    for k,v in contributors.items():
        summary["total_commits"] += v["total_commits"]
        if summary["first_commit"] == None or summary["first_commit"] > v["first_commit"]:
            summary["first_commit"] = v["first_commit"]
        if summary["last_commit"] == None or summary["last_commit"] < v["last_commit"]:
            summary["last_commit"] = v["last_commit"]
        summary["total_additions"] += v["additions"]
        summary["total_deletions"] += v["deletions"]

    return summary

def create_output_html(project_name, title, incubation_date, active_date, deprecation_date, contributors, show_ryg, show_details, show_contributors):
    now = datetime.datetime.now()
    one_month_ago = now + dateutil.relativedelta.relativedelta(months=-1)
    six_months_ago = now + dateutil.relativedelta.relativedelta(months=-6)
    twelve_months_ago = now + dateutil.relativedelta.relativedelta(years=-1)

    active_contributors = {k: v for k, v in contributors.items() if datetime.datetime.fromtimestamp(v["last_commit"]) >= six_months_ago}
    yearly_contributors = {k: v for k, v in contributors.items() if datetime.datetime.fromtimestamp(v["last_commit"]) >= twelve_months_ago}
    new_contributors = {k: v for k, v in contributors.items() if datetime.datetime.fromtimestamp(v["first_commit"]) >= one_month_ago}
    inactive_contributors = {k: v for k, v in contributors.items() if datetime.datetime.fromtimestamp(v["last_commit"]) < six_months_ago}
    repeat_contributors = {k: v for k, v in contributors.items() if v["total_commits"] > 1}

    repeat_sorted = collections.OrderedDict(sorted(repeat_contributors.items(), key=lambda t:t[1]["total_commits"], reverse=True))
    inactive_sorted = collections.OrderedDict(sorted(inactive_contributors.items(), key=lambda t:t[1]["last_commit"], reverse=True))

    core_contributors = get_contributors_who_contributed(contributors, .80)
    core_sorted = collections.OrderedDict(sorted(core_contributors.items(), key=lambda t:t[1]["total_commits"], reverse=True))

    regular_contributors = get_contributors_who_contributed(contributors, .95)
    regular_sorted = collections.OrderedDict(sorted(regular_contributors.items(), key=lambda t:t[1]["total_commits"], reverse=True))

    contributors_sorted = collections.OrderedDict(sorted(contributors.items(), key=lambda t:t[1]["total_commits"], reverse=True))

    total_contributors = len(contributors)
    retention_color = calculate_retention_color((len(active_contributors) / total_contributors), (len(repeat_contributors) / total_contributors))
    diversity_color = calculate_diversity_color(len(regular_sorted) / total_contributors)

    summary = get_summary(contributors)

    # Generate the project report with the given context.
    fname = "./html/" + project_name.lower() + ".html"
    context = {
        'title': title,
        'generation_date_time': now.strftime("%Y-%b-%d %H:%M:%S"),
        'incubation_date': incubation_date,
        'active_date': active_date,
        'deprecation_date': deprecation_date,
        'total_contributors': total_contributors,
        'contributors_in_past_year': len(yearly_contributors),
        'contributors': contributors_sorted,
        'active_contributors': active_contributors,
        'new_contributors': new_contributors,
        'repeat_contributors': repeat_sorted,
        'inactive_contributors': inactive_sorted,
        'core_contributors': core_sorted,
        'regular_contributors': regular_sorted,
        'summary': summary,
        'level_of_interest_color': "grey",
        'conversion_color': "grey",
        'retention_color': retention_color,
        'diversity_color': diversity_color,
        'maturity_color': "grey",
        'show_ryg': show_ryg,
        'show_details': show_details,
        'show_contributors': show_contributors
    }

    with open(fname, 'w') as f:
        html = render_template('report.html', context)
        f.write(html)


def get_api_results(url, username, password):
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

    return r.json()


# NOT USED
def get_project_commit_activity(cfg, project_name, username, password):
    commit_activity = {}
    repos = list(cfg[project_name]['repos'].split('\n'))
    for r in repos:
        t = Template("https://api.github.com/repos/{{repo}}/stats/commit_activity")
        url = t.render(repo=r)
        commit_activity[r] = get_api_results(url, username, password)

    return commit_activity


def get_project_contributors(cfg, project_name, username, password):
    contributors = {}
    repos = list(cfg[project_name]['repos'].split('\n'))
    for r in repos:
        t = Template("https://api.github.com/repos/{{repo}}/stats/contributors")
        url = t.render(repo=r)
        contributors[r] = get_api_results(url, username, password)

    return contributors


def parse_contributor_stats(results):
    rc = {} # The parsed results
    for repo in results:
        for contributor in results[repo]:
            login = contributor["author"]["login"]

            # If this login has not been previously seen, initialize the entry.
            if login not in rc:
                rc[login] = {}
                rc[login]["total_commits"] = 0
                rc[login]["first_commit"] = 0
                rc[login]["last_commit"] = 0
                rc[login]["additions"] = 0
                rc[login]["deletions"] = 0

            # Add the total number of commits for this repository to the
            # contributor's total number of commits
            rc[login]["total_commits"] = rc[login]["total_commits"] + contributor["total"]

            # Determine this contributor's first and last commit week
            for w in contributor["weeks"]:
                if w['c'] > 0:
                    if rc[login]["first_commit"] == 0 or w['w'] < rc[login]["first_commit"]:
                        rc[login]["first_commit"] = w['w']
                    if rc[login]["last_commit"] == 0 or w['w'] > rc[login]["last_commit"]:
                        rc[login]["last_commit"] = w['w']

                # Add the number of additions and deletions to the
                # contributor's total number of additions and deletions
                rc[login]["additions"] = rc[login]["additions"] + w['a']
                rc[login]["deletions"] = rc[login]["deletions"] + w['d']

    return rc


def main():
    if not os.path.exists(os.path.join(PATH, 'html')):
        try:
            os.makedirs(os.path.join(PATH, 'html'))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    parser = argparse.ArgumentParser(description="Generate project reports.")
    parser.add_argument("-c", "--cfg",
        help="Configuration file containing projects and repositories (default=./repos.cfg).",
        default="./repos.cfg")
    parser.add_argument("-u", "--username",
        help="Github username to use for API calls (required)",
        required=True)
    parser.add_argument("-p", "--password",
        help="Github access token to use for API calls (required)",
        required=False)
    parser.add_argument("-g", "--show_ryg", help="Show Health Summary",
        default=False, action='store_true')
    parser.add_argument("-d", "--details", help="Output detailed lists.",
        default=False, action='store_true')
    parser.add_argument("-s", "--show_contributors",
        help="Output all contributors.",
        default=False, action='store_true')
    args = parser.parse_args()

    username = args.username
    password = args.password

    if not password:
        password = getpass.getpass("Please enter github access token:")

    cfg = ConfigParser(interpolation=ExtendedInterpolation())
    cfg.read_file(open(args.cfg))
    for project in cfg.sections():
        print("===== Processing %s repositories =====" % project)
        contributors = parse_contributor_stats(
            get_project_contributors(cfg, project, args.username, args.password))
        if 'title' in cfg[project].keys():
            title = cfg[project]['title']
        else:
            title = project.capitalize()

        if 'incubation_date' in cfg[project].keys():
            incubation_date = cfg[project]['incubation_date']
        else:
            incubation_date = None

        if 'active_date' in cfg[project].keys():
            active_date = cfg[project]['active_date']
        else:
            active_date = None

        if 'deprecation_date' in cfg[project].keys():
            deprecation_date = cfg[project]['deprecation_date']
        else:
            deprecation_date = None

        create_output_html(project, title, incubation_date, active_date, deprecation_date, contributors, args.show_ryg, args.details, args.show_contributors)


if __name__ == "__main__":
    main()
