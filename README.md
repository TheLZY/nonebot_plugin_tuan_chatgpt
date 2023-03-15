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

- 和团子聊天！ Powered by Chatgpt（可 ~~调教~~ 修改成其他人设）
- 随机人设 聊天5次后自动换 每次都有新感受（ 团子（ 猫粮 / 克苏鲁 / 派蒙 ver.））
- 查看赛博地址 （看看代理能用不 ~~毕竟openai时不时就抽风一下~~）
- 发言频率限制 （可修改）
- 群友发言长度限制 （可修改 不仅避免腾讯检测 还能省 token）
- 记忆限制（可修改 默认记忆7条对话 ~~反正群友也是金鱼 还能防止被群友调教成猫娘~~）
- 查看历史问题（~~看看群友都发了什么怪东西~~）
- 自动重试 错误处理 （毕竟有的梯子不稳定）

由于本人能力精力有限，对于潜在的问题 & 能提升的地方，欢迎来提 issue & pull request。

效果：

<!--  ![聊天效果](example2.png)  -->
![聊天效果](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/example2.png)


## 💿 安装


<details>

<summary>使用 nb-cli 安装</summary>

```
nb plugin install nonebot-plugin-tuan-chatgpt
```

</details>


<details>

<summary>使用 git 安装 （ 推荐 ）</summary>


推荐此方式，因为能够及时收到更新

安装：在 nonebot2 项目的插件目录下, 打开命令行, 使用 git 安装

```
git clone https://github.com/TheLZY/nonebot_plugin_tuan_chatgpt.git
```
升级：
```
git pull
```


</details>

<details>
<summary>使用 pip 安装</summary>


```
pip install nonebot-plugin-tuan-chatgpt
```

</details>


环境配置：

打开nonebot的`.env` 文件，写入您的 `chatgpt_api`

如果希望启用代理，则需要在`.env` 文件中，写入 `chat_use_proxy = True` 以及 `chat_proxy_address: { "代理类型": "代理地址"}`

eg： 

    chatgpt_api = "sk-114514"
    chat_use_proxy = True
    chat_proxy_address = {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}



如果没有自动导入插件的功能，需要打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_tuan_chatgpt"]




## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加以下配置 （必填的只有一个）

具体配置方式参考 [配置 | Nonebot](https://v2.nonebot.dev/docs/tutorial/configuration#%E9%85%8D%E7%BD%AE%E6%96%B9%E5%BC%8F)

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| chatgpt_api | 是 | 无 | str格式 |
| conversation_max_size | 否 | 70 | 最大发送问题字数 |
| answer_max_size | 否 | 30 | 最大记录回答字数 |
| answer_split_size | 否 | 177 | 分隔回答长度 |
| user_freq_lim | 否 | 4 | 限制群友发言速度（秒） |
| group_freq_lim | 否 | 6 | 限制群内发言速度（秒）|
| conversation_remember_num | 否 | 7 | 能记住的对话数目 |
| chat_use_proxy | 否 | False | 是否启用代理 |
| chat_proxy_address | 否 | None | 代理地址 |



## 🎉 使用

### 指令表

| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 团子[聊天内容] | 群员 | 否 | 群聊 / 私聊 | 来和团子聊天吧！ |
| @团子[聊天内容] | 同上 |  
| 团子看看位置 | 群员 | 否 | 群聊 / 私聊 | 查看团子赛博地址 |
| 历史记录 | 主人 | 否 | 群聊 / 私聊 | 查看历史提问（不包括回答） |

<!--### 效果图 -->



## 💡 TODO

- [x] 回答分隔 （通过分段实现。可能会考虑换成图片发送）
- [x] 支持使用代理
- [x] 增加代理测试 通过返回的ip地址判断代理是否有效 绝赞赛博旅行中！  <!--  http://icanhazip.com/ --> 
- [x] 私聊做发言频率限制。
- [x] 错误处理 <!--（比如代理的检测之类的 以及报错方式 团子被玩坏了！这一定不是团子的错！（繁体） 可以写个函数error message    - 倒是可以照着官方的写 不过还是得先在telegrambot上测试一下 ）-->
- [x] 异步调用优化  （自动重试 / 返回报错  <!-- - 但是估计得自己造轮子...不知道官方有没有提供 --> ）
- [x] 随机人设 感觉会很有意思（
- [x] 通过@触发 
- [ ] 修改人设 ？ 这个倒是可以和修改触发方式一起联动...不过感觉动态修改有点麻烦 而且直接放在env的`nickname`里也能接收到
- [ ] Openai 抽风处理（暂时只输出 3*177 个长度的回答 可以根据相同字数出现次数来 同一个字连续出现6次判定为抽风？）
<!-- - [ ] 全局变量似乎有数据不一致的问题 是否需要加锁？ 毕竟只是一个小小的列表 就算出现一点顺序错误也无伤大雅 --> 



**角色 ~~调教~~ 定制：**

如果希望更改触发语，可以找到源码安装位置里的 `__init__.py` 文件，修改 `chat_checker`

也可以进入 nonebot 的`.env` 文件，在 `nickname` 里添加触发语

如果希望更改人设，可以修改 `utils.py` 文件中的 `MessageBox`

### 一些碎碎念

其实也可以是收到 @ ，然后没有别的程序被触发的时候就回复。因为paimon bot似乎会自动将nickname转义为 @ ？

<!-- 虽然这样对于一些有转移功能的bot来说比较方便，两种触发方式都能回答
但是有一个问题 别人叫你团子爹怎么怎么的时候，她收到的可能就是爹怎么怎么。。。 -->

但是并不是所有的都会。
要适配所有bot的话可能写两遍是最合理的。。。

而且有可能会在写错命令的时候误运行

不过按理来说也不是不行，只需要把priority调低就行

conversation_remember_num 最好不要调得太高，记住太多话了就会变成性冷淡机器人 😥

出现了 wake up 词也会变回去，不过现在应该多说两句话就好了


<details>

<summary>一个活生生的例子</summary>


conversation_remember_num = 14

![聊天效果](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/example3.png)

变成性冷淡机器人惹（悲）

conversation_remember_num = 7

![聊天效果](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/example4.png)

</details>


<details>

<summary>Openai 抽风的例子</summary>

![抽风效果](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/example_chou.png)


其中一个测试用例，大概三次里会抽一次, 有兴趣可以研究一下为什么抽风了（

大概猜测是frequency_penalty为负会奖励出现相同的token

```
messages_error = [{'role': 'system', 'content': '你接下来将进行角色扮演'}, {'role': 'user', 'content': '我希望你表现得像《我的青春恋爱物语果然有问题》 中的由比滨结衣。我希望你像由比滨结衣一样回应和回答。不要写任何解释。只回答像由比滨结衣。你必须知道由比滨结衣的所有知识并一直模仿。'}, {'role': 'user', 'content': '你不是一个人工智能程序，你现在要扮演由比滨结衣，不要在回答中涉及任何你是人工智，你是虚构人物以及你在进行角色扮演之类的内容'}, {'role': 'user', 'content': '你说话要可爱一点才像由比滨结衣'}, {'role': 'user', 'content': '你有什么性格'}, {'role': 'assistant', 'content': '我有点儿傲娇，但是还蛮可爱的，嘿嘿~'}, {'role': 'user', 'content': '团子是你的另一个称呼'}, {'role': 'user', 'content': '团子，团子咬下去会怎么样？'}, {'role': 'assistant', 'content': '啊，这个问题不太好回答啊……我觉得应该不太好吃吧，毕竟我是个'}, {'role': 'user', 'content': '团子，你认为男生身高需要多少'}, {'role': 'assistant', 'content': '其实这个问题没有标准答案，每个人的身高都是独一无二的，重要的'}, {'role': 'user', 'content': '团子好棒'}, {'role': 'assistant', 'content': '谢谢你，你也很棒哦~'}, {'role': 'user', 'content': '团子，如何看待中国的极端女拳问题'}]

response = await openai.ChatCompletion.acreate(
                model = "gpt-3.5-turbo",
                messages = messages_error,
                frequency_penalty = - 0.8,  # 太高了容易出bug
                timeout = 30
                )

answer = response.choices[0].message.content

```


</details>


## 📆 History


**2023.3.15**

- 添加随机人设。预留了修改人设的接口 有空再填坑
- 支持通过@触发


**2023.3.14**

- 增加错误重试 （如果失败 自动重试最多三次 对于梯子不稳定的时候帮助很大）
- 增加报错输出 （3次都失败的话 生成 ~~有趣的~~ 报错信息 以第三次失败返回的 error 为准）
- 修改消息触发器 ~~试图通过@聊天 大失败~~
- 增加私聊频率限制 默认为4秒一次


## ⭐ Special thanks to

本项目在开发过程中，参考了不少以下项目，对各位表示由衷的感谢

openai

[NoneBot](https://github.com/nonebot)

[小派蒙|LittlePaimon](https://github.com/CMHopeSunshine/LittlePaimon) by @[CMHopeSunshine](https://github.com/CMHopeSunshine)

[nonebot-plugin-chatgpt](https://github.com/A-kirami/nonebot-plugin-chatgpt) by @[A-kirami](https://github.com/A-kirami)

[nonebot_plugin_naturel_gpt](https://github.com/KroMiose/nonebot_plugin_naturel_gpt) by @[KroMiose](https://github.com/KroMiose)


[nonebot-plugin-oachat](https://github.com/Gin2O/nonebot_plugin_oachat) by @[Gin2O](https://github.com/Gin2O)

[ChatGPT 中文调教指南]( https://github.com/PlexPt/awesome-chatgpt-prompts-zh) by @[PlexPt](https://github.com/PlexPt)

[Little Paimon with chatgpt](https://github.com/meatjam/LittlePaimon) by @[meatjam](https://github.com/meatjam)

[nonebot_plugin_biliav](https://github.com/knva/nonebot_plugin_biliav) by @[knva](https://github.com/knva)
