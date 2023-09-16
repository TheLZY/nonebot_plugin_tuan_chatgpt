from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment
# from nonebot.adapters.telegram import Bot
# from nonebot.adapters.telegram.event import MessageEvent
from nonebot import on_command, on_message # ,MatcherGroup
from nonebot.rule import to_me
from nonebot.plugin import PluginMetadata
from nonebot.params import RawCommand
from nonebot.permission import SUPERUSER
from nonebot.log import logger

from .utils import *
from .config import config, NICKNAME, init_name
from .text_to_img import text2img_main
import openai

import asyncio
import re
import random

__plugin_meta__ = PluginMetadata(
    name='团子聊天',
    description='团子聊天 QQ bot ver. powered by Chatgpt',
    usage='团子[聊天内容]',
    extra={
        'author': 'TheLZY',
        'version': '0.4',
        'priority': 8,
        'configs': {
            '群冷却': 4,
            '群成员冷却': 6
        }
    }
)

###==============  初始化  =================###
if config.chatgpt_api:
    openai.api_key = config.chatgpt_api
else:
    logger.error("未配置 tuan-chatgpt api，无法使用chatgpt")

if not init_name:
    logger.warning("未配置 nickname，只会响应@消息")

# 使用api转发
if config.chat_use_api_forward:
    if config.chat_api_address:
        openai.api_base = config.chat_api_address
    else:
        logger.error("请检查 api 转发地址 chat_api_address")

# 使用代理
if config.chat_use_proxy:
    # 优先使用 https （类似openai的做法）
    # 两个都写的话不知道为什么容易报错
    # openai.proxy =  {'http': config.chat_proxy_address_http, 'https': config.chat_proxy_address_https}
    if config.chat_proxy_address_https:
        proxy ={'https': config.chat_proxy_address_https}
    elif config.chat_proxy_address_http:
        proxy = {'http': config.chat_proxy_address_http}
    else:
        logger.error("请检查 tuan-chatgpt 代理地址")
    openai.proxy = proxy

# 初始化路径
path_init()



###==============  主要处理函数  =================###

chat_service = on_message(rule = to_me() , priority = 99, block = False)

chat_service_history = on_command("历史记录",rule = to_me() , permission=SUPERUSER, aliases={'history'}, priority=98, block=True)
chat_service_clean = on_command("清除记忆",rule = to_me() , aliases={'消除记忆','记忆消除','清除历史记录','清空历史记录'}, priority=98, block=True)
chat_service_position = on_command("看看位置",rule = to_me() , aliases={'你在哪儿'}, priority=98, block=True)


@chat_service.handle()
async def main_chat(event: MessageEvent):
    global tuan_freq_limiter
    global messagebox

    # Check cd
    # 对于群聊：使用group_id来限制发言频率
    # 对于私聊：使用uer_id来限制发言频率
    # 去掉回复功能，避免高频呼叫的高频回复

    if isinstance(event, GroupMessageEvent):
        chat_id = f"chat-group{event.group_id}"
    else:
        chat_id = f"chat-user{event.user_id}"

    if not tuan_freq_limiter.check(chat_id):
            # await chat_service.finish(f'你们说话太快啦! { tuan_freq_limiter.left(chat_id) }秒之后再理你们！')
            logger.info(f'{chat_id} 说话太快，此条消息被弃用')
            await chat_service.finish()

    conversation = str(event.original_message)

    conversation = conversation_preprocessing(conversation)
    if not conversation or conversation == "":
        # 空消息直接结束
        # 似乎不能直接break？
        await chat_service.finish()

    # Length detect for conversation
    conversation = limit_conversation_size(conversation, config.conversation_max_size)

    # 将这段聊天加入聊天历史中
    # 聊天历史会和人设信息整合在一起
    # ps.人设信息会随机抽取
    messagebox.add(conversation = conversation, id = chat_id)

    messages = messagebox.get_messages(id = chat_id)
    
    # 主要交流函数
    try:
        answer = await chat(message_list = messages)
    except Exception as e:
        # print("调用API失败：", e)
        # message_list_user.pop()  # 调用失败不保存这个会话 但是这一步的时候协程可能会出现问题 就是加锁又太影响性能了 算了 先这样
        messagebox.delete_fail(id=chat_id)
        error_message = generate_error_message(e = e)
        await chat_service.finish(error_message)
        
    # 储存answer
    answer_add = limit_conversation_size(answer, config.answer_max_size)
    # message_list_user = add_conversation(answer_add, message_list_user, 'assistant')
    messagebox.add(conversation = answer_add, role =  'assistant', id = chat_id)

    # 限制聊天频率
    # 其实可以直接改成 id 的 不过因为分了群聊和私聊还是得弄一下
    if isinstance(event, GroupMessageEvent):
        tuan_freq_limiter.start(f'chat-group{event.group_id}', config.chat_freq_lim)
        # 都设置一个，也不是不行
    tuan_freq_limiter.start(f'chat-user{event.user_id}', config.chat_freq_lim)

    # Length division for answer
    # 避免腾讯风控。
    # 现在的处理方式是分隔成几段，慢慢发
    # 不过其实也可以渲染成图片发出去。但是考虑到长回答的时候大部分是代码有关的，发图会不太方便复制
    if len(answer) < config.answer_split_size:
        await chat_service.finish(answer)

    # 开启图片渲染时：
    # 2条以内 直接发送
    # 否则 只发送前3条
    else:
        if config.chat_use_img2text:
            try:
                img = await text2img_main(text = answer)
            except Exception as e:
                logger.error(f"渲染图片时出错，报错 {e}")
                error_message = generate_error_message(e = e)
                await chat_service.finish(error_message)
            await chat_service.send(img)
        else:
            answer_segments = [answer[i:i + config.answer_split_size] for i in range(0, len(answer), config.answer_split_size)]
            for i in answer_segments[:3]:
                # 避免说话太快被腾讯风控
                await asyncio.sleep(1)
                await chat_service.send(i)


# 调试用。输出最近的几个问题

@chat_service_history.handle()
async def send_messagelist(event: MessageEvent):
    # 太长了容易被腾讯拦截 
    # global message_list_user
    # for conversation in message_list_user:
    #     if conversation['role'] == "user":
    #         print(str(conversation['content']))
    #         # 有时候部分QQ客户端不显示 （PC / 手机） 可能有风控危险
    #         # 间隔一段时间发一次，避免发送速度过快引发腾讯风控
    #         # 但是print是没问题的
    #         await asyncio.sleep(1)
    #         await chat_service_history.send(str(conversation['content']))
    global messagebox
    if isinstance(event, GroupMessageEvent):
        chat_id = f"chat-group{event.group_id}"
    else:
        chat_id = f'chat-user{event.user_id}'

    history_list = messagebox.get_history(id=chat_id)

    if history_list == []:
        await chat_service_history.send(f"你还没有和{NICKNAME}聊过天哦~")

    for conversation in history_list:
        if conversation['role'] == "user":
            # print(str(conversation['content']))
            # 有时候部分QQ客户端不显示 （PC / 手机） 可能有风控危险
            # 间隔一段时间发一次，避免发送速度过快引发腾讯风控
            # 但是print是没问题的
            await asyncio.sleep(1)
            await chat_service_history.send(str(conversation['content']))


@chat_service_clean.handle()
async def clean_history(event: MessageEvent):
    global messagebox
    if isinstance(event, GroupMessageEvent):
        chat_id = f"chat-group{event.group_id}"
    else:
        chat_id = f'chat-user{event.user_id}'

    messagebox.clean(id = chat_id)

    clean_message_list = [f'清除成功啦~ 快来和{NICKNAME}聊天吧~',
                          f'已经全忘惹~ 快来和{NICKNAME}聊天吧~',
                          f'发生什么事啦？ 唔，总之，来和{NICKNAME}聊天吧~',
                          f'{NICKNAME}已经什么都不记得啦~ 快来和我聊天吧~']
    clean_message = random.choice(clean_message_list)
    
    await chat_service_clean.finish(clean_message)

@chat_service_position.handle()
async def check_position(event: MessageEvent):
    
    proxy = None
    try:
        if config.chat_proxy_address_https:
            proxy = config.chat_proxy_address_https
        elif config.chat_proxy_address_http:
            proxy = config.chat_proxy_address_http
        else:
            logger.warning("请检查 tuan-chatgpt 代理地址")

        pos = await get_cyber_pos(config.chat_use_proxy, proxy)
    except Exception as e:
        # print(e)
        await chat_service_history.finish(f'赛博旅游失败！都怪{e}！')
    # 不能写里面，不然finish也会被try视为报错
    await chat_service_history.finish(f'{NICKNAME}现在正在{pos}赛博旅游中~ ') 
