Restrict Access
=====================

Small play to restrict access to a host quickly.

Notes
-----

Used to quickly limit access to a host to a single IP address.

Variables
---------

IP address.

Testing
-------

In order to test locally, please ensure you have Vagrant, VirtualBox, and 
Molecule installed, along with the dependencies required.
```
$ molecule test
```

Running
-------

This role will fail without a specified IP address as an extra var.

`only_source_address` should be specified with the IP of the host you want
to lock down to, this will probably always be the Jenkins IP address (as it's
the one running the role.)

Reverting
---------

By default, this role is for restricting access, however this can be reverted
by setting the variable 'revert_block' to true (using an extra-var.)

To accomplish a reversion, something like the below would be used:

```
only_source_address=<IP You Whitelisted Previously>, revert_block=true
```
