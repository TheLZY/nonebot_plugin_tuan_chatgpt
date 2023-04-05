from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, GroupMessageEvent, PrivateMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment
# from nonebot.adapters.telegram import Bot
# from nonebot.adapters.telegram.event import MessageEvent
from nonebot import on_command, on_message
from nonebot.plugin import PluginMetadata
# from nonebot.params import RawCommand
from nonebot.permission import SUPERUSER
from nonebot.log import logger

from .utils import *
from .config import config
from .text_to_img import text2img_main
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


### 初始化设置
if config.chatgpt_api:
    openai.api_key = config.chatgpt_api
else:
    logger.error("请检查 tuan-chatgpt api")

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



async def chat_checker(event: MessageEvent) -> bool:
    # 检查 是否以团子开头 / to_me. 可能会造成一点性能问题
    res = str(event.get_message())[:2]  == '团子' or event.is_tome()
    return res

chat_service = on_message(rule = chat_checker , priority = 99, block = False)
chat_service_history = on_command("历史记录", permission=SUPERUSER)


# 这样做，每次重启会重置用户对话数据
# 可以考虑用json保存
message_list_user = []


@chat_service.handle()
async def main_chat(bot: Bot, event: MessageEvent):
    global tuan_freq_limiter
    global messagebox
    global message_list_user

    # Check cd
    if not tuan_freq_limiter.check(f'chat-user{event.user_id}'):
        await chat_service.finish(f'你说话太快啦! { tuan_freq_limiter.left(f"chat-user{event.user_id}") }秒之后再理你！')
    if isinstance(event, GroupMessageEvent):
        if not tuan_freq_limiter.check(f'chat-group{event.group_id}'):
            await chat_service.finish(f'你们说话太快啦! {tuan_freq_limiter.left(f"chat-group{event.group_id}")}秒之后再理你们！')


    # 可以不保留前面的团子两个字
    # conversation = str(event.get_message())[2:]
    conversation = str(event.get_message())

    # 没必要再写一个on command
    # 但是之后再来写@触发的时候估计要改
    if conversation == "团子看看位置":
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
        await chat_service_history.finish(f'团子现在正在{pos}赛博旅游中~ ') 

    # Length detect for conversation
    conversation = limit_conversation_size(conversation, config.conversation_max_size)

    message_list_user = add_conversation(conversation, message_list_user)
    message_list_user = check_message_length(message_list = message_list_user, conversation_remember_num = config.conversation_remember_num)

    # 将保存的用户信息和人设信息整合在一起
    # 人设信息会随机抽取
    messages = messagebox.get_messages() + message_list_user
    
    # 主要交流函数
    try:
        answer = await chat(message_list = messages)
    except Exception as e:
        # print("调用API失败：", e)
        message_list_user.pop()  # 调用失败不保存这个会话 但是这一步的时候协程可能会出现问题 就是加锁又太影响性能了 算了 先这样
        error_message = generate_error_message(e = e)
        await chat_service.finish(error_message)
        
    # 储存answer
    answer_add = limit_conversation_size(answer, config.answer_max_size)
    message_list_user = add_conversation(answer_add, message_list_user, 'assistant')

    # 限制聊天频率
    if isinstance(event, GroupMessageEvent):
        tuan_freq_limiter.start(f'chat-group{event.group_id}', config.group_freq_lim)
    tuan_freq_limiter.start(f'chat-user{event.user_id}', config.user_freq_lim)

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
                # Use sleep to avoid Tencent risk management
                await asyncio.sleep(1)
                await chat_service.send(i)

# 调试用。输出最近的几个问题

@chat_service_history.handle()
async def send_messagelist(event: MessageEvent):
    # 太长了容易被腾讯拦截 
    global message_list_user
    for conversation in message_list_user:
        if conversation['role'] == "user":
            print(str(conversation['content']))
            # 有时候部分QQ客户端不显示 （PC / 手机） 可能有风控危险
            # 间隔一段时间发一次，避免发送速度过快引发腾讯风控
            # 但是print是没问题的
            await asyncio.sleep(1)
            await chat_service_history.send(str(conversation['content']))