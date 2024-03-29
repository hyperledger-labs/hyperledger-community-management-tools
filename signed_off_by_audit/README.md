# `get_signed_off_by_audit.sh`
Pull a list of contributors who landed change sets without the 'Signed-off-by' tag from all source repositories (as defined in `../common/repositories.sh`). Will output the results at:
```
/tmp/hyperledger-contributors-<date>/signed_off_by_audit.csv
```

The results file is in the format of:
```
email,name
```

It is possible that a single person may have used multiple emails and/or names to contribute code. In that case, the email and/or name column will contain multiple values separated by a pipe (`|`) character.

The `mailmap` file contains a number of [mappings](https://git-scm.com/docs/git-shortlog) that will ensure that the same contributor does not have multiple email addresses and/or names.

The `cleanup.sed` file will delete non-contributor entries (e.g., those created by tools) and ensure that the format is as specified above.

### Requirements
* `git`
* `sed`
* `awk`
* `sort`

### Usage
This script is used to gather the list of contributors that need to do DCO sign offs on their past contributions.
```
get_signed_off_by_audit.sh [--since mm/dd/yyyy] [--until mm/dd/yyyy] [project-selector]+
 Get contributors without sign offs from Hyperledger repositories.

 Options:
   --fabric:   Include Fabric repositories
   --sawtooth: Include Sawtooth repositories
   --iroha:    Include Iroha repositories
   --indy:     Include Indy repositories
   --besu:     Include Besu repositories
   --cactus:   Include Cactus repositories
   --cello:    Include Cello repositories
   --quilt:    Include Quilt repositories
   --caliper:  Include Caliper repositories
   --ursa:     Include Ursa repositories
   --grid:     Include Grid repositories
   --aries:    Include Aries repositories
   --transact: Include Transact repositories
   --projects: Include Project repositories
   --labs:     Include Labs repositories
   --other:    Include Other repositories
   --github:   Include Github repositories
   --all:      Include all repositories (default)
   --since:    Includes commits more recent than this date (mm/dd/yyyy).
               By default starts from the start of the repo.
   --until:    Includes commits older than this date (mm/dd/yyyy).
               By default ends at the end of the repo.
   --output-dir <dir>: Where should output be placed. (Default: /tmp)
   --help:     Shows this help message

  NOTE: If no options are specified, it is as if you had specified --all
  NOTE: Multiple repository options can be specified
  NOTE: --all will override all commands for individual projects
```
