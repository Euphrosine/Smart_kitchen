# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FanStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Process the received message as needed
        print(f"Received message: {message}")

        # Send a response back to the WebSocket
        await self.send(text_data=json.dumps({
            'message': 'Message received and processed.'
        }))

    async def fan_status(self, event):
        # Send the status to the WebSocket
        await self.send(text_data=json.dumps({
            'status': event['status']
        }))
