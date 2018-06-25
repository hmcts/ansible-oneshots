Testing
=======

Azure Molecule Tests
============================

This assumes you already have a molecule (version 2) test set up, for example, this "role" (ansible-oneshots/centos-check) already has both a Libvirt entry, and a VirtualBox entry, both using the Vagrant driver.

The default, VirtualBox, is invoked with the following:

```
[master] [adam@verence centos-check]$ pwd
/home/adam/Projects/MoJ/GitHub/ansible-oneshots/centos-check
[master] [adam@verence centos-check]$ molecule test
```

If I wanted to invoke the Libvirt test, I would run:

```
[master] [adam@verence centos-check]$ molecule test -s libvirt
```

This is because we've configured 'libvirt' as a scenario, which uses Libvirt.

Adding Our Azure Example
-------------------------------------------------------------

Say you're not in a position to use VirtualBox or Libvirt/KVM, do you give up and ask someone else to do it? No! You use Azure!

We need a prerequisite (that isn't ansible/molecule2):

```
[master] [adam@verence centos-check]$ sudo pip install 'ansible[azure]'
```

First, we initialize the role:

```
[master] [adam@verence centos-check]$ molecule init scenario -d azure -s azure -r centos-check
```

This can be broken down into us:

• Choosing to create a new scenario.
• Choosing to use Azure as our driver.
• Choosing the scenario name 'azure.'
• Specifying the name of the role, 'centos-check.'

Now looking in `molecule/azure/molecule.yml` should show something like:

```
---
dependency:
  name: galaxy
driver:
  name: azure
lint:
  name: yamllint
platforms:
  - name: instance
provisioner:
  name: ansible
  lint:
    name: ansible-lint
scenario:
  name: azure
verifier:
  name: testinfra
  lint:
    name: flake8
```

Setting Up Our Azure Example
---------------------------------------------------------------------

Out of the box, this won't work.

1. There's no credentials passed to the module, meaning it won't be able to connect to Azure.
2. It will use the default Resource Group 'molecule' which is likely already taken.

To solve 1, do the following:

```
[master] [adam@verence centos-check]$ export AZURE_SECRET=*************
[master] [adam@verence centos-check]$ export AZURE_TENANT=********-****-****-****-************
[master] [adam@verence centos-check]$ export AZURE_SUBSCRIPTION_ID=********-****-****-****-************ # Make sure this is sandbox subscription.
[master] [adam@verence centos-check]$ export AZURE_CLIENT_ID=********-****-****-****-************
```

To solve 2, we have to change the way the resource group is created, open `molecule/azure/create.yml` in vim, and ensure the `vars` stanza looks like:

```
  vars:
    resource_group_name: centoscheckmoleculeRG
    location: uksouth
    ssh_user: centoscheckmoleculeuser
    ssh_port: 22
    virtual_network_name: centoscheckmoleculeVnet
    subnet_name: centoscheckmoleculeSubnet
    keypair_path: "{{ lookup('env', 'MOLECULE_EPHEMERAL_DIRECTORY') }}/ssh_key"
```

We need to do the same to the 'destroy' playbook:

```
  vars:
    resource_group_name: centoscheckmoleculeRG
```

We also need to ensure that we're not leaving anything behind following a run, 
to that end, we adjust the 'destroy.yml' playbook, adding the following bits:

```
    location: uksouth
  tasks:

    # Counterintuitive create to allow for destroy to work on new run.
    - name: Create resource group
      azure_rm_resourcegroup:
        name: "{{ resource_group_name }}"
        location: "{{ location }}"
```

Note the 'location' addition under the vars above. We also add:

```
    # Added to account for lingering NSG, Storage Account, and VNET in RG.
    - name: Delete molecule resource group
      azure_rm_resourcegroup:
        name: "{{ resource_group_name }}"
        force: true
        state: absent
      register: rg
```

Running Our Azure Example
-----------------------------------------------------------------

We run the molecule test with:

```
[master ?] [adam@verence centos-check]$ molecule test -s azure
```

I have found that it's easiest to watch the results by going to the Azure portal, and looking up the Resource Group, e.g. 'centoscheckmoleculerg' in the search field.

ToDo:
----------

• I origionally had the resource group and other bits randomly generated using an Ansible lookup pipe, but this caused issues when used with destroy. Need a way to make the create/destroy playbooks more generic, but keeping the unique names to the individual roles (centos-check.)
* Look into a way of templating this, so we're creating tests consistently.
