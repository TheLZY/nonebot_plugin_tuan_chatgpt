<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-tuan-chatgpt

_✨ Come chat with Yuigahama Yui~ _🥰_ ✨_ 

[CN](https://github.com/TheLZY/nonebot_plugin_tuan_chatgpt#readme) | EN


<a href="https://cdn.jsdelivr.net/gh/TheLZY/nonebot_plugin_tuan_chatgpt@master/LICENSE.md">
    <img src="https://img.shields.io/github/license/TheLZY/nonebot_plugin_tuan_chatgpt.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_tuan_chatgpt">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_tuan_chatgpt.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>



## 📖 Introduction

Let's chat with Tuanzi! 🎉

Developed based on the latest model, gpt-3.5-turbo-0301, released by OpenAI on March 1st, which provides an experience close to the web version.

Built on Nonebot 2.0 and OneBot v11, tested as a plugin in Paimon bot.

Features:

- **Chat with Tuanzi! Powered by Chatgpt** (You can ~~train~~ modify the character)
- **Random characters** (After chatting 5 times, the character automatically changes, giving a fresh feeling every time — Tuanzi (Cat Girl / Cthulhu / Paimon ver.))
- **Check cyber address** (See if the proxy is working ~~since OpenAI occasionally has hiccups~~)
- View history of questions (~~See what weird stuff the group members have sent~~)
- Speech frequency limit (modifiable)
- Automatic splitting of long answers (modifiable)
- Group member speech length limit (modifiable, not only avoiding detection by Tencent but also saving tokens)
- Memory limit (modifiable, default memory of 7 conversations ~~after all, group members are goldfish, and it prevents them from training Tuanzi to be a cat girl~~)
- Automatic retry and error handling (since some ladders are unstable)
- Supports proxy and API forwarding

Due to my limited abilities and energy, for potential issues & areas of improvement, feel free to submit issues & pull requests.

Example:

<!--  ![Chat effect](example2.png)  -->
![Chatting result](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/example2.png)

## 🎉 Usage

### Command list

| Command      | Permission | Mention | Scope        | Description                             |
| :----------: | :--------: | :-----: | :----------: | :-------------------------------------: |
| 团子 [chat content] | Group member |  No  | Group chat / Private chat | Let's chat with Tuanzi! |
| @团子 [chat content] | Same as above |  Yes | Same as above | Same as above |
| 团子看看位置 | Group member |  No  | Group chat / Private chat | Check Tuanzi's cyber address |
| 历史记录 | Owner |  No  | Group chat / Private chat | View history of questions (excluding answers) |


## 💿 Installation

<details>

<summary>Install using nb-cli</summary>

```
nb plugin install nonebot-plugin-tuan-chatgpt
```

</details>


<details>

<summary>Install using git (recommended)</summary>

Recommended for timely updates.

Installation: In the Nonebot2 project's plugin directory, open the command line and use git to install.

```
git clone https://github.com/TheLZY/nonebot_plugin_tuan_chatgpt.git
```
Upgrade:
```
git pull
```


</details>

<details>
<summary>Install using pip</summary>


```
pip install nonebot-plugin-tuan-chatgpt
```

</details>


Environment configuration:

Open the Nonebot's `.env` file and enter your `chatgpt_api`.

If you want to enable a proxy, you need to write `chat_use_proxy = True` and `chat_proxy_address_https = "proxy address"` or `chat_proxy_address_http = "proxy address"` in the `.env` file (similar to OpenAI's handling logic, HTTPS is preferred. However, HTTPS often causes errors (both aiohttp and urllib3 may cause problems), so it is recommended to use HTTP only).

If you want to enable API forwarding (similar to [Setting up OpenAI domestic proxy using Tencent Cloud Function](https://github.com/Ice-Hazymoon/openai-scf-proxy) forwarding messages through cloud functions, etc.), you need to write `chat_use_api_forward = True` and `chat_api_address = "proxy address"`.

However, it is not recommended to enable both at the same time.

For specific configuration methods, refer to [Configuration | Nonebot](https://v2.nonebot.dev/docs/tutorial/configuration#%E9%85%8D%E7%BD%AE%E6%96%B9%E5%BC%8F)

eg:

    chatgpt_api = "sk-1145141919"
    # Enable proxy
    chat_use_proxy=True
    chat_proxy_address_http='http://127.0.0.1:10809'
    chat_proxy_address_https='http://127.0.0.1:10809'
    # Enable API forwarding
    chat_use_api_forward=True
    chat_api_address="https://api.openai.com/v1" (This is the official API, just follow this format and you should be fine, probably? It still depends on the specific forwarding method.)

If the plugin is not automatically imported, you need to open the `pyproject.toml` file in the root directory of the Nonebot2 project, and append the following under the `[tool.nonebot]` section:

    plugins = ["nonebot_plugin_tuan_chatgpt"]



## ⚙️ Configuration

The following configurations can be added to the `.env` file in the Nonebot2 project.

Required:
| Configuration Item    | Default Value | Description      |
| :-------------------: | :-----------: | :--------------: |
| chatgpt_api           |      N/A      | str format       |

Proxy-related (optional):
| Configuration Item      | Default Value | Description         |
| :---------------------: | :-----------: | :-----------------: |
| chat_use_proxy          |     False     | Enable proxy        |
| chat_proxy_address      |     None      | Proxy address       |
| chat_use_api_forward    |     False     | Enable API forwarding |
| chat_api_address        |     None      | API forwarding address |

Other configurations (optional):
| Configuration Item       | Default Value | Description                     |
| :---------------------: | :-----------: | :-----------------------------: |
| conversation_max_size    |     300       | Maximum question length sent   |
| answer_max_size          |      50       | Maximum recorded answer length |
| answer_split_size        |     177       | Split answer length            |
| user_freq_lim            |       4       | Limit user speaking speed (seconds) |
| group_freq_lim           |       6       | Limit group speaking speed (seconds) |
| conversation_remember_num |      7       | Number of conversations remembered |



<!--### 效果图 -->



## 💡 TODO

- [x] Answer separation (implemented by splitting. May consider sending as images)
- [x] Proxy support
- [x] Proxy testing: determine proxy validity by returning IP address. Having a great cyber journey! <!-- http://icanhazip.com/ -->
- [x] Private chat frequency limit.
- [x] Error handling <!-- (e.g., proxy detection and error reporting, like "Tuanzi is broken! It's definitely not Tuanzi's fault!" (in traditional Chinese). You can write an error message function. - You can follow the official implementation, but still need to test it on the Telegram bot first.) -->
- [x] Asynchronous call optimization (automatic retry / error return <!-- - But probably need to reinvent the wheel... not sure if the official implementation provides this --> )
- [x] Random character setting - seems interesting!
- [x] Trigger by mentioning
- [ ] Modify character setting?
- [ ] ~~Custom trigger method? This can be linked with modifying the trigger character setting... but dynamic modification seems a bit troublesome.~~ Just add it to the nickname, it's also nice.
- [ ] ~~OpenAI malfunction handling (temporarily only output 3*177 character length answers. Can judge malfunction based on the number of times the same character appears consecutively 6 times?)~~ Haven't encountered this recently, so I assume it's not a problem if you don't modify anything.
- [ ] ~~Long answer merging and forwarding~~ It seems more likely to be controlled by the wind. Never mind. [Reference](https://github.com/Ailitonia/omega-miya/issues/16#issuecomment-827432967)

<!-- - [ ] There seems to be a data inconsistency issue with global variables. Do we need to lock? After all, it's just a tiny list, and a little sequence error won't do any harm. -->

**Character ~~training~~ customization:**

If you want to change the trigger language, you can find the `__init__.py` file in the source code installation location and modify the `chat_checker`.

You can also add trigger language to the `nickname` in Nonebot's `.env` file.

If you want to change the character setting, you can modify the `MessageBox` in the `utils.py` file.

(Thinking about how to add character settings through chatting, but it seems to involve many things)



### Some random thoughts:

It's better not to set the conversation_remember_num too high, or the bot will become an indifferent robot. 😥

When the wake-up word appears, it will also go back to the normal state, but now it should be fine after saying a few more sentences.

How to handle long answers? Forwarding seems to be easily affected by risk control. Sending too many messages is also prone to risk control.
When it comes to rendering images, considering that most long answers are code, sending images might be counterproductive...
Instead, how about providing a QR code? If it's a URL, the configuration is a bit complicated, and if it's Chinese characters, the information density is too low and not enough.

<details>
<summary>An example of an indifferent bot</summary>


conversation_remember_num = 14

![Chatting result](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/example3.png)

An indifferent bot (sad)

conversation_remember_num = 7

![Chatting result](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/example4.png)

</details>


<details>

<summary>Openai glitch example</summary>

![Glitch effect](https://raw.githubusercontent.com/TheLZY/nonebot_plugin_tuan_chatgpt/master/example_chou.png)

This is one of the test cases, with a glitch occurring roughly once every three times. If you're interested, you can investigate why the glitch happens.

It's speculated that a negative frequency_penalty might reward the appearance of the same token. So, it's better not to use frequency_penalty.


```
messages_error = [{'role': 'system', 'content': 'You will role-play next'}, {'role': 'user', 'content': 'I want you to act like Yui Yuigahama from "My Youth Romantic Comedy Is Wrong, As I Expected." I want you to respond and answer like Yui Yuigahama. Do not write any explanations. Only answer as Yui Yuigahama. You must know all about Yui Yuigahama and imitate her continuously.'}, {'role': 'user', 'content': 'You are not an AI program, you are now playing Yui Yuigahama, do not involve any content about you being an AI, you being a fictional character, and you role-playing in your answers'}, {'role': 'user', 'content': 'You need to be more adorable when you speak, like Yui Yuigahama'}, {'role': 'user', 'content': 'What kind of personality do you have?'}, {'role': 'assistant', 'content': 'I am a bit tsundere, but also quite adorable, hehe~'}, {'role': 'user', 'content': 'Tuanzi is another name for you'}, {'role': 'user', 'content': 'Tuanzi, what would happen if I bit into a Tuanzi?'}, {'role': 'assistant', 'content': 'Ah, that's not an easy question to answer... I think it might not taste very good, after all, I am a'}, {'role': 'user', 'content': 'Tuanzi, how tall do you think a boy should be?'}, {'role': 'assistant', 'content': 'Actually, there's no standard answer to this question, as everyone's height is unique, and what's important is'}, {'role': 'user', 'content': 'Tuanzi, you're great'}, {'role': 'assistant', 'content': 'Thank you, you're great too~'}, {'role': 'user', 'content': 'Tuanzi, what's your view on extreme feminism in China?'}]

response = await openai.ChatCompletion.acreate(
model = "gpt-3.5-turbo",
messages = messages_error,
frequency_penalty = - 0.8, # Too high makes it easier to encounter bugs
timeout = 30
)

answer = response.choices[0].message.content

```


</details>


## 📆 History

**2023.3.23**

- Added API forwarding support

**2023.3.15**

- Added random character settings. Reserved interface for modifying character settings, to be filled when available.
- Support activation by @mention

**2023.3.14**

- Added error retry (automatically retries up to three times if failed, helpful for unstable ladder situations)
- Added error output (generates ~~interesting~~ error messages if all three attempts fail, based on the error returned from the third failure)
- Modified message triggers ~~attempted to trigger by @chat, big failure~~
- Added private chat frequency limit, default is once every 4 seconds

**2023.3.12**

- Added cyber address detection feature
- Added selective recording feature (removes responses that remind her she's an AI to avoid constantly saying she's an AI)

**2023.3.10**

- Added proxy support

**2023.3.9**

- Switched to the official asynchronous API

## ⭐ Special thanks to

Translation is helped by chatgpt.

This project referenced several projects during development. We express our heartfelt thanks to everyone involved:

openai

[NoneBot](https://github.com/nonebot)

[Little Paimon](https://github.com/CMHopeSunshine/LittlePaimon) by @[CMHopeSunshine](https://github.com/CMHopeSunshine)

[nonebot-plugin-chatgpt](https://github.com/A-kirami/nonebot-plugin-chatgpt) by @[A-kirami](https://github.com/A-kirami)

[nonebot_plugin_naturel_gpt](https://github.com/KroMiose/nonebot_plugin_naturel_gpt) by @[KroMiose](https://github.com/KroMiose)

[nonebot-plugin-oachat](https://github.com/Gin2O/nonebot_plugin_oachat) by @[Gin2O](https://github.com/Gin2O)

[ChatGPT Chinese Training Guide](https://github.com/PlexPt/awesome-chatgpt-prompts-zh) by @[PlexPt](https://github.com/PlexPt)

[Little Paimon with chatgpt](https://github.com/meatjam/LittlePaimon) by @[meatjam](https://github.com/meatjam)

[nonebot_plugin_biliav](https://github.com/knva/nonebot_plugin_biliav) by @[knva](https://github.com/knva)
