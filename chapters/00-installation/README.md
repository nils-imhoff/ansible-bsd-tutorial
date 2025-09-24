# Chapter 00 - Ansible Installation (BSD)

Installation guide for Ansible on FreeBSD, OpenBSD, and NetBSD.

## Prerequisites

- Python 3 (usually pre-installed or available through package management)
- Root or sudo privileges

## FreeBSD

Ansible can be installed directly through the package management:

```bash
sudo pkg install py311-ansible
```

Alternatively, a different Python version can be chosen (e.g. py311-ansible).

## OpenBSD

Ansible is also available as a package on OpenBSD:

```bash
doas pkg_add ansible
```

## NetBSD

On NetBSD, Ansible is installed via pkgin:

```bash
sudo pkgin install ansible
```

If pkgin is not installed, it can be installed afterwards with pkgsrc.

## Mac

```bash
brew install ansible
```

## Verification of Installation

After installation, the version can be checked:

```bash
ansible --version
```

The output should show the installed Ansible version and the Python version used.
