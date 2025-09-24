# Chapter 14 extras

We can create compressed tar archives using Ansible and the archive module. The backup is
local unless the destination path specified is a network mount. Note that this is just a task we
can store this as its own YAML file but it cannot be executed independently.

```bash
#A new project folder
mkdir -p ansible/extra

#We create a task
vim backup.yaml

- name: 'Backup /etc directory on system'
  archive:
    path: '/etc/'
    dest: "/tmp/etc-{{ ansible_hostname }}.tgz"

#Now the playbook
vim archive.yaml

- name: 'Backup and schedule backups'
  hosts: 'all'
  become: true
  gather_facts: true
  tasks:
  - include_tasks: backup.yaml


#Now let the playbook run
ansible-playbook archive.yaml

#Did it work
ls /tmp/
```

To schedule a similar backup we can use the cron system.

```bash
#We create a new task
vim schedule.yaml

- name: 'Scheduled backup of /etc'
  ansible.builtin.cron:
    name: 'backup /etc'
    weekday: '5'
    minute: '0'
    hour: '2'
    user: 'root'
    job: "tar -czf /tmp/etc-{{ ansible_hostname }}.tgz /etc"
    cron_file: etc_backup


#We extend our playbook
vim archive.yaml

- name: 'Backup and schedule backups'
  hosts: 'all'
  become: true
  gather_facts: true
  tasks:
  - include_tasks: backup.yaml
  - include_tasks: schedule.yaml

#Run the playbook
ansible-playbook archive.yaml

#Was the job created?
sudo ls /etc/cron.d/

sudo cat /etc/cron.d/etc_backup
```

We can import playbooks

```bash
#We import the playbooks
vim playbook.yaml

- import_playbook: archive.yaml

#And the last and final check
ansible-playbook playbook.yaml
```
