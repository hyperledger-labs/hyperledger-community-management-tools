# Get Lines of Code
Gets the lines of code and the number of files from all source repositories (as defined in `../common/repositories.sh`). Will output the results at:
```
/<output-dir>/hyperledger-lines-of-code-<date>/loc.csv
```

The results file is in the format of:
```
<repo>,<number-of-files>,<lines-of-code>
...
<repo>,<number-of-files>,<lines-of-code>
```

### Requirements
* `git`

### Usage
```
get_loc.sh
Get the lines of code from all Hyperledger repositories, including labs and supporting repos.

Options:
  --output-dir <dir>: Where should output be placed. (Default: /tmp)
  --help:  Shows this help message

```

