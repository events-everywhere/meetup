Meetup
======
Simple Python command line script for creating, updating and displaying meetup details.

Requirements
------------
`requests <https://pypi.python.org/pypi/requests>`

Command examples
----------------
*All examples assume you have already setup your api key in config.json!*

.. code-block:: bash

    $ ./meetup.py -h
    $ ./meetup.py create --title 'New event' --desc 'An awesome event descritpion' --date '2013-11-11 16:16'
    $ ./meetup.py update --id 142805422 --desc 'An awesome event descritpion update'
    $ ./meetup.py details --id 'http://www.meetup.com/Sydney-Linux-User-Group/events/142805422/'
    $ ./meetup.py details --id 142805422

