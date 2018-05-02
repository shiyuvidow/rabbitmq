# RABBITMQ

Version: 2.7

基于RabbitMQ rpc实现的主机管理：

可以对指定的多个机器异步执行命令，每台机器执行一个命令生成一个任务IP，通过check_task task_id获得任务结果
例子：

run "df -h" --hosts 192.168.3.55 
Please check_task d83d1245-12bd-4ead-8413-d9d9ec8957d6
check_task d83d1245-12bd-4ead-8413-d9d9ec8957d6 

配置说明：

rabbitmq_client:

```
conf/settings.py
# RABBITMQ信息, 配置连接rabbitmq的主机、用户名、密码
RABBITMQ_INFO = {
    'host': 'xx.xx.xx.xx',
    'user': 'admin',
    'passwd': '123456'
}
```

rabbitmq:

```
conf/settings.py
# RABBITMQ信息, 配置连接rabbitmq的主机、用户名、密码
RABBITMQ_INFO = {
    'host': 'xx.xx.xx.xx',
    'user': 'admin',
    'passwd': '123456'
}
# 网卡
IFNAME = "eth0"
```

使用说明：

```进到PARSSH的bin目录
# 先在需要执行命令的机器上(多台)启动rabbitmq端，监听消息
# 进到RABBITMQ的bin目录下
python rpc.py
# 然后启动rabbitmq_client端
# python rpc_client.py
>>:run free -k --hosts xx.xx.xx.xx xx.xx.xx.xx
 [x] Requesting hosts:xx.xx.xx.xx, cmd:free -k
 [.] Please check_task d83d1245-12bd-4ead-8413-d9d9ec8957d6
 [x] Requesting hosts:xx.xx.xx.xx, cmd:free -k
 [.] Please check_task f91ed94d-2f3c-45df-8816-cca66ccb77cc
>>:check_task d83d1245-12bd-4ead-8413-d9d9ec8957d6
...
>>:check_task f91ed94d-2f3c-45df-8816-cca66ccb77cc
...
```