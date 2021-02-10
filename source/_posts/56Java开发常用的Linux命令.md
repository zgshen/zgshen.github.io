---
title: Java开发常用的Linux命令
categories: 技术
tags: Linux
date: 2021-2-5
---

## 系统信息

### 1. uname
用于查看系统信息
```
uname -a    显示全部信息
```

### 2. lscpu  
cpu 架构信息


## 文件和目录操作

### 1. ls
列出文件或者目录的信息，目录的信息就是其中包含的文件。

```
## ls [-aAdfFhilnrRSt] file|dir
-a ：列出全部的文件
-d ：仅列出目录本身
-l ：以长数据串行列出，包含文件的属性与权限等等数据
-h : 和 -l 一起使用，列出文件同时以合理易读的单位显示文件大小
```

### 2. cd
更换当前目录。
```
cd [相对路径或绝对路径]
```

### 3. mkdir
创建目录。
```
## mkdir [-mp] 目录名称
-m ：配置目录权限
-p ：递归创建目录
```

### 4. rmdir
删除目录，目录必须为空。
```
rmdir [-p] 目录名称
-p ：递归删除目录
```

### 5. touch
更新文件时间或者建立新文件。
```
## touch [-acdmt] filename
-a ： 更新 atime
-c ： 更新 ctime，若该文件不存在则不建立新文件
-m ： 更新 mtime
-d ： 后面可以接更新日期而不使用当前日期，也可以使用 --date="日期或时间"
-t ： 后面可以接更新时间而不使用当前时间，格式为[YYYYMMDDhhmm]
```

### 6. cp
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

### 7. rm
删除文件。
```
## rm [-fir] 文件或目录
-r ：递归删除
```

### 8. mv
移动文件。
```
## mv [-fiu] source destination
## mv [options] source1 source2 source3 .... directory
-f ： force 强制的意思，如果目标文件已经存在，不会询问而直接覆盖
```

## 查看文件内容
### 1. cat
取得文件内容。
```
## cat [-AbEnTv] filename
-n ：打印出行号，连同空白行也会有行号，-b 不会

```

### 2. tac
是 cat 的反向操作，从最后一行开始打印。

### 3. more
和 cat 不同的是它可以一页一页查看文件内容，比较适合大文件的查看。

### 4. less
和 more 类似，但是多了一个向前翻页的功能。

### 5. head
取得文件前几行。
```
## head [-n number] filename
-n ：后面接数字，代表显示几行的意思
```

### 6. tail
是 head 的反向操作，只是取得是后几行。

### 7. od
以字符或者十六进制的形式显示二进制文件。

## 用户和用户组

## 权限操作

## 搜索

## 压缩和打包

## 防火墙

## vi/vim 基本操作

## 进程管理



## 参考

- [1] [Linux基本概念及常用命令实现汇总](https://reid.run/archives/linux1#toc-head-45)

- [2] [Linux 命令大全](https://www.runoob.com/linux/linux-command-manual.html)