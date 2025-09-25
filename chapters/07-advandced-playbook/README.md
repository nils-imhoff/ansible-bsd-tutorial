# Chapter 10 advanced playbook

```bash
#We create a new directory for our new project
mkdir -p ~/ansible/loop; cd ~/ansible/loop

vim loopdevice.yaml 
- name: 'Manage Disk File' 
  hosts: freebsd_hosts
  remote_user: ansible
  become: true
  gather_facts: false
  tasks:
    - name: "Create sparse Disk File"
      command:
        cmd: 'truncate -s 1G /root/disk0'


#We extend the playbook

vim loopdevice.yaml

- name: 'Manage Disk File' 
  hosts: freebsd_hosts
  become: true
  remote_user: ansible
  gather_facts: false
  tasks:
    - name: "Create sparse Disk File"
      command:
        cmd: 'truncate -s 1G /root/disk0'
        creates: '/root/disk0'

#We adjust the playbook

vim loopdevice.yaml

- name: 'Manage Disk File'
  hosts: freebsd_hosts
  become: true
  remote_user: ansible
  gather_facts: false
  vars:
    disk_file: '/root/disk0'
    lmd_unit: 'md100'
  tasks:
    - name: 'Create sparse disk file'
      command:
        cmd: "truncate -s 1G {{ disk_file }}"
        creates: "{{ disk_file }}"

vim loopdevice.yaml

- name: 'Manage Disk File'
  hosts: freebsd_hosts
  become: true
  remote_user: ansible
  gather_facts: false
  vars:
    disk_file: '/root/disk0'
    md_unit: 'md100'
  tasks:
    - name 'Install required packages'
      package:
        name: 'util-linux'
        state: present
    - name: 'Create sparse disk file'
      command:
        cmd: "truncate -s 1G {{ disk_file }}"
        creates: "{{ disk_file }}"

    - name: 'Attach memory disk device'
      command:
        cmd: "mdconfig -a -t vnode -f {{ disk_file }} -u {{ md_unit }}"
        creates: "/dev/{{ md_unit }}"

    - name: 'Create UFS filesystem'
      filesystem:
        fstype: ufs
        dev: "/dev/{{ md_unit }}"

vim install-packages.yaml
  
- name: Install multiple packages
  package:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - git
    - htop
    - tmux

```
