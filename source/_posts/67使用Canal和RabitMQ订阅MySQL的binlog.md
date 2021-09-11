---
title: 使用 canal 和 RabitMQ 订阅 MySQL 的 binlog
categories: 技术
tags: 
  - 技术
  - 数据库
date: 2021-09-11
---

记录下用 RabitMQ 订阅 binlog 的方法，相关编码的 GitHub 地址在 https://github.com/zgshen/lin/tree/master/lin-mq

### 1.数据库

数据库新建 canal 从库用户用于订阅

```sql
CREATE USER canal IDENTIFIED BY 'canal&*123ABC';
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'canal'@'%';
FLUSH PRIVILEGES;
```

查看是否开启 binlog 模式，如果log_bin的值为OFF是未开启，为ON是已开启

```sql
SHOW VARIABLES LIKE '%log_bin%'
```

修改/etc/my.cnf 需要开启binlog模式

```bash
[mysqld]
log-bin=mysql-bin # 开启 binlog
binlog-format=ROW # 选择 ROW 模式
server_id=1 # 配置 MySQL replaction 需要定义，不要和 canal 的 slaveId 重复
```

### 2.canal

下载 canal

```bash
# 迫于墙的问题。源地址 download 太慢，用镜像
wget https://mirror.ghproxy.com/\?q\=https%3A%2F%2Fgithub.com%2Falibaba%2Fcanal%2Freleases%2Fdownload%2Fcanal-1.1.5%2Fcanal.deployer-1.1.5.tar.gz
# 文件名格式有问题改下
mv index.html\?q=https:%2F%2Fgithub.com%2Falibaba%2Fcanal%2Freleases%2Fdownload%2Fcanal-1.1.5%2Fcanal.deployer-1.1.5.tar.gz canal.deployer.tar.gz
tar -zvxf canal.deployer.tar.gz
```

配置

conf/canal.properties

```bash
# tcp, kafka, rocketMQ, rabbitMQ
canal.serverMode = rabbitMQ

rabbitmq.host = 172.17.0.1
rabbitmq.virtual.host = /
rabbitmq.exchange = BINLOG_MQ_EXCHANGE
rabbitmq.username = mq
rabbitmq.password = mq123
# 当且仅当参数为2时，才会开启消息持久化，参数未配置、参数值为空或者参数值不等于2时，均不开启rabbitmq消息持久化
rabbitmq.deliveryMode =
```

conf/example/instance.properties

```bash
# username/password  用户名密码
canal.instance.dbUsername=canal
canal.instance.dbPassword=canal&*123ABC
canal.instance.connectionCharset = UTF-8

# table regex  正则匹配，这里是匹配所有表，根据需要匹配
canal.instance.filter.regex=.*\\..*
# table black regex
canal.instance.filter.black.regex=mysql\\.slave_.*

# mq config 设置路由键，需要匹配 MQ 队列的规则
#canal.mq.topic=example
canal.mq.topic=BINLOG_MQ_KEY.canal
```

启动没成功，错误

```bash
OpenJDK 64-Bit Server VM warning: Ignoring option PermSize; support was removed in 8.0
OpenJDK 64-Bit Server VM warning: Ignoring option MaxPermSize; support was removed in 8.0
OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was deprecated in version 9.0 and will likely be removed in a future release.
Unrecognized VM option 'UseCMSCompactAtFullCollection'
Error: Could not create the Java Virtual Machine.
Error: A fatal exception has occurred. Program will exit.
```

环境用的 openjdk11，有些 JVM 参数不能用所有启动失败了，改下启动脚本指定用 java8，或者自己改下 JVM 参数试试，如果你懂的话

```bash
## 编辑 canal/bin/startup.sh
## set java path
if [ -z "$JAVA" ] ; then
  //JAVA=$(which java) which 出来的是系统变量的 java 路径，换成你想要的，这里我的 java8 路径是 /usr/local/java/bin/java
  JAVA=/usr/local/java/bin/java
fi
```

### 3.RabbitMQ 和 Java 工程消费

建一个 topic 模式的交换机 BINLOG_MQ_EXCHANGE，再建一个队列 BINLOG_MQ_QUEUE 绑定交换机，路由键设置为 BINLOG_MQ_KEY.*

Spring Boot Java 工程 MQ 的配置

```java
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class BinlogMQConfig {

    public final static String BINLOG_MQ_EXCHANGE = "BINLOG_MQ_EXCHANGE";
    
    public final static String BINLOG_MQ_QUEUE = "BINLOG_MQ_QUEUE";
    
    public final static String BINLOG_MQ_KEY = "BINLOG_MQ_KEY.*";

    @Bean
    public TopicExchange binlogTopicExchange() {
        return new TopicExchange(BINLOG_MQ_EXCHANGE);
    }

    @Bean
    public Queue binlogQueue() {
        return new Queue(BINLOG_MQ_QUEUE);
    }

    @Bean
    Binding bindingBinlogExchangeMessages(Queue queue, TopicExchange topicExchange) {
        return BindingBuilder.bind(queue).to(topicExchange).with(BINLOG_MQ_KEY);
    }
}
```

消费者这里用了事物确认模式，手动 ACK 以下

```java
import com.rabbitmq.client.Channel;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.core.ExchangeTypes;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.*;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Slf4j
@Component
public class BinlogConsumerService {

    @RabbitListener(bindings = @QueueBinding(
            value = @Queue(value = BinlogMQConfig.BINLOG_MQ_QUEUE, autoDelete = "false"),
            exchange = @Exchange(value = BinlogMQConfig.BINLOG_MQ_EXCHANGE, type = ExchangeTypes.TOPIC), key = BinlogMQConfig.BINLOG_MQ_KEY),
            containerFactory = "pointTaskContainerFactory")
    @RabbitHandler
    public void process(Message msg, Channel channel) throws IOException {
        log.info("===binlog消费者获取mq消息：{}", msg);
        log.info("===msg properties: " + msg.getMessageProperties().toString());
        log.info("===msg body: " + new String(msg.getBody()));
        //com.lin.mq.rabbitmq.config.RabbitMQConfig.rabbitTransactionManager 有设置事务模式需要手动ack
        channel.basicAck(msg.getMessageProperties().getDeliveryTag(),false);
    }
}
```

测试插入和更新

```sql
INSERT INTO `lin`.`sys_log` (`user_id`, `username`, `operation`, `time`, `method`, `params`, `ip`, `gmt_create`) VALUES 
('100', 'admin', '用户登录', '162', 'com.admin.system.controller.LoginController.ajaxLogin()', NULL, '127.0.0.1', '2021-09-11 17:59:33');

UPDATE sys_log SET user_id='101' WHERE id = 9563;
```

消费日志

```bash
2021-09-11 18:20:49.246  INFO 3500 --- [ntContainer#0-2] com.lin.mq.binlog.BinlogConsumerService  : ===binlog消费者获取mq消息：(Body:'[B@59cec6f8(byte[704])' MessageProperties [headers={}, contentLength=0, redelivered=false, receivedExchange=BINLOG_MQ_EXCHANGE, receivedRoutingKey=BINLOG_MQ_KEY.canal, deliveryTag=1, consumerTag=amq.ctag-sERW0IDERXfdDJVX9qbBvQ, consumerQueue=BINLOG_MQ_QUEUE])
2021-09-11 18:20:49.247  INFO 3500 --- [ntContainer#0-2] com.lin.mq.binlog.BinlogConsumerService  : ===msg properties: MessageProperties [headers={}, contentLength=0, redelivered=false, receivedExchange=BINLOG_MQ_EXCHANGE, receivedRoutingKey=BINLOG_MQ_KEY.canal, deliveryTag=1, consumerTag=amq.ctag-sERW0IDERXfdDJVX9qbBvQ, consumerQueue=BINLOG_MQ_QUEUE]
2021-09-11 18:20:49.247  INFO 3500 --- [ntContainer#0-2] com.lin.mq.binlog.BinlogConsumerService  : ===msg body: {"data":[{"id":"9563","user_id":"100","username":"admin","operation":"用户登录","time":"162","method":"com.admin.system.controller.LoginController.ajaxLogin()","params":null,"ip":"127.0.0.1","gmt_create":"2021-09-11 17:59:33"}],"database":"lin","es":1631355648000,"id":4,"isDdl":false,"mysqlType":{"id":"bigint(20)","user_id":"bigint(20)","username":"varchar(50)","operation":"varchar(50)","time":"int(11)","method":"varchar(200)","params":"text","ip":"varchar(64)","gmt_create":"datetime"},"old":null,"pkNames":["id"],"sql":"","sqlType":{"id":-5,"user_id":-5,"username":12,"operation":12,"time":4,"method":12,"params":-4,"ip":12,"gmt_create":93},"table":"sys_log","ts":1631355648355,"type":"INSERT"}
2021-09-11 18:21:15.380  INFO 3500 --- [ntContainer#0-3] com.lin.mq.binlog.BinlogConsumerService  : ===binlog消费者获取mq消息：(Body:'[B@7e7756ad(byte[719])' MessageProperties [headers={}, contentLength=0, redelivered=false, receivedExchange=BINLOG_MQ_EXCHANGE, receivedRoutingKey=BINLOG_MQ_KEY.canal, deliveryTag=1, consumerTag=amq.ctag-EYi2Ci4Y1kEAXzT33FSBmA, consumerQueue=BINLOG_MQ_QUEUE])
2021-09-11 18:21:15.380  INFO 3500 --- [ntContainer#0-3] com.lin.mq.binlog.BinlogConsumerService  : ===msg properties: MessageProperties [headers={}, contentLength=0, redelivered=false, receivedExchange=BINLOG_MQ_EXCHANGE, receivedRoutingKey=BINLOG_MQ_KEY.canal, deliveryTag=1, consumerTag=amq.ctag-EYi2Ci4Y1kEAXzT33FSBmA, consumerQueue=BINLOG_MQ_QUEUE]
2021-09-11 18:21:15.380  INFO 3500 --- [ntContainer#0-3] com.lin.mq.binlog.BinlogConsumerService  : ===msg body: {"data":[{"id":"9563","user_id":"101","username":"admin","operation":"用户登录","time":"162","method":"com.admin.system.controller.LoginController.ajaxLogin()","params":null,"ip":"127.0.0.1","gmt_create":"2021-09-11 17:59:33"}],"database":"lin","es":1631355674000,"id":5,"isDdl":false,"mysqlType":{"id":"bigint(20)","user_id":"bigint(20)","username":"varchar(50)","operation":"varchar(50)","time":"int(11)","method":"varchar(200)","params":"text","ip":"varchar(64)","gmt_create":"datetime"},"old":[{"user_id":"100"}],"pkNames":["id"],"sql":"","sqlType":{"id":-5,"user_id":-5,"username":12,"operation":12,"time":4,"method":12,"params":-4,"ip":12,"gmt_create":93},"table":"sys_log","ts":1631355674489,"type":"UPDATE"}
```

### 4.参考

- [1] [canal 整合RabbitMQ](https://www.jianshu.com/p/60a9176a8825)
- [2] [Home · alibaba/canal Wiki](https://github.com/alibaba/canal/wiki)