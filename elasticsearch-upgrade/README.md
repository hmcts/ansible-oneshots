Elasticsearch Upgrade
=====================

Used to perform a rolling upgrade of an Elasticsearch cluster

Notes
-----

The play does not currently handle the repo files for Yum.
Prior to running the play you'll need to make sure the relevant repos
are correctly in place.

Variables
---------

* elk_dst_version - target version of ELK that we're heading towards.

* elk_rolling_upgrade - If true then we're only performing a minor upgrade 
and we can perform a rolling restart, otherwise a full cluster shutdown is 
required for a major version number upgrade.

* elk_es_host - elasticsearch host used for monitoring cluster health

* elk_es_user - username with suitable privileges for cluster maintenance

* elk_es_pass - password for above user

* elk_plugin_base_url - base URL of where to find the plugin ZIP files

