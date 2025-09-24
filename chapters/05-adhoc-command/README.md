# Chapter 5 Adhoc Commands

```bash
ansible-doc -l
ansible-doc -l | wc -l
ansible-doc ping
ansible server -m ping
ansible server -m raw -a '/usr/bin/uptime'
ansible server -m shell -a 'python3 -V'
ansible all -a 'whoami'
MYVAR='myvalue;ls -la /etc/hosts'
echo $MYVAR
ansible freebsd-hosts -m command -a "echo $MYVAR"
ansible freebsd-hosts -m shell -a "echo $MYVAR" 
ansible freebsd-hosts -m file -a "path=/home/ansible/file.txt state=touch mode=700"
ansible freebsd-hosts -m file -a "path=/home/ansible/file2.txt content='foo-bar' force=no mode=700"
ansible freebsd-hosts -m file -a "path=/home/ansible/file.txt mode=600"
ansible freebsd-hosts -m file -a "path=/home/ansible/file.txt mode=600 owner=root group=root"
ansible freebsd-hosts -m file -a "path=/home/ansible/newdir mode=755 state=directory"
ansible freebsd-hosts -m file -a "path=/home/ansible/newdir mode=755 state=directory state=absent"
ansible freebsd-hosts -m package -a "name=nginx state=present"
ansible freebsd-hosts -m copy -a "src=/home/ansible/hosts dest=/tmp/"
ansible freebsd-hosts -m fetch -a "src=/tmp/file dest=/tmp/"
ansible freebsd-hosts -m package -a "name=nginx state=absent" -u root
ansible freebsd-hosts -Kbm package -a "name=nginx state=present"
ansible freebsd-hosts -m lineinfile -a "dest=/tmp/file
state=absent regexp=^pattern1"
ansible freebsd-hosts -m lineinfile -a "dest=/tmp/file
insertafter='^pattern1' line='pattern2 = false'"
ansible freebsd-hosts -m replace -a "dest=/tmp/file
regexp='^replace1 = 123' replace='^replace1 = 321'"
```
