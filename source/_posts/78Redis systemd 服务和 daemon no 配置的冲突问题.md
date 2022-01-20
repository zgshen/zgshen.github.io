---
title: Redis systemd 服务和 daemon no 配置的冲突问题
categories: 技术
tags: 
    - 技术
    - Redis
date: 2022-01-16
---

Ubuntu 虚拟机安装 Reis，`sudo apt install redis -y`。

然后照着以前的经验修改了配置文件`/etc/redis/redis.conf`，关闭保护模式，设置守护线程，去掉外网访问限制：

```bash
# By default protected mode is enabled. You should disable it only if
# you are sure you want clients from other hosts to connect to Redis
# even if no authentication is configured, nor a specific set of interfaces
# are explicitly listed using the "bind" directive.
#protected-mode yes
protected-mode no

# By default Redis does not run as a daemon. Use 'yes' if you need it.
# Note that Redis will write a pid file in /var/run/redis.pid when daemonized.
# daemonize yes
# apt 安装方式这里默认是 yes 开启守护线程，改错的就是这个地方
# 但是自己手动官网下压缩包这个值是 no，才要改成 yes
daemonize no

# IF YOU ARE SURE YOU WANT YOUR INSTANCE TO LISTEN TO ALL THE INTERFACES
# JUST COMMENT THE FOLLOWING LINE.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#bind 127.0.0.1 ::1
```

因为当时没有立刻重启验证没发现问题，后来过几天用到了 Redis 测试能直接连接就直接用了。然后在跑项目的时候就出问题了。项目中有用到 Lua 脚本，项目刚启动的时候没问题，但过一两分钟就会报 `NOSCRIPT No matching script. Please use EVAL` 脚本找不到的问题，在服务器上查询脚本是否存在：

```bash
127.0.0.1:6379> SCRIPT EXISTS 54a45387997c486efb954b3bf990f34881e41b7a
1) (integer) 1
127.0.0.1:6379> SCRIPT EXISTS 54a45387997c486efb954b3bf990f34881e41b7a
1) (integer) 0
```

项目启动加载 Lua 脚本到 Redis 一开始存在，一会就没了，奇怪，看看 systemd status：

```bash
$ systemctl status redis-server.service
● redis-server.service - Advanced key-value store
     Loaded: loaded (/lib/systemd/system/redis-server.service; enabled; vendor preset: enabled)
     Active: activating (start) since Mon 2022-01-17 22:16:03 CST; 54s ago
       Docs: http://redis.io/documentation,
             man:redis-server(1)
Cntrl PID: 14160 (redis-server)
      Tasks: 4 (limit: 4612)
     Memory: 1.9M
     CGroup: /system.slice/redis-server.service
             └─14160 /usr/bin/redis-server *:6379

Jan 17 22:16:03 vb-ubuntu systemd[1]: Starting Advanced key-value store...
```

还在 activating 中，但此时 Redis 是已经可以访问的了，再看看 journalctl 的日志：

```bash
$ journalctl -b -u redis-server
-- Logs begin at Tue 2021-11-16 10:31:34 CST, end at Mon 2022-01-17 22:30:57 CST. --
Jan 16 16:49:47 vb-ubuntu systemd[1]: Starting Advanced key-value store...
Jan 16 16:51:18 vb-ubuntu systemd[1]: redis-server.service: start operation timed out. Terminating.
Jan 16 16:51:18 vb-ubuntu systemd[1]: redis-server.service: Failed with result 'timeout'.
Jan 16 16:51:18 vb-ubuntu systemd[1]: Failed to start Advanced key-value store.
Jan 16 16:51:19 vb-ubuntu systemd[1]: redis-server.service: Scheduled restart job, restart counter is at 1.
Jan 16 16:51:19 vb-ubuntu systemd[1]: Stopped Advanced key-value store.
```

可以看到 Failed with result 'timeout' 后接着 Scheduled restart job，Redis 重启，一直循环反复。Redis   持久化并没有保存 Lua 脚本的，重启后就会丢失，所有项目会有脚本找不到的问题。

此时问题很清晰了，应该是改了一些配置导致出问题，先看看 Redis 服务的配置：

```bash
# /etc/systemd/system/redis.service
[Service]
Type=forking
ExecStart=/usr/bin/redis-server /etc/redis/redis.conf
PIDFile=/run/redis/redis-server.pid
TimeoutStopSec=0
Restart=always
Restart=no
User=redis
Group=redis
RuntimeDirectory=redis
RuntimeDirectoryMode=2755
```

`Restart=always` 服务启动失败了也会一直尝试重启。`Type=forking` 和 `/etc/redis/redis.conf` 中的 `daemonize no` 冲突了。

`man systemd.service` 可以看 Type 为 forking 的解释：如果设为 forking ，那么表示 ExecStart= 进程将会在启动过程中使用 fork() 系统调用。 也就是当所有通信渠道都已建好、启动亦已成功之后，父进程将会退出，而子进程将作为主服务进程继续运行。 这是传统UNIX守护进程的经典做法。 在这种情况下，systemd 会认为在父进程退出之后，该服务就已经启动完成。 如果使用了此种类型，那么建议同时设置 PIDFile= 选项，以帮助 systemd 准确可靠的定位该服务的主进程。 systemd 将会在父进程退出之后 立即开始启动后继单元。

“父进程将会退出，而子进程将作为主服务进程继续运行”，所以 Redis 设置为非守护进程就有问题了。
