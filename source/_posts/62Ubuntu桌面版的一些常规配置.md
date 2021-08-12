---
title: Ubuntu 桌面版的一些常规配置
categories: 技术
tags: 基础
date: 2021-8-11
---
以前一直在 Windows 桌面环境下做开发，接触的 Linux 机器都是服务器，基本上全都是在终端操作。最近来兴趣尝试在 Linux 桌面下做开发，总的来说，以日常开发办公的体验还可以，真正的 Linux 环境下工程的编译和部署调试比起虚拟机和远程终端还是好太多。但桌面的上手顺畅程序和 Windows 和 macOS 还是完全没法比，有些工具安装方式也比较麻烦，而且不同的 Linux 发行版差异巨大。

尝试过 CentOS、Debian、Manjaro 和 Ubuntu 之后，个人感觉 Ubuntu 的总体体验是最好的，用的的人多，资料好早，不会常年不更新也不会更新太激进。下面记录一下使用 Ubuntu 20.04 LTS 一些配置。

### 1. 科学上网设置

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

### 3. 输入法设置

Linux 下的输入法大多拉跨，搜狗的兼容性问题巨多，根本不可用，要么用系统自带的 IBus 或自己装的 Fcitx 框架，自带的中文输入体验都不行，最好是在框架上装其他输入法引擎，试用下来 rime 的体验还不错。最烦人的问题是在 JetBrains 家的 IDE 下编辑文本，不管什么输入法多少都有问题，输入法无法跟随光标。

首次使用 IBus，打开设置中的语言管理，Ubuntu 会提示你更新依赖，更新完毕添加拼音输入源，重启系统就可以使用系统自带的中文输入了。

然后安装 rime `sudo apt-get install ibus-rime`

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

### 4. 其他常用软件安装

亮度调节

系统装完没有亮度调节，看别人说法应该发是显卡驱动或者内核版本的问题，不想折腾这些了，干脆装个小工具解决。

```bash
sudo add-apt-repository ppa:apandada1/brightness-controller
sudo apt update
sudo apt install brightness-controller-simple
```

资源监控

用来看网速、cpu 和 内存占用。

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

### 5. 设置恢复

Ubunut20.02 桌面启动器 gonme 恢复默认设置，包括桌面布局、图标和系统应用（如输入法和终端等）都会恢复为默认设置

```bash
dconf reset -f /org/gnome/
```

### 6. 中文文件夹改为英文

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

### 7. 挂载 Windows 系统的硬盘

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

Windows 盘的原因，unclean 啥的，没正常关机导致的。好吧前一天开的 Windows 睡觉时休眠，早上打开的时候不是进入 Windows ，也没多想就没管进 Ubuntu了，确实没正常关机。网上看到别人也有相似问题 [解决 Linux 挂载 NTFS 分区只读不能写的问题](https://cloud.tencent.com/developer/article/1520766)。

重启进入 Windows 再正常重启进入 Ubuntu 就行了。