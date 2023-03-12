import tiktoken
import openai

import asyncio
import aiohttp
# Freq limiter
from collections import defaultdict
import time


def num_tokens_from_messages(message_list, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in message_list:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
                See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")



# 有时候会冒出来这样的字
# 一旦冒出来他就会一直说自己是人工智能了 （毕竟 presence_penalty 设置得比较高，如果出现了就甩不掉了）
# 为了维持人设，必须把这样的词删掉
wake_up_word = ["AI","助手","人工智能","语言模型","程序","预训练","虚构","角色","扮演","模拟"]

def add_conversation(conversation: str, message_list : list, role: str = "user",):
    if role == "assistant":
        if any(item in conversation for item in wake_up_word):
            return message_list
    message_list.append({"role": role, "content": conversation})

    return message_list


def limit_conversation_size(conversation: str, conversaton_max_size: int) -> str :
    # Each Chinese character / English character / punctuation takes up 1 pos.
    if len(conversation) > conversaton_max_size:
        return conversation[:conversaton_max_size]
    else:
        return conversation


def check_message_length(message_list, message_remember_num) -> list :
    while num_tokens_from_messages(message_list) > 2000 or len(message_list) > message_remember_num:   # tiaojiao have 7 items. So it can remember 7 other conversations.
        try:
            message_list.pop(7)
        except Exception as e:
            print(e)
    return message_list

# Use openai async api
async def chat(message_list):
    try:
        response = await openai.ChatCompletion.acreate(
        model = "gpt-3.5-turbo",
        messages = message_list,
        # temperature = 0.5,
        presence_penalty = -1.4
        )
        answer = await response['choices'][0]['message']['content'].strip()
        
        if len(answer) != 0:  # Avoid blank answer.
            return answer
        else:
            return None
            # raise Exception
    except Exception as e:
        print(e) 
        return None



# ref: LittlePaimon
# https://github.com/CMHopeSunshine/LittlePaimon
class FreqLimiter:
    """
    频率限制器（冷却时间限制器）
    """

    def __init__(self):
        """
        初始化一个频率限制器
        """
        self.next_time = defaultdict(float)

    def check(self, key: str) -> bool:
        """
        检查是否冷却结束
            :param key: key
            :return: 布尔值
        """
        return time.time() >= self.next_time[key]

    def start(self, key: str, cooldown_time: int = 0):
        """
        开始冷却
            :param key: key
            :param cooldown_time: 冷却时间(秒)
        """
        self.next_time[key] = time.time() + (cooldown_time if cooldown_time > 0 else 60)

    def left(self, key: str) -> int:
        """
        剩余冷却时间
            :param key: key
            :return: 剩余冷却时间
        """
        return int(self.next_time[key] - time.time()) + 1

freq_limiter = FreqLimiter()



# Get cyber position
# aka. Check the avaliability of proxy

async def get_cyber_pos(use_proxy: bool = False, proxies: dict = None):
    async with aiohttp.ClientSession() as session:
        url = 'https://ipapi.co/json/'
        # 优先使用http。与openai 协程查询逻辑相同。
        if use_proxy:
            if "https" in proxies.keys():
                proxy_check = proxies['https']
            else:
                proxy_check = list(proxies.values())[0]
        else:
            proxy_check = None
        async with session.get(url, proxy = proxy_check) as response:
            resp_json = await response.json()
            # print(response)
            return resp_json["country_name"]
