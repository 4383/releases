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

import argparse
import datetime
import os.path

import openstack_releases
from openstack_releases import yamlutils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'series',
        help='the release series, such as "newton" or "ocata"',
    )
    parser.add_argument(
        '--deliverables-dir',
        default=openstack_releases.deliverable_dir,
        help='location of deliverable files',
    )
    args = parser.parse_args()

    series = args.series

    # Find the schedule file.
    schedule_filename = os.path.abspath(os.path.join(
        args.deliverables_dir,
        '..',
        'doc', 'source', series,
        'schedule.yaml',
    ))

    with open(schedule_filename, 'r') as f:
        schedule_data = yamlutils.loads(f.read())

    print('Release Team Calendar for {}\n'.format(series.title()))

    print('Review dashboard: https://tiny.cc/ReleaseInbox')
    print('Process document: https://releases.openstack.org/reference/process.html')
    print('Storyboard: https://storyboard.openstack.org/#!/board/64')
    print('Release email content: https://etherpad.openstack.org/p/relmgmt-weekly-emails')
    print()

    print('Meeting info')
    print('Thursdays at 16:00 UTC in #openstack-release')
    print('Meeting stanza: #startmeeting releaseteam')
    print('Ping list: ')
    print()

    print('Review Days')
    print('[make list format]')
    print('Mon: ')
    print('Tue: ')
    print('Wed: ')
    print('Thu: ')
    print('Fri: ')
    print()

    print('First apply title formatting to all week titles. Then apply list')
    print('format to the following content, and copy-paste it in every week:')
    print()
    print('Team availability notes')
    print('Tasks')
    print('Meeting Agenda')
    print('Countdown email content to send this week')
    print()

    for week in schedule_data['cycle']:
        if not week.get('name'):
            continue
        start = datetime.datetime.strptime(week['start'], '%Y-%m-%d')
        week['start_date'] = start
        end = datetime.datetime.strptime(week['end'], '%Y-%m-%d')
        week['end_date'] = end
        print('{name} ({start_date:%b %d} - {end_date:%b %d})'.format(**week),
              end='')
        if week.get('x-project'):
            print(' [', ', '.join(week['x-project']), ']')
        else:
            print()
