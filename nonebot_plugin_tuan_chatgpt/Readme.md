TO Do：

- 优化一下get_cyber_pos 函数
- 写一个 path controlloer 的类？ 每次判断一大堆path太傻逼了



# 碎碎念：

碎碎念什么的还是写在这里面吧

代码什么的还是得同步了，要不然容易出bug





init.py:

```python
# 暂时用不到 不过以后就不一定了 可以再看看
# from nonebot.adapters.telegram import Bot
# from nonebot.adapters.telegram.event import MessageEvent


# 测试用的
# print(conversation)
# print(messages)



# 储存answer ？有无必要 ？
# 必须得加answer！ 不然容易串群！！！
# 比如叫他写一首诗，可能会第二次回复还是写一首诗。
# 其实也可以将其写成一个class，每个群单独拥有messages, 类似freq_limiter
# 但是会有点麻烦，因为要维护的东西就多了，然而总共就只有7句话而已。
# 但是总感觉这种实现方法更优雅，而且可以大家分开。但是只有私聊有用
# 可以考虑之后加上。

# 测试用的
# print(len(messages))
# print(answer)
# await bot.send(event, event.get_message())
# await bot.send(event, answer)


# 查看历史功能：
# 有一个问题 这个messages变量再两个函数里面都是共通的吗
# 如果不是的话 那chat的时候直接用finish结束事件 岂不是message就清零了
# 好吧 实践证明并不会清零
```





utils.py:

```python
# 主要的聊天函数
# ？这个函数也需要协程吗 ？ 
# 这个等待的时候，应该也不会阻塞其他bot，毕竟这是main函数内部
# 而 main 函数是有协程的
# 不过反正不会造成性能损耗，问题不大
# 先这样
# 草 我发现了 await只能在async function里面用
# 一切都变得合理了起来


# response 里面的 timeout 问题
response = await openai.ChatCompletion.acreate(
                model = "gpt-3.5-turbo-0301",   # 最新的模型抽风了好几次 怕了怕了
                messages = message_list,
                # temperature = 0.5,
                presence_penalty = - 0.8,
                # frequency_penalty = - 0.5,  # 这个加了容易出bug
                timeout = 20
                # 这个如果报错 TryAgain 会自动重试 但是是api返回的 所以还是自己写 retries 吧
                )


# tuanzi message 问题
# 这个改成不要在回答中说会不会好一点？ 之后如果出现问题可以再看看.
```

openai内关于api_base的定义：
`__init__.py`

```
api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
api_type = os.environ.get("OPENAI_API_TYPE", "open_ai")
```


openai使用异步调用时，会优先启用https的proxy。 根据：

openai 内关于代理的定义：

`api_requestor.py`

```
def _aiohttp_proxies_arg(proxy) -> Optional[str]:
    """Returns a value suitable for the 'proxies' argument to 'aiohttp.ClientSession.request."""
    if proxy is None:
        return None
    elif isinstance(proxy, str):
        return proxy
    elif isinstance(proxy, dict):
        return proxy["https"] if "https" in proxy else proxy["http"]
    else:
        raise ValueError(
            "'openai.proxy' must be specified as either a string URL or a dict with string URL under the https and/or http keys."
        )
```
