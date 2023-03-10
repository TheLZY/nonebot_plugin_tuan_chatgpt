from nonebot import get_driver
from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    chatgpt_api: str = ""
    conversation_max_size: int = 50  # For each conversation, only use first 50 words
    answer_max_size: int = 30        # For each answer, only record first 30 words
    answer_split_size: int = 177     # Length division for answer
    user_freq_lim: int = 4           # Limit the speaking speed of group members. (second)
    group_freq_lim: int = 6          # Limit the speaking speed in a group. 
    conversation_remember_num: int = 14    # The number of conversation that is remembered. 14 means she can remember 7 conversation from user.
    chat_use_proxy: bool = False      # Use proxy or not. In fact it's not needed. Just to remind everyone this function exists.
    chat_proxy_address: dict = None  # Example: {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'} By the way, seems like openai proxy only accept http / https.
    
config = Config.parse_obj(get_driver().config)