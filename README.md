About
=====

IMPORTANT: This job is not designed to run every single role in the estate, nor
is it designed to run a collection of roles in a playbook, for that, 
Ansible-Management should be used.

What this job is actually for:

* Running any one of the collection of simple ansible oneshots, 
initially written to solve a few requirements for for loops.

An example oneshot in the form of 'datecheck' has been written.

This example also includes a molecule test setup (using Vagrant/VirtualBox) 
that can be copied and adjusted as needed.

* Running 'roles' that are usually used as part of a larger job in 
Ansible-Management, for example, you might want to run the 'clamav-role' 
against a box, but not want to have to apply the entire pipeline of a project.

Or you might want to apply a 'filebeat' change across the entire estate, 
without having to run every associated playbook at the same time.

This functionality was added after the original 'oneshots' idea. It is both
powerful and dangerous.

Because of the above, any attempt to make 'ansible-oneshots' into a second 
version of Ansible-Management, will be rejected.

README Files
------------

See individual oneshots for their respective README files.
