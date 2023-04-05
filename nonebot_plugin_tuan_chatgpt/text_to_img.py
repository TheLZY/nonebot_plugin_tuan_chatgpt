# Ref:
# https://github.com/lss233/chatgpt-mirai-qq-bot/blob/browser-version/utils/text_to_img.py

import itertools
import os
# import pathlib
# import shutil
import textwrap

import aiohttp
# import asyncio
# import imgkit

import qrcode
import unicodedata
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from io import BytesIO
# import base64
from nonebot.adapters.onebot.v11 import MessageSegment
# from nonebot.adapters.telegram import MessageSegment
from .perf_timer import PerfTimer
from typing import Union
from pathlib import Path


from nonebot.log import logger

from .config import config


# 制作只有文字，背景透明的图片
def text_to_image_raw(text, 
                      canvas_width = config.chat_canvas_width, 
                      data_path = config.chat_data_path,
                      font_path = config.chat_font_path,
                      font_name = config.chat_font_name,
                      font_size = config.chat_font_size, 
                      offset_x = config.chat_offset_x,
                      offset_y = config.chat_offset_y) -> Image  :
    '''
    text to image
    使用pillow画图 不渲染markdown
    可以添加背景 会自动使用高斯模糊
    字体会自动加描边
    字体画布的大小为 ( canvas_width - 2 * offset_x , canvas_height - offset_y , )
    canvas_height 由计算得到。

    :param canvas_width: 画布总宽度。
    '''

    canvas_text_width = canvas_width - 2 * offset_x

    
    if data_path == 'data/tuan_chat': # 未定义时，使用工作目录
        pwd_path = Path.cwd()   # 使用bot的工作目录 （应该与 bot.py 相同）
        data_path = os.path.join(pwd_path, data_path)
    
    # Use the specified font to measure the size of the text
    if font_path == 'font':
        fpath = os.path.join(data_path, 'font', font_name)
    else:
        fpath = os.path.join(font_path, font_name)
    
    if not os.path.exists(fpath):
        logger.error(f"Font file not found in {fpath}. Check your file.")
        raise FileNotFoundError
    font = ImageFont.truetype(fpath , font_size)

    lines = text.split('\n')
    char_width = font.getbbox('啊')[2] - font.getbbox('啊')[0]
    char_height = font.getbbox('啊')[2] - font.getbbox('啊')[0]

    # '啊' is counted as 2 in width.
    wrapper = TextWrapper(width = int( 2 * canvas_text_width / char_width), break_long_words=True)
    wrapped_text = [wrapper.wrap(i) for i in lines if i != '']
    wrapped_text = list(itertools.chain.from_iterable(wrapped_text))

    # print(wrapped_text)

    # # Calculate the height of the image based on all lines of text
    # # 可以 但没必要。 就用 char_height 也不是不可以
    # # 计算每行文本的 size 并提取高度。这种方式更为准确，但是相应的计算量也会大一点
    # text_bboxes = [font.getbbox(line) for line in wrapped_text]
    # text_heights = [bbox[3] - bbox[1] for bbox in text_bboxes]
    # # 用 最长的行高 * 0.3 来作为行间距
    # line_spacing = 0.3 * max(text_heights)
    line_spacing = 0.3 * char_height
    
    # 计算文字画布的高度，以及总画布的高度
    canvas_text_height = (len(wrapped_text)) * (line_spacing + char_height)
    canvas_height = int(canvas_text_height + offset_y)

    # Create a new image with the calculated height and the specified width
    image = Image.new('RGBA', (canvas_width, canvas_height), color=(255, 255, 255, 0))
    # Create a draw object that can be used to draw on the image
    draw = ImageDraw.Draw(image)

    # Draw the wrapped text on the image
    # spacing 要减去描边 stroke_width
    draw.text((offset_x, offset_y), '\n'.join(wrapped_text), font = font, fill = 'black', spacing = line_spacing - 3*2, stroke_width = 3, stroke_fill='white')

    return image

    
# 缝合 qr_code 以及 原始图片
async def add_qr_code(image_origional, text)   ->  Image  :
    """
    将二维码附在图片的右下角.
    """

    async def get_qr_code(text):
        """
        将 Markdown 文本保存到 Mozilla Pastebin, 并获得 URL
        然后制作二维码
        """
        async with aiohttp.ClientSession() as session:
            payload = {'expires': '86400', 'format': 'url', 'lexer': '_markdown', 'content': text}
            try:
                async with session.post('https://pastebin.mozilla.org/api/', data=payload) as resp:
                    resp.raise_for_status()
                    url = await resp.text()
            except Exception as e:
                url = "上传失败：" + str(e)
            image = qrcode.make(url)
            return image

    qr_image = await get_qr_code(text)

    # 获取两张图片的尺寸
    image_width, image_height = image_origional.size
    # qr_width, qr_height = qr_image.size

    qr_image_resized = qr_image.resize((140,140))

    # 创建一个新图片，尺寸为（原图宽度， 原图高度 + 200）
    combined_image = Image.new("RGBA", (image_width, image_height + 200), (255,255,255,0))

    # 将两张图片粘贴到新图片上
    combined_image.paste(image_origional, (0, 0), mask = image_origional)
    combined_image.paste(qr_image_resized, (image_width - 170, image_height + 30 ))
    return combined_image


def add_background(image: Image) -> Image :
    '''Add white background for image, or its transparent'''
    
    image_width, image_height = image.size

    output_image = Image.new("RGB", (image_width, image_height), color=(255,255,255))

    output_image.paste(image, mask=image)
    # image.paste(local_image_blurred)
    # Use the specified font to write the text on the image
    # font = ImageFont.truetype(font_name, font_size)
    return output_image
    

def add_background_with_local_image(
        image: Image,
        data_path: str = config.chat_data_path,
        background_image_path: str = config.chat_background_path  ) -> Image :
    '''
    从文件夹中随机选取图片作为背景图片。
    会自动增加高斯模糊效果
    '''

    if data_path == 'data/tuan_chat': # 使用默认值时，使用工作目录。否则使用默认值的绝对目录
        pwd_path = Path.cwd()   # 使用bot的工作目录 （应该与 bot.py 相同）
        data_path = os.path.join(pwd_path, data_path)

    # Use the specified font to measure the size of the text
    if background_image_path == 'background':
        fpath = os.path.join(data_path, background_image_path)
    else:
        fpath = background_image_path
    if not os.path.exists(fpath):
        logger.error(f"Background photo not found in {fpath}. Automatically render without background image. Please check your file.")
        return add_background(image)
        # raise FileNotFoundError

    files = os.listdir(fpath)
    # 通过文件扩展名筛选图片文件
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    images = [file for file in files if file.lower().endswith(image_extensions)]
    if not images:
        logger.error(f"No file found in path {fpath}. Check your background path ")
        raise FileNotFoundError

    # 随机选择一个图片文件
    random_image = random.choice(images)

    # 返回随机选择的图片的完整路径
    imagepath =  os.path.join(fpath, random_image)

    local_image = Image.open(imagepath)

    # 获取两张图片的尺寸
    image_width, image_height = image.size
    local_image_width, local_image_height = local_image.size

    # 计算缩放比例并调整图片高度
    scale_ratio = image_width / local_image_width
    new_height = int(local_image_height * scale_ratio)
    local_image_resized = local_image.resize((image_width, new_height))

    # 应用高斯模糊
    blur_radius = 4  # 模糊半径，可根据需要调整。增加此值可增加模糊程度
    local_image_blurred = local_image_resized.filter(ImageFilter.GaussianBlur(blur_radius))

    # 前面加一层半透明的白色
    add_image = Image.new("RGBA", (image_width, new_height), color=(255,255,255,150))
    local_image_blurred.paste(add_image, mask=add_image)


    # 全部叠到output上
    output_image = Image.new("RGB", (image_width, image_height), color=(255,255,255))


    if new_height < image_height: # 缩放后的背景图更小：居中放置
        output_image.paste(local_image_blurred, (0, 0.5 * (image_height - new_height)))
    else:
        output_image.paste(local_image_blurred)

    output_image.paste(image, mask=image)

    return output_image



# # 不好用，电影院报错了两小时
# def image_to_base64(image: Image.Image, fmt='png') -> str:
#     output_buffer = BytesIO()
#     image.save(output_buffer, format=fmt)
#     byte_data = output_buffer.getvalue()
#     base64_str = base64.b64encode(byte_data).decode('utf-8')
#     return f'data:image/{fmt};base64,' + base64_str


# ref:
# https://github.com/kexue-z/nonebot-plugin-setu-now/blob/63cd10f5e0d8267180327e38937932e0cec14f0f/nonebot_plugin_setu_now/img_utils.py
def image_segment_convert(img: Union[Path, Image.Image, bytes]) -> MessageSegment:
    if isinstance(img, Path):
        return MessageSegment.image(img)
    elif isinstance(img, bytes):
        img = Image.open(BytesIO(img))
    elif isinstance(img, Image.Image):
        pass
    else:
        raise ValueError(f"Unsopported image type: {type(img)}")
    image_bytesio = BytesIO()
    save_timer = PerfTimer.start(f"Save bytes {img.width} x {img.height}")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(
        image_bytesio,
        format="JPEG",
        quality="keep" if img.format in ("JPEG", "JPG") else 95,
    )
    save_timer.stop()
    return MessageSegment.image(image_bytesio)  # type: ignore


async def text2img_main(text: str = '',
                        config = config,
                        ) -> Image:
    
    try:
        image = text_to_image_raw(text = text)

        if config.chat_use_qr:
            image = await add_qr_code(image_origional = image, text= text)

        if config.chat_use_background:
            output_image = add_background_with_local_image(image = image)
        else:
            output_image = add_background(image = image)
        output = image_segment_convert(output_image)
        return output
    
    except Exception as e:
        raise e







# TextWrapper
# 用于给文本分段
class TextWrapper(textwrap.TextWrapper):
    char_widths = {
        'W': 2,  # Wide
        'Na': 1,  # Narrow
        'F': 2,  # Fullwidth
        'H': 1,  # Half-width
        'A': 2,  # ?
        'N': 1  # Neutral
    }

    def _strlen(self, text):
        """
        Calcaute display length of a line according to unicodedata.east_asian_width()
        Not accurate, considering each font is different.
        But enough to use, since we still have padding
        """
        charslen = 0
        for char in text:
            charslen += self.char_widths[unicodedata.east_asian_width(char)]
        return charslen

    def _wrap_chunks(self, chunks):
        """_wrap_chunks(chunks : [string]) -> [string]
        Code from https://github.com/python/cpython/blob/3.9/Lib/textwrap.py
        Wrap a sequence of text chunks and return a list of lines of
        length 'self.width' or less.  (If 'break_long_words' is false,
        some lines may be longer than this.)  Chunks correspond roughly
        to words and the whitespace between them: each chunk is
        indivisible (modulo 'break_long_words'), but a line break can
        come between any two chunks.  Chunks should not have internal
        whitespace; i.e. a chunk is either all whitespace or a "word".
        Whitespace chunks will be removed from the beginning and end of
        lines, but apart from that whitespace is preserved.
        """
        lines = []
        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)
        if self.max_lines is not None:
            if self.max_lines > 1:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            if len(indent) + len(self.placeholder.lstrip()) > self.width:
                raise ValueError("placeholder too large for max width")

        # Arrange in reverse order so items can be efficiently popped
        # from a stack of chucks.
        chunks.reverse()

        while chunks:

            # Start the list of chunks that will make up the current line.
            # cur_len is just the length of all the chunks in cur_line.
            cur_line = []
            cur_len = 0

            # Figure out which static string will prefix this line.
            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent

            # Maximum width for this line.
            width = self.width - len(indent)

            # First chunk on line is whitespace -- drop it, unless this
            # is the very beginning of the text (ie. no lines started yet).
            if self.drop_whitespace and chunks[-1].strip() == '' and lines:
                del chunks[-1]

            while chunks:
                l = self._strlen(chunks[-1])

                # Can at least squeeze this chunk onto the current line.
                if cur_len + l <= width:
                    cur_line.append(chunks.pop())
                    cur_len += l

                # Nope, this line is full.
                else:
                    break

            # The current line is full, and the next chunk is too big to
            # fit on *any* line (not just this one).
            if chunks and self._strlen(chunks[-1]) > width:
                self._handle_long_word(chunks, cur_line, cur_len, width)
                cur_len = sum(map(self._strlen, cur_line))

            # If the last chunk on this line is all whitespace, drop it.
            if self.drop_whitespace and cur_line and cur_line[-1].strip() == '':
                cur_len -= self._strlen(cur_line[-1])
                del cur_line[-1]

            if cur_line:
                if (self.max_lines is None or
                        self._strlen(lines) + 1 < self.max_lines or
                        (not chunks or
                         self.drop_whitespace and
                         self._strlen(chunks) == 1 and
                         not chunks[0].strip()) and cur_len <= width):
                    # Convert current line back to a string and store it in
                    # list of all lines (return value).
                    lines.append(indent + ''.join(cur_line))
                else:
                    while cur_line:
                        if (cur_line[-1].strip() and
                                cur_len + self._strlen(self.placeholder) <= width):
                            cur_line.append(self.placeholder)
                            lines.append(indent + ''.join(cur_line))
                            break
                        cur_len -= len(cur_line[-1])
                        del cur_line[-1]
                    else:
                        if lines:
                            prev_line = lines[-1].rstrip()
                            if (self._strlen(prev_line) + self._strlen(self.placeholder) <=
                                    self.width):
                                lines[-1] = prev_line + self.placeholder
                                break
                        lines.append(indent + self.placeholder.lstrip())
                    break

        return lines

    def _get_space_left(self, text, requested_len):
        """
        Calcuate actual space_left
        """
        charslen = 0
        counter = 0
        for char in text:
            counter = counter + 1
            charslen += self.char_widths[unicodedata.east_asian_width(char)]
            if (charslen >= requested_len):
                break
        return counter

    def _handle_long_word(self, reversed_chunks, cur_line, cur_len, width):
        """_handle_long_word(chunks : [string],
                             cur_line : [string],
                             cur_len : int, width : int)
        Handle a chunk of text (most likely a word, not whitespace) that
        is too long to fit in any line.
        """
        # Figure out when indent is larger than the specified width, and make
        # sure at least one character is stripped off on every pass
        if width < 1:
            space_left = 1
        else:
            space_left = width - cur_len

        # If we're allowed to break long words, then do so: put as much
        # of the next chunk onto the current line as will fit.
        space_left = self._get_space_left(reversed_chunks[-1], space_left)
        if self.break_long_words:
            cur_line.append(reversed_chunks[-1][:space_left])
            reversed_chunks[-1] = reversed_chunks[-1][space_left:]

        # Otherwise, we have to preserve the long word intact.  Only add
        # it to the current line if there's nothing already there --
        # that minimizes how much we violate the width constraint.
        elif not cur_line:
            cur_line.append(reversed_chunks.pop())

        # If we're not allowed to break long words, and there's already
        # text on the current line, do nothing.  Next time through the
        # main loop of _wrap_chunks(), we'll wind up here again, but
        # cur_len will be zero, so the next line will be entirely
        # devoted to the long word that we can't handle right now.

    def _split_chunks(self, text):
        text = self._munge_whitespace(text)
        return self._split(text)
