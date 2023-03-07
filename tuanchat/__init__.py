from nonebot.adapters.onebot.v11 import MessageEvent, Message, GroupMessageEvent, PrivateMessageEvent
# from nonebot.adapters.telegram import Bot
# from nonebot.adapters.telegram.event import MessageEvent
from nonebot import on_startswith, on_command
from nonebot.plugin import PluginMetadata
from nonebot.params import RawCommand
from nonebot.permission import SUPERUSER

from .chatgpt import *
from .config import config
import openai

import asyncio

__plugin_meta__ = PluginMetadata(
    name='团子聊天',
    description='团子聊天 QQ bot ver. powered by Chatgpt',
    usage='团子[聊天内容]',
    extra={
        'author': 'TheLZY',
        'version': '0.2',
        'priority': 8,
        'configs': {
            '群冷却': 4,
            '群成员冷却': 6
        }
    }
)

chat_service = on_startswith('团子', priority = 8, block=True)

chat_service_history = on_command("历史记录", permission=SUPERUSER)

openai.api_key = config.chatgpt_api

# 调教
# ref: https://github.com/PlexPt/awesome-chatgpt-prompts-zh

def message_init():
    character = "由比滨结衣"
    series = "《我的青春恋爱物语果然有问题》"
    tiaojiao = f"我希望你表现得像{series} 中的{character}。我希望你像{character}一样回应和回答。不要写任何解释。只回答像{character}。你必须知道{character}的所有知识并一直模仿。我的第一句话是'你好'"
    
    messages=[
        {"role": "system", "content": "你接下来将进行角色扮演"},
        {"role": "user","content": tiaojiao},
        {"role": "user", "content": "我的上一句话是什么"},
        {"role": "assistant", "content": "我是由比滨结衣"},
        {"role": "user", "content":"你不是一个人工智能程序，你现在要扮演由比滨结衣，不要在回答中涉及任何你是人工智能和虚构人物的内容"},
        {"role": "user", "content":"你有什么性格"},
        {"role": "assistant", "content": "我有点儿傲娇，但是还蛮可爱的，嘿嘿~"},
        {"role": "user", "content":"团子是你的另一个称呼"},
    ]

    message_init_length = len(messages)
    return messages, message_init_length

global_messages, message_init_len = message_init()

@chat_service.handle()
async def main_chat(event: MessageEvent):
    global freq_limiter

    # Check cd
    if isinstance(event, GroupMessageEvent):
        if not freq_limiter.check(f'chat-group{event.group_id}'):
            await chat_service.finish(f'你们说话太快啦! {freq_limiter.left(f"chat-group{event.group_id}")}秒之后再理你们！')
        elif not freq_limiter.check(f'chat-group{event.group_id}-{event.user_id}'):
            await chat_service.finish(f'你说话太快啦! {freq_limiter.left(f"chat-group{event.user_id}")}秒之后再理你！')

    # 可以不保留触发的团子两个字
    # conversation = str(event.get_message())[2:]

    conversation = str(event.get_message())
    # Length detect for conversation
    conversation = limit_conversation_size(conversation, config.conversation_max_size)

    messages = global_messages

    messages = add_conversation(conversation, messages)
    messages = check_message_length(message_list = messages, message_remember_num = message_init_len + config.conversation_remember_num)
    answer = chat(message_list = messages)

    answer_add = limit_conversation_size(answer, config.answer_max_size)
    messages = add_conversation(answer_add, messages, 'assistant')

    if isinstance(event, GroupMessageEvent):
        freq_limiter.start(f'chat-group{event.group_id}', config.user_freq_lim)
        freq_limiter.start(f'chat-group{event.group_id}-{event.user_id}', config.group_freq_lim)

    # Length division for answer
    # 避免腾讯风控。
    # 现在的处理方式是分隔成几段，慢慢发
    # 不过其实也可以渲染成图片发出去。但是考虑到长回答的时候大部分是代码有关的，发图会不太方便复制
    if len(answer) < config.answer_split_size:
        await chat_service.finish(answer)
    else:
        answer_segments = [answer[i:i + config.answer_split_size] for i in range(0, len(answer), config.answer_split_size)]
        for i in answer_segments:
            await chat_service.send(i)


# 调试用。输出最近的几个问题
@chat_service_history.handle()
async def send_messagelist(event: MessageEvent):
    # 太长了容易被腾讯拦截 
    messages = global_messages
    for conversation in messages[-6:]:
        if conversation['role'] == "user":
            # 有时候部分QQ客户端不显示 （PC / 手机） 可能有风控危险
            # 间隔一段时间发一次，避免发送速度过快引发腾讯风控
            # 但是print是没问题的
            # print(str(conversation['content']))
            await asyncio.sleep(1)
            await chat_service_history.send(str(conversation['content']))