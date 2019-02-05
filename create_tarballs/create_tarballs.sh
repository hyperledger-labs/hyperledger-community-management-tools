#!/bin/bash

#Default variables
repositories=()
filename="hyperledger-source"
tarball=TRUE
output_dir=/tmp
INCLUDE_PROJECT_OPTIONS=1
short_description="Create a tarball of the latest source in the specified repositories."

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

. ${script_dir}/../common/command-line.sh

today=`date -u +%Y-%m-%d-%H-%M-%S`
today_date_only=`date -u +%Y-%m-%d`
mkdir -p /tmp/${filename}-${today}
cd /tmp/${filename}-${today}

for i in ${repositories[@]};
do
echo "Processing $i..."
git clone $i
done

cd ..
tar czvf ${filename}-${today}.tar.gz --exclude .git ${filename}-${today}
rm -fr ${filename}-${today}

mkdir -p "${output_dir}"/${today_date_only}/tarballs
mv ${filename}-${today}.tar.gz "${output_dir}"/${today_date_only}/tarballs
