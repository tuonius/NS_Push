### 演示
- TG频道：[https://t.me/nans_wind](https://t.me/nans_wind)
### 简介
- 使用NodeSeek论坛rss接口实现的定时抓取交易贴程序
- 提供青龙面板部署教程，其他环境 举一反三
### 使用教程
1. 在依赖管理里面安装`requests`

2. 青龙面板配置环境变量

   - `tg_user_id`:接收推送消息的用户/群组/频道
   - `tg_bot_token `: TG机器人token
   - `keywords`: 标题关键字列表；示例：`['收','出']`

3. 订阅管理里 填写本仓库地址，定时规则填写`00 01 * * *`
   - 保存后运行一次，然后重新编辑该订阅，关闭 自动添加任务，自动删除任务 这两个功能

4. 定时任务里

   1. 删除push.py这个定时任务
   2. 更改main.py的定时规则为`*/10 * 7-23 * * *`

   - 含义：每10秒拉取一次，0:00-7:00这个时间段不拉取
   > Tips：经观察，深夜鸡几乎不靠谱，正经鸡谁会在大晚上出啊!
   > 拒绝深夜冲动消费 掉入深坑
---

*备注*
- 第一次运行可能会收到多条推送消息，这是因为数据库还没有存储最近发送的交易贴