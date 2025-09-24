# Chapter 02 - Ansible Ping Test

Test Ansible connectivity to BSD systems using the ping module.

## Details

In this exercise, we verify that Ansible can communicate with python. The `ping` module tests the  Python interpreter functionality.

## Execution

```bash
ansible localhost -m ping bsd_servers
```

```bash
ansible localhost -m setup -a "filter=*family*"
```
