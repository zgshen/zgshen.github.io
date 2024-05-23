---
title: Ubuntu 滚动更新碰到问题记录
categories: 技术
tags:
  - 技术
toc: true
date: 2024-05-21
---

很久没更新Ubuntu系统，更新出了点问题记录一下。

<!-- more -->

之前禁止了内核更新，最近想更新一下，unhold 了内核版本，重新 apt update 并且 upgrade 更新了下，结果在`neofetch`看到 OS 信息居然变成了 TONGWANDOU？这才想起之前为了安装国内的一些软件添加的一个源：[铜豌豆
](https://www.atzlinux.com/allpackages.htm)，结果更新的时候这源不知道加了什么料把系统更新覆盖了，连 grub 都改了...

因为这源的软件也用不上了，然后我就把这个源移除掉重新更新，好了一更新这个铜豌豆干掉了，但是连系统信息也干掉了，`lsb_release -a`看到 Ubuntu 直接退成了 Debian，原因是`/usr/lib/os-release`被删，用 zsh 的时候都提示`grep: /etc/os-release: No such file or directory is printed`。

```bash
$ ls -l /etc/os-release
lrwxrwxrwx 1 root root 21 Aug  2  2023 /etc/os-release -> ../usr/lib/os-release
```

看下`/etc/os-release`其实是外链到`/usr/lib/os-release`，所以在`/usr/lib/os-release`补上系统信息就行了。

`vi /usr/lib/os-release`编辑文件并输入
```bash
PRETTY_NAME="Ubuntu 22.04.4 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.4 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
```

保存再执行`lsb_release -a`就能看到正确的Ubuntu信息了。
```bash
$ lsb_release -a             
LSB Version:	core-11.1.0ubuntu4-noarch:security-11.1.0ubuntu4-noarch
Distributor ID:	Ubuntu
Description:	Ubuntu 22.04.4 LTS
Release:	22.04
Codename:	jammy
```
以后一些奇怪的三方源还是别乱用。
