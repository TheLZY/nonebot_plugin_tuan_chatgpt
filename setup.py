from setuptools import setup, find_packages

setup(
    name="nonebot_plugin_tuan_chatgpt",
    version="0.1.0-beta",
    author="TheLZY",
    author_email="thelzy@qq.com",
    description="Chat with tuanzi ~",
    license="MIT License",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Nonebot Plugins',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    url="https://github.com/TheLZY/nonebot_plugin_tuan_chatgpt",

    install_requires=["nonebot2", 
                      "nonebot-adapter-onebot"
                      "openai>=0.27.0",
                      "tiktoken>=0.3.0"]
    packages=find_packages()
)