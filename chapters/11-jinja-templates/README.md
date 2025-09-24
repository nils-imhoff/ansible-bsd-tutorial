# Chapter 11 jinja templates

```bash
mkdir -p ~/ansible/nginx
cd ~/ansible/nginx

- name: 'Manage nginx Deployment'
  hosts: freebsd-hosts
  become: true
  remote_user: ansible
  gather_facts: false
  tasks:
    - name: 'Install nginx Web Server'
      package:
        name: 'nginx'
        state: 'present'

    - name: 'Enable nginx service at boot'
      lineinfile:
        path: /etc/rc.conf
        line: 'nginx_enable="YES"'
        create: yes

    - name: 'Start nginx service'
      service:
        name: 'nginx'
        state: 'started'

vim index.html
<h1>This is my page</h1>
This is a web page

mkdir web

mv index.html web

echo "a second page" > web/page2.html

ls web

- name: 'Configure Web Pages on BSD Systems'
  hosts: freebsd-hosts
  become: true
  remote_user: ansible
  gather_facts: false
  vars:
    web_root: '/var/www/htdocs'
  tasks:

    - name: 'Add simple welcome page'
      copy:
        dest: "{{ web_root }}/index.html"
        content: "<h1>Welcome to the web site</h1>"

    - name: 'Add multiline welcome page'
      copy:
        dest: "{{ web_root }}/index.html"
        content: |
          This is a simple page
          <h1>welcome</h1>

    - name: 'Copy index.html from local file'
      copy:
        dest: "{{ web_root }}/index.html"
        src: "web/index.html"

    - name: 'Copy entire web directory'
      copy:
        dest: "{{ web_root }}/"
        src: "web/"
        mode: preserve

vim index.html.j2

<html>
<center>
<h1>Der Computername von diesem System ist {{ ansible_hostname }}</h1>
<h3>Das Betriebsystem von diesem Computer ist {{ ansible_os_family }}</h3>
<small>Die Dateiversion ist {{ file_version }}<small>
{# Dieser Eintrag wird nicht in der index-html Datei zu finden sein #}
</center>
</html>

```
