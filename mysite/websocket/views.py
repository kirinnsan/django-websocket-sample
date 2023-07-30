# chat/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.cache import cache

def index(request):
    return render(request, "websocket/index.html")
  
def room(request, client_id):
    return render(request, "websocket/socket.html", {"client_id":client_id})  
  
def handle_external_request(request):
    if request.method == 'GET':
        
        data = dict(request.GET)
        client_id = data["client_id"][0]
        channel_name =  cache.get(client_id)
        if not channel_name:
          return JsonResponse({'status': 'error', 'message': 'Not exist channel name'})

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(channel_name, {
            "type": "chat.message",
            "text": "Message from another endpoint!",
        })

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
  
 