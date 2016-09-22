#!/bin/bash
#
# Add release notes links to deliverable files when they page exists
# and the link is not already in the file.
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

if [ -z "$1" ]; then
    echo "Usage: $0 SERIES"
    exit 1
fi

SERIES="$1"

function url_exists {
    local url="$1"

    code=$(curl --silent -I -w "%{http_code}" -o /dev/null "$url")
    if [[ $code = 200 ]]; then
        return 0
    else
        return 1
    fi
}

for filename in deliverables/$SERIES/*.yaml; do
    deliverable=$(basename $filename .yaml)
    echo -n $deliverable
    url="http://docs.openstack.org/releasenotes/${deliverable}/${SERIES}.html"
    if ! url_exists $url; then
        echo " no release notes page at $url"
    else
        # Remove any existing links, since they might point to the
        # "unreleased" page.
        sed -i -e '/release-notes/d' $filename
        # Add the link pointing to the series-specific page.
        sed -i -e "/releases:/i \
release-notes: $url" $filename
        echo
    fi
done
