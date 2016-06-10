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
"""Class for manipulating all of the deliverable data.
"""

from __future__ import print_function

import collections
import glob
import os

import pbr.version
import yaml


def _safe_semver(v):
    """Get a SemanticVersion that closely represents the version string.

    We can't always get a SemanticVersion instance because some of the
    legacy tags don't comply with the parser. This method corrects
    some of the more common mistakes in formatting to make it more
    likely we can construct a SemanticVersion, even if the results
    don't quite match the input.

    """
    orig = v = str(v)
    # Remove "v" prefixes.
    v = v.lstrip('v')
    # Remove any stray "." at the start or end, after the other
    # cleanups.
    v = v.strip('.')
    # If we have a version with 4 positions that are all integers,
    # drop the fourth.
    parts = v.split('.')
    if len(parts) > 3:
        try:
            int(parts[3])
        except ValueError:
            pass
        else:
            parts = parts[:3]
        v = '.'.join(parts)
    if v != orig:
        print('  changed version %r to %r' % (orig, v))
    return pbr.version.SemanticVersion.from_pip_string(v)


def _version_sort_key(release):
    """Return a value we can compare for sorting.
    """
    return _safe_semver(release['version'])


def _collapse_deliverable_history(name, info):
    """Collapse pre-releases into their final release.

    Edit the info dictionary in place.

    """
    sorted_releases = sorted(
        info.get('releases', []),
        key=_version_sort_key,
    )
    # Collapse pre-releases into their final release.
    releases = []
    known_versions = set()
    for r in reversed(sorted_releases):
        try:
            parsed_vers = pbr.version.SemanticVersion.from_pip_string(
                str(r['version']))
            vers_tuple = parsed_vers.version_tuple()
        except:
            # If we can't parse the version, it must be some sort
            # of made up legacy tag. Ignore the parse error
            # and include the value in our output.
            releases.append(r)
        else:
            if len(vers_tuple) != 3:
                # This is not a normal release, so assume it
                # is a pre-release.
                final = parsed_vers.brief_string()
                if final in known_versions:
                    print('[deliverables] ignoring %s %s' %
                          (name, r['version']))
                    continue
                releases.append(r)
                known_versions.add(r['version'])
    info['releases'] = list(reversed(releases))


class Deliverables(object):

    def __init__(self, root_dir):
        self._root_dir = root_dir

        # Map team names to a list of all of their deliverables.
        self._team_deliverables = collections.defaultdict(set)
        # Map team names to a set of all the series in which they
        # produced anything.
        self._team_series = collections.defaultdict(set)
        # Map both team and series name to a list of the deliverable
        # files.
        self._by_team_and_series = collections.defaultdict(list)
        self._by_series = collections.defaultdict(list)
        # Map filenames to parsed content.
        self._by_filename = {}

        self._load_deliverable_files(root_dir)

    def _load_deliverable_files(self, root_dir):
        deliverable_files = glob.glob(os.path.join(root_dir, '*/*.yaml'))
        for filename in sorted(deliverable_files):
            print('[deliverables] reading %s' % filename)
            series = self._series_from_filename(filename)
            deliverable = self._deliverable_from_filename(filename)
            with open(filename, 'r') as f:
                d_info = yaml.load(f.read())
                _collapse_deliverable_history(deliverable, d_info)
            team = d_info['team']
            self._add_deliverable_file(
                filename, series, team, deliverable, d_info,
            )

    @staticmethod
    def _series_from_filename(filename):
        return os.path.basename(os.path.dirname(filename))

    @staticmethod
    def _deliverable_from_filename(filename):
        return os.path.splitext(os.path.basename(filename))[0]

    def _add_deliverable_file(self, filename, series, team, deliverable,
                              d_info):
        self._by_filename[filename] = d_info
        self._by_team_and_series[(team, series)].append(filename)
        self._by_series[series].append(filename)
        self._team_deliverables[team].add(deliverable)
        self._team_series[team].add(series)

    def get_team_deliverables(self, team):
        "Returns a list of deliverable names produced by the team."
        return list(sorted(self._team_deliverables[team]))

    def get_team_series(self, team):
        "Return the names of the series in which the team produced anything."
        return self._team_series[team]

    def get_teams(self):
        "Return all of the names of all of the teams seen."
        return list(self._team_series.keys())

    def get_deliverables(self, team, series):
        """Return a sequence of deliverable data for the team and series.

        Return tuples containing team, series, deliverable, and parsed
        deliverable file content.

        If the team or series is None, treat that value as a wildcard.

        """
        if team is None:
            if series is None:
                series = '_independent'
            filenames = self._by_series[series]
        else:
            filenames = self._by_team_and_series[(team, series)]
        for filename in filenames:
            yield (
                team,
                self._series_from_filename(filename),
                self._deliverable_from_filename(filename),
                self._by_filename.get(filename, {}),
            )
