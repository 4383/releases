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

from __future__ import print_function

import argparse

import openstack_releases
from openstack_releases import defaults
from openstack_releases import deliverable


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='show more than the deliverable name',
    )
    parser.add_argument(
        '--team',
        help='the name of the project team, such as "Nova" or "Oslo"',
    )
    parser.add_argument(
        '--deliverable',
        help='the name of the deliverable, such as "nova" or "oslo.config"',
    )
    parser.add_argument(
        '--series',
        default=defaults.RELEASE,
        help='the release series, such as "newton" or "ocata"',
    )
    model = parser.add_mutually_exclusive_group()
    model.add_argument(
        '--model',
        help=('the release model, such as "cycle-with-milestones"'
              ' or "independent"'),
    )
    model.add_argument(
        '--cycle-based',
        action='store_true',
        default=False,
        help='include all cycle-based code repositories',
    )
    parser.add_argument(
        '--type',
        help='deliverable type, such as "library" or "service"',
    )
    parser.add_argument(
        '--deliverables-dir',
        default=openstack_releases.deliverable_dir,
        help='location of deliverable files',
    )
    parser.add_argument(
        '--no-stable-branch',
        default=False,
        action='store_true',
        help='limit the list to deliverables without a stable branch',
    )
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument(
        '--unreleased',
        default=False,
        action='store_true',
        help='limit the list to deliverables not released in the cycle',
    )
    grp.add_argument(
        '--missing-milestone',
        help=('deliverables that do not have the specified milestone as '
              'the most current release; for example 2 would look for .0b2 '
              'in the version number (implies --model cycle-with-milestones)'),
    )
    grp.add_argument(
        '--missing-rc',
        action='store_true',
        help=('deliverables that do not have a release candidate, yet '
              '(implies --model cycle-with-milestones)'),
    )
    args = parser.parse_args()

    # Deal with the inconsistency of the name for the independent
    # directory.
    series = args.series
    if series == 'independent':
        series = '_independent'

    if args.missing_milestone:
        model = 'cycle-with-milestones'
        version_ending = '.0b{}'.format(args.missing_milestone)
    elif args.missing_rc:
        model = 'cycle-with-milestones'
        version_ending = None
    else:
        model = args.model
        version_ending = None

    all_deliv = deliverable.Deliverables(
        root_dir=args.deliverables_dir,
        collapse_history=False,
    )
    for entry in all_deliv.get_deliverables(args.team, series):
        deliv = deliverable.Deliverable(*entry)

        if model and deliv.model != model:
            continue
        if args.cycle_based and not deliv.is_cycle_based:
            continue
        if args.type and deliv.type != args.type:
            continue
        if args.no_stable_branch:
            if deliv.get_branch_location('stable/' + series) is not None:
                continue
        if args.unreleased and deliv.versions:
            continue
        if version_ending and deliv.latest_release and deliv.latest_release.endswith(version_ending):
            continue
        if args.missing_rc and deliv.latest_release and 'rc' in deliv.latest_release:
            continue
        if args.verbose:
            print('{:30} {:15} {}'.format(deliv.name, deliv.latest_release, deliv.team))
        else:
            print(deliv.name)
