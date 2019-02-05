#!/bin/bash

#Default variables
repositories=()
filename="hyperledger-lines-of-code"
since=""
output_dir=/tmp
INCLUDE_PROJECT_OPTIONS=1
short_description="Get the lines of code from all Hyperledger repositories."

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

. ${script_dir}/../common/command-line.sh

today=`date -u +%Y-%m-%d-%H-%M-%S`
outfile="${output_dir}"/${filename}-${today}/loc.csv
mkdir -p "${output_dir}"/${filename}-${today}

echo "Repository,Number of Files,Lines of Code" > "${outfile}"

srcdir=/tmp/${filename}-${today}
mkdir -p ${srcdir}/source
cd ${srcdir}/source

for i in ${repositories[@]};
do
  echo "Processing $i..."
  git clone $i
  repo=`basename -s .git $i`
  cd ${repo}

  hash=`git hash-object -t tree /dev/null`
  out=`git diff --shortstat $hash | sed -e "s/ file[s]* changed, /,/" -e "s/ insertion[s]*.*$//"`
  echo "$repo,$out" >> "${outfile}"

  cd ..
done

cd ..

rm -fr ${srcdir}/source
