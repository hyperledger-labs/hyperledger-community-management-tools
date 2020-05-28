# `create_tarballs.sh`
Creates a GZIP'd tarball of the latest source code for the specified repositories. It does this by cloning the source code from Github and then creating a GZIP'd tarball containing the checked out code. The tarball will be created in:

```
<output_dir>/<date>/hyperledger-source-<project-name>-<datetime>.tar.gz
```

A single project may contain multiple source repositories (as defined in `repositories.sh`). The tarball will contain all files from each of the repositories making up the project.

### Requirements
* `git`
* `gzip`
* `tar`

### Usage
This script is used for creating GZIP'd tarballs that can be used by the license scanning process.
```
        ./create_tarballs.sh [options]
        Create a tarball of the latest source in the specified repositories.

        Options:
          --fabric:   Include Fabric repositories
          --sawtooth: Include Sawtooth repositories
          --iroha:    Include Iroha repositories
          --burrow:   Include Burrow repositories
          --indy:     Include Indy repositories
          --besu:     Include Besu repositories
          --cactus:   Include Cactus repositories
          --cello:    Include Cello repositories
          --explorer: Include Explorer repositories
          --quilt:    Include Quilt repositories
          --caliper:  Include Caliper repositories
          --ursa:     Include Ursa repositories
          --grid:     Include Grid repositories
          --aries:    Include Aries repositories
          --transact: Include Transact repositories
          --avalon:   Include Avalon repositories
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

