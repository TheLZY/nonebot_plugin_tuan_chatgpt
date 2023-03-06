from nonebot import get_driver
from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    chatgpt_api: str = ""
    conversation_max_size: int = 50  # For each conversation, only use first 50 words
    answer_max_size: int = 30   # For each answer, only record first 30 words
    answer_split_size: int = 177  # TODO
    user_freq_lim: int = 4    # Limit the speaking speed of group members. (second)
    group_freq_lim: int = 6   # Limit the speaking speed in a group. 


config = Config.parse_obj(get_driver().config)