.. Checkout the Readthedocs theme for an example structure
.. https://github.com/rtfd/sphinx_rtd_theme/tree/master/docs/demo

======================
biowdl-input-converter
======================

.. All the documentation will be in one page for now. With navigation on the
.. side to allow quickly going to the section you want. The documentation is
.. not yet big enough to be benefited by a nested structure.

.. contents:: Table of contents


============
Introduction
============

biowdl-input-converter converts samplesheets that are readable by humans into
a format that can be easily processed by a BioWDL pipeline.

For more information on BioWDL check out the documentation on
https://biowdl.github.io.

============
Samplesheet
============
A samplesheet provides information about fastq files.

- Sample name
- Library name (for each sample usually one library is used to prepare the
  sample for sequencing)
- Readgroup name (which lane on the sequencer was used)
- Location of the forward read (R1) on the filesystem
- Forward read (R1) md5sum
- Location of the reverse read (R2) on the filesystem
- Reverse read (R2) md5sum
- additional properties (if necessary)

A samplesheet can be a comma- or tab-delimited file. An example looks like
this

.. code-block::

    "sample";"library";"readgroup";"R1";"R1_md5";"R2";"R2_md5"
    "s1";"lib1";"rg1";"r1_1.fq";181a657e3f9c3cde2d3bb14ee7e894a3;"r1_2.fq";ebe473b62926dcf6b38548851715820e
    "s2";"lib1";"rg1";"r2_1.fq";7e79b87d95573b06ff2c5e49508e9dbf;"r2_2.fq";dc2776dc3a07c4f468455bae1a8ff872

The md5sums are optional and can be left out:

.. code-block::

    "sample";"library";"readgroup";"R1";"R1_md5";"R2";"R2_md5"
    "s1";"lib1";"rg1";"r1_1.fq";;"r1_2.fq"
    "s2";"lib1";"rg1";"r2_1.fq";;"r2_2.fq"

Additional properties at the sample level can be set additional columns:

.. code-block::

    "sample";"library";"readgroup";"R1";"R1_md5";"R2";"R2_md5";"HiSeq4000";"other_property"
    "s1";"lib1";"rg1";"r1_1.fq";;"r1_2.fq";"yes";"pizza"
    "s2";"lib1";"rg1";"r2_1.fq";;"r2_2.fq";"no";"broccoli"

These files can be easily generated using a spreadsheet program (such as 
Microsoft Excel or LibreOffice Calc). 

Create a table:


+-------+--------+----------+--------+---------+--------+---------+----------+----------------+
|sample |library |readgroup | R1     | R1_md5  |R2      |  R2_md5 |HiSeq4000 | other_property |
+-------+--------+----------+--------+---------+--------+---------+----------+----------------+
|s1     | lib1   |rg1       |r1_1.fq | af283ad |r2_1.fq |         |yes       |                |
+-------+--------+----------+--------+---------|--------+---------+----------+----------------+
|s2     | lib1   | rg1      |r2_1.fq |         |r2_2.fq |d82ca29  | no       |broccoli        |
+-------+--------+----------+--------+---------+--------+---------+----------+----------------+

======
Usage
======

.. argparse::
   :module: biowdl_input_converter
   :func: argument_parser
   :prog: biowdl-input-converter

.. include:: CHANGELOG.rst