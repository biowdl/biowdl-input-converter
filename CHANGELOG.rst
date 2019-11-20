==========
Changelog
==========

.. Newest changes should be on top.

.. NOTE: This document is user facing. Please word the changes in such a way
.. that users understand how the changes affect the new version.

0.2.1
---------------
+ Bugfix: R1_md5 and R2_md5 columns are not required to be defined anymore in a
  csv file.

0.2.0
---------------
+ Make sure only one line of additional properties per sample is need in a
  csv file.
+ Fix a bug where an empty field for an additional property in a csv
  samplesheet would be defined as ``""`` instead of ``None``.

0.1.0
---------------
+ Added documentation and readthedocs page
+ Added changelog and release procedures
+ Added test suite with coverage metrics, enabled CI
+ Add validate flag to allow users to validate files
+ Added command line interface with ability to write to stdout and files
+ Added ability to check files for presence and md5sum checking
+ Added sample group -> old style JSON/YAML conversion
+ Added sample group -> new style JSON/YAML conversion
+ Added yaml -> sample group conversion
+ Reworked csv conversion by @DavyCats to fit the new sample group structure
+ Added sample group structure to enable any-to-any conversions
