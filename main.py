"""
@author: wangye(Wayne)
@license: Apache Licence
@file: main.py
@time: 20221206
@contact: wang121ye@hotmail.com
@site:  wangyendt@github.com
@software: PyCharm

# code is far away from bugs.
"""

from CONFIG import *
import os
import asyncio
from typing import List, Optional, Union
from wechaty_puppet import FileBox, MessageType  # type: ignore
from wechaty import Wechaty, Contact
from wechaty.user import Message, Room
from chat_gpt.main import Chat
import paddlehub as hub

os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = TOKEN
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = '127.0.0.1:8080'


class MyBot(Wechaty):

    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact: Optional[Contact] = msg.talker()
        text = msg.text()
        room: Optional[Room] = msg.room()
        if text == 'ding':
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('dong')
            file_box = FileBox.from_url(
                'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
                'u=1116676390,2305043183&fm=26&gp=0.jpg',
                name='ding-dong.jpg')
            await conversation.say(file_box)


class VoiceBot(Wechaty):
    def __init__(self):
        super().__init__()
        self.module_lover_words = hub.Module(name="ernie_gen_lover_words")
        self.module_couplet = hub.Module(name="ernie_gen_couplet")
        self.chatter = Chat(USERNAME, PASSWORD)
        self.cache_dir = '.'
        self.available_group = {
            '健康算法与可行性组',
            '哈哈群',
            '神鸟干饭小分队',
            '幸福港湾',
            '幸福家庭',
            '高管高工前沿科技科普群'
        }

    async def on_message(self, msg: Message) -> None:
        """listen message event"""
        # if msg.is_self():
        #     return
        if msg.room() and msg.chatter().payload.topic in self.available_group:
            if msg.message_type() == MessageType.MESSAGE_TYPE_TEXT:
                await msg.ready()
                in_content = msg.text()
                if any(in_content.startswith(prefix) for prefix in ('>>>', '提问:', '提问：')):
                    text = msg.text()[3:]
                    print(text)
                    answer = self.chatter.ask(text)
                    print(answer)
                    await msg.room().say(f'[来自ChatGPT:]\n{answer}')
                elif any(in_content.startswith(prefix) for prefix in ('藏头诗<5>：', '藏头诗<5>:')):
                    text = msg.text()[7:]
                    print(text)
                    module = hub.Module(name="ernie_gen_acrostic_poetry", line=len(text), word=5)
                    results = module.generate(texts=[text], use_gpu=True, beam_width=1)
                    print(results[0][0])
                    await msg.room().say(f'[来自PaddlePaddle:]\n{results[0][0]}')
                elif any(in_content.startswith(prefix) for prefix in ('藏头诗<7>：', '藏头诗<7>:')):
                    text = msg.text()[7:]
                    print(text)
                    module = hub.Module(name="ernie_gen_acrostic_poetry", line=len(text), word=7)
                    results = module.generate(texts=[text], use_gpu=True, beam_width=1)
                    print(results[0][0])
                    await msg.room().say(f'[来自PaddlePaddle:]\n{results[0][0]}')
                elif any(in_content.startswith(prefix) for prefix in ('情话：', '情话:')):
                    text = msg.text()[3:]
                    print(text)
                    results = self.module_lover_words.generate(texts=[text], use_gpu=True, beam_width=1)
                    print(results[0][0])
                    await msg.room().say(f'[来自PaddlePaddle:]\n{results[0][0]}')
                elif any(in_content.startswith(prefix) for prefix in ('对联：', '对联:')):
                    text = msg.text()[3:]
                    print(text)
                    results = self.module_couplet.generate(texts=[text], use_gpu=True, beam_width=1)
                    print(results[0][0])
                    await msg.room().say(f'[来自PaddlePaddle:]\n{results[0][0]}')
                elif in_content == '机器人帮助':
                    helper_message = ''
                    await msg.room().say(helper_message)

            # group_name = msg.chatter()
            # print(group_name.payload.topic)
            # print(msg.type(), msg.text(), msg.is_self(), msg.is_ready(), msg.age(), msg.date(), msg.to(),msg.chatter(),msg.talker(),msg.room().room_id)
        else:
            print(msg.type(), msg.text(), msg.is_self(), msg.is_ready(), msg.age(), msg.date(), msg.to(), msg.chatter(), msg.talker(), msg.room().room_id)

        # if msg.type() == MessageType.MESSAGE_TYPE_AUDIO:
        #     # 保存用户发送的语音文件
        #     file_box = await msg.to_file_box()
        #     saved_file = os.path.join(self.cache_dir, file_box.name)
        #     await file_box.to_file(saved_file)
        #
        #     # 将本地保存的语音文件发送给说话者
        #     new_audio_file = FileBox.from_file(saved_file)
        #     new_audio_file.metadata = {
        #         "voiceLength": 2000
        #     }
        #     await msg.talker().say(new_audio_file)
        # elif msg.type() == MessageType.MESSAGE_TYPE_TEXT:
        #     await msg.talker().say(msg.text())


# asyncio.run(MyBot().start())
asyncio.run(VoiceBot().start())
