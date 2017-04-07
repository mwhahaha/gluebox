===============================
gluebox
===============================

puppet openstack version manipulating tools

* Free software: Apache license

Why gluebox?
------------

I needed a random name and I used a tool_ to generate one. So gluebox it is.

.. _tool: http://mrsharpoblunto.github.io/foswig.js/


Features
--------

* Single or Multiple modules can be updated at once
* Different version manipulations (major, minor, static, -dev updates)
* Automatically updates metadata.json and sorts it via keys

TODO:

* Automatically updates reno version numbers
* Generates release yaml for OpenStack releases_ repo

.. _releases: https://git.openstack.org/cgit/openstack/releases


How to use
----------

remove -dev from version numbers (example: 10.0.0-dev -> 10.0.0)::

    gluebox git checkout -f modules.txt --topic prep-release-10.0.0
    gluebox bump dev -f modules.txt
    gluebox git commit -F release-message.txt -f modules.txt
    gluebox git review -f modules.txt
    gluebox git cleanup -f modules.txt

minor version bump with -dev (example: 10.0.0 -> 10.1.0-dev)::

    gluebox git checkout -f modules.txt --topic minor-version-10.1.0-dev
    gluebox bump minor -f modules.txt --dev
    gluebox git commit -F release-message.txt -f modules.txt
    gluebox git review -f modules.txt
    gluebox git cleanup -f modules.txt

major version bump with -dev (example: 10.0.0 -> 11.0.0-dev)::

    gluebox git checkout -f modules.txt --topic major-version-11.0.0-dev
    gluebox bump minor -f modules.txt --dev
    gluebox git commit -F release-message.txt -f modules.txt
    gluebox git review -f modules.txt
    gluebox git cleanup -f modules.txt


static version: (example: 10.1.1)::

    gluebox git checkout -m puppet-openstacklib --topic static-version-10.1.1
    gluebox bump minor -m puppet-openstacklib --static-version 10.1.1
    gluebox git commit -F release-message.txt -m puppet-openstacklib
    gluebox git review -m puppet-openstacklib
    gluebox git cleanup -m puppet-opesntacklib


