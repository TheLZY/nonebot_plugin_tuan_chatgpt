<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-tuan-chatgpt

_✨ 来和团子一起聊天吧~ ✨_ 

CN | [EN](https://github.com/TheLZY/nonebot_plugin_tuan_chatgpt/blob/master/README_EN.md)


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

- **和团子聊天！ Powered by Chatgpt** （可 ~~调教~~ 修改成其他人设）
- **随机人设**   （ 聊天5次后自动换 每次都有新感受 —— 团子（ 猫娘 / 克苏鲁 / 派蒙 ver.））
- **查看赛博地址**  （看看代理能用不 ~~毕竟openai时不时就抽风一下~~）
- 长回答渲染图片
- 查看历史问题  （~~看看群友都发了什么怪东西~~）
- 发言频率限制  （可修改）
- 长回答自动分割 （可修改）
- 群友发言长度限制  （可修改 不仅避免腾讯检测 还能省 token）
- 记忆限制  （可修改 默认记忆7条对话 ~~反正群友也是金鱼 还能防止被群友调教成猫娘~~）
- 自动重试 错误处理  （毕竟有的梯子不稳定）
- 支持代理及 api 转发

由于本人能力精力有限，对于潜在的问题 & 能提升的地方，欢迎来提 issue & pull request。

举个栗子 🌰：

<!--  ![聊天效果](example2.png)  -->
![聊天效果](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/examples/example2.png)


## 🎉 使用

### 指令表

| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 团子[聊天内容] | 群员 | 否 | 群聊 / 私聊 | 来和团子聊天吧！ |
| @团子[聊天内容] | 同上 |  是 | 同上 | 同上 |
| 团子看看位置 | 群员 | 否 | 群聊 / 私聊 | 查看团子赛博地址 |
| 历史记录 | 主人 | 否 | 群聊 / 私聊 | 查看历史提问（不包括回答） |



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

如果希望启用代理，则需要在`.env` 文件中，写入 `chat_use_proxy = True` 以及 `chat_proxy_address_https = "代理地址"` 或 `chat_proxy_address_http = "代理地址"`  (处理逻辑类似openai，优先使用https。但是https经常会报错（aiohttp和urllib3都可能会造成问题），推荐只使用http)

如果希望启用api转发 (类似 [腾讯云函数搭建 OpenAI 国内代理](https://github.com/Ice-Hazymoon/openai-scf-proxy) 通过云函数等方式实现反代 )，则需要写入写入 `chat_use_api_forward = True` 以及 `chat_api_address = "代理地址"` 

但是不推荐两者同时启用

如果希望启用图片渲染，则需要写入 `chat_use_img2text=True`, 以及在工程目录的 `/data/tuan_chatgpt` 文件夹（`/data` 文件夹与 `bot.py` / `env` / 运行`nb run` 的地方同级 ）中分别添加字体文件和背景文件到 `/font` 以及 `/bachground` 文件夹中。
默认的字体文件可参考本仓库，背景文件则会从中随机抽取。文件夹不存在时会自动创建，也可自行设定文件夹路径。
也可以直接下载 Release 的 [tuan_chatgpt.zip](https://github.com/TheLZY/nonebot_plugin_tuan_chatgpt/files/11163988/tuan_chatgpt.zip) 扔到 `/data` 里去

图片渲染功能启用后，会自动启用二维码添加以及背景图片添加。可以选择关闭。

具体配置方式参考 **⚙️ 配置** 以及 [配置 | Nonebot](https://v2.nonebot.dev/docs/tutorial/configuration#%E9%85%8D%E7%BD%AE%E6%96%B9%E5%BC%8F)

eg： 

    chatgpt_api = "sk-1145141919"
    # 启用代理
    chat_use_proxy=True
    chat_proxy_address_http='http://127.0.0.1:10809'
    chat_proxy_address_https='http://127.0.0.1:10809'
    # 启用api转发
    chat_use_api_forward=True
    chat_api_address="https://api.openai.com/v1" （这个是官方接口 照着写没问题，大概？ 还是得看具体的转发方式）
    # 启用图片渲染
    chat_use_img2text=True




如果没有自动导入插件的功能，需要打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_tuan_chatgpt"]




## ⚙️ 配置

在 nonebot2 项目的`.env`文件中支持添加以下配置

必填项：
| 配置项               | 默认值 | 说明           |
| :-----------------: | :----: | :------------: |
| chatgpt_api         |   无   | str格式         |

代理相关（可选）：
| 配置项                   | 默认值 | 说明                 |
| :---------------------: | :----: | :------------------: |
| chat_use_proxy           | False | 是否启用代理         |
| chat_proxy_address       | None  | 代理地址             |
| chat_use_api_forward     | False | 是否启用api转发       |
| chat_api_address         | None  | api转发地址          |

渲染图片相关（可选）：
| 配置项                | 默认值                          | 说明                           |
| :------------------: | :-----------------------------: | :----------------------------: |
| chat_use_img2text    | False                          | 是否渲染文本并发送图片          |
| chat_use_qr          | True                           | 是否渲染文本并发送图片          |
| chat_use_background  | True                           | 是否渲染文本并发送图片          |
| chat_data_path       | 'data/tuan_chatgpt'               | 数据路径。修改用绝对路径                        |
| chat_font_path       | 'font'                         | 字体路径（默认为data/tuan_chat/font     |
| chat_background_path | "background"                   | 背景路径（默认为data/tuan_chat/background）|
| chat_font_name       | 'sarasa-mono-sc-regular.ttf'   | 使用的字体                      |
| chat_canvas_width    | 1000                           | 发送图片的宽度                   |
| chat_font_size       | 30                             | 字号                            |
| chat_offset_x        | 50                             | 起始绘制点的横坐标                |
| chat_offset_y        | 50                             | 起始绘制点的纵坐标                |


其他配置（可选）：
| 配置项                   | 默认值 | 说明                 |
| :---------------------: | :----: | :------------------: |
| conversation_max_size  |  300  | 最大发送问题字数 |
| answer_max_size         |   50  | 最大记录回答字数 |
| answer_split_size       |  177  | 分隔回答长度   |
| user_freq_lim           |   4   | 限制群友发言速度（秒） |
| group_freq_lim          |   6   | 限制群内发言速度（秒） |
| conversation_remember_num |   7   | 能记住的对话数目      |



## 🍉 效果图

图片渲染

 ![图片渲染效果](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/examples/example_img2text.PNG)

历史记录

 ![历史记录效果](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/examples/example_history.png) 



## 💡 TODO

- [x] 回答分隔 （通过分段实现。可能会考虑换成图片发送）
- [x] 支持使用代理
- [x] 增加代理测试 通过返回的ip地址判断代理是否有效 绝赞赛博旅行中！  <!--  http://icanhazip.com/ --> 
- [x] 私聊做发言频率限制。
- [x] 错误处理 <!--（比如代理的检测之类的 以及报错方式 团子被玩坏了！这一定不是团子的错！（繁体） 可以写个函数error message    - 倒是可以照着官方的写 不过还是得先在telegrambot上测试一下 ）-->
- [x] 异步调用优化  （自动重试 / 返回报错  <!-- - 但是估计得自己造轮子...不知道官方有没有提供 --> ）
- [x] 随机人设 感觉会很有意思（
- [x] 通过@触发 
- [ ] 修改人设 ？ 
- [ ] markdown 渲染 ？ 
- [ ] ~~自定义触发方式？ 这个倒是可以和修改触发人设一起联动...不过感觉动态修改有点麻烦。~~ 在nickname里面加吧，也挺好
- [ ] ~~Openai 抽风处理（暂时只输出 3*177 个长度的回答 可以根据相同字数出现次数来 同一个字连续出现6次判定为抽风？）~~ 最近没遇到 鉴定为不瞎改就不会有问题
- [ ] ~~长回答合并转发~~ 似乎更容易被风控 算了。 [参考](https://github.com/Ailitonia/omega-miya/issues/16#issuecomment-827432967)

<!-- - [ ] 全局变量似乎有数据不一致的问题 是否需要加锁？ 毕竟只是一个小小的列表 就算出现一点顺序错误也无伤大雅 --> 

**角色 ~~调教~~ 定制：**

如果希望更改触发语，可以找到源码安装位置里的 `__init__.py` 文件，修改 `chat_checker`

也可以进入 nonebot 的`.env` 文件，在 `nickname` 里添加触发语

如果希望更改人设，可以修改 `utils.py` 文件中的 `MessageBox`

（正在思考怎么用聊天来添加人设 不过感觉要涉及的东西比较多

### 一些碎碎念

<!-- 
代码重构，符合OOC ？ 但是感觉复杂度并不高，可以，但没必要 -->

<!-- 
其实也可以是收到 @ ，然后没有别的程序被触发的时候就回复。因为paimon bot似乎会自动将nickname转义为 @ ？ -->

<!-- 虽然这样对于一些有转移功能的bot来说比较方便，两种触发方式都能回答
但是有一个问题 别人叫你团子爹怎么怎么的时候，她收到的可能就是爹怎么怎么。。。

但是并不是所有的都会。
要适配所有bot的话可能写两遍是最合理的。。。

而且有可能会在写错命令的时候误运行

不过按理来说也不是不行，只需要把priority调低就行 -->


conversation_remember_num 最好不要调得太高，记住太多话了就会变成性冷淡机器人 😥

出现了 wake up 词也会变回去，不过现在应该多说两句话就好了

长回答处理？ 转发的方式似乎容易被风控。发太多了也容易被风控。
渲染图片的话，本来是有造轮子的，但是我试了好久跑不起来（悲 😥 这下不得不自己造了 （万恶的 windows 啊）
markdown 渲染好像有点复杂，还得再研究研究


<details>

<summary>一个性冷淡 bot 的例子</summary>


conversation_remember_num = 14

![聊天效果](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/examples/example3.png)

变成性冷淡机器人惹（悲）

conversation_remember_num = 7

![聊天效果](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/examples/example4.png)

</details>


<details>

<summary>Openai 抽风的例子</summary>

![抽风效果](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/examples/example_chou.png)

其中一个测试用例，大概三次里会抽一次, 有兴趣可以研究一下为什么抽风了（

大概猜测是frequency_penalty为负会奖励出现相同的token。那还是不要用frequency_penalty比较好。

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


**2023.4.4**

- 增加图片渲染功能


**2023.3.23**

- 增加 api 转发支持

**2023.3.15**

- 添加随机人设。预留了修改人设的接口 有空再填坑
- 支持通过@触发


**2023.3.14**

- 增加错误重试 （如果失败 自动重试最多三次 对于梯子不稳定的时候帮助很大）
- 增加报错输出 （3次都失败的话 生成 ~~有趣的~~ 报错信息 以第三次失败返回的 error 为准）
- 修改消息触发器 ~~试图通过@聊天 大失败~~
- 增加私聊频率限制 默认为4秒一次

**2023.3.12**

- 增加赛博地址检测功能
- 增加选择性记录功能 （去掉会让她想起来自己是ai的回答 避免一直说自己是ai）

**2023.3.10**

- 增加代理支持

**2023.3.9**

- 切换成官方异步调用接口


## ⭐ Special thanks to

本项目在开发过程中，参考了不少以下项目，对各位表示由衷的感谢

openai

[NoneBot](https://github.com/nonebot)

[小派蒙|LittlePaimon](https://github.com/CMHopeSunshine/LittlePaimon) by @[CMHopeSunshine](https://github.com/CMHopeSunshine)

[nonebot-plugin-chatgpt](https://github.com/A-kirami/nonebot-plugin-chatgpt) by @[A-kirami](https://github.com/A-kirami)

[chatgpt-mirai-qq-bot](https://github.com/lss233/chatgpt-mirai-qq-bot) by @[lss233](https://github.com/lss233/lss233)

[nonebot_plugin_naturel_gpt](https://github.com/KroMiose/nonebot_plugin_naturel_gpt) by @[KroMiose](https://github.com/KroMiose/KroMiose)

[nonebot-plugin-setu-now](https://github.com/kexue-z/nonebot-plugin-setu-now) by [kexue-z](https://github.com/kexue-z/kexue-z)

[nonebot-plugin-oachat](https://github.com/Gin2O/nonebot_plugin_oachat) by @[Gin2O](https://github.com/Gin2O)

[ChatGPT 中文调教指南]( https://github.com/PlexPt/awesome-chatgpt-prompts-zh) by @[PlexPt](https://github.com/PlexPt)

[Little Paimon with chatgpt](https://github.com/meatjam/LittlePaimon) by @[meatjam](https://github.com/meatjam)

[nonebot_plugin_biliav](https://github.com/knva/nonebot_plugin_biliav) by @[knva](https://github.com/knva)