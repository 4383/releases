#!/bin/bash
#
# Script to manage series of releases.
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

set -e

if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ ! -d $BASEDIR/.tox/venv ]]; then
        (cd $BASEDIR && tox -e venv --notest)
    fi
    source $BASEDIR/.tox/venv/bin/activate
fi

function help {
# Display helping message
cat <<EOF
Usage: $0 [<args>]

Manage series of releases.

This tool aim to provide some shortcut to manage series of release.
It consume a file who should contain a list of instruction, example:

oslo.config feature
oslo.cache bugfix
neutron rc
oslo.messaging feature

Each line must contain a project name followed by the type of release to
generate.

For more details about the valide types of release:

    $ tox -e venv -- new-release -h


Arguments:
    -f, --file          instruction file to consume
    -s, --serie         the openstack release to use
                        (master, stein, rocky, queens, etc...)
                        (default to lastest)
    -t, --topic         topic to assign to reviews
    -m, --commit-msg    base commit message
    -d, --debug         Turn on the debug mode
    -h, --help          show this help message and exit
examples:
    $0 --serie=stein
EOF
}

function prepare {
    # prefix all the line with "#-#" to avoid issue during future parsing
    # the output of the previous command is only informational
    awk 'NF' /tmp/${UUID}.tmp > /tmp/${UUID}.tmp2
    sed -i -e 's/^/#-# /' /tmp/${UUID}.tmp2
    cat /tmp/${UUID}.tmp2 >> /tmp/${UUID}
}

function bump {
    echo "Releasing"
    edited_file=/tmp/${CURRENT_BRANCH/${OSLO_TOOLS_PREFIX}//}

    while read el
    do
        if [[ "${el}" = "#-#"* ]]; then
            continue
        fi
        tools/new_release.sh ${SERIE/stable\//} ${el}
    done < ${edited_file}
    echo "Done!"
}

function commit {
    echo "Commit your changes"
    git add deliverables/${SERIE/stable\//}
    git commit -m "Oslo release for ${SERIE}"
    echo "Done!"
}

function review {
    echo "Publishing oslo's releases"
    git review -t oslo-${SERIE/stable\//}
}


function run {
    # Drop white space in the final version to reduce the length of the report
    rm /tmp/${UUID}.tmp*
    while read line
    do
        TMP_UUID=$(cat /proc/sys/kernel/random/uuid)
        id=$(echo ${line} | awk '{print $1}')
        git checkout -b ${UUID} origin/master
        git cherry-pick ${id}
        git review -t r1-final-rc-deadline
    done < ${FILE}
}

# Setup default values
TOOLSDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASEDIR=$(dirname $TOOLSDIR)
SERIE=master
FILE=""
TOPIC="release-team"
COMMIT_MSG=""
UUID=$(cat /proc/sys/kernel/random/uuid)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Parse command line user inputs
for i in "$@"
do
    case $i in
        # The serie to use
        -s=*|--serie=*)
            SERIE="${i#*=}"
            shift 1
        ;;
        # File to consume
        -f=*|--file=*)
            FILE="${i#*=}"
            if [ ! -f ${FILE} ]; then
                echo "Instruction file not found (${FILE})"
            fi
            shift 1
        ;;
        # Topic to assign
        -t=*|--topic=*)
            TOPIC="${i#*=}"
            shift 1
        ;;
        # Topic to assign
        -m=*|--commit-msg=*)
            COMMIT_MSG="${i#*=}"
            shift 1
        ;;
        # Turn on the debug mode
        -d|--debug)
        set -x
        shift 1
        ;;
        # Display the helping message
        -h|--help)
        help
        exit 0
        ;;
    esac
done

run
