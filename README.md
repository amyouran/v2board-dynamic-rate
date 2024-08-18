## v2board 动态倍率脚本

**使用 v2board 后端提供的 Api 配合 Linux Crontab 定时任务实现动态调整节点倍率功能。**

<p>
  <a href="https://www.python.org/downloads/release/python-3120/"><img src="https://img.shields.io/badge/python-3.12.0-blue.svg"></a>
  <a href="https://github.com/v2board/v2board/tree/1.7.4"><img alt="Custom Badge" src="https://img.shields.io/badge/v2board-1.7.4-purple?style=flat-square""></a>
  <a href="https://t.me/zeroThemeGroup"><img alt="Telegram" src="https://img.shields.io/badge/交流群组-Telegram-blue?style=flat-square"></a>
</p>

## 介绍
不用修改任何v2board后端代码、不侵入v2board数据库、安全无风险的实现动态倍率调节。
脚本每次运行会根据配置文件筛选出符合当前时间，需要修改倍率的节点。以此构造http请求，通过v2board后端提供的api修改节点数据。配合定时任务即可实现全自动动态节点倍率。

## 配置 Config.yaml 
| Field                 | Desc                                                       | 
| --------------------- | ------------------------------------------------------------ | 
| host          | 后台域名                   |    
| admin_path                | 后台路径                               |      
| admin_account             | 管理员账号                         |  
| admin_password          | 管理员密码                   |
| nodes          | 节点列表                   |
| id | 节点id | 
| type | 节点类型(shadowsocks/vmess/trojan/hysteria/vless(reality) ) | 
| rate_config              | 该节点倍率配置列表                           | 
| rate        | 倍率               | 
| start_time        | 开始时间(24h)               | 
| end_time        | 结束时间(24h)               | 

## 使用方法

1. 上传脚本到服务器 or 服务器直接 `git clone` 本项目

2. 安装Python依赖 `pip install -r requirements.txt`

3. 根据需求修改`config.yaml`

4. 配置并启动 `Linux crontab` 定时任务


## 推荐

- [简约、优雅的v2board主题](https://github.com/amyouran/V2b-Zero-Theme)
- [高性能、高负载、部署简单的 v2board telegram 机器人](https://github.com/amyouran/v2board-telegram-bot)
- [龙腾云](https://lty.lol)

## License

[MIT](https://opensource.org/licenses/MIT)

Copyright (c) 2014-present, [Linki](https://t.me/is_linki)
