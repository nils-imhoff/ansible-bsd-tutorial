# Chapter 09 - Your First Playbook

Create your first Ansible playbook

```bash
#Let's create a folder for our ansible "project"
mkdir -p ~/ansible/simple

#Move in to the new folder
cd ~/ansible/simple 

vim FirstPlay.yaml

- name: My First Play 
  hosts: all
  remote_user: ansible  
  become: true 
  tasks: 
    - name: My First Task 
      package: 
        name: tree 
        state: present 

#Exit the editor

#Install the yamllint feature
sudo pkg install py311-yamllint
sudo yum install yamllint

#We can install the ansible-lint Python modules that will check you Playbook against style guidelines.
yamllint tree.yaml

#We can also check the correct syntax is employed in the playbook.
ansible-playbook tree.yaml --syntax-check

#Going beyond syntax checking we can try the option -C to check the operation without
#implementing change. This works best with the verbose option -v.
ansible-playbook -C -v tree.yaml

ansible freebsd-host -m setup

ansible freebsd-host -m setup -a "filter=*family*"

vim tree.yaml

- name: Install a package
  hosts: all
  become: true
  remote_user: ansible
  gather_facts: true
  tasks:
    - name: Install tree
      package:
        name: tree
        state: present
    - name: Print Progress
      debug:
        msg: "This is {{ ansible_distribution }}" # {{ ansible_os_family }}

find /usr/lib -name 'debug.py'

find /usr/lib -name 'package.py'

ansible-doc -l 

ansible-doc user
```
