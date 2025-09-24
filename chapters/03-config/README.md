# Exercise 03 - Ansible Config file

Ansible checks for configuration in the following order:

- `ANSIBLE_CONFIG` (environment variable)
- `ansible.cfg` (in the current working directory)
- `.ansible.cfg` (in the user's home directory)
- `/usr/local/etc/ansible/ansible.cfg` (system-wide default)

[Documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html)

## Execution

```bash
ansible --version
less /usr/local/etc/ansible/ansible.cfg
```

```bash
ansible localhost -m package -a 'name=nginx state=present'
```

```bash
ansible localhost -m package -b -a 'name=nginx state=present'
```

```bash
cd
touch .ansible.cfg
ls -la
ansible --version
```

```bash
mkdir nginx
cd nginx
touch ansible.cfg
ansible --version
cd
ansible --version
rm -rf .ansible.cfg
```

```bash
ansible-config init --disabled > ansible.cfg
less ansible.cfg
rm ansible.cfg
cd nginx
vim ansible.cfg
ansible-config view
ansible-config dump
ansible-config dump --only-change
```
