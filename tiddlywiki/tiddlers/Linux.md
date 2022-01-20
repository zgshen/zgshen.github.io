
## 1. 系统信息

### 1.1. 目录结构

- /bin：
bin 是 Binaries (二进制文件) 的缩写, 这个目录存放着最经常使用的命令。

- /boot：
这里存放的是启动 Linux 时使用的一些核心文件，包括一些连接文件以及镜像文件。

- /dev ：
dev 是 Device(设备) 的缩写, 该目录下存放的是 Linux 的外部设备，在 Linux 中访问设备的方式和访问文件的方式是相同的。

- /etc：
etc 是 Etcetera(等等) 的缩写,这个目录用来存放所有的系统管理所需要的配置文件和子目录。

- /home：
用户的主目录，在 Linux 中，每个用户都有一个自己的目录，一般该目录名是以用户的账号命名的，如上图中的 alice、bob 和 eve。

- /lib：
lib 是 Library(库) 的缩写这个目录里存放着系统最基本的动态连接共享库，其作用类似于 Windows 里的 DLL 文件。几乎所有的应用程序都需要用到这些共享库。

- /lost+found：
这个目录一般情况下是空的，当系统非法关机后，这里就存放了一些文件。

- /media：
linux 系统会自动识别一些设备，例如U盘、光驱等等，当识别后，Linux 会把识别的设备挂载到这个目录下。

- /mnt：
系统提供该目录是为了让用户临时挂载别的文件系统的，我们可以将光驱挂载在 /mnt/ 上，然后进入该目录就可以查看光驱里的内容了。

- /opt：
opt 是 optional(可选) 的缩写，这是给主机额外安装软件所摆放的目录。比如你安装一个ORACLE数据库则就可以放到这个目录下。默认是空的。

- /proc：
proc 是 Processes(进程) 的缩写，/proc 是一种伪文件系统（也即虚拟文件系统），存储的是当前内核运行状态的一系列特殊文件，这个目录是一个虚拟的目录，它是系统内存的映射，我们可以通过直接访问这个目录来获取系统信息。
这个目录的内容不在硬盘上而是在内存里，我们也可以直接修改里面的某些文件，比如可以通过下面的命令来屏蔽主机的ping命令，使别人无法ping你的机器：
  ```
  echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all
  ```

- /root：
该目录为系统管理员，也称作超级权限者的用户主目录。

- /sbin：
s 就是 Super User 的意思，是 Superuser Binaries (超级用户的二进制文件) 的缩写，这里存放的是系统管理员使用的系统管理程序。

- /selinux：
 这个目录是 Redhat/CentOS 所特有的目录，Selinux 是一个安全机制，类似于 windows 的防火墙，但是这套机制比较复杂，这个目录就是存放selinux相关的文件的。

- /srv：
 该目录存放一些服务启动之后需要提取的数据。

- /sys：
这是 Linux2.6 内核的一个很大的变化。该目录下安装了 2.6 内核中新出现的一个文件系统 sysfs 。

  sysfs 文件系统集成了下面3种文件系统的信息：针对进程信息的 proc 文件系统、针对设备的 devfs 文件系统以及针对伪终端的 devpts 文件系统。

  该文件系统是内核设备树的一个直观反映。

  当一个内核对象被创建的时候，对应的文件和目录也在内核对象子系统中被创建。

- /tmp：
tmp 是 temporary(临时) 的缩写这个目录是用来存放一些临时文件的。

- /usr：
 usr 是 unix shared resources(共享资源) 的缩写，这是一个非常重要的目录，用户的很多应用程序和文件都放在这个目录下，类似于 windows 下的 program files 目录。

- /usr/bin：
系统用户使用的应用程序。

- /usr/sbin：
超级用户使用的比较高级的管理程序和系统守护程序。

- /usr/src：
内核源代码默认的放置目录。

- /var：
var 是 variable(变量) 的缩写，这个目录中存放着在不断扩充着的东西，我们习惯将那些经常被修改的目录放在这个目录下。包括各种日志文件。

- /run：
是一个临时文件系统，存储系统启动以来的信息。当系统重启时，这个目录下的文件应该被删掉或清除。如果你的系统上有 /var/run 目录，应该让它指向 run。

在 Linux 系统中，有几个目录是比较重要的，平时需要注意不要误删除或者随意更改内部文件。

- /etc： 上边也提到了，这个是系统中的配置文件，如果你更改了该目录下的某个文件可能会导致系统不能启动。

- /bin, /sbin, /usr/bin, /usr/sbin: 这是系统预设的执行文件的放置目录，比如 ls 就是在 /bin/ls 目录下的。

  值得提出的是，/bin, /usr/bin 是给系统用户使用的指令（除root外的通用户），而/sbin, /usr/sbin 则是给 root 使用的指令。

- /var： 这是一个非常重要的目录，系统上跑了很多程序，那么每个程序都会有相应的日志产生，而这些日志就被记录到这个目录下，具体在 /var/log 目录下，另外 mail 的预设放置也是在这里。

## 2. 系统信息

### 2.1. uname
用于查看系统信息
```
uname -a    显示全部信息
```

### 2.2. lscpu
cpu 架构信息


## 3. 文件和目录操作

### 3.1. ls
列出文件或者目录的信息，目录的信息就是其中包含的文件。

```
## ls [-aAdfFhilnrRSt] file|dir
-a ：列出全部的文件
-d ：仅列出目录本身
-l ：以长数据串行列出，包含文件的属性与权限等等数据
-h : 和 -l 一起使用，列出文件同时以合理易读的单位显示文件大小
```

### 3.2. cd
更换当前目录。
```
cd [相对路径或绝对路径]
```

### 3.3. mkdir
创建目录。
```
## mkdir [-mp] 目录名称
-m ：配置目录权限
-p ：递归创建目录
```

### 3.4. rmdir
删除目录，目录必须为空。
```
rmdir [-p] 目录名称
-p ：递归删除目录
```

### 3.5. touch
更新文件时间或者建立新文件。
```
## touch [-acdmt] filename
-a ： 更新 atime
-c ： 更新 ctime，若该文件不存在则不建立新文件
-m ： 更新 mtime
-d ： 后面可以接更新日期而不使用当前日期，也可以使用 --date="日期或时间"
-t ： 后面可以接更新时间而不使用当前时间，格式为[YYYYMMDDhhmm]
```

### 3.6. cp
复制文件。如果源文件有两个以上，则目的文件一定要是目录才行。
```
cp [-adfilprsu] source destination
-a ：相当于 -dr --preserve=all
-d ：若来源文件为链接文件，则复制链接文件属性而非文件本身
-i ：若目标文件已经存在时，在覆盖前会先询问
-p ：连同文件的属性一起复制过去
-r ：递归复制
-u ：destination 比 source 旧才更新 destination，或 destination 不存在的情况下才复制
--preserve=all ：除了 -p 的权限相关参数外，还加入 SELinux 的属性, links, xattr 等也复制了
```

### 3.7. rm
删除文件。
```
## rm [-fir] 文件或目录
-r ：递归删除
```

### 3.8. mv
移动文件。
```
## mv [-fiu] source destination
## mv [options] source1 source2 source3 .... directory
-f ： force 强制的意思，如果目标文件已经存在，不会询问而直接覆盖
```

## 4. 查看文件内容
### 4.1. cat
取得文件内容。
```
## cat [-AbEnTv] filename
-n ：打印出行号，连同空白行也会有行号，-b 不会

```

### 4.2. tac
是 cat 的反向操作，从最后一行开始打印。

### 4.3. more
和 cat 不同的是它可以一页一页查看文件内容，比较适合大文件的查看。

### 4.4. less
和 more 类似，但是多了一个向前翻页的功能。

### 4.5. head
取得文件前几行。
```
## head [-n number] filename
-n ：后面接数字，代表显示几行的意思
```

### 4.6. tail
是 head 的反向操作，只是取得是后几行。  
常用：  
```bash
tail -f xx  #实时查看
tail -100f xx  #实时查看最后的一百行
```

### 4.7. od
以字符或者十六进制的形式显示二进制文件。

## 5. 用户和用户组

### 5.1. 用户

查看所有用户列表
```bash
cat /etc/passwd #可以查看所有用户的列表
cat /etc/passwd | grep ${username} #查询用户
w #可以查看当前活跃的用户列表
```

添加新的用户账号使用 useradd 命令，删除使用 userdel 命令，修改使用 usermod 命令
```bash
useradd 选项 用户名
useradd mysql -g mysql #添加 mysql 用户归属 mysql 用户组
```
```bash
userdel 选项 
userdel -r sam  #-r的作用是把用户的主目录一起删除
```
此命令删除用户sam在系统文件中（主要是/etc/passwd, /etc/shadow, /etc/group等）的记录，同时删除用户的主目录

```bash
usermod 选项 用户名
usermod -s /bin/ksh -d /home/z –g developer sam
```
此命令将用户sam的登录Shell修改为ksh，主目录改为/home/z，用户组改为developer


### 5.2. 用户组

查看用户组
```bash
cat /etc/group #查看用户组
groups #当前用户所属的组列表
groups ${username} #指定用户所属的组列表
id #打印指定用户及其用户组的信息，省略用户名则显示当前用户信息
```

增加用户组
```
groupadd 选项 用户组
```

删除用户组
```
groupdel 用户组
```

修改用户组
```
groupmod 选项 用户组
```

切换用户组
```
newgrp 群组名称
```

## 6. 权限操作
chmod ［who］ ［+ | - | =］ ［mode］ 文件名  
命令中各选项的含义为：
操作对象who可是下述字母中的任一个或者它们的组合：
```
u 表示“用户（user）”，即文件或目录的所有者。
g 表示“同组（group）用户”，即与文件属主有相同组ID的所有用户。
o 表示“其他（others）用户”。
a 表示“所有（all）用户”。它是系统默认值。
```
操作符号可以是：
```
+ 添加某个权限。
- 取消某个权限。
= 赋予给定权限并取消其他所有权限（如果有的话）。
```
设置mode所表示的权限可用下述字母的任意组合：
```
r 可读。
w 可写。
x 可执行。
X 只有目标文件对某些用户是可执行的或该目标文件是目录时才追加x 属性。
s 在文件执行时把进程的属主或组ID置为该文件的文件属主。方式“u＋s”设置文件的用户ID位，“g＋s”设置组ID位。
t 保存程序的文本到交换设备上。
u 与文件属主拥有一样的权限。
g 与和文件属主同组的用户拥有一样的权限。
o 与其他用户拥有一样的权限。
```
可以将一组权限用数字来表示，此时一组权限的 3 个位当做二进制数字的位，从左到右每个位的权值为 4、2、1，即每个权限对应的数字权值为 r : 4、w : 2、x : 1。

示例：
ls -l 命令 查看文件显示
```bash
drw-rw-rw- 4 root root 4096 Dec  3 06:05 SSR-Bash-Python
-rw-r--r-- 1 root root   22 Jan 11 22:38 test.txt
```
前面的  drw-rw-rw- 之类  ，第一位含义：  
- 普通文件的文件权限第一个字符为“-”  
- 目录文件的文件权限第一个字符为“d”  
- 字符设备文件的文件权限第一个字符为“c”  
- 块设备文件的文件权限第一个字符为“b”  
- 符号链接文件的文件权限第一个字符为“s”

后面九位为三个用户组的权限，每个用户组三位，读、写、执行权限为 rwx ，没哪个则哪个为 - ，如 r-- 为只读，没有写和执行权限。  
添加权限方式  
- chmod a+w filename   为所有用户给filename文件增加写(w)权限  
- chmod 777 filename  所用用户拥有filename的所有权限

## 7. 搜索
### 7.1. which
指令搜索。
```
## which [-a] command
-a ：将所有指令列出，而不是只列第一个
```

### 7.2. whereis
文件搜索。速度比较快，因为它只搜索几个特定的目录。
```
## whereis [-bmsu] dirname/filename
```

### 7.3. locate
文件搜索。可以用关键字或者正则表达式进行搜索。


## 8. 压缩和打包
### 8.1. 压缩文件名
Linux 底下有很多压缩文件名，常见的如下：

|扩展名|压缩程序|
|--- | ---|
|*.Z	|compress
|*.zip	|zip
|*.gz	|gzip
|*.bz2	|bzip2
|*.xz	|xz
|*.tar	|tar 程序打包的数据，没有经过压缩
|*.tar.gz	|tar 程序打包的文件，经过 gzip 的压缩
|*.tar.bz2	|tar 程序打包的文件，经过 bzip2 的压缩
|*.tar.xz	|tar 程序打包的文件，经过 xz 的压缩

### 8.2. 压缩指令
### 8.3. gzip
gzip 是 Linux 使用最广的压缩指令，可以解开 compress、zip 与 gzip 所压缩的文件。  
经过 gzip 压缩过，源文件就不存在了。  
有 9 个不同的压缩等级可以使用。  
可以使用 zcat、zmore、zless 来读取压缩文件的内容。
```
$ gzip [-cdtv#] filename
-c ：将压缩的数据输出到屏幕上
-d ：解压缩
-t ：检验压缩文件是否出错
-v ：显示压缩比等信息
-# ： # 为数字的意思，代表压缩等级，数字越大压缩比越高，默认为 6
```

### 8.4. bzip2
提供比 gzip 更高的压缩比。  
查看命令：bzcat、bzmore、bzless、bzgrep。
```
$ bzip2 [-cdkzv#] filename
-k ：保留源文件
```

### 8.5. xz
提供比 bzip2 更佳的压缩比。  
可以看到，gzip、bzip2、xz 的压缩比不断优化。不过要注意的是，压缩比越高，压缩的时间也越长。  
查看命令：xzcat、xzmore、xzless、xzgrep。
```
$ xz [-dtlkc#] filename
```

### 8.6. 打包
压缩指令只能对一个文件进行压缩，而打包能够将多个文件打包成一个大文件。tar 不仅可以用于打包，也可以使用 gzip、bzip2、xz 将打包文件进行压缩。
```
$ tar [-z|-j|-J] [cv] [-f 新建的 tar 文件] filename...  ==打包压缩
$ tar [-z|-j|-J] [tv] [-f 已有的 tar 文件]              ==查看
$ tar [-z|-j|-J] [xv] [-f 已有的 tar 文件] [-C 目录]    ==解压缩
-z ：使用 zip；
-j ：使用 bzip2；
-J ：使用 xz；
-c ：新建打包文件；
-t ：查看打包文件里面有哪些文件；
-x ：解打包或解压缩的功能；
-v ：在压缩/解压缩的过程中，显示正在处理的文件名；
-f : filename：要处理的文件；
-C 目录 ： 在特定目录解压缩。
```
|使用方式|命令|
|---|---|
|打包压缩	|tar -jcv -f filename.tar.bz2 要被压缩的文件或目录名称
|查看	|tar -jtv -f filename.tar.bz2
|解压缩	|tar -jxv -f filename.tar.bz2 -C 要解压缩的目录


## 9. 网络
### 9.1. iptables
永久开启/关闭 iptables
```
开启： chkconfig iptables on  
关闭： chkconfig iptables off   
```

重启后失效  
```
开启： service iptables start   
关闭： service iptables stop   
状态 service iptables status  
```

查看、添加和删除
```bash
iptables -nL --line-number #查看当前规则
iptables -A INPUT -p tcp --dport 80 -j ACCEPT #允许访问80端口，-A 排在最后面，从上往下匹配
iptables -D INPUT 2 #删除 INPUT 指定行规则，第二行
iptables -I INPUT -p tcp --dport 80 -j ACCEPT #允许访问80端口，-I 排在前面，从上往下匹配
iptables -I INPUT -p tcp --dport 5700 -j DROP #禁止端口访问
service iptables save #保存修改规则
cat /etc/sysconfig/iptables #查看系统规则
```

### 9.2. firewalld
```
service firewalld status; #查看防火墙状态
service firewalld start;  或者 #systemctl start firewalld.service;#开启防火墙
service firewalld stop;  或者 #systemctl stop firewalld.service;#关闭防火墙
service firewalld restart;  或者 #systemctl restart firewalld.service;  #重启防火墙
systemctl disable firewalld.service#禁止防火墙开启自启

firewall-cmd --list-all #查看防火墙规则
firewall-cmd --zone=public --list-ports #查看所有打开的端口
firewall-cmd --zone=public --permanent --add-port=15672/tcp #添加端口，--permanent永久生效，没有此参数重启后失效
firewall-cmd --reload #重新载入，添加端口后重新载入生效
firewall-cmd --zone=public --remove-port=80/tcp --permanent #删除，同样需要重载生效
```

### 9.3. ss
ss是Socket Statistics的缩写。ss命令用来显示处于活动状态的套接字信息。它可以显示和netstat类似的内容。但ss的优势在于它能够显示更多更详细的有关TCP和连接状态的信息，而且比netstat更快速更高效。

```
ss [参数]
-n	不解析服务名称，已数字方式显示
-a	显示所有套接字
-l	显示处于监听状态的套接字
-o	显示计时器信息
-e	显示详细的套接字信息
-m	显示套接字的内存使用情况
-p	显示使用套接字的进程
```

```
ss -t -a #显示TCP套接字
ss -u -a #显示UDP套接字
ss -s #显示套接字使用概况
ss -lnp|grep 80 #80端口占用
```


## 10. vi/vim 基本操作
### 10.1. vi与vim两者区别
它们都是多模式编辑器，不同的是vim 是vi的升级版本，它不仅兼容vi的所有指令，而且还有一些新的特性在里面。  
vim的这些优势主要体现在以下几个方面：  
1.多级撤消  
我们知道在vi里，按 u只能撤消上次命令，而在vim里可以无限制的撤消。  
2.易用性  
vi只能运行于unix中，而vim不仅可以运行于unix,windows ,mac等多操作平台。  
3.语法加亮  
vim可以用不同的颜色来加亮你的代码。  
4.可视化操作  
就是说vim不仅可以在终端运行，也可以运行于x window、 mac os、 windows。  
5.对vi的完全兼容  
某些情况下，你可以把vim当成vi来使用

### 10.2. 使用 vi  文件名  或者  vim 文件名   打开文件
按i进入编辑  
按esc退出编辑  
打开状态操作：  
```
u   撤销上一步操作
ctrl+r   恢复上一步被撤销的操作
/字符串    搜索字符串
:%s/aa/bb    把aa替换成bb
编辑状态操作：
:w   保存
:q   退出，有提示
:q!   强制退出
:wq   保存退出（强制写入文件并退出）
:x   保存退出（有修改时才写入文件并退出）
```
按esc回到打开状态

其他操作
```
gg  回到顶端
G  到底端
u  撤销  
ctrl+r  恢复上一步被撤销的操作
ctrl+b 向上翻页
ctrl+f  向下翻页
```

### 10.3. vi操作异常中断
提示Found a swap file by the name  
删除目录下的隐藏文件，恢复操作;  
ls -a 查看swap隐藏文件，rm 命令删除即可。

## 11. 进程管理

### 11.1. 1.ps

```
ps -l # 查看自己的进程
ps aux # 查看系统所有进程
ps aux | grep nginx # 查看特定进程nginx
ps -ef | grep nginx # 同上
pstree -A # 查看进程树
```

![https://zguishen.com/images/20210219/1613749448742.png](https://zguishen.com/images/20210219/1613749448742.png)

2.top

![https://zguishen.com/images/20210220/1613793448107.png](https://zguishen.com/images/20210220/1613793448107.png)

**第一行，任务队列信息，同 uptime 命令的执行结果**

系统时间：23:46:16运行时间：up 179 days, 11:16,当前登录用户： 1 users负载均衡 (uptime) load average: 0.00, 0.02, 0.05

average 后面的三个数分别是 1 分钟、5 分钟、15 分钟的负载情况。load average 数据是每隔 5 秒钟检查一次活跃的进程数，然后按特定算法计算出的数值。如果这个数除以逻辑 CPU 的数量，结果高于 5 的时候就表明系统在超负荷运转了

**第二行，Tasks — 任务（进程）**总进程：96 total, 运行：1 running, 休眠：95 sleeping, 停止: 0 stopped, 僵尸进程: 0 zombie

**第三行，cpu 状态信息**0.3% us【user space】— 用户空间占用 CPU 的百分比0.5% sy【sysctl】— 内核空间占用 CPU 的百分比0.0% ni【】— 改变过优先级的进程占用 CPU 的百分比99.2% id【idolt】— 空闲 CPU 百分比0.0% wa【wait】— IO 等待占用 CPU 的百分比0.0% hi【Hardware IRQ】— 硬中断占用 CPU 的百分比0.0% si【Software Interrupts】— 软中断占用 CPU 的百分比

**第四行，内存状态**8009128 total, 832280 free, 1235088 used, 5941760 buff/cache【buffers 缓存的内存量】

**第五行，swap 交换分区信息**0 total, 0 free, 0 used. 6469384 avail Mem【cached 缓冲的交换区总量】

备注：可用内存 = free + buffer + cached 对于内存监控，在 top 里我们要时刻监控第五行 swap 交换分区的 used，如果这个数值在不断的变化，说明内核在不断进行内存和 swap 的数据交换，这是真正的内存不够用了。第四行中使用中的内存总量（used）指的是现在系统内核控制的内存数，第四行中空闲内存总量（free）是内核还未纳入其管控范围的数量。纳入内核管理的内存不见得都在使用中，还包括过去使用过的现在可以被重复利用的内存，内核并不把这些可被重新使用的内存交还到 free 中去，因此在 linux 上 free 内存会越来越少，但不用为此担心。

## 12. JDK 常用命令

Sun JDK 监控和故障处理命令有 jps jstat jmap jhat jstack jinfo

- jps，JVM Process Status Tool，显示指定系统内所有的 HotSpot 虚拟机进程；
- jstat，JVM statistics Monitoring，用于监视虚拟机运行时状态信息的命令，它可以显示出虚拟机进程中的类装载、内存、垃圾收集、JIT 编译等运行数据；
- jmap，JVM Memory Map 命令用于生成 heap dump 文件；
- jhat，JVM Heap Analysis Tool 命令是与 jmap 搭配使用，用来分析 jmap 生成的 dump 文件，jhat 内置了一个微型的 HTTP/HTML 服务器，生成 dump 的分析结果后，可以在浏览器中查看；
- jstack，用于生成 java 虚拟机当前时刻的线程快照；
- jinfo，JVM Configuration info 这个命令作用是实时查看和调整虚拟机运行参数。

## 13. 参考

- [1] [Linux 基本概念及常用命令实现汇总](https://reid.run/archives/linux1#toc-head-45)
- [2] [Linux 命令大全](https://www.runoob.com/linux/linux-command-manual.html)
- [3] [鸟哥的 Linux 私房菜](http://linux.vbird.org/)