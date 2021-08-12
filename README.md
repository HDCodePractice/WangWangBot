# WangWangBot
汪汪Bot是一个Telegram Bot，用于帮助你管理一台服务器上的Docker运行的Bot。


### 第一次运行

准备 .env

```
BOT_TOKEN=你的BOT_TOKEN
ADMINS=使用,分隔的管理员ID列表
```

创建并运行容器

```
docker run -d --name=wangwangbot --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v `pwd`:/data hdcola/wangwangbot
```

停止、移除容器

```
docker stop wangwangbot
docker rm wangwangbot
```

更新image

```
docker pull hdcola/wangwangbot
```