---
title: Mysql清除错误临时表
categories: 技术
tags: 技术
date: 2019-09-26
---


去年对数据库一个大表做了 optimize 操作，由于不了解具体操作就草草执行了。此操作会拷贝原表数据到临时表，如果此时硬盘空间不够，就会报错，或者表太大，执行时间将及其漫长，反正哪种都是不可接受的。
<!--more-->
这是当时的日志
![image](https://user-images.githubusercontent.com/20520272/65656809-c0057000-e053-11e9-82ba-399e98adcd48.png)


当时就把进程 kill 掉了，但是留下了一个 75G 没有用的临时表，后来因为服务器加了硬盘空间，就没有去管它。最近硬盘又快占满，这个 75G 废弃文件实在碍眼，就着手看看怎么安全删除。

首先暴力 rm 必定不可取，参考互联网资料，这个应该是官方的一个解决方案
https://mariadb.com/resources/blog/get-rid-of-orphaned-innodb-temporary-tables-the-right-way/

![image](https://user-images.githubusercontent.com/20520272/65656922-2094ad00-e054-11e9-8c49-2ee8d50397e6.png)


试着按参考链接执行建同名表，正常建表命令肯定不会影响数据库，找到原来的表结构建表
CREATE TABLE `#sql-5df6_36c` (
  `id` bigint(32) NOT NULL AUTO_INCREMENT,
  `card` varchar(50) DEFAULT NULL COMMENT '卡券号',
  `createTime` datetime DEFAULT NULL COMMENT '创建时间',
  `status` varchar(1) DEFAULT NULL COMMENT '状态',
  `posData` text COMMENT 'POS请求的数据',
  `ffData` text COMMENT '飞凡返回的data',
  `reason` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `card_index` (`card`)
) ENGINE=InnoDB AUTO_INCREMENT=152943355 DEFAULT CHARSET=utf8;

![image](https://user-images.githubusercontent.com/20520272/65656942-2e4a3280-e054-11e9-90e6-6f338e8b5416.png)


结果残缺的 #sql-5df6_36c.frm 被自动删掉
![image](https://user-images.githubusercontent.com/20520272/65656964-3ace8b00-e054-11e9-8237-80a89a339ce7.png)


接下来剩下缺失表结构的大文件
cp cc_card_log.frm /app/mysql/data/watsons_coupon/#sql-ib2460-3936078760.frm
复制表结构命名与临时表相同

![image](https://user-images.githubusercontent.com/20520272/65656989-4ae66a80-e054-11e9-9cd5-c9d36f4b2757.png)


再 drop 表，提示表不存在
![image](https://user-images.githubusercontent.com/20520272/65657013-5cc80d80-e054-11e9-9c0a-100e0467ce8b.png)


先再建表
![image](https://user-images.githubusercontent.com/20520272/65657025-66ea0c00-e054-11e9-9bc2-4bb41efbe406.png)


可以看到与临时表同名多会生成这两个文件，原来的两个文件也还在的
![image](https://user-images.githubusercontent.com/20520272/65657033-70737400-e054-11e9-9e00-4b53ba93e40f.png)


再试试 drop 表
![image](https://user-images.githubusercontent.com/20520272/65657048-7cf7cc80-e054-11e9-9c28-189f9c8de552.png)

发现不行，四个文件都还在
再尝试
![image](https://user-images.githubusercontent.com/20520272/65657062-8aad5200-e054-11e9-920a-8cd054a5ccc1.png)


@0023sql@002dib2460@002d3936078760 两个文件倒是删掉了
#sql-ib2460-3936078760 两个还好好的
仔细一看
#sql-ib2460-3936078760.frm  用户组用户都是 root ，cp 的时候用了 sudo 执行，需要授权用户

chown mysql:mysql \#sql-ib2460-3936078760.frm
![image](https://user-images.githubusercontent.com/20520272/65657080-9ac53180-e054-11e9-939e-6c5c0cdb95ce.png)

再 drop 表
![image](https://user-images.githubusercontent.com/20520272/65657103-a9134d80-e054-11e9-8dcd-88cecd594ce1.png)

75G文件5s多drop掉，总算删掉了
