[//]: # (SPDX-License-Identifier: CC-BY-4.0)

# Hyperledger Community Management Tools
Tools used to manage and evaluate the Hyperledger Community

# Scope of Lab
This lab will contain tools that can be used to manage and evaluate the Hyperledger Community, including:
- project reporting tools
- contributor statistic tools
- contributor diversity tools

All tools will be documented fully so that anyone in the community can run them. In addition, all tools will contain a `--help` option to provide help from the command line.

# Tools

## Hyperledger-Specific Tools

These tools currently only work for the Hyperledger and Hyperledger Labs GitHub organizations as they utilize the list of repositories as defined in `./common/repositories.sh`.
- **get_contributors** - generates a comma-separated file containing a list of contributors.
  - [Get Contributors README](./get_contributors/README.md)
- **get_lines_of_code** - generates a comma-separated file containing a list of repositories, the number of files, and the lines of code.
  - [Get Lines of Code README](./get_lines_of_code/README.md)
- **create_tarballs** - creates tarballs of the latest source in the specified repositories
  - [Create tarballs README](./create_tarballs/README.md)
- **repo_structure** - provides a report about how a project lines up with the common repository structure.
  - [Common Repository Structure README](./repo_structure/README.md)
- **signed_off_by_audit** - creates a list of contributors who landed change sets without the 'Signed-off-by' tag from all source repositories (as defined in `../common/repositories.sh`).
  - [Signed-off by Audit README](./signed_off_by_audit/README.md)

## Generic Tools

These tools should work for any GitHub organization as they either use the GitHub GraphQL API](https://docs.github.com/en/graphql) or are designed to take a configuration file for specifying what you wish to report on.
- **Project Reports** - generates a health assessment report for each project within Hyperledger, as well as other projects that might be of interest.
  - [Project Report Requirements](./project-reports/docs/requirements.md) specifies the proposed content
  - [Project Report README](./project-reports/README.md) provides details on how to run
- **list-old-repos** - creates a list of repositories for a specified organization where the last commit on the main branch is older than a specified date.
  - [List Old Repos README](./list-old-repos/README.md)
- **org-dashboard** - generates a markdown dashboard showing information about GitHub repositories for a specified organization
  - [Org Dashboard README](./org-dashboard/README.md)
- **org-repo-info** - generates a JSON file containing information for a specified organization
  - [Org Repo Info README](./org-repo-info/README.md)
