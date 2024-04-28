---
title: Redis 消息队列在 SpringBoot 中的使用
categories: 技术
tags:
  - Redis
toc: true
date: 2024-04-27
---

Redis 除了做数据缓存，做 NoSQL 数据库，也可以当做轻量级消息队列使用，并且提供了基于 List 实现的、基于 Pub/Sub 机制的订阅/发布模式、基于 sorted set 的实现和基于 Stream 类型的实现几种实现方式。其中 List 实现的分非阻塞和阻塞方式，Stream 则是新版 Redis 5 才支持的消息队列。

<!-- more -->

之前代码已经写过了，只是工程整合搞得比较复杂，所以这里算是写份注释文档。

关联代码地址[lin/lin-redis at master · zgshen/lin](https://github.com/zgshen/lin/tree/master/lin-redis)。

### 使用 List 类型实现

List 就是列表数据结构，用来做消息队列这是最简单直观的了，也是典型的点对点消息模型，先看下 Redis 列表提供的操作命令。

push 压入：

- LPUSH key value1 [value2 ...] 将一个或多个值插入到列表头部
- RPUSH key value1 [value2 ...] 将一个或多个值插入到列表尾部

pop 弹出：

- LPOP key 移除并获取列表的第一个元素
- RPOP key 移除并获取列表的最后一个元素

阻塞弹出；：

- BLPOP key1 [key2 ...] timeout 移除并获取列表的第一个元素，若列表为空则阻塞等待
- BRPOP key1 [key2 ...] timeout 移除并获取列表的最后一个元素，若列表为空则阻塞等待

压入和弹出前面的 L 和 R 表示从队列左端和右端压入和弹出，阻塞弹出的 B 代表就是 blocking 的意思。

使用队列一般遵循先进先出，所以要么左近右出，要么右近左出，框架提供的 RedisTemplate 封装了 Redis 的操作命令，push 和 pop 直接调用就行。

```java
@Autowired
private RedisTemplate redisTemplate;

//左进
public Long push(String... params) {
    Long aLong = redisTemplate.opsForList().leftPushAll(LIST_PUSH_POP_MSG, params);
    return aLong;
}

//右出，轮询检测
public String pop() {
    String str = redisTemplate.opsForList().rightPop(LIST_PUSH_POP_MSG).toString();
    return str;
}
```

再看下堵塞弹出的异步操作。

```java
public void blockingConsume() {
    List<Object> obj = redisTemplate.executePipelined(new RedisCallback<Object>() {
        //   @Nullable
        @Override
        public Object doInRedis(RedisConnection connection) throws DataAccessException {
            //队列没有元素会阻塞操作，直到队列获取新的元素或超时
            //return connection.bRPop(PUB_SUB_TIME_OUT, LIST_PUSH_POP_MSG.getBytes());
            return connection.bLPop(PUB_SUB_TIME_OUT, LIST_PUSH_POP_MSG.getBytes());
        }
    }, new StringRedisSerializer());
    for (Object str : obj) {
        log.info("blockingConsume : {}", str);
    }
}
```

此外 Redis 还有两个命令 RPOPLPUSH、BRPOPLPUSH（阻塞）可以从一队列获取队列并且写入另一个队列，可以用于简单保证消息可靠性，业务成功处理后再移除另一队列的消息，如果业务处理失败又可以从另一队列恢复。

```java
public String rightPopLeftPush() {
    String str;
    try {
        str = redisTemplate.opsForList().rightPopAndLeftPush(LIST_PUSH_POP_MSG, LIST_PUSH_POP_BACKUP_MSG).toString();
        // 其他业务，处理失败了还能在 LIST_PUSH_POP_BACKUP_MSG 队列找到备份
    } catch (Exception e) {
        log.error("业务异常：{}", e.getMessage());
        throw new RuntimeException(e);
    }
    // 先进先出业务完毕出栈，让异常的消息留在队列里
    redisTemplate.opsForList().leftPop(LIST_PUSH_POP_BACKUP_MSG);
    return str;
}
```

### 使用 Sorted Set 实现

Sorted Set 是有序集合，元素唯一不可重复，元素按照 score 值升序排列，支持范围操作，所以适合做简单的延迟消息队列。

添加元素：

- ZADD key score member [score member ...] 向有序集合中加入一个或多个成员,或更新已存在成员的分数

获取元素：

- ZRANGE key start stop [WITHSCORES] 按位置范围遍历集合,可附加分数
- ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT...] 按分数范围遍历集合

以下是简单的生产和消费程序：

```java
/**
 * @param businessId 业务 id（如订单 id 等）
 * @param expiredTime 延时时间，单位秒
 */
public void produce(String businessId, long expiredTime) {
    redisTemplate.opsForZSet().add(MsgConstant.SORTED_SET_MSG, businessId, System.currentTimeMillis() + expiredTime * 1000);
}

/**
 * 简单的消费程序
 * 死循环，仅做测试
 */
public void consume() {
    while (true) {
        //(K key, double min, double max, long offset, long count)
        //键，要取区间score最小值，要取区间score最大值，偏移（从哪个位置开始），数量
        Set<String> set = redisTemplate.opsForZSet().rangeByScore(MsgConstant.SORTED_SET_MSG, 0, System.currentTimeMillis(), 0, 1);
        if (set == null || set.isEmpty()) continue;
        log.info(set.toString());
        String next = set.iterator().next();
        Long remove = redisTemplate.opsForZSet().remove(MsgConstant.SORTED_SET_MSG, next);
        if (remove > 0) log.info("{} remove success.", next);
    }
}
```

### 使用 Pub/Sub 订阅发布模式

发布者把消息发到某个频道，订阅改频道的所有消费者都会收到消息，即消息多播，并且订阅支持模糊匹配频道。这种方式就是常规的消费者-消费者模型，不过与典型的 MQ 还是有区别，Pub/Sub 订阅发布更像是个广播，不能并发消费，不支持持久化，也没有 ACK 确认。

发布命令：

- PUBLISH channel message : 将消息 message 发布到指定的频道 channel

订阅命令：

- SUBSCRIBE channel [channel ...] : 订阅一个或多个频道
- PSUBSCRIBE pattern [pattern ...] : 订阅一个或多个模式,用于模糊匹配频道

Spring 工程的配置类：

```java
@Bean
public RedisMessageListenerContainer container(RedisConnectionFactory connectionFactory,
                                                MessageListenerAdapter adapter, MessageListenerAdapter adapter1) {
    RedisMessageListenerContainer container = new RedisMessageListenerContainer();
    container.setConnectionFactory(connectionFactory);
    //主题的监听，adapter 和 adapter1 对应下面两个 bean 实例，有多少
    container.addMessageListener(adapter, new PatternTopic(PUB_SUB_MSG));//普通的订阅者
    container.addMessageListener(adapter1, new PatternTopic(PUB_SUB_MSG_FUZZY));//模糊匹配的订阅者
    return container;
}

/**
 * 多个订阅
 * @param message
 * @return
 */
@Bean
public MessageListenerAdapter adapter(MessageSubscribe message){
    // MessageSubscribe 的 onMessage 监听获取订阅数据
    return new MessageListenerAdapter(message, "onMessage");
}

@Bean
public MessageListenerAdapter adapter1(MessageSubscribe1 message){
    // MessageSubscribe1 的 onMessage
    return new MessageListenerAdapter(message, "onMessage");
}
```

订阅者类：
```java
@Slf4j
@Component
public class MessageSubscribe implements MessageListener {

    @Override
    public void onMessage(Message message, byte[] bytes) {
        log.info("sub, topic name: {}, message: {}", new String(bytes), new String(message.getBody()));
    }

}
```

发布者类：
```java
@Service
public class MessagePublish {

    @Autowired
    StringRedisTemplate redisTemplate;

    public void publish(String channel, String msg) {
        redisTemplate.convertAndSend(channel, msg);
    }

}
```

### 使用 Stream

Redis 5.0 新增了 Stream 的数据结构，与 Pub/Sub 订阅发布模式相比，Redis Stream 提供了消息的持久化和主备复制功能。

添加消息：
```
XADD key ID field value [field value ...] 
```
其中ID，消息id，可使用 * 表示由 redis 生成，可以自定义，但是要自己保证递增性

读取消息：
```
XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] id [id ...]
```
milliseconds 设置堵塞秒数，没设置就是非阻塞模式。

创建消费者组：
```
XGROUP [CREATE key groupname id-or-$] [SETID key groupname id-or-$] [DESTROY key groupname] [DELCONSUMER key groupname consumername]
```
key 队列名，不存在就创建；groupname 组名；$ 表示从尾部开始消费，只接受新消息，当前 Stream 消息会全部忽略。
```
# 从头开始消费
XGROUP CREATE mystream consumer-group-name 0-0  

# 从尾部开始消费
XGROUP CREATE mystream consumer-group-name $
```

读取消费者组中的消息：
```
XREADGROUP GROUP group consumer [COUNT count] [BLOCK milliseconds] [NOACK] STREAMS key [key ...] ID [ID ...]
```
group 消费组名；consumer 消费者名；count 读取数量；milliseconds 阻塞毫秒数；key 队列名；ID 消息 ID。

例子：
```
XREADGROUP GROUP consumer-group-name consumer-name COUNT 1 STREAMS mystream >
```

看下在 Spring Boot 中的使用：

```java
/**
 * 启动初始化配置，注册 listener
 */
@Slf4j
@Component
public class RedisStreamRunner implements ApplicationRunner, DisposableBean {

    private StreamMessageListenerContainer<String, MapRecord<String, String, String>> container;
    private final ThreadPoolTaskExecutor executor;
    private final RedisConnectionFactory redisConnectionFactory;
    private final StringRedisTemplate stringRedisTemplate;

    public RedisStreamRunner(ThreadPoolTaskExecutor executor, RedisConnectionFactory redisConnectionFactory, StringRedisTemplate stringRedisTemplate) {
        this.executor = executor;
        this.redisConnectionFactory = redisConnectionFactory;
        this.stringRedisTemplate = stringRedisTemplate;
    }

    @Override
    public void run(ApplicationArguments args) throws Exception {
        StreamMessageListenerContainer.StreamMessageListenerContainerOptions<String, MapRecord<String, String, String>> options =
                StreamMessageListenerContainer.StreamMessageListenerContainerOptions.builder()
                        .batchSize(10)// 一次性最多拉取多少条消息
                        .executor(executor)// 执行消息轮询的执行器
                        .pollTimeout(Duration.ZERO)// 超时时间，设置为0，表示不超时（超时后会抛出异常）
                        .build();

        StreamMessageListenerContainer<String, MapRecord<String, String, String>> container =
                StreamMessageListenerContainer.create(redisConnectionFactory, options);

        initStreamAndGroup(stringRedisTemplate.opsForStream(), STREAM_KEY, STREAM_GROUP);
        // receive 方法内部 autoAcknowledge 为 false，需要手动 ack 的
        container.receive(Consumer.from(STREAM_GROUP, STREAM_CONSUMER), //消费组和消费者，这里只演示一个消费者
                StreamOffset.create(STREAM_KEY, ReadOffset.lastConsumed()),//读取 id 大于消费者组最后消费的所有新到达元素
                new TestStreamListener(stringRedisTemplate));//消费消息，业务处理

        this.container = container;
        this.container.start();
    }

    /**
     * 消费组，不存在则创建
     */
    private void initStreamAndGroup(StreamOperations<String, ?, ?> ops, String streamKey, String group) {
        String status = "OK";
        try {
            StreamInfo.XInfoGroups groups = ops.groups(streamKey);
            if (groups.stream().noneMatch(xInfoGroup -> group.equals(xInfoGroup.groupName()))) {
                status = ops.createGroup(streamKey, group);
            }
        } catch (Exception exception) {
            RecordId initialRecord = ops.add(ObjectRecord.create(streamKey, "Initial Record"));
            Assert.notNull(initialRecord, "Cannot initialize stream with key '" + streamKey + "'");
            status = ops.createGroup(streamKey, ReadOffset.from(initialRecord), group);
        } finally {
            Assert.isTrue("OK".equals(status), "Cannot create group with name '" + group + "'");
        }
    }

    @Override
    public void destroy() {
        this.container.stop();
    }

}
```

TestStreamListener 处理消息：

```java
@Slf4j
public class TestStreamListener implements StreamListener<String, MapRecord<String, String, String>> {

    StringRedisTemplate redisTemplate;

    public TestStreamListener(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    @Override
    public void onMessage(MapRecord<String, String, String> message) {

        log.info("MessageId: " + message.getId());
        log.info("Stream: " + message.getStream());
        log.info("Body: " + message.getValue());
        //记得手动确认
        redisTemplate.opsForStream().acknowledge(STREAM_GROUP, message);
    }
}
```

生产者：
```java
@Service
public class TestStreamProducer {

    @Autowired
    StringRedisTemplate redisTemplate;

    //发送流信息
    public void add(String streamKey, String msg) {
        redisTemplate.opsForStream().add(Record.of(msg).withStreamKey(streamKey));
    }

}
```

### 参考

- [1][Claude AI](https://claude.ai/)
- [2][Redis 消息队列的三种方案（List、Streams、Pub/Sub）](https://juejin.cn/post/6917511713315586061)
- [3][Redis Stream | 菜鸟教程](https://www.runoob.com/redis/redis-stream.html)
- [4][Spring boot使用redis-stream实现监听者](https://zwy.xn--fiqs8s/archives/springboot-shi-yong-redis-stream-shi-xian-jian-ting-zhe)


