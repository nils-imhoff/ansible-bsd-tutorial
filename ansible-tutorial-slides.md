---
marp: true
title: Ansible Tutorial
description:  Ansible Tutorial - Infrastructure Automation
theme: gaia
paginate: true
_paginate: false
---

<style>
section {
  background: black;
  color: white;
  font-size: 26px;
  padding: 40px;
}

h1 {
  color: orange;
  text-align: center
}

h2 {
  color: orange;
  text-align: center
}

strong {
  font-weight: bold;
  color: orange;
}
  
code {
  color: orange;
  background: black;
}

.columns {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

</style>

# Ansible Tutorial

**Nils Imhoff**  
*September 25, 2025*

---

## Agenda

1. **Introduction and Setup** (60 min)
2. **Introduction to Ansible and First Steps** (60 min)
3. **Inventory, Variables and Playbooks** (90 min)
4. **Roles and Advanced Concepts** (90 min)
5. **Security, Vaults and Best Practices** (60 min)
6. **Real-world Project and Troubleshooting** (60 min)

---

## About Me

### Brief Introduction -- Nils Imhoff

- Works for as a DevOps-Engineer
- @work: mostly Ansible, Terraform, K8s, Linux
- @freetime: mostly BSD, Nixos
- Reachable via `nils@d4d1.de`
- GitHub: [`@nils-imhoff`](https://github.com/nils-imhoff)

---

## Introduction to Ansible and the Tutorial

---

## Why Ansible

- Manual setup is inefficient at scale
- Central control for:
  - Config deployment
  - Software installation
  - System queries
- Define desired state, not commands
- Use DSLs to abstract OS differences
- Treat config as Infrastructure as Code:
  - Shareable, reusable, extensible
  - Deploy changes quickly & in parallel

---

## Introdction to Ansible

- Use Ansible for reliable & consistent machine management
- Handles tasks like:
  - Configuration
  - Software deployment
  - System updates
- Key features:
  - Client-less (uses SSH)
  - Easy to get started
- Two usage modes:
  - Ad-hoc commands via CLI
  - Playbooks for complex changes

---

## How does Ansible work?

### Idempotency

- **Idempotency**: Operation gives the same result whether run once or multiple times  
- Crucial for **safe system changes**:
  - Avoids redundant or harmful actions  
  - Ensures consistency
- Examples:
  - **Adding a user**: If user exists, no change  
  - **Editing config files**: Check if line exists before adding
- Common in **configuration management**, **computer science**, and **math**

---

## Setting Up Ansible

- **Install Ansible** on a control machine (can also be the target)
- Control machine sends commands to **target systems via SSH**
- Requirements:
  - SSH daemon on targets  
  - SSH access + sudo on control machine  
  - Python **3.8+** on all systems
- **Modules** may have extra dependencies (check docs)
- File transfers via **SFTP** or **SCP**
- No special services needed on control machine
- Install via package managers: `apt`, `pkg`, `pip`, etc.

---

Would you like all four slides bundled into a PowerPoint or PDF?

---

## How do I install Ansible?

**Via BSD package managers:**

- **FreeBSD**: `pkg install py311-ansible` or `cd /usr/ports/sysutils/ansible && make install`
- **OpenBSD**: `pkg_add ansible`
- **NetBSD**: `pkgin install ansible` or via pkgsrc: `cd /usr/pkgsrc/sysutils/ansible && make install`

**From source (all BSD variants):**

- `pip install ansible`
- `tar.gz` from <https://github.com/ansible/ansible/releases>

**Note**: Ensure Python 3.x is installed first on your BSD system

---

## Secure Communication with Ansible via SSH

- Ansible uses **SSH** to connect to managed systems  
- **SSH daemon** must be running on target nodes  
- Set up **key-based authentication**:
  - Exchange public keys for passwordless login  
  - Use a dedicated user (e.g. `ansible`)  
  - Protect keys with a **passphrase**
- Use an **SSH agent** to cache the key and avoid repeated passphrase entry
- Setup steps:
  1. Create SSH key pair  
  2. Distribute public key to targets  
  3. Start SSH agent to manage the key

---

## First Steps with Ansible

---

## My Repository

For the tutorial, I have prepared a repository:

[https://github.com/nils-imhoff/ansible-bsd-tutorial](https://github.com/nils-imhoff/ansible-bsd-tutorial)

Please clone it:

```bash
git clone https://github.com/nils-imhoff/ansible-bsd-tutorial.git
```

The exercises are located in the `exercises/` subdirectory.

---

## Adhoc Commands

- Run **one-off commands** from the CLI — no need to save for later  
- Executes on all specified hosts **simultaneously**
- Hosts are defined in the **inventory file**
- Syntax:

  ```bash
  ansible <host-pattern> [-f forks] [-m module] [-a args]
  ```

- Parameters:
  - `-f`: Parallelism level (default: 5)  
  - `-m`: Module to run  
  - `-a`: Arguments for the module
  - `-i`: Location of the inventory
  - `-u`: Username (default: current username)
  - `-b`: Actions executed with specified user rights

---

## Package Managment

- Common tasks:
  - **Install**, **update**, **remove**, and **configure** software
- Uses OS-native **package managers** or language-specific tools
- Ansible simplifies package handling:
  - Abstracts away platform-specific commands
- Requires **admin privileges** for most package operations
- Some modules may offer **additional options** for fine control

---

## Basic Package Management

- Use the **`package` module** to manage software across Unix systems
- Example: Install Nginx  

  ```bash
  ansible webservers -m package -a "name=nginx state=present"
  ```

- Ansible checks system state and installs if not present
- Update to latest version:
  
  ```bash
  ansible webservers -m package -a "name=nginx state=latest"
  ```

- Remove a package:
  
  ```bash
  ansible webservers -m package -a "name=nginx state=absent"
  ```

- No need to handle version numbers manually—Ansible handles it via the package manager

---

## Ansible Command Permissions**

- **Admin privileges** are needed for tasks like package installation
- By default, Ansible runs as the **invoking user**
- Override remote user with `-u`:

  ```bash
  ansible webservers -m package -a "name=nginx state=absent" -u root
  ```

- Use **sudo** for privilege escalation:
  - Ensure user (e.g. `ansible`) is in the `sudo` group
  - Use `-b` (become) and `-K` (ask for password):

    ```bash
    ansible webservers -Kbm package -a "name=nginx state=present"
    ```

---

## Inventory and Variables

---

## Inventory

The inventory collects various BSD systems and consists of one or more files:

```ini
freebsd01.example.org
openbsd01.example.org
netbsd01.example.org

[webservers]
freebsd01.example.org
openbsd01.example.org
[databases]
netbsd01.example.org
```

---

## Inventory

### Format

The inventory can be in **INI format** or as **YAML file**:

**INI Format:**

```ini
[bsd_webservers]
freebsd01.example.org
openbsd01.example.org
```

**YAML Format:**

```yaml
all:
  hosts:
    freebsd01.example.org
    openbsd01.example.org
    netbsd01.example.org
  children:
    bsd_webservers:
      freebsd01.example.org:
      openbsd01.example.org:
```

---

## Default Groups

Ansible creates two groups by default:

- **`all`**
- **`ungrouped`**

You can define additional groups yourself and sort hosts there or in child groups.

---

## Dynamic Inventories

Inventories are not necessarily static. New hosts are added, old ones are removed from the system. Depending on the environment, this can happen very dynamically.

Ansible uses inventory plugins or scripts for this: `ansible-doc -t inventory -l`

This builds inventories dynamically and uses them with Ansible.

---

## Variables

There can be differences between individual systems. Ansible uses **variables** to manage these differences.

These variables can be:

- Passed on the command line
- Stored in a file (playbook, inventory, etc.)
- Evaluated as return values

---

## Simple Variables

A variable name can contain letters, numbers, and underscores and can be defined using YAML as follows: `http_port: 80`

Access in the playbook can be done as:
`port: '{{ http_port }}'`

---

## Inventory Variables

Variables can also be used for groups within inventories:

```ini
[bsd_webservers]
freebsd01.example.org
openbsd01.example.org

[bsd_webservers:vars]
http_port=8080
package_manager=pkg
```

---

## YAML: Human-Friendly Configuration Language

- **Easy to read, tricky to master**  
  - Relies heavily on **correct indentation** and **spacing**  
  - Misalignment can lead to parsing errors

- **Minimal syntax**  
  - Less clutter than JSON or XML  
  - Designed for **human readability**

- **Used in Ansible playbooks**  
  - Learning YAML is essential for writing effective automation scripts

- **Editor tip for `vim` users**:  
  - Add this to `.vimrc` for proper YAML formatting:  

    ```vim
    autocmd FileType yaml setlocal ai et ts=2 sw=2 cuc cul
    ```

---

## YAML Syntax Essentials

- **File structure**:  
  - Start with `---` (like `#!/bin/sh` in shell scripts)  
  - End with `...` (optional, but good style for parsers)

- **Comments**:  
  - Begin with `#` and continue to the end of the line

- **Strings**:  
  - No need to quote unless using special characters (e.g., `:`)  
  - Use **single quotes** to enclose **double quotes** when needed  
  - Examples:

    ```yaml
    --- # this starts the YAML file  
    This is a string  
    "This is a string in quotes with 'single' quotes"  
    ...
    ```

---

## YAML Syntax Essentials

- **Boolean values**:  
  - Accepted forms for `true`:  
    `true`, `True`, `TRUE`, `yes`, `Yes`, `YES`, `on`, `On`, `ON`, `y`, `Y`  
  - Accepted forms for `false`:  
    `false`, `False`, `FALSE`, `no`, `No`, `NO`, `off`, `Off`, `OFF`, `n`, `N`

---

## YAML Lists (Sequences)

- **Lists = Arrays** in other languages (e.g., C++, Java)  
  - Represent a **collection of values**

- **Standard list syntax**:  
  - Use **hyphens** (`-`) followed by a space  
  - Items must be on the **same indentation level**  
  - Example:  
  
    ```yaml
    list:
      - item1
      - item2
      - item3
    ```

- **Alternative inline syntax**:
  
    ```yaml
    list: [item1, item2, item3]
    ```

---

## YAML Dictionaries (Mappings)

- **Dictionaries = Key-Value Pairs**  
  - Similar to maps or objects in other languages  
  - Use a **colon and space** (`:`) to separate key and value  
  - Example:  
  
    ```yaml
    conference:
      name: EuroBSDCon
      year: 2025
      location: Zagreb
    ```

- **Alternative inline syntax**:

    ```yaml
    conference: (name: EuroBSDCon, year: 2025, location: Zagreb)
    ```

- **Mixing lists and dictionaries**:  
  - Use **indentation levels** to nest structures  
  - Similar to using `{}` and `[]` in C

---

## Wrapping Long YAML Lines

- **Why wrap lines?**  
  - Long module arguments or values can exceed line length limits  
  - Wrapping improves **readability** and **maintainability**

- **Line folding characters**:  
  - `>` (folded style):  
    - **Ignores newlines**, treats content as a single line  
    - Example:  

      ```yaml
      tutorial: >
        Ansible for Unix Administrators,
        EuroBSDCon2025
      ```

  - `|` (literal style):  
    - **Preserves newlines** exactly as written

---

## Exercise 3

Now web servers will be installed and configured using BSD-specific package managers. We'll demonstrate differences between FreeBSD, OpenBSD, and NetBSD package management.

You'll get output like:
> "The URL is: <http://xxx.xxx.xxx.xxx/>"

This allows you to see a simple web page served by each BSD system.

---

## Playbooks Introduction

**Playbooks** are Ansible's configuration, deployment, and orchestration language. They describe a policy you want your remote systems to enforce.

**Key concepts:**

- Written in YAML
- Contain one or more **plays**
- Each play contains one or more **tasks**
- Tasks call Ansible **modules**

---

## Your First Playbook

```yaml
---
- name: Configure BSD Web Servers
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install web server package
      package:
        name: "{{ web_package }}"
        state: present
        
    - name: Start web service
      service:
        name: "{{ web_service }}"
        state: started
        enabled: yes
```

---

## Handlers

**Handlers** are special tasks that only run when notified by other tasks. Perfect for restarting services after configuration changes.

```yaml

tasks:
  - name: Update web server config
    template:
      src: nginx.conf.j2
      dest: /usr/local/etc/nginx/nginx.conf
    notify: restart nginx

handlers:
  - name: restart nginx
    service:
      name: nginx
      state: restarted
```

---

## Exercise 7

In Exercise 7, we pass the variable `year` via the command line.

## Loops and Conditionals

**Loops** help you repeat tasks efficiently:

```yaml
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

**Conditionals** make tasks run only when certain conditions are met:

```yaml
- name: Install FreeBSD-specific packages
  package:
    name: "portmaster"
    state: present
  when: ansible_os_family == "FreeBSD"
```

---

## Facts and Variables Deep Dive

**Ansible Facts** are automatically discovered information about target systems:

```yaml
- name: Debug system information
  debug:
    msg: |
      System: {{ ansible_system }}
      OS Family: {{ ansible_os_family }}
      Architecture: {{ ansible_architecture }}
      Python Version: {{ ansible_python_version }}
      Memory: {{ ansible_memtotal_mb }}MB
```

**Custom Facts** can be created:

```yaml
- name: Set custom fact
  set_fact:
    deployment_date: "{{ ansible_date_time.iso8601 }}"
    is_production: "{{ inventory_hostname.startswith('prod') }}"
```
## Templates with Jinja2

---

## Templates

Besides copying simple files, we can also create templates. Ansible builds the correct file from them and uploads it to the target system. The basis for templates is Jinja2.

```yaml
- name: BSD-specific configuration
  template: 
    src: httpd.conf.j2 
    dest: "{{ web_config_path }}"
  vars:
    web_config_path: "{% if ansible_os_family == 'OpenBSD' %}/etc/httpd.conf{% else %}/usr/local/etc/nginx/nginx.conf{% endif %}"
```

---

## Jinja2

The template language Jinja2 comes from the Python ecosystem and works with current versions (2.6.x, 2.7.x, from 3.3.x) of the language.

---

## Jinja2

### Variables

In the `vars` subdirectory, variables can be included in the `main.yml` file. The template file accesses these and inserts the values.

```yaml
bsd_services:
  - name: nginx
    freebsd_name: nginx
    openbsd_name: httpd  
    netbsd_name: nginx
    port: 80
  - name: postgresql
    freebsd_name: postgresql-server
    openbsd_name: postgresql-server
    netbsd_name: postgresql-server
    port: 5432
```

---

## Advanced Role Features

**Role Dependencies** in `meta/main.yml`:

```yaml
dependencies:
  - role: common
  - role: security
    vars:
      security_level: high
  - role: firewall
    when: enable_firewall | default(false)
```

**Role Inheritance and Includes:**

```yaml
# In a task file
- name: Include OS-specific variables
  include_vars: "{{ ansible_os_family }}.yml"

- name: Include common tasks
  include_tasks: common.yml

- name: Include BSD-specific tasks
  include_tasks: bsd.yml
  when: ansible_os_family in ["FreeBSD", "OpenBSD", "NetBSD"]
```

---

## Roles

---

## Roles

### Introduction

At some point, the work should be better organized. Usually, many small tasks should be executed instead of one large one.

Since Ansible 2.4, there's the possibility to include content from other files (`import` and `include`).

Roles are an older method. They rely on a predefined directory structure and can execute tasks, access variables, etc.

---

## Roles

### Directory Structure

<div class="columns">

**Requirements:**

- At least one of the directories must exist
- Existing directories must contain a file named `main.yml`

```
/
└── roles
    └── RoleName
        ├── tasks
        ├── handlers
        ├── files
        ├── templates
        ├── vars
        ├── defaults
        └── meta
```

</div>

---

## Roles

### Directory Contents

- **tasks**: Contains the list of tasks executed by the role
- **handlers**: Handlers used by the role
- **files**: Files used by this role
- **templates**: Templates that are then deployed
- **vars**: Variables for the role
- **defaults**: Default values for variables
- **meta**: Dependencies of the role

---

## Ansible Vault and Security

**Ansible Vault** encrypts sensitive data:

```bash
# Create encrypted file
ansible-vault create secrets.yml

# Edit encrypted file
ansible-vault edit secrets.yml

# Encrypt existing file
ansible-vault encrypt inventory/group_vars/production.yml

# Decrypt file
ansible-vault decrypt secrets.yml
```

**Using vault in playbooks:**

```yaml
- name: Create database user
  postgresql_user:
    name: "{{ db_user }}"
    password: "{{ db_password }}"  # encrypted in vault
    state: present
```

---

## Best Practices and Production Considerations

**Directory Structure:**

```
ansible-project/
├── ansible.cfg
├── inventories/
│   ├── production/
│   │   ├── hosts
│   │   └── group_vars/
│   └── staging/
│       ├── hosts
│       └── group_vars/
├── roles/
├── playbooks/
├── filter_plugins/
└── library/
```

**Configuration Management:**

- Use `ansible.cfg` for project settings
- Version control everything (except vault passwords)
- Tag your tasks for selective execution
- Use check mode (`--check`) for dry runs

---

## Troubleshooting and Debugging

**Common Issues and Solutions:**

```bash
# Test connectivity
ansible all -m ping -i inventory

# Debug variables
ansible-playbook playbook.yml --extra-vars "debug=true"

# Verbose output
ansible-playbook -vvv playbook.yml

# Check syntax
ansible-playbook --syntax-check playbook.yml

# Dry run
ansible-playbook --check playbook.yml
```

**Performance Optimization:**

- Use fact caching
- Increase forks in ansible.cfg
- Use `async` for long-running tasks
- Leverage `gather_facts: no` when appropriate

---

## BSD Package Management

Different BSD systems use different package managers:

- **FreeBSD**: `pkg` (binary packages) or ports (`/usr/ports`)
- **OpenBSD**: `pkg_add` and `pkg_delete`
- **NetBSD**: `pkgin` (binary) or `pkgsrc` (source-based)

Ansible handles these differences through modules and variables!

---

## BSD-Specific Ansible Modules

```yaml
# FreeBSD
- name: Install nginx on FreeBSD
  community.general.pkgng:
    name: nginx
    state: present

# OpenBSD  
- name: Install httpd on OpenBSD
  community.general.openbsd_pkg:
    name: nginx
    state: present

# NetBSD
- name: Install nginx on NetBSD  
  community.general.pkgin:
    name: nginx
    state: present
```

---

## Thank You

**Questions about BSD and Ansible?**

Contact me:

- Nils Imhoff: `nils@d4d1.de`
- GitHub: [@nils-imhoff](https://github.com/nils-imhoff)

**Resources:**

- FreeBSD Handbook: [https://handbook.freebsd.org/](https://handbook.freebsd.org/)
- OpenBSD FAQ: [https://openbsd.org/faq/](https://openbsd.org/faq/)
- NetBSD Guide: [https://netbsd.org/docs/guide/](https://netbsd.org/docs/guide/)
- Ansible Documentation: [https://docs.ansible.com/](https://docs.ansible.com/)
- Ansible Galaxy: [https://galaxy.ansible.com/](https://galaxy.ansible.com/)
