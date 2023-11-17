import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
import redis
from django.core.files.base import ContentFile
import base64

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.file_id = self.scope['url_route']['kwargs']['file_id']
        self.room_group_name = f"file_{self.file_id}"
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        
        image_data = data['image']
        x_position = data['x_position']
        y_position = data['y_position']
        
        # Декодирование base64 данных изображения
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        image_content = ContentFile(base64.b64decode(imgstr), name=f'picture.{ext}')
        
        picture_object = PictureObject.objects.create(
            x_position=x_position,
            y_position=y_position
        )
        picture_object.picture = image_content
        
        
        picture_object.save()
        
        File.objects.get(id=self.file_id).picture_objects.add(picture_object)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat.data',
                'x_position': x_position,
                'y_position': y_position,
                'picture_url': picture_object.picture.url,
            }
        )

    def chat_data(self, event):
        # Отправляем сообщение конкретному клиенту
        x_position = event['x_position']
        y_position = event['y_position']
        picture_url = event['picture_url']
        self.send(text_data=json.dumps({
            'x_position': x_position,
            'y_position': y_position,
            'picture_url': picture_url,
        }))
