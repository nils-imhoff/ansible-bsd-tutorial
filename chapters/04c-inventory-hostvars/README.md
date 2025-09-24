# Chapter 4 Hostvars

We can define host specific variables in the inventory using the following commands

```bash
mkdir {host,group}_vars
ls
ansible -m ping ctrlhost
ansible -m localhost
echo "ansible_connection: local" > host_vars/localhost
cat host_vars/localhost
ansible -m ping ctrlhost
```