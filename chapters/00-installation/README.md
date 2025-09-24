host_key_checking = False
hosts = hosts
remote_user = admin
private_key_file = ~/.ssh/id_rsa
ssh_args = -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no

# Exercise 00 - Ansible Installation (BSD)

Installation guide for Ansible on FreeBSD, OpenBSD, and NetBSD.

## Details

This exercise describes how to install Ansible on BSD systems so that they can be used as control nodes.

## Voraussetzungen

- Python 3 (meistens bereits vorinstalliert oder über die Paketverwaltung installierbar)
- Root- oder Sudo-Rechte

## FreeBSD

Ansible kann direkt über die Paketverwaltung installiert werden:

```bash
sudo pkg install py311-ansible
```

Alternativ kann auch eine andere Python-Version gewählt werden (z.B. py311-ansible).

## OpenBSD

Auch auf OpenBSD steht Ansible als Paket zur Verfügung:

```bash
doas pkg_add ansible
```

## NetBSD

Auf NetBSD wird Ansible über pkgin installiert:

```bash
sudo pkgin install ansible
```

Falls pkgin nicht installiert ist, kann es mit pkgsrc nachinstalliert werden.

## Mac

```bash
brew install ansible
```

## Überprüfung der Installation

Nach der Installation kann die Version geprüft werden:

```bash
ansible --version
```

Die Ausgabe sollte die installierte Ansible-Version und die verwendete Python-Version anzeigen.

## Hinweise

- Ansible muss nur auf dem Steuerungsrechner installiert werden, nicht auf den Zielsystemen.
- Für die Nutzung von Ansible ist eine funktionierende SSH-Verbindung zu den Zielsystemen erforderlich.

## Nächste Schritte

- SSH-Zugang zu den Zielsystemen testen (siehe nächste Übung)
- Inventory-Datei anlegen
- Erstes Ansible-Modul testen
