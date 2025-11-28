# 群老婆插件（wife_plugin）
本插件是基于napcat api开发的抽群老婆娱乐插件，当你在群里发送“抽老婆”时，会随机选择一位群u做你的今日群老婆~

## 插件安装

- clone本仓库到plugins目录下即可
- 首次启动会自动创建config.toml文件，详见下文
- 请确认bot_config.toml文件中的qq_account字段配置正确，否则会影响插件的正常运行
## 安装依赖
- 本插件无需额外安装依赖
## napcat设置
需要在napcat的webui中，选择网络设置，新建HTTP服务器，`port`字段默认为6666（可在配置文件中修改）
`host`字段填`0.0.0.0`，启用CORS和Websocket，名称自定义即可

示例：

<img src="./images/napcat.png" alt="示例" width="338" height="428">

## 配置文件详解
```toml
# wife_plugin - 自动生成的配置文件
# 可以在群聊中选择一位幸运群u做群老婆

[plugin]

# 插件名称
name = "wife_plugin"

# 插件版本
version = "1.0.0"

# 是否启用插件
enabled = true


[napcat]

# napcat端口
port = 6666  #可视情况修改，与napcat端的设置保持一致即可


[other]

# 神秘开关，改成某个qq号可以让此用户始终抽到麦麦
target = 0  #黑幕（bushi）

```
## 使用方法
配置完成后，在群聊中发送“抽老婆”即可触发插件（私聊无效）

## 使用示例
- 抽老婆：

<img src="./images/抽老婆.png" alt="示例" width="305" height="383">

- 今日内已抽过群老婆：

<img src="./images/今日内已抽过群老婆.png" alt="示例" width="305" height="402">

- 抽到了麦麦：

<img src="./images/抽到了麦麦.png" alt="示例" width="305" height="392">

## 黑幕（确信）
将config.toml文件下的target字段修改为某用户的qq号，那这个用户每天抽到的老婆就必定是麦麦~
设置为`0`则此功能不生效
## 鸣谢
其实本插件的灵感来自于群里另一个机器人“花花”，但由于主人不常露面，机器人的具体采用的框架，以及抽老婆功能的具体实现方法均不清楚，
本插件模仿了“花花”的抽老婆功能。

花花：
<img src="./images/鸣谢花花.png" alt="示例" width="305" height="615">
~~给Hug高兴坏了.jpg~~

## 目前可能存在的问题
1. 为了保证每个人每天只能抽一次老婆，抽老婆之后会将群老婆数据保存到`data`目录下，但目前尚未做过期文件清理
2. 没有对请求速率做限制，请使用时避免大范围刷屏

以上问题作者将尽快解决