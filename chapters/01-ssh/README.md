# Chapter 01 - SSH Connectivity to BSD Systems

Test connectivity to FreeBSD system:

```bash
ssh ansible@freebsd0x.d4d1.de
```

Test connectivity to OpenBSD system:

```bash
ssh ansible@openbsd0x.d4d1.de
```

## Create a ssh-key

```bash
ssh-keygen -t ed25519 -C "nick@example.com"
```

## Add the ssh key to the ssh-agent

```bash
$ eval `ssh-agent -c`
> Agent pid 59566
```

## Add the ssh key to the hosts

```bash
ssh-copy-id ansible@freebsd0x.d4d1.de
```

```bash
ssh-copy-id ansible@openbsd0x.d4d1.de
```
