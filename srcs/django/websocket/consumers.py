import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import uuid

class MatchConsumer(AsyncWebsocketConsumer):
    waiting_users = []
    user_info = {}

    async def connect(self):
        await self.accept()
        self.user_id = self.scope['user'].id
        self.channel_id = str(uuid.uuid4())  # 一意のUUIDを生成
        self.user_info[self.channel_id] = {
            'channel_name': self.channel_name,
            'user_id': self.user_id
        }

    async def disconnect(self, close_code):
        if self.channel_id in self.waiting_users:
            self.waiting_users.remove(self.channel_id)
        if self.channel_id in self.user_info:
            del self.user_info[self.channel_id]

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        if action == 'join':
            self.waiting_users.append(self.channel_id)
            await self.match_users()

    async def match_users(self):
        if len(self.waiting_users) >= 2:
            uuid1 = self.waiting_users.pop(0)
            uuid2 = self.waiting_users.pop(0)
            user1_info = self.user_info[uuid1]
            user2_info = self.user_info[uuid2]
            group_name = f'match_{uuid1}_{uuid2}'

            # 両方のユーザーをグループに追加
            await self.channel_layer.group_add(group_name, user1_info['channel_name'])
            await self.channel_layer.group_add(group_name, user2_info['channel_name'])

            # グループにマッチメッセージを送信
            match_url = f'/match-game/{uuid1}_{uuid2}/'  # 対戦ページのURLを生成
            await self.channel_layer.group_send(
                group_name,
                {
                    'type': 'match_message',
                    'message': f'User {uuid1} matched with User {uuid2}',
                    'url': match_url
                }
            )

    async def match_message(self, event):
        message = event['message']
        url = event['url']
        await self.send(text_data=json.dumps({
            'message': message,
            'url': url
        }))
        await self.close()  # 接続を閉じる
