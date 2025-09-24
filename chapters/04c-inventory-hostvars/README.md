# Chapter 4 Hostvars

We can define host specific variables in the inventory using the following commands

```bash
mkdir {host,group}_vars
ls
ansible ctrlhost -m ping ctrlhost
ansible localhost -m ping
echo "ansible_connection: local" > host_vars/localhost
cat host_vars/localhost
ansible -m ping ctrlhost
```
