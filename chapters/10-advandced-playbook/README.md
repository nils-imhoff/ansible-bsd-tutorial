# Chapter 10 advanced playbook

```bash
#We create a new directory for our new project
mkdir -p ~/ansible/loop; cd ~/ansible/loop

vim loopdevice.yaml 
- name: 'Manage Disk File' 
  hosts: freebsd-hosts
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
  hosts: freebsd-hosts
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
  hosts: freebsd-hosts
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
  hosts: freebsd-hosts
  become: true
  remote_user: ansible
  gather_facts: false
  vars:
    disk_file: '/root/disk0'
    md_unit: 'md100'
  tasks:
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

vim loopdevice.yaml

- name: 'Manage Disk File '
  hosts: all
  gather_facts: true
  become: true
  remote_user: ansible
  vars:
    disk_file: '/root/disk0'
    md_unit: 'md100'
    vnd_unit: 'vnd0'
  tasks:
    - name: 'Create sparse disk file'
      when: ansible_facts['os_family'] in ['FreeBSD', 'OpenBSD']
      command:
        cmd: "dd if=/dev/zero of={{ disk_file }} bs=1 count=0 seek=1G"
        creates: "{{ disk_file }}"

    - name: 'Attach memory disk on FreeBSD'
      when: ansible_facts['os_family'] == 'FreeBSD'
      command:
        cmd: "mdconfig -a -t vnode -f {{ disk_file }} -u {{ md_unit }}"
        creates: "/dev/{{ md_unit }}"

    - name: 'Create UFS filesystem on FreeBSD'
      when: ansible_facts['os_family'] == 'FreeBSD'
      filesystem:
        fstype: ufs
        dev: "/dev/{{ md_unit }}"

    - name: 'Attach vnode disk on OpenBSD'
      when: ansible_facts['os_family'] == 'OpenBSD'
      command:
        cmd: "vnconfig {{ vnd_unit }} {{ disk_file }}"
        creates: "/dev/{{ vnd_unit }}"

    - name: 'Create FFS filesystem on OpenBSD'
      when: ansible_facts['os_family'] == 'OpenBSD'
      command:
        cmd: "newfs /dev/r{{ vnd_unit }}c"

  
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
