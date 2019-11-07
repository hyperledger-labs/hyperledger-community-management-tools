# `create_tarballs.sh`
Creates a GZIP'd tarball of the latest source code for the specified repositories. It does this by cloning the source code from Gerrit or Github and then creating a GZIP'd tarball containing the checked out code. The tarball will be created in:

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
          --composer: Include Composer repositories
          --cello:    Include Cello repositories
          --explorer: Include Explorer repositories
          --quilt:    Include Quilt repositories
          --caliper:  Include Caliper repositories
          --ursa:     Include Ursa repositories
          --grid:     Include Grid repositories
          --projects: Include Project repositories
          --labs:     Include Labs repositories
          --other:    Include Other repositories
          --gerrit:   Include Gerrit repositories
          --github:   Include Github repositories
          --all:      Include all repositories (default)
          --output-dir <dir>: Where should output be placed. (Default: /tmp)
          --help:     Shows this help message

        NOTE: If no options are specified, it is as if you had specified --all
        NOTE: Multiple repository options can be specified
        NOTE: --all will override all commands for individual projects
```

