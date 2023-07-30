import json
from django.core.cache import cache
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.client_id = self.scope["url_route"]["kwargs"]["client_id"]
        print(self.client_id)
        cache.set(self.client_id, self.channel_name)
        value = cache.get(self.client_id)
        print(value)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.send(text_data=json.dumps({"message": message}))

    def chat_message(self, event):
        print(event)
        self.send(text_data=json.dumps({"message": event["text"]}))