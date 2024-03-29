---
title: Ubuntu 桌面版的一些常规配置
categories: 技术
tags: 基础
date: 2021-8-11
toc: true
---

![Ubuntu-Desktop](../images/202108/20210817231422.jpg)

以前一直在 Windows 桌面环境下做开发，接触的 Linux 机器都是服务器，基本上全都是在终端操作。最近来兴趣尝试在 Linux 桌面下做开发，总的来说，以日常开发办公的体验还可以，真正的 Linux 环境下工程的编译和部署调试比起虚拟机和远程终端还是好太多。但桌面的上手顺畅程序和 Windows 和 macOS 还是完全没法比，有些工具安装方式也比较麻烦，而且不同的 Linux 发行版差异巨大。

尝试过 CentOS、Debian、Manjaro 和 Ubuntu 之后，个人感觉 Ubuntu 的总体体验是最好的，用的的人多，资料好早，不会常年不更新也不会更新太激进。总结一下：  
- 想要好的桌面体验用 Windows 或者 Mac，Linux 再怎么折腾都比不了
- 用 Linux 就要忍得了 Linux 的桌面和输入法问题
- 如果你是不折腾就会死星人，就用 Arch 系的发行版，KDE 桌面还行，能看懂 Arch 的文档就能解决大多数问题
- 如果不想折腾只要安心开发就用 debian 系的发行版，Ubuntu 应该是用户最多的 Linux 发行版，资料多，坑也有大多数用户帮你踩了

下面记录一下使用 Ubuntu 20.04 LTS 一些配置。

### 1. 分区
装系统的时候最好自己手动分下区，注意别因为格式化硬盘丢数据了，如果有数据的话。
我自己 500G 空间的划分
```
/boot   主分区 1G
/       逻辑分区 300G
/home   逻辑分区 199G
```
安装启动引导器的设备选择 /boot 分区所在的设备。

### 2. vi 编辑器
上手先设置下 vi 吧，Ubuntu 默认的 vi 使用方向键和退格键有问题，可以通过修改配置或安装 full 版本的 vi 解决。

编辑/etc/vim下的vimrc.tiny文件 `sudo vi /etc/vim/vimrc.tiny`
将 set compatible 改成 set nocompatible ，然后添加 set backspace=2 即可解决。

或者卸载旧版 vi 装新的
```bash
sudo apt-get remove vim-common
sudo apt-get install vim
```

### 3. 科学上网设置

使用并对比几个客户端，Qv2Ray 是比较好用的一个。

下载 Qv2Ray 和 v2Ray

到 https://github.com/Qv2ray/Qv2ray 下载 deb 格式安装包；

到 https://github.com/v2ray/v2ray-core/releases/ 下载 v2ray-linux-64.zip 压缩包。

```bash
unzip v2ray-linux-64.zip
sudo apt install  Qv2ray.....deb
```

点击分组，添加订阅，输入订阅地址更新订阅。

首选项-内核设置，填入 v2ray 解压文件的路径。

V2Ray  核心可执行文件路径 `/home/nathan/app/v2ray/v2ray`

V2Ray 资源目录 `/home/nathan/app/v2ray/`

### 4. 输入法设置

Linux 下的输入法大多拉跨，搜狗的兼容性问题巨多，根本不可用，要么用系统自带的 IBus 或自己装的 Fcitx 框架，自带的中文输入体验都不行，最好是在框架上装其他输入法引擎，试用下来 rime 的体验还不错。最烦人的问题是在 JetBrains 家的 IDE 下编辑文本，不管什么输入法多少都有问题，输入法无法跟随光标，需要重新编译 JetBrainsRuntime 来解决。

> 2021/08/17 更新，搜狗输入法 2.4.0.3469 版本修复了许多问题，退格删除不会删除已输入文字了，IDEA 中也能正常使用。

**IBus**

首次使用 IBus，打开设置中的语言管理，Ubuntu 会提示你更新依赖，更新完毕添加拼音输入源，重启系统就可以使用系统自带的中文输入了。但是用 IBus 在 Jetbrains 家 IDE 下输入框被固定在了左下角，光标不跟随输入法，后面换 Fcitx 就没问题了。

IBus 框架下 rime 输入法体验还不错，安装 ibus-rime `sudo apt-get install ibus-rime`

安装输入法方案，有很多，双拼全拼还是五笔自己选一个 https://github.com/rime/home/wiki/RimeWithIBus#ubuntu

```bash
sudo apt-get install librime-data-pinyin-simp
```

另一种方法官方推荐使用 [/plum/](https://github.com/rime/plum) 安裝最新版本

创建配置文件 `vi ~/.config/ibus/rime/default.custom.yaml`

```yml
patch:
  "menu/page_size": 9 #每页候选词个数
  "ascii_composer/switch_key/Shift_L": commit_code #左shift提交字母
  "style/color_scheme": dota_2
```

创建配置文件 `vi ~/.config/ibus/rime/build/ibus_rime.yaml`

```bash
style:
  horizontal: true #横向候选框
```

到语言设置添加输入源，重新部署即可生效。

或者命令重启 ibus，执行 `ibus-daemon -d -x -r`

其他设置看官方文档 https://github.com/rime/home/wiki/CustomizationGuide

**关于扩充词库：**

找找下载别人的词库文件，格式类似 luna_pinyin.chat.dict.yaml，以 dict.yml 结尾。

新建编辑 luna_pinyin.extended.dict.yaml 文件，import_tables 下的列表就是词库。列表名

```bash
# Rime dictionary
# encoding: utf-8

---
name: luna_pinyin.extended
version: "2021.08.12"
sort: by_weight
use_preset_vocabulary: true
import_tables:
  - luna_pinyin
  - luna_pinyin.extra_hanzi
```

创建 luna_pinyin_simp.custom.yaml，translator/dictionary 设 luna_pinyin.extended

```bash
patch:
  switches:
    - name: ascii_mode
      reset: 1                                          # 默认英文
      states: ["中", "英"]
    - name: full_shape
      reset: 0                                          # 默认半角
      states: ["半", "全"]
    - name: zh_simp
      reset: 1                                          # 预设简体
      states: ["繁", "简"]
    - name: ascii_punct
      states: ["。，", "．，"]
    - options: [utf8, gbk]                              # 字符集
      reset: 1                                          # 默认 GBK
      states: ["utf8", "gbk"]

  "engine/filters/@next": charset_filter@gbk            # 默认 GBK
  "engine/translators/@next": reverse_lookup_translator

  translator:
    dictionary: luna_pinyin.extended
    prism: luna_pinyin_simp

  "speller/algebra/@before 0": xform/^([b-df-hj-np-tv-z])$/$1_/

  punctuator:                                           # 符号快速输入和部分符号的快速上屏
    import_preset: symbols
    full_shape:
      "\\": "、"
    half_shape:
      "#": "#"
      "`": "`"
      "~": "~"
      "@": "@"
      "=": "="
      "/": ["/", "÷"]
      '\': "、"
      "'": {pair: ["「", "」"]}
      "[": ["【", "["]
      "]": ["】", "]"]
      "$": ["¥", "$", "€", "£", "¢", "¤"]
      "<": ["《", "〈", "«", "<"]
      ">": ["》", "〉", "»", ">"]

  recognizer:
    patterns:
      email: "^[A-Za-z][-_.0-9A-Za-z]*@.*$"
      uppercase: "[A-Z][-_+.'0-9A-Za-z]*$"
      url: "^(www[.]|https?:|ftp[.:]|mailto:|file:).*$|^[a-z]+[.].+$"
      punct: "^/([a-z]+|[0-9]0?)$"
      reverse_lookup: "`[a-z]*'?$"
```

然后重新部署

**Fcitx**

与 IBus 的部署类似，安装

```bash
sudo apt-get install fcitx-rime
```

在 `sudo apt-get install fcitx-rime` 下创建默认配置文件 default.custom.yaml

```bash
patch:
  menu/page_size: 9 #每页候选词个数
  ascii_composer/switch_key/Shift_L: commit_code #左shift提交字母
```

词库的配置与 IBus 也一样，将 luna_pinyin.extended.dict.yaml 、luna_pinyin_simp.custom.yaml 和词库文件复制过来重新部署就是了。如果有问题就从最简单的一个词库文件配起，慢慢排查问题。

fcitx 皮肤导入路径 /usr/share/fcitx/skin，直接将皮肤文件夹丢在这里就行了，比如我用这个 [https://github.com/henices/rime](https://github.com/henices/rime)  ，还可以自己修改字体和配置 

```bash
vi usr/share/fcitx/skin/mac-gray/fcitx_skin.conf
#输入栏字体和颜色设置
[SkinFont]
FontSize=14
MenuFontSize=11
RespectDPI=True
TipColor=25 120 200
InputColor=25 120 200
IndexColor=25 120 200
FirstCandColor=240 50 50
UserPhraseColor=25 120 200
CodeColor=0 0 0
OtherColor=105 105 105
ActiveMenuColor=255 255 255
InactiveMenuColor=0 0 0
```

**搜狗**

官网下载 deb 文件直接安装就好了。

搜狗的环境配置文件路径是 `~/.config/sogoupinyin/conf/enc.ini`

隐藏状态栏 `StatusAppearance=0` 

**JetBrains IDE 中文输入法不跟随光标问题**

运行环境的问题，官方一直不做修复，需要打补丁重新编译 JetBrainsRuntime，比较麻烦，可以直接下载别人已经编译好的环境直接用。

讨论
https://bbs.archlinuxcn.org/viewtopic.php?id=10529

编译步骤
https://blog.csdn.net/qq_41859728/article/details/109187748

GitHub Action 自动化编译的环境 https://github.com/RikudouPatrickstar/JetBrainsRuntime-for-Linux-x64

直接下载，IDEA 装个 Choose Runtime 选择切换到下载的环境就可以了，或者修改 idea.sh 在文件开头添加环境变量。切换环境后用 IBus 输入法还是有问题，所以后面换成 Fictx 了就解决问题了。
```bash
# export IDEA_JDK=/JetBrainsRuntime/build/linux-x86_64-normal-server-release/images/jdk
export IDEA_JDK= 下载别人的环境/自己编译好的环境
```


### 5. 其他常用软件安装

**亮度调节**

笔记本外接显示器发现没有亮度调节的控件没了，应该是缺少对应显示器驱动，装个小工具凑合用

```bash
sudo add-apt-repository ppa:apandada1/brightness-controller
sudo apt update
sudo apt install brightness-controller-simple
```

**资源监控**

安装 System Monitor Indicator 用来看网速、cpu 和 内存占用。

```bash
# 添加软件源的命令
sudo add-apt-repository ppa:fossfreedom/indicator-sysmonitor && sudo apt update
# 如果需要删除该软件源可以使用
sudo add-apt-repository -r ppa:fossfreedom/indicator-sysmonitor

# 安装 indicator-sysmonitor
sudo apt install indicator-sysmonitor -y
```

打开 System Monitor Indicator，Perference - General - Run on startup 设置开机启动。

Advanced 中自定义在顶栏显示的格式 cpu:{cpu} men:{men}  net:{net}


或者使用 Resource Monitor 插件也不错

https://extensions.gnome.org/extension/1634/resource-monitor/

**VS Code**

不要用 snap 商店安装 VS Code，没法用中文输入法的，到官网下载 deb 文件安装吧。由于 D 盘文件比较多，打开的时候会报错 "Visual Studio Code is unable to watch for file changes in this large workspace" (error ENOSPC)。把这个系统变量调大就行了
```bash
cat /proc/sys/fs/inotify/max_user_watches
```

The limit can be increased to its maximum by editing `/etc/sysctl.conf` (except on Arch Linux, read below) and adding this line to the end of the file:

```bash
fs.inotify.max_user_watches=524288
```

The new value can then be loaded in by running `sudo sysctl -p`.

### 6. 默认设置恢复

Ubunut20.02 桌面启动器 gonme 恢复默认设置，包括桌面布局、图标和系统应用（如输入法和终端等）都会恢复为默认设置

```bash
dconf reset -f /org/gnome/
```

### 7. 中文文件夹改为英文

打开终端，在终端中输入命令:

``` bash
export LANG=en_US
xdg-user-dirs-gtk-update
```

跳出对话框询问是否将目录转化为英文路径,同意并关闭.在终端中输入命令:

``` bash
export LANG=zh_CN
```

关闭终端，下次重启进入系统，会提示是否把转化好的目录改回中文，选择不再提示，并取消修改，主目录的中文转英文就完成了。

### 8. 挂载 Windows 系统的硬盘

由于以前的工程全在 Windows 系统下，想在 Ubuntu 直接打开编辑，发现 IDEA 一直报错

Unable to save settings: Failed to save settings. Please restart IntelliJ IDEA ，找了下问题挂载的硬盘权限是没问题了，但就是不能创建文件和编辑文件。

重新挂载硬盘 

```bash
nathan@nathan-tp:/media/nathan$ sudo mount /dev/sda2 /media/nathan/testd
The disk contains an unclean file system (0, 0).
Metadata kept in Windows cache, refused to mount.
Falling back to read-only mount because the NTFS partition is in an
unsafe state. Please resume and shutdown Windows fully (no hibernation
or fast restarting.)
Could not mount read-write, trying read-only
ntfs-3g-mount: failed to access mountpoint /media/nathan/testd: 没有那个文件或目录
```

Windows 盘的原因，unclean 啥的，没正常关机导致的。我是睡觉时把 Windows 休眠了，早上打开直接进 Ubuntu了，确实没正常关机。网上看到别人也有相似问题 [解决 Linux 挂载 NTFS 分区只读不能写的问题](https://cloud.tencent.com/developer/article/1520766)。

重启进入 Windows 再正常关机重启进入 Ubuntu 就行了。

**设置开机自动挂载硬盘**

运行如下命令查看硬盘分区：

```bash
sudo blkid
```

看输出找到自己需要挂载的盘，比如这里要挂载的是 c 盘 `/dev/sdb1` 和 d 盘 `/dev/sda2`

```
/dev/sdb1: LABEL="win-c" UUID="96A8CBEBA8CBC7C7" TYPE="ntfs" PARTUUID="995606b6-6b82-7ed4-84e7-007d680f31d3"
/dev/sdb2: UUID="0C38-06FF" TYPE="vfat" PARTUUID="dc885421-8944-2273-207d-3685601c7169"
/dev/sda1: PARTLABEL="Microsoft reserved partition" PARTUUID="140f0f24-f5ff-4ea3-b95e-cd12128e0d58"
/dev/sda2: LABEL="win-d" UUID="04BECAB2BECA9C14" TYPE="ntfs" PARTLABEL="Basic data partition" PARTUUID="9a67d1d2-7618-4173-a9d8-d05bf45e924f"
```

修改配置文件 `sudo vi /etc/fstab` 最后加上

```bash
# Windows disks
/dev/sdb1                      /media/nathan/win-c
/dev/sda2                      /media/nathan/win-d
```

重启系统完事

### 9. 禁止休眠和系统唤醒

**休眠问题**

笔记本盖子关闭外接显示器的时候，一关闭显示器系统就休眠了， 不想休眠可以通过编辑 logind.conf 配置来设置

```bash
sudo vi /etc/systemd/logind.conf
```

修改其中的 HandleLidSwitch 配置为  ignore 后重启机器

```bash
# poweroff 关闭盖子时关闭计算机
# hibernate 关闭盖子时计算机休眠
# suspend 关闭盖子时暂停计算机
# ignore 不执行任何操作
#HandleLidSwitch=suspend
HandleLidSwitch=ignore
```

**usb 设备唤醒**

查看所有 usb 设备的电源唤醒状态

```bash
nathan@nathan-tp:~$ grep . /sys/bus/usb/devices/*/power/wakeup
/sys/bus/usb/devices/1-1.3/power/wakeup:enabled
/sys/bus/usb/devices/1-1.4/power/wakeup:disabled
/sys/bus/usb/devices/1-1/power/wakeup:disabled
/sys/bus/usb/devices/1-6/power/wakeup:disabled
/sys/bus/usb/devices/1-7/power/wakeup:disabled
/sys/bus/usb/devices/2-1/power/wakeup:disabled
/sys/bus/usb/devices/usb1/power/wakeup:disabled
/sys/bus/usb/devices/usb2/power/wakeup:disabled
```

`lsusb` 查看外接设备 

```bash
nathan@nathan-tp:~$ lsusb
Bus 002 Device 005: ID 0424:5744 Microchip Technology, Inc. (formerly SMSC) Hub
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 007: ID 04f2:b541 Chicony Electronics Co., Ltd Integrated Camera
Bus 001 Device 005: ID 8087:0a2b Intel Corp. 
Bus 001 Device 003: ID 138a:0090 Validity Sensors, Inc. VFS7500 Touch Fingerprint Sensor
Bus 001 Device 016: ID 046d:c084 Logitech, Inc. G203 Gaming Mouse
Bus 001 Device 015: ID 1c4f:0002 SiGma Micro Keyboard TRACER Gamma Ivory
Bus 001 Device 014: ID 0424:2744 Microchip Technology, Inc. (formerly SMSC) Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

用这个也可以看到

```bash
nathan@nathan-tp:~$ grep . /sys/bus/usb/devices/*/product
/sys/bus/usb/devices/1-1.3/product:USB Keyboard
/sys/bus/usb/devices/1-1.4/product:G102 Prodigy Gaming Mouse
/sys/bus/usb/devices/1-1/product:USB2744
/sys/bus/usb/devices/1-8/product:Integrated Camera
/sys/bus/usb/devices/2-1/product:USB5744
/sys/bus/usb/devices/usb1/product:xHCI Host Controller
/sys/bus/usb/devices/usb2/product:xHCI Host Controller
```

两个 usb 都是 disabled，全都改成 enabled 得了

用管理员修改 wakeup 值为 enabled

```bash
echo 'enabled' > /sys/bus/usb/devices/usb1/power/wakeup
echo 'enabled' > /sys/bus/usb/devices/usb2/power/wakeup
```