import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.file_id = self.scope['url_route']['kwargs']['file_id']
        self.room_group_name = self.file_id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    def chat_message(self, event):
        # Отправляем сообщение конкретному клиенту
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))