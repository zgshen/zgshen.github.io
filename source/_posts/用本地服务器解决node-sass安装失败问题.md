---
title: 用本地服务器解决node-sass安装失败问题
categories: 技术
tags: 其他
date: 2017-08-20
---

今天要用到node-sass这东西，使用命令 `npm install node-sass --save` 安装。然而搞半天始终下载不来，换成淘宝的镜像都不行，因为下载时还会去github下载一个 `win32-x64-48_binding.node` 的包，然后下不来就一直卡着最后失败。<!--more-->
一种解决方法就是根据下载失败提示的链接直接把那个二进制包下载下来，然后放在本地服务器目录下，比如可以根据失败提示的版本号在Nginx的html目录下以版本号建个文件夹放进去，像这样 `nginx-1.10.1\html\v4.5.3\win32-x64-48_binding.node` ,然后执行 `npm install node-sass --save-dev --sass-binary-site=http://localhost:8090/ --registry=https://registry.npm.taobao.org` 端口号为Nginx设置的端口号， `v4.5.3\win32-x64-48_binding.node` 这一串不用加，这样 `win32-x64-48_binding.node` 这个包就直接从本地服务器下载了。





