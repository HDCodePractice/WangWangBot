# WangWangBot
汪汪Bot是一个Telegram Bot，用于帮助你管理一台服务器上的Docker运行的Bot。这是使用视频：

![bot_use](https://user-images.githubusercontent.com/1254855/129272231-41566908-e808-44bb-bead-d48108d367ab.gif)


## 部署说明

### 安装运行

准备 local.env

```
BOT_TOKEN=你的BOT_TOKEN
ADMINS=使用,分隔的管理员ID列表
```

创建并运行容器

```
docker run -d --name=wangwangbot --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v `pwd`:/data hdcola/wangwangbot
```

### 升级

停止、移除容器

```
docker stop wangwangbot
docker rm wangwangbot
```

更新image

```
docker pull hdcola/wangwangbot
```

之后再运行一遍创建并运行容易即可。


## 开发者调试

运行状态下使用交互模式进入容器

```
docker exec -it wangwangbot bash
```

非运行状态下使用交互模式启动一次性容器

```
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock -v `pwd`:/data hdcola/wangwangbot bash
```
