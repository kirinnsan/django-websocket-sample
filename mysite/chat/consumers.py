import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


# 非同期パターン
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # ルームグループに参加
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # WebSocket 接続を受け入れ
        await self.accept()

    
    async def disconnect(self, code):
        # ルームグループを抜ける
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # ルームグループにメッセージを送る
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
    
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


# 同期パターン
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name
        
#         # ルームグループに参加
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
        
#         # WebSocket 接続を受け入れ
#         self.accept()

#     def disconnect(self, code):
#         # ルームグループを抜ける
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
        
#         # ルームグループにメッセージを送る
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,  {"type": "chat_message", "message": message}
#         )        
#         # self.send(text_data=json.dumps({"message":message}))
        
#     # ルームグループからメッセージを受け取る
#     def chat_message(self, event):
#         message = event["message"]

#         # WebSocketにメッセージを送る
#         self.send(text_data=json.dumps({"message": message}))        