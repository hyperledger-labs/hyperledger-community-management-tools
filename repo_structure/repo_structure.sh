#!/bin/bash

#Default variables
repositories=()
filename="hyperledger-repository-structure"
since=""
until=""
output_dir=/tmp
INCLUDE_PROJECT_OPTIONS=1
INCLUDE_DATE_OPTIONS=1
short_description="Reports on conformance to the Hyperledger Repository Structure."

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

. ${script_dir}/../common/command-line.sh

today=`date -u +%Y-%m-%d-%H-%M-%S`
outdir="${output_dir}"/${filename}-${today}
outfile="${outdir}"/repo_structure.txt
mkdir -p "${outdir}"/working

srcdir=/tmp/${filename}-${today}
mkdir -p ${srcdir}/source
cd ${srcdir}/source

for i in ${repositories[@]};
do
  echo "Processing $i..."
  cd ${srcdir}/source
  git clone --single-branch $i
  repo=`basename -s .git $i`
  cd ${repo}
  echo >> ${outfile}
  echo "Report for $i" >> ${outfile}

  cp ${script_dir}/repolint.json .
  npx repolinter -r ${script_dir}/repolint.json > repoliter.tmpresult
  set pass=$?
  # Filter out passing and not-run tests
  grep -v ✔ repoliter.tmpresult | grep -v ℹ >> ${outfile}
  rm repoliter.tmpresult
  if [ ${pass} -eq 0 ]; then
    echo "PASSED - $i" >> ${outfile}
  else
    echo "FAILED - $i" >> ${outfile}
  fi
done


rm -fr ${srcdir}/source
