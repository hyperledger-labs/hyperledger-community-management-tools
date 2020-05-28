# Common Repository Structure

This tool provides a report about how a project lines up with the common repository structure

## Common Structure

This is a list of required and recommended files in each Hyperledger source repository. When there
is a difference between the tool and this specification, the specification dominates.

### Files with Specified Content

Repositories MUST have these files with the specific content in the linked files. These files MUST
be at the root of the repository:

- [`LICENSE`](LICENSE.md)
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- [`SECURITY.md`](SECURITY.md)

(Note that current automation does not validate that the contents are identical).

### Required Files

Repositories MUST have these files. Named files MUST be at the root of the repository.

- `README` or `README.md` \
  A description of the project and contain information or links to information such as
  - A reference to the apache license (required).
  - The current and important past releases
  - Documentation for developers and uses
- `MAINTAINERS.md` \
  A list of all current maintainers and contacts/identifiers of the maintainers, one of which must be
  each maintainer's LFID. This file may be maintainer curated or mechanically produced.
- `CONTRIBUTING.md` \
  Directions on how to contribute code to the project, or a pointer to the Wiki page with that information.
- `CHANGELOG.md` \
  A human readable list of recent changes. Changes should at least include the current release. This
  file may be maintainer curated or mechanically produced.
- Testing code \
  Code to test the code in the repository (such as unit tests), in a location appropriate for the language.
- Continuous Integration / Continuous Delivery (CICD) configurations \
  Configurations needed to run CICD on Hyperledger provided systems.

### Recommended

Repositories SHOULD have these files. These files SHOULD be at the root of the repository

- `NOTICE`
- Apache License Header information in each source code file \
  This SHOULD include the snippet `SPDX-License-Identifier: Apache-2.0` as part of the header.
- Build files consistent with the implementation language
  - For JavaScript/Node.js a `package.json` file
  - For Ruby a `Gemfile` file
  - For Java one of a Maven `pom.xml`, an Apache Ant `build.xml`, or a Gralde `build.gradle` file
  - For Python `setup.py` and `requirements.txt` files
  - //TODO C, Go, and Rust build files

### Prohibited

Repositories MUST NOT have these files

- Executable binaries and libraries \
  This includes `.exe`, `.dll` files not otherwise part of a third party library.

## Usage

```
repo_structure.sh [options]
Reports on conformance to the Hyperledger Repository Structure.

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
