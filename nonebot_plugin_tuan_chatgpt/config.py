from nonebot import get_driver
from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    chatgpt_api: str = None
    conversation_max_size: int =  300 # For each conversation, only use first 77 words
    answer_max_size: int = 50        # For each answer, only record first 30 words
    answer_split_size: int = 177     # Length division for answer
    user_freq_lim: int = 4           # Limit the speaking speed of group members. (second)
    group_freq_lim: int = 6          # Limit the speaking speed in a group. 
    conversation_remember_num: int = 7    # The number of conversation that is remembered. 7 means she can remember 4 conversation from user. （太大了会忘记）
    chat_use_proxy: bool = False     # Use proxy or not. In fact it's not needed. Just to remind everyone this function exists.
    chat_proxy_address_http: str = None
    chat_proxy_address_https: str = None
    chat_use_api_forward: bool = False    # Use api forward or not. If it's true, the api address must be specified.
    chat_api_address: str = None
    
config = Config.parse_obj(get_driver().config)