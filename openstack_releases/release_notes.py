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

"""Generates a standard set of release notes for a repository."""

import glob
import logging
import os
import random
import subprocess

import jinja2
import parawrap
from reno import config as reno_config
from reno import formatter
from reno import loader

from openstack_releases import rst2txt
from openstack_releases import yamlutils

LOG = logging.getLogger(__name__)


EMOTIONS = [
    'are amped to',
    'are chuffed to',
    'contentedly',
    'are delighted to',
    'eagerly',
    'are ecstatic to',
    'enthusiastically',
    'are excited to',
    'exuberantly',
    'are glad to',
    'are gleeful to',
    'are happy to',
    'high-spiritedly',
    'are jazzed to',
    'joyfully',
    'jubilantly',
    'are overjoyed to',
    'are pleased to',
    'are psyched to',
    'are pumped to',
    'are satisfied to',
    'are stoked to',
    'are thrilled to',
    'are tickled pink to',
]

# The email headers for generating a message to go right into sendmail
# or msmtp.
EMAIL_HEADER_TPL = """
{%- if email %}
From: {{email_from}}
To: {{email_to}}
Reply-To: {{email_reply_to}}
Subject: {{email_tags}} {{project}} {{end_rev}}{% if series %} ({{series}}){% endif %}
{% endif %}
"""

PYPI_URL_TPL = 'https://pypi.org/project/%s'

# This will be replaced with template values and then wrapped using parawrap
# to correctly wrap at paragraph boundaries...

HEADER_RELEASE_TPL = """
We {{ emotion }} announce the release of:

{% if description %}
{{ project }} {{ end_rev }}: {{ description }}
{% else %}
{{ project }} {{ end_rev }}
{% endif %}

{% if first_release -%}
This is the first release of {{project}}.
{%- endif %}
{% if series -%}
This release is part of the {{series}} {% if stable_series %}stable {% endif %}release series.
{%- endif %}
{% if source_url %}

The source is available from:

    {{ source_url }}
{% endif %}

Download the package from:

{% if pypi_url %}
    {{ pypi_url }}
{% else %}
    https://tarballs.openstack.org/{{publishing_dir_name}}/
{% endif %}
{% if bug_url %}

Please report issues through:

    {{ bug_url }}
{% endif %}

For more details, please see below.
"""

# This will just be replaced with template values (no wrapping applied).
CHANGE_RELEASE_TPL = """{% if reno_notes %}{{ reno_notes }}{% endif %}
{% if changes %}{{ change_header }}{% if skip_requirement_merges %}

NOTE: Skipping requirement commits...
{%- endif %}

{% for change in changes -%}
{{ change }}
{% endfor %}
{%- endif %}
{% if diff_stats %}
{% if not first_release -%}
Diffstat (except docs and test files)
-------------------------------------

{% for change in diff_stats -%}
{{ change }}
{% endfor %}
{%- endif %}
{% if requirement_changes %}
Requirements updates
--------------------

{% for change in requirement_changes -%}
{{ change }}
{% endfor %}
{%- endif %}
{% endif %}
"""

CHANGES_ONLY_TPL = """{{ change_header }}
{% for change in changes -%}
{{ change }}
{% endfor %}
"""

RELEASE_CANDIDATE_TPL = """
Hello everyone,

A new release candidate for {{project}} for the end of the {{series|capitalize}}
cycle is available!  You can find the source code tarball at:

    https://tarballs.openstack.org/{{publishing_dir_name}}/

Unless release-critical issues are found that warrant a release
candidate respin, this candidate will be formally released as the
final {{series|capitalize}} release. You are therefore strongly encouraged
to test and validate this tarball!

Alternatively, you can directly test the stable/{{series|lower}} release
branch at:

    {{source_url}}/src/branch/stable/{{series|lower}}

Release notes for {{project}} can be found at:

    https://docs.openstack.org/releasenotes/{{publishing_dir_name}}/

{% if bug_url -%}
If you find an issue that could be considered release-critical, please
file it at:

    {{bug_url}}

and tag it *{{series|lower}}-rc-potential* to bring it to the {{project}}
release crew's attention.
{%- endif %}
"""


def parse_deliverable(series, repo, deliverable_file=None):
    """Parse useful information out of the deliverable file.

    Currently only parses the bug URL, but could potentially be expanded to get
    other useful settings.

    :param series: The release series being processed.
    :param repo: The name of the repo.
    :param deliverable_file: The deliverable file.
    """
    release_repo = os.path.realpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

    if deliverable_file is None:
        deliverable_file = os.path.join(
            'deliverables', series.lower(), '%s.yaml' % repo)

    deliverable_path = os.path.join(release_repo, deliverable_file)

    # Hard coding source URL for now
    sections = {
        'bug_url': '',
        'source_url': 'https://opendev.org/openstack/%s' % repo,
    }

    try:
        with open(deliverable_path, 'r') as d:
            deliverable_info = yamlutils.loads(d)
    except Exception:
        # TODO(smcginnis): If the deliverable doesn't match the repo name, we
        # can try to find it by loading all deliverable data and iterating on
        # each deliverables repos to find it.
        LOG.warning('Unable to parse %s %s deliverable file', repo, series)
        return sections

    if deliverable_info.get('launchpad'):
        sections['bug_url'] = (
            'https://bugs.launchpad.net/%s/+bugs' %
            deliverable_info['launchpad'])
    elif deliverable_info.get('storyboard'):
        sections['bug_url'] = (
            'https://storyboard.openstack.org/#!/project/%s' %
            deliverable_info['storyboard'])

    return sections


def expand_template(contents, params):
    if not params:
        params = {}
    tpl = jinja2.Template(source=contents, undefined=jinja2.StrictUndefined)
    return tpl.render(**params)


def run_cmd(cmd, cwd=None, encoding='utf-8'):
    stdout = subprocess.check_output(cmd, cwd=cwd)
    return stdout.decode(encoding)


def is_skippable_commit(skip_requirement_merges, line):
    return (skip_requirement_merges and
            line.lower().endswith('updated from global requirements'))


def generate_release_notes(repo, repo_path,
                           start_revision, end_revision,
                           show_dates, skip_requirement_merges,
                           is_stable, series,
                           email, email_from,
                           email_reply_to, email_tags,
                           include_pypi_link,
                           changes_only,
                           first_release,
                           deliverable_file, description,
                           publishing_dir_name,
                           ):
    """Return the text of the release notes.

    :param repo: The name of the repo.
    :param repo_path: Path to the repo repository on disk.
    :param start_revision: First reference for finding change log.
    :param end_revision: Final reference for finding change log.
    :param show_dates: Boolean indicating whether or not to show dates
        in the output.
    :param skip_requirement_merges: Boolean indicating whether to
        skip merge commits for requirements changes.
    :param is_stable: Boolean indicating whether this is a stable
        series or not.
    :param series: String holding the name of the series.
    :param email: Boolean indicating whether the output format should
        be an email message.
    :param email_from: String containing the sender email address.
    :param email_reply_to: String containing the email reply-to address.
    :param email_tags: String containing the email header topic tags to add.
    :param include_pypi_link: Boolean indicating whether or not to
        include an automatically generated link to the PyPI package
        page.
    :param changes_only: Boolean indicating whether to limit output to
        the list of changes, without any extra data.
    :param first_release: Boolean indicating whether this is the first
        release of the project
    :param deliverable_file: The deliverable file path from the repo root.
    :param description: Description of the repo
    :param publishing_dir_name: The directory on publishings.openstack.org
        containing the package.
    """
    repo_name = repo.split('/')[-1]
    # Determine if this is a release candidate or not.
    is_release_candidate = 'rc' in end_revision

    # Do not mention the series in independent model since there is none
    if series == 'independent':
        series = ''

    if not email_from:
        raise RuntimeError('No email-from specified')

    # Get the commits that are in the desired range...
    git_range = "%s..%s" % (start_revision, end_revision)
    if show_dates:
        format = "--format=%h %ci %s"
    else:
        format = "--oneline"
    cmd = ["git", "log", "--no-color", format, "--no-merges", git_range]
    stdout = run_cmd(cmd, cwd=repo_path)
    changes = []
    for commit_line in stdout.splitlines():
        commit_line = commit_line.strip()
        if not commit_line or is_skippable_commit(skip_requirement_merges,
                                                  commit_line):
            continue
        else:
            changes.append(commit_line)

    # Filter out any requirement file changes...
    requirement_changes = []
    requirement_files = list(glob.glob(os.path.join(repo_path,
                                                    '*requirements*.txt')))
    if requirement_files:
        cmd = ['git', 'diff', '-U0', '--no-color', git_range]
        cmd.extend(requirement_files)
        stdout = run_cmd(cmd, cwd=repo_path)
        requirement_changes = [line.strip()
                               for line in stdout.splitlines() if line.strip()]

    # Get statistics about the range given...
    cmd = ['git', 'diff', '--stat', '--no-color', git_range]
    stdout = run_cmd(cmd, cwd=repo_path)
    diff_stats = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line or line.find("tests") != -1 or line.startswith("doc"):
            continue
        diff_stats.append(line)

    # Extract + valdiate needed sections...
    sections = parse_deliverable(
        series, repo_name, deliverable_file=deliverable_file)
    change_header = ["Changes in %s %s" % (repo, git_range)]
    change_header.append("-" * len(change_header[0]))

    # Look for reno notes for this version.
    if not changes_only:
        logging.getLogger('reno').setLevel(logging.WARNING)
        cfg = reno_config.Config(
            reporoot=repo_path,
        )
        branch = None
        if is_stable and series:
            branch = 'origin/stable/%s' % series
        cfg.override(branch=branch)
        ldr = loader.Loader(conf=cfg, ignore_cache=True)
        if end_revision in ldr.versions:
            rst_notes = formatter.format_report(
                loader=ldr,
                config=cfg,
                versions_to_include=[end_revision],
            )
            reno_notes = rst2txt.convert(rst_notes).decode('utf-8')
        else:
            LOG.warning(
                ('Did not find revision %r in list of versions '
                 'with release notes %r, skipping reno'),
                end_revision, ldr.versions,
            )
            reno_notes = ''
    else:
        reno_notes = ''

    # The recipient for announcements should always be the
    # release-announce@lists.openstack.org ML (except for
    # release-test and release candidates)
    email_to = 'release-announce@lists.openstack.org'
    if repo_name == 'openstack-release-test':
        email_to = 'release-job-failures@lists.openstack.org'
    elif is_release_candidate:
        email_to = 'openstack-discuss@lists.openstack.org'

    params = dict(sections)
    params.update({
        'project': repo,
        'description': description,
        'end_rev': end_revision,
        'range': git_range,
        'lib': repo_path,
        'skip_requirement_merges': skip_requirement_merges,
        'changes': changes,
        'requirement_changes': requirement_changes,
        'diff_stats': diff_stats,
        'change_header': "\n".join(change_header),
        'emotion': random.choice(EMOTIONS),
        'stable_series': is_stable,
        'series': series,
        'email': email,
        'email_from': email_from,
        'email_to': email_to,
        'email_reply_to': email_reply_to,
        'email_tags': email_tags,
        'reno_notes': reno_notes,
        'first_release': first_release,
        'publishing_dir_name': publishing_dir_name,
    })
    if include_pypi_link:
        params['pypi_url'] = PYPI_URL_TPL % repo_name
    else:
        params['pypi_url'] = None

    response = []
    if changes_only:
        response.append(expand_template(CHANGES_ONLY_TPL, params))
    else:
        if email:
            email_header = expand_template(EMAIL_HEADER_TPL.strip(), params)
            response.append(email_header.lstrip())
        if is_release_candidate:
            response.append(expand_template(RELEASE_CANDIDATE_TPL, params))
        else:
            header = expand_template(HEADER_RELEASE_TPL.strip(), params)
            response.append(parawrap.fill(header))
            response.append(expand_template(CHANGE_RELEASE_TPL, params))
    return '\n'.join(response)
