defusedcsv
==========

.. image:: https://img.shields.io/pypi/v/defusedcsv.svg
   :target: https://pypi.python.org/pypi/defusedcsv

.. image:: https://travis-ci.org/raphaelm/defusedcsv.svg?branch=master
   :target: https://travis-ci.org/raphaelm/defusedcsv

.. image:: https://codecov.io/gh/raphaelm/defusedcsv/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/raphaelm/defusedcsv

If your Python application offers CSV export of user-generated data, that user-generated data might contain malicious
payloads that might trigger vulnerabilities in the spreadsheet software of the user that downloads the file (i.e. MS
Excel or LibreOffice).

This library tries to mitigate that by prepending all cells starting with ``@``, ``+``,
``-``, ``=``, ``|`` or ``%`` with an apostrophe ``'`` and additionally replacing all
``|`` characters in these cells with ``\|``. This will of course change the resulting
CSV files, but Excel will not display the ``'`` character to the user.

Tested with Python 3.4 to 3.6.

Usage
-----

This library acts as a drop-in replacement for the standard library's ``csv`` module. You can use it by just replacing
``import csv`` with ``from defusedcsv import csv`` in your code.

Useful Links
------------

* `CSV Injection Software Attack | OWASP Foundation <https://owasp.org/www-community/attacks/CSV_Injection>`_
* `Comma Separated Vulnerabilities | Context Information Security <https://www.contextis.com/resources/blog/comma-separated-vulnerabilities/>`_
* `CSV Injection Mitigations & Dangers | ZeroSec - Adventures In Information Security <https://blog.zsec.uk/csv-dangers-mitigations/>`_

License
-------
The code in this repository is published under the terms of the Apache License. 
See the LICENSE file for the complete license text.

This project is maintained by Raphael Michel <mail@raphaelmichel.de>. See the
AUTHORS file for a list of all the awesome folks who contributed to this project.
