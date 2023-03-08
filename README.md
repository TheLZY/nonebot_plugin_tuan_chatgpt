<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-tuan-chatgpt

_✨ 来和团子一起聊天吧~ ✨_


<a href="https://cdn.jsdelivr.net/gh/TheLZY/nonebot_plugin_tuan_chatgpt@master/LICENSE.md">
    <img src="https://img.shields.io/github/license/TheLZY/nonebot_plugin_tuan_chatgpt.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_tuan_chatgpt">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_tuan_chatgpt.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>



## 📖 介绍

来与团子聊天吧！

基于 openai 于3月1日放开的最新模型 gpt-3.5-turbo-0301 开发，能够实现近乎于网页端的体验。

基于Nonebot 2.0, onebot v11开发，已作为插件在Paimon bot测试。

功能：

- 角色扮演聊天 Powered by Chatgpt（可 ~~调教~~ 修改成其他人设）
- 发言频率限制 （可修改）
- 群友发言长度限制 （可修改 不仅避免腾讯检测 还能省 token）
- 记忆限制（可修改 默认记忆14条对话 ~~反正群友也是金鱼 还能防止被群友调教成猫娘~~）
- 查看历史问题（~~看看群友都发了什么怪东西~~）

由于本人能力精力有限，对于潜在的问题 & 能提升的地方，欢迎来提 issue & pull request。

效果：

![聊天效果](example2.png)



## 💿 安装

<details>
<summary>使用git安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 使用 git 安装

```
git clone https://github.com/TheLZY/nonebot_plugin_tuan_chatgpt.git
```

</details>

<details>
<summary>使用pip安装</summary>

```
pip install nonebot-plugin-tuan-chatgpt
```

</details>


环境配置：

打开nonebot的`.env` 文件，写入你的chatgpt_api

```
chatgpt_api=""
```

如果没有自动导入插件的功能，需要打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_tuan_chatgpt"]




## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| chatgpt_api | 是 | 无 | str格式 |
| conversation_max_size | 否 | 50 | 最大发送问题字数 |
| answer_max_size | 否 | 30 | 最大记录回答字数 |
| answer_split_size | 否 | 177 | 分隔回答长度 |
| user_freq_lim | 否 | 4 | 限制群友发言速度（秒） |
| group_freq_lim | 否 | 6 | 限制群内发言速度（秒）|
| conversation_remember_num | 否 | 14 | 能记住的对话数目 |



## 🎉 使用

### 指令表

| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 团子[聊天内容] | 群员 | 否 | 群聊 | 来和团子聊天吧！ |
| 历史记录 | 主人 | 否 | 群聊 / 私聊 | 查看3条最近问题 |

<!--### 效果图 -->



## 💡 TODO

- [√] 回答分隔 （通过分段实现。可能会考虑换成图片发送）
- [ ] 未对私聊做发言频率限制。可能以后会添加？
- [ ] 支持使用梯子？
- [ ] 错误处理？
- [ ] api 异步调用优化 （ 自动重试 / 报错）
- [ ] 人格转换功能？
- [ ] 通过@触发 ？ 



**角色~~调教~~定制：**

pip下载时可用

如果希望更改触发语，可以修改 `service = on_startswith('团子', priority = 8, block=True)`

如果希望更改人设，可以修改 `message_init()`

### 一些碎碎念

其实也可以是收到 @ ，然后没有别的程序被触发的时候就回复。因为paimon bot似乎会自动将nickname转义为 @ ？

<!-- 虽然这样对于一些有转移功能的bot来说比较方便，两种触发方式都能回答
但是有一个问题 别人叫你团子爹怎么怎么的时候，她收到的可能就是爹怎么怎么。。。 -->

但是并不是所有的都会。
要适配所有bot的话可能写两遍是最合理的。。。

而且有可能会在写错命令的时候误运行


不过按理来说也不是不行，只需要把priority调低就行



## ⭐ Special thanks to

本项目在开发过程中，参考了不少以下项目，对各位表示由衷的感谢

openai

[NoneBot](https://github.com/nonebot)

[小派蒙|LittlePaimon](https://github.com/CMHopeSunshine/LittlePaimon) by @[CMHopeSunshine](https://github.com/CMHopeSunshine/CMHopeSunshine)

[nonebot-plugin-chatgpt](https://github.com/A-kirami/nonebot-plugin-chatgpt) by @[A-kirami](https://github.com/A-kirami/A-kirami)

[nonebot-plugin-oachat](https://github.com/Gin2O/nonebot_plugin_oachat) by @[Gin2O](https://github.com/Gin2O)

[ChatGPT 中文调教指南]( https://github.com/PlexPt/awesome-chatgpt-prompts-zh) by @[PlexPt](https://github.com/PlexPt/PlexPt)

[Little Paimon with chatgpt](https://github.com/meatjam/LittlePaimon) by @[meatjam](https://github.com/meatjam)

[nonebot_plugin_biliav](https://github.com/knva/nonebot_plugin_biliav) by @[knva](https://github.com/knva/knva)