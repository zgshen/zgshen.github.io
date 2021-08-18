---
title: ssh 登录远程服务器很慢原因
categories: 技术
tags: 基础
date: 2021-8-18
---

在远程服务器添加客户端的公钥之后，在 `~/.ssh/config` 文件中配置如下远程服务器链接后就能，通过命令 `ssh 服务器名` 登录远程服务器了，比如这里就是 `ssh tx`

```bash
#ssh 远程机器配置
#腾讯云
Host tx
HostName xxx.xxx.xxx.xxx
User root
Port 22
IdentityFile ~/.ssh/id_rsa
# 公钥默认文件名就是这个，IdentityFile 配置可以省略，如果文件是别的名称就指定下
```

但是有个问题就是，登录的时候总要要等个 20 来秒才连接上，这是什么原因呢

使用 `ssh -v tx` 可以看登录的日志

```
debug1: SSH2_MSG_SERVICE_ACCEPT received
debug1: Authentications that can continue: publickey,gssapi-keyex,gssapi-with-mic,password
debug1: Next authentication method: gssapi-with-mic
debug1: Unspecified GSS failure.  Minor code may provide more information
No Kerberos credentials available (default cache: FILE:/tmp/krb5cc_1000)


debug1: Unspecified GSS failure.  Minor code may provide more information
No Kerberos credentials available (default cache: FILE:/tmp/krb5cc_1000)


debug1: Next authentication method: publickey

```

登录的时候首先会尝试去使用 gssapi-with-mic 的方式，然后这里卡了 20 多秒失败了，之后才会去用 publickey 的方式登录上去。

看看 ssh config 文档怎么说的，`man ssh_config`

```
PreferredAuthentications
    Specifies the order in which the client should try authentication methods.  This allows a client to prefer one method (e.g.
    keyboard-interactive) over another method (e.g. password).  The default is:

        gssapi-with-mic,hostbased,publickey,
        keyboard-interactive,password

# 指定客户端尝试进行身份认证的方式。允许客服端优先选择一种方式比如（键盘输入），而不是另一种方式（比如密码）。默认方式有：...
```

所以，在 config 文件中指定 PreferredAuthentications 的优先选择的验证方式就好了，秒进。

```
#ssh 远程机器配置
#腾讯云
Host tx
HostName xxx.xxx.xxx.xxx
User root
Port 22
IdentityFile ~/.ssh/id_rsa
PreferredAuthentications publickey
```


