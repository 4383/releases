#!/bin/bash

TOOLSDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASEDIR=$(dirname $TOOLSDIR)
instructions=$1

if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ ! -d $BASEDIR/.tox/venv ]]; then
        (cd $BASEDIR && tox -e venv --notest)
    fi
    source $BASEDIR/.tox/venv/bin/activate
fi

current_series=$(python -c 'import openstack_releases.defaults; \
    print(openstack_releases.defaults.RELEASE)')

while read instruct
do
    if [[ "${instruct}" = "#-#"* ]]; then
        continue
    fi
    tools/new_release.sh ${current_series} ${instruct}
done < ${instructions}
echo "Done!"

#while read instruct
#do
#    UUID=$(cat /proc/sys/kernel/random/uuid)
#    id=$(echo ${instruct} | awk '{print $1}')
#    git checkout -b ${UUID} origin/master
#    git cherry-pick ${id}
#    git review -t r1-final-rc-deadline
#done < $(pwd)/list
