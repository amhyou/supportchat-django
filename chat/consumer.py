import json

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        stream = self.scope["url_route"]["kwargs"]["stream"]
        port = str(self.scope["client"][1])
        await self.channel_layer.group_add(
            'admin' if stream=="admin" else port,
            self.channel_name
        )
        await self.accept()
        
        if stream!="admin":
            await self.channel_layer.group_send(
                'admin',
                {
                    "type":"chat_message",
                    'from':port,
                    "do":"new"
                }
            )

    async def receive(self, text_data):
        event = json.loads(text_data)
        print(str(self.scope["client"][1]))
        await self.channel_layer.group_send(
                event.get("to",""),
            {
                'type':"chat_message",
                'msg':event.get("msg"),
                'from':str(self.scope["client"][1]),
                "do":"msg"
                
            })
        
        
    async def chat_message(self, event):
        await self.send(json.dumps(event))

    async def disconnect(self, message):
        stream = self.scope["url_route"]["kwargs"]["stream"]
        
        if stream!="admin":
            await self.channel_layer.group_discard(
                str(self.scope["client"][1]),
                self.channel_name
            )
            await self.channel_layer.group_send(
                'admin',
                {
                    "type":"chat_message",
                    'from':str(self.scope["client"][1]),
                    "do":"old"
                }
            )
        else:
            await self.channel_layer.group_discard(
                'admin',
                self.channel_name
            )
