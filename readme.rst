=========================
spss-sav-pseudonymization
=========================

A command line utility that replaces numeric identifiers in a given SAV
file column with randomly chosen numbers using a UUID generator. Output
of this program is a new SAV file and a file containing the mapping
between old and pseudonymised numbers. This mapping can be reused by
pointing to it via an input parameter.

Running the installation as documented below *should* add a new entry point
to the Python installation scripts directory, though you might have to
add that to your **$PATH** or **%PATH%** (on Windows).

Installation
------------

To install *spss-sav-pseudonymization* and all dependencies into
your Python environment, run:

.. code:: sh

    $   pip install spss-sav-pseudonymization

or..

.. code:: sh

    $   pip install -r requirements.txt
    $   python setup.py install

.. note::
    Depending on your platform, you have to configure SavReaderWriter with
    some additional steps. See `here <https://pythonhosted.org/savReaderWriter/>`_
    for its documentation.

Requirements
^^^^^^^^^^^^

These dependencies will have to be installed:

 - savReaderWriter==3.4.2
 - click==6.7

Example usage
-------------

.. code:: sh

    $   pseudonymise --help

    $   pseudonymise </path/to/sav-file>

    $   pseudonymise </path/to/sav-file> --columns 0,4

    $   pseudonymise </path/to/sav-file> --names Identifier,SecondIdentifier

    $   pseudonymise </path/to/sav-file> --mapping-file <path/to/mapping-file>


Licence
-------

GPLv3

