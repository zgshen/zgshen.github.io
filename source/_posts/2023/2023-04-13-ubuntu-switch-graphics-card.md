---
title: Ubuntu 切换集显及碰到的小坑
categories: 技术
tags:
  - Linux
  - Ubuntu
toc: true
date: 2023-04-14
---

T460p 用到现在已经不太行了，任务繁重些就发热严重，想着把独显禁用减少点功耗发热。

打开 NVIDIA X Server Setting，如果没有的话就安装一下：

```bash
sudo apt-fast install nvidia-settings nvidia-prime -y
```

在 PRIME Profiles 选项可以切换性能模式和按需使用模式，单独使用 intel 集显选项是灰色的，可以使用命令开启，执行后重启电脑。

```bash
# intel 集显
sudo prime-select intel
# 性能模式，nvidia 独显
#sudo prime-select nvidia
# 按需切换
#sudo prime-select on-demand
```

重启后就能在 Setting - About 里面看到显卡只有集显了，原先是有独显和集显。

Ubuntu 22.04 的默认显示服务器用的 Wayland，禁用独显后可能会导致输入法启动不起来（中文输入法是用的搜狗），手动执行 `fcitx` 看到和 Wayland 相关的错误。

```bash
# nathan @ gs-ubuntu in ~ [17:55:57] 
$ fcitx
(INFO-21681 addon.c:151) Load Addon Config File:fcitx-kimpanel-ui.conf   
...

(ERROR-21681 ime.c:432) fcitx-keyboard-tr-otk already exists
(ERROR-21681 ime.c:432) fcitx-keyboard-us already exists
auth ok
(ERROR-21681 xim.c:239) Start XIM error. Another XIM daemon named ibus is running?
(ERROR-21681 instance.c:443) Exiting.
Warning: Ignoring XDG_SESSION_TYPE=wayland on Gnome. Use QT_QPA_PLATFORM=wayland to run on Wayland anyway.
Warning: Ignoring XDG_SESSION_TYPE=wayland on Gnome. Use QT_QPA_PLATFORM=wayland to run on Wayland anyway.
start
sgim_gd_cell.bin copy fail
No such file or directory: No such file or directory
```

我也没有深入去看具体什么原因，既然跟 Wayland 有关，那就换成 Xrog 试试，logout 后 login 的界面选择 xrog 登录，输入法恢复正常。
