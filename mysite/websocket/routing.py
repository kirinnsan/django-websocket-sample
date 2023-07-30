from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # as_asgi() クラスメソッドを呼び出して、
    # ユーザ接続ごとにコンシューマのインスタンスを生成する ASGI アプリケーションを取得します
    re_path(r"ws/socket/(?P<client_id>\w+)/$", consumers.ChatConsumer.as_asgi())
]
