=======================
 Stein Release Schedule
=======================

3 September 2018 - 8 April 2019 (32 weeks)

.. datatemplate::
   :source: schedule.yaml
   :template: schedule_table.tmpl

.. ics::
   :source: schedule.yaml
   :name: Stein

`Subscribe to iCalendar file <schedule.ics>`__

.. note::

   With the exception of the final release date and cycle-trailing release
   date, deadlines are generally the Thursday of the week on which they are
   noted above. Exceptions to this policy will be explicitly mentioned in the
   event description.

Cross-project events
====================

.. _s-tc-email-deadline:

Stein TC Election
-----------------

Stein TC Election Email Deadline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Contributors that will be in the electorate for the upcoming election
should confirm their gerrit email addresses by this date (September 9th, 2018
at 00:00 UTC). Electorate rolls are generated after this date and ballots will
be sent to the listed gerrit email address.

.. _s-tc-nominations:

Stein TC Election Nomination Begins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Technical committee candidates interested in serving for the next calendar year
should announce their candidacies and platforms during this week.  Please see
the `Election site`_ for specific timing information.

.. _s-tc-campaigning:

Stein TC Election Campaigning Begins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The electorate has time to ask candidates questions about their platforms
and debate topics before polling begins.  Please see the `Election site`_ for
specific timing information.

.. _s-tc-polling:

Stein TC Election Polling Begins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Election polling week for open seats on the TC.  Please see the
`Election site`_ for specific timing information.

Train TC Election
-----------------

.. _t-email-deadline:

Train Election Email Deadline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Contributors that will be in the electorate for the upcoming PTL and TC elections
should confirm their gerrit email addresses by this date (February 19th, 2019
at 00:00 UTC). Electorate rolls are generated after this date and ballots will
be sent to the listed gerrit email address.

.. _t-tc-nominations:

Train TC Election Nomination Begins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Technical committee candidates interested in serving for the next calendar year
should announce their candidacies and platforms during this week.  Please see
the `Election site`_ for specific timing information.

.. _t-tc-campaigning:

Train TC Election Campaigning Begins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The electorate has time to ask candidates questions about their platforms
and debate topics before polling begins.  Please see the `Election site`_ for
specific timing information.

.. _t-tc-polling:

Train TC Election Polling Begins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Election polling week for open seats on the TC.  Please see the
`Election site`_ for specific timing information.

Keystone
--------

.. _s-keystone-spec-proposal-freeze:

Keystone Spec Proposal Freeze
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All Keystone specs targeted to Stein must be submitted to the keystone-specs
repository by the end of the week.

.. _s-keystone-spec-freeze:

Keystone Spec Freeze
^^^^^^^^^^^^^^^^^^^^

All Keystone specs targeted to Stein must be approved by the end of the week.

.. _s-keystone-fpfreeze:

Keystone Feature Proposal Freeze
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All new Keystone features must be proposed and substantially completed, with
unit tests and documentation by the end of the week.

.. _s-keystone-ffreeze:

Keystone Feature Freeze
^^^^^^^^^^^^^^^^^^^^^^^

All new Keystone features must be merged by the end of the week.

.. _s-goals-research:

Stein Goals Research
--------------------

Pre-cycle planning and investigation into `the community-wide goals
for Stein <https://governance.openstack.org/tc/goals/stein/index.html>`__.

.. _s-ptg:

Stein Project Team Gathering (PTG)
----------------------------------

`Project team gathering <https://www.openstack.org/ptg>`__ for the Stein
cycle 10 - 14 September in Denver, Colorado, USA.

.. _s-1:

Stein-1 milestone
-----------------

25 October 2018 is the Stein-1 milestone.

.. _s-goals-ack:

Stein Community Goals Acknowledgement
-------------------------------------

Teams should prepare their acknowledgement of `the community-wide
goals for Stein
<https://governance.openstack.org/tc/goals/stein/index.html>`__.

.. _s-summit:

OpenStack Summit
----------------

The OpenStack Summit happens during this week in Berlin, Germany. It will
include a "Forum" in which people from all parts of our community will gather
to give feedback on the last release (Rocky) and discuss requirements for the
next development cycle (Stein).

.. _s-2:

Stein-2 milestone
-----------------

10 January 2019 is the Stein-2 milestone.

.. _s-final-lib:

Final release for non-client libraries
--------------------------------------

Libraries that are not client libraries (Oslo and others) should issue their
final release during this week. That allows to give time for last-minute
changes before feature freeze.

.. _s-3:

Stein-3 milestone
-----------------

28 February 2019 is the Stein-3 milestone.

.. _s-goals-complete:

Stein Community Goals Completed
-------------------------------

Teams should prepare their documentation for completing `the
community-wide goals for Stein
<https://governance.openstack.org/tc/goals/stein/index.html>`__.

.. _s-ff:

Feature freeze
--------------

The Stein-3 milestone marks feature freeze for projects following the
`release:cycle-with-rc`_ model. No featureful patch should be landed
after this point. Exceptions may be granted by the project PTL.

.. _s-rf:

Requirements freeze
-------------------

After the Stein-3 milestone, only critical requirements and constraints changes
will be allowed. Freezing our requirements list gives packagers downstream an
opportunity to catch up and prepare packages for everything necessary for
distributions of the upcoming release. The requirements remain frozen until the
stable branches are created, with the release candidates.

.. _s-final-clientlib:

Final release for client libraries
----------------------------------

Client libraries should issue their final release during this week, to match
feature freeze.

.. _s-soft-sf:

Soft StringFreeze
-----------------

You are no longer allowed to accept proposed changes containing modifications
in user-facing strings. Such changes should be rejected by the review team and
postponed until the next series development opens (which should happen when RC1
is published).

.. _s-mf:

Membership Freeze
-----------------

Projects made official after the second milestone, are not considered
part of the release for the cycle. This does not apply to cycle-trailing
packaging / lifecycle management projects.

.. _s-rc1:

RC1 target week
---------------

This week is the target for projects following the
`release:cycle-with-rc`_ model to issue their first release candidate,
with a deadline of 21 March 2019.

.. _release:cycle-with-rc: https://releases.openstack.org/reference/release_models.html#cycle-with-rc

.. _s-hard-sf:

Hard StringFreeze
-----------------

This happens when the RC1 for the project is tagged. At this point, ideally
no strings are changed (or added, or removed), to give translator time to
finish up their efforts.

.. _s-finalrc:

Final RCs and intermediary releases
-----------------------------------

The week of 1 April 2019 is the last week to issue release candidates or
intermediary releases before release week. During release week, only
final-release-critical releases will be accepted (at the discretion of the
release team).

.. _s-cycle-highlights:

Cycle highlights marketing deadline
-----------------------------------

Cycle highlights need to be added to the release deliverables by this point to
be included in any marketing release messaging. Highlights may be added after
this point, but they will likely only be useful for historical purposes.

See the `project team guide <https://docs.openstack.org/project-team-guide/release-management.html#cycle-highlights>`_
for more details and instructions on adding these highlights.

.. _s-release:

Stein release
-------------

The Stein coordinated release will happen on 10 April 2019.

.. _s-trailing-release:

Stein cycle-trailing release deadline
-------------------------------------

The release deadline for projects using the release:cycle-trailing model that
follow the main release cycle is set to 11 July, 2019.

Project-specific events
=======================

PTL Elections
-------------

.. _t-ptl-nominations:

Train PTL self-nomination
^^^^^^^^^^^^^^^^^^^^^^^^^

Project team lead candidates for the Stein cycle should announce their
candidacy during this week.  Refer to the `Election Site`_ for exact deatls.

.. _t-ptl-poll:

Train PTL Election Polling Begins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Election week for Project team leads (where an election must be held to
determine the winner).  Refer to the `Election Site`_ for exact deatls.

.. _Election site: https://governance.openstack.org/election/

Manila
------

.. _s-manila-spec-freeze:

Manila Spec Freeze
^^^^^^^^^^^^^^^^^^

All Manila specs must be approved by 8 Nov 2018 (23:59 UTC).

.. _s-manila-driver-deadline:

Manila New Driver Submission Deadline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The deadline for submitting new backend drivers to to Manila is 10 Jan 2019
(23:59 UTC). New drivers must be substantially complete, with unit tests, and
passing 3rd party CI by this date. Drivers do not need to be merged until the
feature freeze date, but drivers that don't meet this deadline will not be
considered at all for Rocky.

.. _s-manila-fp-freeze:

Manila Feature Proposal Freeze
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All new Manila features must be proposed and substantially complete, with unit
tests by 21 February 2019 (23:59 UTC).

Cinder
------

.. _s-cinder-spec-freeze:

Cinder Spec Freeze
^^^^^^^^^^^^^^^^^^

All Cinder Specs must be approved by 10 Jan 2019 (23:59 UTC).

.. _s-cinder-driver-deadline:

Cinder New Driver Submission Deadline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The deadline for submitting new backend drivers to Cinder is 10 Jan 2019 (23:59 UTC).
New drivers must be complete with unit tests at this point in time.  The backend
driver must also have a 3rd Party CI running reliably and the driver must be
merged at this point to be included in the Stein release.

.. _s-cinder-target-driver-deadline:

Cinder New Target Driver Submission Deadline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The deadline for submitting new target drivers to Cinder is 10 Jan 2019 (23:59 UTC).
New target drivers must be complete with unit tests at this point in time.  The target
driver must also have a 3rd Party CI running reliably and the target driver must
be merged at this point to be included in the Stein release.

.. _s-cinder-fp-freeze:

Cinder Feature Proposal Freeze
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All new Cinder features must be proposed and substantially complete with unit tests
by 07 Mar 2019 (23:59 UTC).

Oslo
----

.. _s-oslo-feature-freeze:

Oslo Feature Freeze
^^^^^^^^^^^^^^^^^^^

All new Oslo features must be proposed and substantially complete, with unit
tests by the end of the week.
