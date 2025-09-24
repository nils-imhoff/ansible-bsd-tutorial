# Chapter 4 Inventory Groups

Host can be grouped in the inventory. This could be usefull if we plan to work with variables an playbooks

```bash
less /usr/local/etc/ansible/hosts
vim hosts
ansible --list all
ansible --list ungrouped
ansible --list server
ansible -m ping server
```
