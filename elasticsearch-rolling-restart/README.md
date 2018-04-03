Elasticsearch Rolling Restart
=============================

Performs a rolling restart of the Elasticsearch cluster.
Useful when apply certain types of configuration changes.

Variables
=========

elk_es_host - Host used for checking cluster health.  The ELK LB VS on the F5s
should be fine for this.

elk_es_user - Username that has sufficient cluster priveleges to view cluster
health. Default's to 'elastic' as that is an out of the box built-in system
user name.

elk_es_pass - Password for the above user.  Details for this should be in
vault.
