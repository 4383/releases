=======================
Ussuri Release Schedule
=======================

.. note::

   Deadlines are generally the Thursday of the week on which they are noted
   below. Exceptions to this policy will be explicitly mentioned in the event
   description.

21 October 2019 - 15 May 2020 (30 weeks)

.. datatemplate::
   :source: schedule.yaml
   :template: schedule_table.tmpl

.. ics::
   :source: schedule.yaml
   :name: Ussuri

`Subscribe to iCalendar file <schedule.ics>`_

Cross-project events
====================

.. _u-goals-research:

Ussuri Goals Research
---------------------

Pre-cycle planning and investigation into `the community-wide goals
for Ussuri <https://governance.openstack.org/tc/goals/ussuri/index.html>`__.

.. _u-summit:

Open Infrastructure Summit
--------------------------

The Open Infrastructure Summit happens during this week in Shanghai, China. It
will include a “Forum” in which people from all parts of our community will
gather to give feedback on the last release (Train) and discuss requirements
for future releases.

.. _u-1:

Ussuri-1 milestone
------------------

12 December, 2019 is the Ussuri-1 milestone. See project-specific notes for
relevant deadlines.

.. _u-goals-ack:

Ussuri Community Goals Acknowledgement
--------------------------------------

Teams should prepare their acknowledgement of `the community-wide
goals for Ussuri
<https://governance.openstack.org/tc/goals/ussuri/index.html>`__.

.. _u-2:

Ussuri-2 milestone
------------------

13 February, 2020 is the Ussuri-2 milestone. See project-specific notes for
relevant deadlines.

.. _u-final-lib:

Final release for non-client libraries
--------------------------------------

Libraries that are not client libraries (Oslo and others) should issue their
final release during this week. That allows to give time for last-minute
changes before feature freeze.

.. _u-3:

Ussuri-3 milestone
------------------

9 April, 2020 is the Ussuri-3 milestone. See project-specific notes for
relevant deadlines.

.. _u-goals-complete:

Ussuri Community Goals Completed
--------------------------------

Teams should prepare their documentation for completing `the
community-wide goals for Ussuri
<https://governance.openstack.org/tc/goals/ussuri/index.html>`__.

.. _u-extra-atcs:

Extra-ATCs deadline
-------------------
Project teams should identify contributors who have had a significant impact
this cycle but who would not qualify for ATC status using the regular process
because they have not submitted a patch. Those names should be added to the
governance repo for consideration as ATC for the future.

.. _u-ff:

Feature freeze
--------------

The Ussuri-3 milestone marks feature freeze for projects following the
`release:cycle-with-rc`_ model. No featureful patch should be landed
after this point. Exceptions may be granted by the project PTL.

.. _release:cycle-with-rc: https://releases.openstack.org/reference/release_models.html#cycle-with-rc

.. _u-rf:

Requirements freeze
-------------------

After the Ussuri-3 milestone, only critical requirements and constraints changes
will be allowed. Freezing our requirements list gives packagers downstream an
opportunity to catch up and prepare packages for everything necessary for
distributions of the upcoming release. The requirements remain frozen until the
stable branches are created, with the release candidates.

.. _u-final-clientlib:

Final release for client libraries
----------------------------------

Client libraries should issue their final release during this week, to match
feature freeze.

.. _u-soft-sf:

Soft StringFreeze
-----------------

You are no longer allowed to accept proposed changes containing modifications
in user-facing strings. Such changes should be rejected by the review team and
postponed until the next series development opens (which should happen when RC1
is published).

.. _u-mf:

Membership Freeze
-----------------

Projects must participate in at least two milestones in order to be considered
part of the release. Projects made official after the second milestone, or
which fail to produce milestone releases for at least one of the first and
second milestones as well as the third milestone, are therefore not considered
part of the release for the cycle. This does not apply to cycle-trailing
packaging / lifecycle management projects.

.. _u-rc1:

RC1 target week
---------------

The week of 20 April is the target date for projects following the
`release:cycle-with-rc`_ model to issue their first release candidate.

.. _u-hard-sf:

Hard StringFreeze
-----------------

This happens when the RC1 for the project is tagged. At this point, ideally
no strings are changed (or added, or removed), to give translators time to
finish up their efforts.

.. _u-finalrc:

Final RCs and intermediary releases
-----------------------------------

The week of 4 May is the last week to issue release candidates or
intermediary releases before release week. During release week, only
final-release-critical releases will be accepted (at the discretion of the
release team).

.. _u-final:

Ussuri release
--------------

The Ussuri coordinated release will happen on Wednesday, 13 May, 2020.

Project-specific events
=======================

PTL Elections
-------------

