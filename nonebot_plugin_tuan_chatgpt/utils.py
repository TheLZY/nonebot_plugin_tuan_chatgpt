import tiktoken
import openai

import asyncio
import aiohttp
# Freq limiter
from collections import defaultdict
import time
import asyncio
from nonebot.log import logger
import random

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
wake_up_word = ["AI","助手","人工智能","语言模型","程序","预训练","虚构","角色","扮演","模拟","模仿"]

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


def check_message_length(message_list, message_init_len, conversation_remember_num) -> list :
    while num_tokens_from_messages(message_list) > 2000 or len(message_list) > message_init_len + conversation_remember_num:   # tiaojiao have 7 items. So it can remember 7 other conversations.
        try:
            message_list.pop(message_init_len)
        except Exception as e:
            logger.error(f'check_message_length 发生错误 {e}')
    return message_list
        # messages

# Use openai async api
async def chat(message_list):
    retries = 0
    last_exception = None
    while retries < 3:  # 如果失败 自动重试3次 否则raise 最后一次错误
        try:
            response = await openai.ChatCompletion.acreate(
                model = "gpt-3.5-turbo-0301",   # 最新的模型抽风了好几次 怕了怕了
                messages = message_list,
                # temperature = 0.5,
                presence_penalty = - 0.8,
                # frequency_penalty = - 0.5,  # 这个加了容易出bug
                timeout = 20
                # 这个如果报错 TryAgain 会自动重试 但是是api返回的 所以还是自己写 retries 吧
                )

            answer = response.choices[0].message.content
            if len(answer) != 0:  #避免返回空白
                return answer
            else:
                last_exception =  'Empty answer received'
        # 也可以用openai自己的报错
        # except openai.error.OpenAIError as e:
        # print(e.http_status)
        # print(e.error)
        except Exception as e:
            retries += 1
            last_exception = e
            logger.error(f'第 {retries} 次请求openai api 发生错误，报错信息为{e}')
            await asyncio.sleep(1)  # 暂停一秒钟后重试
    raise last_exception



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



def generate_error_message(e)  -> str:
    '''
    根据错误信息 产生错误消息
    '''
    
    if str(e) == "Error communicating with OpenAI":
        e = "梯子又出问题了！"

    error_message_list = [
        f'呜呜呜，风好太，网好差，听不清，等风小了再试试嘛 \n对了，我刚才捡到张纸条，上面写了 {e}',
        f'团子被玩兒壞了！這肯定不是团子的問題！絕對不是！要怪就怪{e} ！',
        f'（无感情声线） 报错 {e}'
    ]

    error_message = random.choice(error_message_list)
    return error_message