# setu-bot
build instructions for a coolq setu-bot. <br>
兴趣使然的色图机器人安装指南

## 使用方法
下载->切换目录->执行
```
git clone https://github.com/GoodManWEN/setu-bot.git
cd setu-bot
bash coolq.bot.install
```
↑以上服务器设置完成 <br>
接下来打开coolq图形界面登录 <br>
访问网址 你的服务器IP:8080 按照提示操作 <br>
\# <br>
登录过后，右键点击图标 -> 应用 -> 应用管理 -> 重载应用 -> HTTP API -> 开启 <br>
<br>
编写环境 ： ubuntu 16.04 LTS

## 组件逻辑
```
+--------------+    ws   +------------+   ws  +-----------+
| Python Logic | <====== | coolq-http | <==== | picfinder | 
+--------------+         +------------+       +-----------+
                            api || event
                                ||
                         +------------+ 
                         | coolq-wine | 
                         +------------+
                                || 
                                ||
                         +--------------+
                         | coolq-server |
                         +--------------+    
                                ||  request
                                ||
+--------------+         +--------------+
| QQ user pc / | message |   server of  |
| phone client | <======>|   Tencent    |
+--------------+         +--------------+
```

## 使用项目
- [docker-wine-coolq](https://github.com/CoolQ/docker-wine-coolq)
- [coolq-http-api](https://github.com/richardchien/coolq-http-api)
- [python-aiocqhttp](https://github.com/richardchien/python-aiocqhttp)
- [CQ-picfinder-robot](https://github.com/Tsuk1ko/CQ-picfinder-robot)
