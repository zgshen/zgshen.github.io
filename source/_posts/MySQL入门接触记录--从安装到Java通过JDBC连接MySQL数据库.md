---
title: MySQL入门接触记录--从安装到Java通过JDBC连接MySQL数据库
categories: 技术
tags: 数据库
date: 2015-12-12
---
一、安装MySQL
1.本人用的版本是mysql-5.6.24-winx64解压免装版，链接：
http://xiazai.zol.com.cn/detail/4/33431.shtml
解压后找到my-default.ini文件，复制改名为my.ini，修改添加以下语句：<!--more-->
[client]
port=3306
default-character-set=utf8

[mysqld]
port=3306
character_set_server=utf8
#以下路径为你解压到的文件夹
basedir = D:\Program Files\mysql-5.6.24-winx64
datadir = D:\Program Files\mysql-5.6.24-winx64\data
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
2.配置环境变量：计算机-属性-高级系统设置-高级-环境变量，在Path中添加
D:\Program Files\mysql-5.6.24-winx64\bin
路径依然根据自己所解压到的路径决定，注意添加时前面用；分号隔开。
3.win+r进dos，cd到解压文件目录的bin文件下
安装服务：mysqld -install
启动服务:net start mysql
如果要删除服务，命令为：mysqld -remove
安装结束----------

二、创建数据库和表
以一个简单例子为例，步骤如下:
win+r进dos并cd到解压路径的bin文件下，执行mysql -uroot -p
因为初始密码为空，直接回车，如图

show databases;  显示目前所有的数据库
create database 库名;  因为之前person已经创建过，所有提示存在
创建完我们使用它，use person;


接着创建一个表名student的表,有两个简单的属性, 命令:create table <表名> (<字段名 1> <类型 1> [,..<字段名 n> <类型 n>]); 具体如下:

查看表结构命令: show columns from 表名;
插入数据命令:insert into <表名> [( <字段名 1>[,..<字段名 n > ])] values ( 值 1 )[, ( 值 n )]
以下随便插入两个
select * from 表名;  显示表所有内容


三、在eclipse上通过JDBC连接MySQl数据库
1.下载对应MySQL的驱动包 http://dev.mysql.com/downloads/connector/j/
解压驱动包，eclipse新建一个java工程MysqlDemo，复制驱动包的.jar文件，在java工程右键paste，接着在.jar包右键Build Path - Configure Build Path,这样驱动就加载进来了

测试程序参考自http://qq163230530.blog.163.com/blog/static/4289250620081186262719/
```java
import java.sql.*;

public class MysqlDemo {
	public static void main(String[] args) {
        //声明Connection对象
        Connection con;
        //驱动程序名
        String driver = "com.mysql.jdbc.Driver";
        //URL指向要访问的数据库名mydata
        String url = "jdbc:mysql://localhost:3306/person";
        //MySQL配置时的用户名
        String user = "root";
        //MySQL配置时的密码
        String password = "";
        //遍历查询结果集
        try {
            //加载驱动程序
            Class.forName(driver);
            //1.getConnection()方法，连接MySQL数据库！！
            con = DriverManager.getConnection(url,user,password);
            if(!con.isClosed())
                System.out.println("Succeeded connecting to the Database!");
            //2.创建statement类对象，用来执行SQL语句！！
            Statement statement = con.createStatement();
            //要执行的SQL语句
            String sql = "select * from student";
            //3.ResultSet类，用来存放获取的结果集！！
            ResultSet rs = statement.executeQuery(sql);
            System.out.println("-----------------");
            System.out.println("执行结果如下所示:");  
            System.out.println("-----------------");  
            System.out.println(" 学号" + "\t" + " 姓名");  
            System.out.println("-----------------");  
             
            String name = null;
            String id = null;
            while(rs.next()){
                //获取stuname这列数据
                name = rs.getString("name");
                //获取stuid这列数据
                id = rs.getString("id");
                //首先使用ISO-8859-1字符集将name解码为字节序列并将结果存储新的字节数组中。
                //然后使用GB2312字符集解码指定的字节数组。
                name = new String(name.getBytes("ISO-8859-1"),"gb2312");
                //输出结果
                System.out.println(id + "\t" + name);
            }
            rs.close();
            con.close();
        } catch(ClassNotFoundException e) {   
            //数据库驱动类异常处理
            System.out.println("Sorry,can`t find the Driver!");   
            e.printStackTrace();   
            } catch(SQLException e) {
            //数据库连接失败异常处理
            e.printStackTrace();  
            }catch (Exception e) {
            // TODO: handle exception
            e.printStackTrace();
        }finally{
            System.out.println("数据库数据成功获取！！");
        }
    }
}
```
run结果


印象流程大概这样，水平有限，记录。


