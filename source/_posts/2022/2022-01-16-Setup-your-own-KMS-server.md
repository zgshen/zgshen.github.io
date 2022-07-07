---
title: Setup your own KMS server
categories: 技术
tags: 
    - KMS
    - Windows
    - Office
date: 2022-01-16
toc: true
---

I have setup a KMS server on my CentOS VPS, it allows me to significantly simply the process of activating Microsoft products on the corporate network.

Here are the installation steps:

### Firstly, download the latest version of [vlmcsd](https://github.com/Wind4/vlmcsd) and unzip.

```bash
# find latest version on https://github.com/Wind4/vlmcsd/releases
wget https://github.com/Wind4/vlmcsd/releases/download/svn1113/binaries.tar.gz
tar -zxvf binaries.tar.gz
# according your OS and CPU type
cd binaries/Linux/intel/static/
```

Startup vlmcsd with command:

```bash
./vlmcsd-x64-musl-static -L 0.0.0.0:xxxx
# if you not use -L, default port is 1688
# ./vlmcsd-x64-musl-static -L 0.0.0.0:16882
```

Just use the IP+Port is all right, certainly you can also bind domain by Nginx forward.

```bash
server {
        listen       80;
        server_name  kms.example.com;
        location ^~ / {
            proxy_pass http://127.0.0.1:1688/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
```

### Secondly check availability.

```bash
# other port ./vlmcs-x64-musl-static 0.0.0.0:16882
# default
$ ./vlmcs-x64-musl-static
Connecting to 0.0.0.0:1688 ... successful
Sending activation request (KMS V6) 1 of 1  -> 03612-00206-566-464396-03-1103-14393.0000-2672021 (3A1C049600B60076)
```

On Windows open CMD, enter `\binaries\Windows\intel` directory.

```bash
vlmcs-Windows-x86.exe [IP or domain]:[Port]
```

### Finally activate Windows/Office

Find the Vol key that corresponds to [Windows](https://docs.microsoft.com/zh-cn/windows-server/get-started/kmsclientkeys) or [Office](https://docs.microsoft.com/en-us/DeployOffice/vlactivation/gvlks) (make sure the Office is Vol version).

#### Windows

Install the key you find above:

```bash
slmgr /ipk xxxxx-xxxxx-xxxxx-xxxxx-xxxxx
```

Set KMS server：

```bash
slmgr /skms [IP或domain]:[端口号]
```

Activate OS：

```bash
slmgr /ato
```

#### Office

Go to the Office installation directory, for example the default for 64-bit Office 2016 is:

```
C:\Program Files\Microsoft Office\Office16
```

Install the key you find above:

```
cscript ospp.vbs /inpkey:xxxxx-xxxxx-xxxxx-xxxxx-xxxxx
```

Run CMD with administrator, and registry KMS server address:

```
cscript ospp.vbs /sethst:[domain]
# if you use other port, set ip and port separately
# cscript ospp.vbs /sethst:[IP]
# cscript ospp.vbs /setprt:[Port]
```

Activate Office：

```
cscript ospp.vbs /act
```

查看激活信息：

View activation info:

```
cscript ospp.vbs /dstatus
```

### Registry service

The KMS method of activation is valid for 180 days, so keep the vlmcsd service running, it will request a renewal automatically.

Create a `vlmcsd.service` file and edit.

```bash
[Unit]
Description=KMS Server By vlmcsd
After=network.target

[Service]
Type=forking
PIDFile=/var/run/vlmcsd.pid
# ExecStart=/home/nathan/app/binaries/Linux/intel/static/vlmcsd-x64-musl-static -L 0.0.0.0:16882 -p /var/run/vlmcsd.pid
ExecStart=/binaries/Linux/intel/static/vlmcsd-x64-musl-static -p /var/run/vlmcsd.pid
ExecStop=/bin/kill -HUP $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Configure vlmcsd as a system service.

```bash
cp vlmcsd.service /etc/systemd/system/
```

Then you can Manage vlmcsd service with `systemctl`.

```bash
# reload 
systemctl daemon-reload
# Turn on boot up
systemctl enable vlmcsd
# startup
systemctl start vlmcsd
# running info
systemctl status vlmcsd
```
