import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import uuid
import asyncio

class MatchConsumer(AsyncWebsocketConsumer):
    waiting_users = []
    user_info = {}

    async def connect(self):
        await self.accept()
        self.user_id = self.scope['user'].id
        self.channel_id = str(uuid.uuid4())
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

            await self.channel_layer.group_add(group_name, user1_info['channel_name'])
            await self.channel_layer.group_add(group_name, user2_info['channel_name'])

            match_url = f'/match-game/{uuid1}_{uuid2}/'
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
        await self.close()
# ボールをクラス化
screen_width = 5
screen_height = 8
class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update_position(self):
        self.x += self.vx
        self.y += self.vy

        # 壁との衝突判定
        if self.x <= 0 or self.x >= screen_width:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= screen_height:
            self.vy = -self.vy

class GameConsumer(AsyncWebsocketConsumer):
    rooms = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'game_{self.room_name}'

        if self.room_group_name not in self.rooms:
            self.rooms[self.room_group_name] = {
                'score': {'player1': 0, 'player2': 0},
                'ball_position': {'x': 0, 'y': 0},
            }

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def send_ball_position(self, ball_position):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'ball_position_update',
                'ball_position': ball_position
            }
        )

    async def ball_position_update(self, event):
        ball_position = event['ball_position']

        await self.send(text_data=json.dumps({
            'ball_position': ball_position
        }))
    async def update_ball_position(consumer):
        while True:
            # ボールの座標を計算するロジック
            ball_position = calculate_ball_position()
            await consumer.send_ball_position(ball_position)
            await asyncio.sleep(0.1)

