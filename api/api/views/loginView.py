import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions

from api.models import User
from api.serializers import UserSerializer
from ..utils.auth import NormalAuthentication
from ..utils.utils import Utils

"""[ログイン]
    ログイン処理
Returns:
    [Response]: [リクエストのレスポンス]
"""
class Login(APIView):
  authentication_classes = [NormalAuthentication,]
  serializer_class = UserSerializer
  def post(self, request, *args, **kwargs):
    user_id = request.data.get("user_id")
    try:
      # 最終ログイン時間を更新
      user_obj = User.objects.filter(mail_address=user_id).first()
      user_serializer = UserSerializer(data=user_obj)
      user_serializer.updateLoginDateTime(user_obj, Utils.getNow())

      response = Response()
      # クッキーの残存期間は1時間としておく（JWTの有効期間と同値）
      response.set_cookie('jwt', request.user, max_age=60 * 60, httponly=True, samesite="None", secure=True)

      # HTTPのサーバにアップする場合、以下じゃないと認証通らない
      # response.set_cookie('jwt', request.user, max_age=60 * 60, httponly=True)

      response.data = {'user': request.auth}
    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      msg = "ログインに失敗しました"
      raise exceptions.AuthenticationFailed(msg)

    return response
