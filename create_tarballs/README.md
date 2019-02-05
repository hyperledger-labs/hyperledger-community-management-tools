# `create_tarballs.sh`
Creates a GZIP'd tarball of the latest source code for the specified repositories. It does this by cloning the source code from Gerrit or Github and then creating a GZIP'd tarball containing the checked out code. The tarball will be created in:

```
/tmp/hyperledger-source-<project-name>-<date>.tar.gz
```

A single project may contain multiple source repositories (as defined in `repositories.sh`). The tarball will contain all files from each of the repositories making up the project.

### Requirements
* `git`
* `gzip`
* `tar`

### Usage
This script is used for creating GZIP'd tarballs that can be used by the license scanning process.
```
create_tarball.sh [options]
Create a tarball of the latest source in the specified repositories.

Options:
  --fabric:     Create a tarball containing Fabric repositories
  --sawtooth:   Create a tarball containing Sawtooth repositories
  --iroha:      Create a tarball containing Iroha repositories
  --burrow:     Create a tarball containing Burrow repositories
  --indy:       Create a tarball containing Indy repositories
  --composer:   Create a tarball containing Composer repositories
  --cello:      Create a tarball containing Cello repositories
  --explorer:   Create a tarball containing Explorer repositories
  --quilt:      Create a tarball containing Quilt repositories
  --gerrit:     Create a tarball containing Gerrit repositories
  --github:     Create a tarball containing Github repositories
  --all:        Create a tarball containing all repositories
  --no-tarball: Check out files only

NOTE: If no options are specified, it is as if you had specified --all
NOTE: Multiple repository options can be specified to be included in a
      single tarball.
NOTE: --all will override all commands for individual projects.
```

