# Chapter 15

We can manager user-accounts with ansible

```bash

#We create a new project directory
mkdir -p ansible/user

#Create a new user

vim user.yaml

- name: 'Manage User Account'
  hosts: all
  become: true
  remote_user: ansible
  gather_facts: false
  tasks:
    - name: 'Manage User'
      user:
        name: 'tutorial'
        state: 'present'
        shell: '/bin/sh'

#Change the playbook a bit
vim user.yaml

- name: 'Manage User Account'
  hosts: all 
  become: true 
  remote_user: ansible
  gather_facts: false 
  tasks: 
    - name 'Manage User' 
      user: 
        name: "{{ user_account | default('tutorial') }}" 
        state: 'present' 
        shell: '/bin/sh' 


#Now we can use the variables
ansible-playbook -e user_account=joe user.yaml

#Without the variable => default will be used
ansible-playbook user.yaml


#Change the playbook a bit
vim user.yaml

- name: 'Create and Manage Users'
  hosts: all
  become: true
  remote_user: ansible
  gather_facts: false
  tasks:
    - name: 'Create User Account'
      user:
        name: "{{ user_account | default('tutorial') }}"
        state: 'present'
        shell: '/bin/sh'
      when: user_create == 'yes'  
    - name: 'Delete User Account'
      user:
        name: "{{ user_account | default('tutorial') }}"
        state: 'absent'
        remove: true
      when: user_create == 'no' 


#Now we can use the variables
ansible-playbook -e user_account=joe -e user_create=yes user.yaml -v

ansible-playbook -e user_account=joe -e user_create=no user.yaml -v

#Without the variable => default will be used
ansible-playbook -e user_create=no user.yaml -v

ansible-playbook -e user_create=yes user.yaml -v

#Change the playbook a bit
vim user.yaml

---
- name: 'Create and Manage Users'
  hosts: all
  become: true
  gather_facts: false
  tasks:
    - name: 'Create User Account'
      user:
        name: "{{ user_account | default('ansible') }}"
        state: 'present'
        shell: '/bin/sh'
        password: "{{ 'Password1' | password_hash('sha512') }}"
        update_password: 'on_create'
      when: user_create == 'yes'

    - name: 'Delete User Account'
      user:
        name: "{{ user_account | default('ansible') }}"
        state: 'absent'
        remove: true
      when: user_create == 'no'

ansible-playbook -e user_account=joe -e user_create=yes user.yaml -v

vim localuser.yaml

---

- name: 'Manage Local Account'
  hosts: 'ctrlnode'
  become: true
  gather_facts: false
  tasks:
    - name: 'Manage User Account'
      user:
        name: "{{ user_account }}"
        state: 'present'
        generate_ssh_key: true
        ssh_key_type: 'ecdsa'
        ssh_key_file: '.ssh/id_ecdsa'
    
    
ansible-playbook -e user_account=$USER localuser.yaml


#Change the playbook a bit
vim user.yaml

---

- name: 'Create and Manage Users'
  hosts: all
  become: true
  gather_facts: false
  tasks:
    - name: 'Create User Account'
      user:
        name: "{{ user_account | default('ansible') }}"
        state: 'present'
        shell: '/bin/sh'
        password: "{{ 'Password1' | password_hash('sha512') }}"
        update_password: 'on_create'
      when: user_create == 'yes'  
    - name: 'Allow SSH Authentication via key to new remote account'
      authorized_key:
        user: "{{ user_account | default('ansible') }}"
        state: 'present'
        manage_dir: true
        key: "{{ lookup('file', '/home/' ~ user_account ~ '/.ssh/id_ecdsa.pub') }}"
      when: user_create == 'yes'  
    - name: 'Delete User Account'
      user:
        name: "{{ user_account | default('ansible') }}"
        state: 'absent'
        remove: true
      when: user_create == 'no'


#Start the playbook
ansible-playbook user.yaml -e user_create=yes -e user_account=$USER

#Change the playbook a bit
vim user.yaml

---

- name: 'Manage Local Account'
  hosts: 'ctrlnode'
  become: true
  gather_facts: false
  tasks:
    - name: 'Manage User Account'
      user:
        name: 'vagrant'
        state: 'present'
        generate_ssh_key: true
        ssh_key_type: 'ecdsa'
        ssh_key_file: '.ssh/id_ecdsa'

- name: 'Create and Manage Remote Ansible User'
  hosts: all
  become: true
  gather_facts: false
  tasks:
    - name: 'Create User Account, SSH Auth and Sudoers Entry'
      block:
        - name: 'Create Ansible User'
          user:
            name: 'ansible'
            state: 'present'
            shell: '/bin/bash'
            password: "{{ 'Password1' | password_hash('sha512') }}"
            update_password: 'on_create'       
        - name: 'Allow SSH Authentication via key for vagrant account to new remote account'
          authorized_key:
            user: 'ansible'
            state: 'present'
            manage_dir: true
            key: "{{ lookup('file', '/home/' ~ user_account ~ '/.ssh/id_ecdsa.pub') }}"
        - name: 'Copy Sudoers file' 
          copy:
            dest: '/usr/local/etc/sudoers.d/ansible'
            content: 'ansible ALL=(root) NOPASSWD: ALL'
      when: user_create == 'yes'        
    - name: 'Delete User Account'
      user:
        name: 'ansible'
        state: 'absent'
        remove: true
      when: user_create == 'no'


#Start the playbook
ansible-playbook user.yaml -e user_create=yes -e user_account=$USER

#Lets check
ssh -i ~/.ssh/id_ecdsa ansible@centos

sudo -l

ssh -i ~/.ssh/id_ecdsa ansible@ubuntu

sudo -l
```
