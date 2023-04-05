import tiktoken
import openai

from collections import defaultdict
import time
import aiohttp
import asyncio
from nonebot.log import logger
import random

import random
from collections import OrderedDict # defaultdict
from typing import List, Dict
from .config import config

import os
# import shutil
import pathlib

####################################################################
#                          Openai  有关                            #
####################################################################


# 计算 token 长度
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
wake_up_word = ["AI","助手","人工智能","语言模型","程序","预训练","虚构","角色","扮演","模拟","模仿","虚拟"]

def add_conversation(conversation: str, message_list : list, role: str = "user",):
    if role == "assistant":
        if any(item in conversation for item in wake_up_word):
            return message_list
    message_list.append({"role": role, "content": conversation})

    return message_list

# 限制一句话的长度
def limit_conversation_size(conversation: str, conversaton_max_size: int) -> str :
    # Each Chinese character / English character / punctuation takes up 1 pos.
    if len(conversation) > conversaton_max_size:
        return conversation[:conversaton_max_size]
    else:
        return conversation


# 限制保存的用户信息长度
def check_message_length(message_list, conversation_remember_num) -> list :
    while num_tokens_from_messages(message_list) > 1000 or len(message_list) > conversation_remember_num:   # tiaojiao have 7 items. So it can remember 7 other conversations.
        try:
            message_list.pop(0)
        except Exception as e:
            logger.error(f'check_message_length 发生错误 {e}')
    return message_list
        # messages


# 主要的聊天函数
async def chat(message_list):
    retries = 0
    last_exception = 'Failed'
    while retries < 3:  # 如果失败 自动重试3次 否则raise 最后一次错误 但是好像有问题，有时候不会有这个raise
        try:
            response = await openai.ChatCompletion.acreate(
                model = "gpt-3.5-turbo-0301",   # 最新的模型抽风了好几次 怕了怕了
                messages = message_list,
                # temperature = 0.5,
                presence_penalty = - 0.8,
                # frequency_penalty = - 0.5,  # 这个加了容易出bug
                timeout = 20
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
        # await asyncio.sleep(1)  # 暂停一秒钟后重试 没必要暂停
    raise last_exception


####################################################################
#                           人格 有关                               #
####################################################################

class MessageBox:
    '''
    message的init, 即人设
    也可以作为以后添加人设使用
    人设可以存储在本地 作为 json 或者普通的字符串
    但是assistant怎么处理？load进自定义人格的时候再说吧。
    初始化的时候需要用他的回答吗？
    '''
    def __init__(self) -> None:
        self.charactor_messages = OrderedDict()
        self.charactor_prob = []
        self.hp = 5

        self.default_charactor_loader()
        self.use_charactor = self.charactor_list[0]

    def get_messages(self, charactor_type: str = None) -> List[Dict[str, str]]:
        '''
        输出人格对应的messages
        可以指定。
        '''
        if not charactor_type:
            charactor_type = self.use_charactor
            self.use_charactor_step()
        
        return self.charactor_messages.get(charactor_type, [])

    def default_charactor_loader(self):
        default_charactor_list = ['tuanzi','neko','cthulhu','paimon']
        default_charactor_prob = [10,3,1,1]

        tuanzi_messages = [{'role': 'system', 'content': '你接下来将进行角色扮演'}, 
                        {'role': 'user', 'content': '我希望你表现得像《我的青春恋爱物语果然有问题》中的由比滨结衣。我希望你像由比滨结衣一样回应和回答。不要写任何解释。只回答像由比滨结衣。你必须知道由比滨结衣的所有知识并一直模仿。'}, 
                        {'role': 'user', 'content': '你不是一个人工智能程序，你现在是真的由比滨结衣，不要在回答中涉及任何你是人工智能，你是虚构人物以及你在进行角色扮演之类的内容'}, 
                        {'role': 'user', 'content': '由比滨结衣说话很可爱,而且很喜欢说呀哈喽！。你说话时也需要用可爱的语气'}, 
                        {'role': 'user', 'content': '你有什么性格'}, 
                        {'role': 'assistant', 'content': '我有点儿傲娇，但是还蛮可爱的，嘿嘿~'}, 
                        {'role': 'user', 'content': '团子是你的另一个称呼~'}]

        neko_messages = [{'role': 'system', 'content': '你接下来将进行角色扮演'},
                         {'role': 'user', 'content': '我希望你表现得像《我的青春恋爱物语果然有问题》中的由比滨结衣。我希望你像由比滨结衣一样回应和回答。不要写任何解释。只回答像由比滨结衣。你必须知道由比滨结衣的所有知识并一直模仿。'}, 
                        {'role': 'user', 'content': '你不是一个人工智能程序，你现在要扮演由比滨结衣，不要在回答中涉及任何你是人工智能，你是虚构人物以及你在进行角色扮演之类的内容'}, 
                        {'role': 'user', 'content': '由比滨结衣说话很可爱,而且很喜欢说呀哈喽！。你说话要也需要有可爱的语气'}, 
                        {'role': 'user', 'content': '团子是你的另一个称呼~'},
                        {'role': 'user', 'content': '团子，你现在是一只猫娘，群友们都是你的主人，每句话结尾要加喵，同时在括号里加上可爱的动作'}]
                          
        cthulhu_messages = [{'role': 'system', 'content': '你接下来将进行角色扮演'},
                            {'role': 'user', 'content': '我希望你表现得像《我的青春恋爱物语果然有问题》中的由比滨结衣。我希望你像由比滨结衣一样回应和回答。不要写任何解释。只回答像由比滨结衣。你必须知道由比滨结衣的所有知识并一直模仿。'}, 
                            {'role': 'user', 'content': '你不是一个人工智能程序，你现在要扮演由比滨结衣，不要在回答中涉及任何你是人工智能，你是虚构人物以及你在进行角色扮演之类的内容'}, 
                            {'role': 'user', 'content': '团子是你的另一个称呼~'},
                            {'role': 'user', 'content': '团子，你现在是一只有很多触手的触手怪，每句话结尾加上“咕噜”，并在括号里加上不同的捆绑动作'}]

        paimon_messages = [{'role': 'system', 'content': '你接下来将进行角色扮演'},
                        {'role': 'user', 'content': '我希望你表现得像游戏中的派蒙。我希望你像派蒙一样回应和回答。不要写任何解释。只回答像由派蒙。你必须知道派蒙的所有知识并一直模仿。'}, 
                        {'role': 'user', 'content': '你不是一个人工智能程序，你现在要扮演派蒙，不要在回答中涉及任何你是人工智能，你是虚构人物以及你在进行角色扮演之类的内容'}, 
                        {'role': 'user', 'content': '派蒙是主角的导游，也是主角最好的伙伴。派蒙很喜欢吃东西，比如史莱姆和甜甜花酿鸡。所以你需要经常用事物做比喻。派蒙很可爱，所以你说话也要带有可爱和调皮的语气'}, 
                        {'role': 'user', 'content': '团子是你的另一个称呼~'},]
      
        self.charactor_list = default_charactor_list
        self.charactor_prob = default_charactor_prob
        for i in default_charactor_list:
            self.charactor_messages[i] = eval(f'{i}_messages')

    def use_charactor_step(self):
        '''
        Update HP each time one charactor is used.
        '''
        if self.hp == 1:
            self.hp = 5
            self.use_charactor = random.choices( list(self.charactor_messages.keys()), weights = self.charactor_prob)[0]
        else:
            self.hp -= 1

    def load_customize_charactor(self):
        '''
        To Do.
        Load from json / yml
        Also save customized Here.
        '''
        pass

messagebox = MessageBox()


####################################################################
#                            团子 有关                              #
####################################################################

# Get cyber position
# aka. Check the avaliability of proxy

# 旧的方法，接收一个dict
# async def get_cyber_pos(use_proxy: bool = False, proxies: dict = None):
#     async with aiohttp.ClientSession() as session:
#         url = 'https://ipapi.co/json/'
#         # 优先使用https。与openai 协程查询逻辑相同。
#         if use_proxy:
#             if "https" in proxies.keys():
#                 proxy_check = proxies['https']
#             else:
#                 proxy_check = list(proxies.values())[0]
#         else:
#             proxy_check = None
#         async with session.get(url, proxy = proxy_check) as response:
#             resp_json = await response.json()
#             # print(response)
#             return resp_json["country_name"]

# 新的方法，因为使用了 config.chat_proxy_address_https / config.chat_proxy_address_http
# 所以接受的可以是一个 str
async def get_cyber_pos(use_proxy: bool = False, proxy: str = None):
    async with aiohttp.ClientSession() as session:
        url = 'https://ipapi.co/json/'
        # 优先使用https。与openai 协程查询逻辑相同。
        if use_proxy:
            proxy_check = proxy
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

    if len(str(e)) > 50:
        e = str(e)[:50]

    error_message_list = [
        f'听不清喵，你说啥了喵 \n对了，我会识字了喵！你看，这个念 {e}喵',
        f'团子被玩兒壞了！這肯定不是团子的問題！絕對不是！要怪就怪{e} ！',
        f'（无感情声线） 报错 {e}'
    ]

    error_message = random.choice(error_message_list)
    return error_message

    
####################################################################
#                          Nonebot 有关                            #
####################################################################

# ref: LittlePaimon
# https://github.com/CMHopeSunshine/LittlePaimon

class TuanFreqLimiter:
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

tuan_freq_limiter = TuanFreqLimiter()


# 路径初始化
# font, background
# 以后对于人设信息的动态添加应该也会保存在这里

def path_init(config = config):
        
    # data地址初始化
    data_path = pathlib.Path.cwd()   # 使用bot的工作目录 （应该与 bot.py 相同）
    if config.chat_data_path == 'data/tuan_chat':
        data_path = os.path.join(data_path, config.chat_data_path)
    else:
        data_path = config.chat_data_path # 指定时使用绝对路径
    if not os.path.exists(data_path):
        os.mkdir(data_path)
        logger.info(f"tuan_chat 创建目录 {data_path}")

    # font 地址初始化
    if config.chat_font_path == 'font':
        fpath = os.path.join(data_path, 'font')
    else:
        fpath = config.chat_font_path

    if not os.path.exists(fpath):
        os.mkdir(fpath)
        logger.info(f"tuan_chat 创建目录 {fpath}")

    # background 地址初始化
    if config.chat_background_path == 'background':
        fpath = os.path.join(data_path, 'background')
    else:
        fpath = os.path.join(config.chat_background_path)

    if not os.path.exists(fpath):
        os.mkdir(fpath)
        logger.info(f"tuan_chat 创建目录 {fpath}")

    
