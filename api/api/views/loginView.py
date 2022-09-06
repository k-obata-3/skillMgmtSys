from rest_framework.response import Response
from rest_framework.views import APIView
from ..utils.auth import NormalAuthentication

"""[ログイン]
    ログイン処理
Returns:
    [Response]: [リクエストのレスポンス]
"""
class Login(APIView):
  authentication_classes = [NormalAuthentication,]
  def post(self, request, *args, **kwargs):
    response = Response()
    # クッキーの残存期間は1時間としておく（JWTの有効期間と同値）
    # response.set_cookie('jwt', request.user, max_age=60 * 60, httponly=True, samesite="None", secure=True)

    # HTTPのサーバにアップする場合、以下じゃないと認証通らない
    response.set_cookie('jwt', request.user, max_age=60 * 60, httponly=True)

    # response.data = {'token': request.user, 'user': request.auth}
    response.data = {'user': request.auth}
    return response
