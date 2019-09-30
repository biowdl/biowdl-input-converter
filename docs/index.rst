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

======
Usage
======

.. argparse::
   :module: biowdl_input_converter
   :func: argument_parser
   :prog: biowdl-input-converter

.. include:: CHANGELOG.rst
