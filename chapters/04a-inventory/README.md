# Exercise 04 - Inventories

We start using inventories by creating a simple example inventory file

```bash
ansible localhost -m package -a 'name=python state=present' -C
pwd
vim hosts
ansible --list all
ansible --list ungrouped
```
