#!/bin/bash

#Default variables
repositories=()
filename="hyperledger-contributors"
since=""
until=""
output_dir=/tmp
INCLUDE_PROJECT_OPTIONS=1
INCLUDE_DATE_OPTIONS=1
short_description="Get contributors from Hyperledger repositories."

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

. ${script_dir}/../common/command-line.sh

if [ "$(uname)" == "Darwin" ]; then
  MD5SUM="md5 -r"
else
  MD5SUM="md5sum"
fi

today=`date -u +%Y-%m-%d-%H-%M-%S`
outdir="${output_dir}"/${filename}-${today}
hashdir="${hashjs_dir:-${outdir}}"
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

set -x
# Generate the hashes.js file
cat >"${hashdir}"/hashes.js << EOM_HASHJS_PRE
'use strict';

class Hashes {

  static check(hash) {
    const hashes = {
EOM_HASHJS_PRE

for i in $(cut -d , -f 1 "${outdir}"/contributors.csv); do
  hash=$(echo -n "${i}" | ${MD5SUM} | cut -d ' ' -f 1)
  echo "      \"${hash}\":\"\"," >> "${hashdir}"/hashes.js
done

cat >>"${hashdir}"/hashes.js << EOM_HASHJS_POST
    };
    return hashes.hasOwnProperty(hash);
  }
}
if (typeof module != 'undefined' && module.exports) module.exports = Hashes;
EOM_HASHJS_POST
set +x

echo "since=${since:+${since}} through until=${until:+${until}}" > "${outdir}"/arguments.txt

rm -fr ${srcdir}/source
