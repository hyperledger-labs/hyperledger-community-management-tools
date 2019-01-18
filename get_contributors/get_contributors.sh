#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

. ${script_dir}/../common/repositories.sh

#Default variables
repositories=()
filename="hyperledger-contributors"
since=""
until=""
all_specified=FALSE
output_dir=/tmp

# Handle command line arguments
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --fabric)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${fabric_repositories[@]}" )
        filename+="-fabric"
      fi
    ;;
    --sawtooth)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${sawtooth_repositories[@]}" )
        filename+="-sawtooth"
      fi
    ;;
    --iroha)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${iroha_repositories[@]}" )
        filename+="-iroha"
      fi
    ;;
    --burrow)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${burrow_repositories[@]}" )
        filename+="-burrow"
      fi
    ;;
    --indy)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${indy_repositories[@]}" )
        filename+="-indy"
      fi
    ;;
    --composer)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${composer_repositories[@]}" )
        filename+="-composer"
      fi
    ;;
    --cello)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${cello_repositories[@]}" )
        filename+="-cello"
      fi
    ;;
    --explorer)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${explorer_repositories[@]}" )
        filename+="-explorer"
      fi
    ;;
    --quilt)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${quilt_repositories[@]}" )
        filename+="-quilt"
      fi
    ;;
    --caliper)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${caliper_repositories[@]}" )
        filename+="-caliper"
      fi
    ;;
    --ursa)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${ursa_repositories[@]}" )
        filename+="-ursa"
      fi
    ;;
    --grid)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${grid_repositories[@]}" )
        filename+="-grid"
      fi
    ;;
    --projects)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${project_repositories[@]}" )
        filename+="-projects"
      fi
    ;;
    --labs)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${labs_repositories[@]}" )
        filename+="-labs"
      fi
    ;;
    --other)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${other_repositories[@]}" )
        filename+="-other"
      fi
    ;;
    --gerrit)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${gerrit_repositories[@]}" )
        filename+="-gerrit"
      fi
    ;;
    --github)
      if [[ "$all_specified" == FALSE ]] ; then
        repositories+=( "${github_repositories[@]}" )
        filename+="-github"
      fi
    ;;
    --all)
      all_specified=TRUE
      filename+="-all"
      repositories="${all_repositories[@]}"
    ;;
    --since)
      since="$2"
      shift # past argument or value. 2nd shift below
      ;;
    --until)
      until="$2"
      shift # past argument or value. 2nd shift below
      ;;
    --output-dir)
      output_dir=$2
      shift # past argument or value. 2nd shift below
    ;;
    --help)
      cat << EOM
        get_contributors.sh [--since mm/dd/yyyy] [--until mm/dd/yyyy]
        Get contributors from Hyperledger repositories.

        Options:
          --fabric:   Include Fabric repositories
          --sawtooth: Include Sawtooth repositories
          --iroha:    Include Iroha repositories
          --burrow:   Include Burrow repositories
          --indy:     Include Indy repositories
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
          --all:      Include all repositories
                      Does not include labs or other repositories. (default)
          --since:    Includes commits more recent than this date (mm/dd/yyyy).
                      By default starts from the start of the repo.
          --until:    Includes commits older than this date (mm/dd/yyyy).
                      By default ends at the end of the repo.
          --output-dir <dir>: Where should output be placed. (Default: /tmp)
          --help:     Shows this help message
EOM
    exit;
    ;;
    *)
      echo "Unknown option $key"
      exit 1
    ;;
esac
shift # past argument or value
done

# if no repositories were specified, then act as if --all was specified
if [ "$repositories" == "" ]
then
  repositories="${all_repositories[@]}"
  filename+="-all"
fi

today=`date -u +%Y-%m-%d-%H-%M-%S`
outdir="${output_dir}"/${filename}-${today}
mkdir -p "${outdir}"/working

srcdir=/tmp/${filename}-${today}
mkdir -p ${srcdir}/source
cd ${srcdir}/source

for i in ${repositories[@]};
do
echo "Processing $i..."
git clone --single-branch $i
repo=`basename -s .git $i`
cd ${repo}

# Get emails and names of contributors of commits from the git log
git log --pretty='%aN <%aE>' ${since:+--since=${since}} ${until:+--until=${until}}| git -c mailmap.file=${script_dir}/mailmap check-mailmap --stdin > "${outdir}"/working/${repo}.gitlog

# Replace duplicate emails with preferred email
sed -f ${script_dir}/cleanup.sed "${outdir}"/working/${repo}.gitlog > "${outdir}"/working/${repo}.contributors

# Sort contributors based on email (1st key) ignoring case
LC_ALL=C sort -i -t "|" -k 1 -u -f "${outdir}"/working/${repo}.contributors > "${outdir}"/working/${repo}.sorted

# Get unique contributors based on email (1st key) ignoring case
awk 'BEGIN { FS = "|" }
     tolower($1)!=key { if (key != "") print out; key=tolower($1); out=$0; next }
     { out=out","$2 }
     END { print out }' "${outdir}"/working/${repo}.sorted > "${outdir}"/working/${repo}.uniq-contributors

# Flip commas and pipes
awk 'BEGIN { FS = "|" }
     {
       col1=$1
       gsub(/,/,"|",col1)
       col2=$2
       gsub(/,/,"|",col2)
       print col1 "," col2
     }' "${outdir}"/working/${repo}.uniq-contributors > "${outdir}"/${repo}.uniq-contributors.csv
cd ..
done

LC_ALL=C sort -i -t "|" -k 1 -u -f "${outdir}"/working/*.sorted | awk 'BEGIN { FS = "|" }
  tolower($1)!=key { if (key != "") print out; key=tolower($1); out=$0; next }
  { out=out","$2 }
  END { print out }' > "${outdir}"/working/uniq-emails

LC_ALL=C sort -i -t "|" -k 2 -f "${outdir}"/working/uniq-emails | awk 'BEGIN { FS = "|" }
  tolower($2)!=key { if (key != "") print out; key=tolower($2); out=$0; next }
  {out=$1","out }
  END { print out }' > "${outdir}"/working/contributors

# Flip commas and pipes
awk 'BEGIN { FS = "|" }
     {
       col1=$1
       gsub(/,/,"|",col1)
       col2=$2
       gsub(/,/,"|",col2)
       print col1 "," col2
     }' "${outdir}"/working/contributors > "${outdir}"/contributors.csv

echo "since=${since:+${since}} through until=${until:+${until}}" > "${outdir}"/arguments.txt

rm -fr ${srcdir}/source
