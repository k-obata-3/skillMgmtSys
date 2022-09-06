import time
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from .utils import Utils
from api.models import User
from api.models import UserInfo

# SHA256でmediaproから生成
SECRET_KEY = 'aa785c482395933b5fa6535b976653894a10b258209f7f5c43416129a6249774'

class NormalAuthentication(BaseAuthentication):
  def authenticate(self, request):
    user_id = request.data.get("user_id")
    password = request.data.get("password")
    # 停止ユーザは照合対象外
    user_obj = User.objects.filter(mail_address=user_id, state=1).first()
    if not user_obj:
      raise exceptions.AuthenticationFailed('認証失敗')
    elif user_obj.password != password:
      raise exceptions.AuthenticationFailed('パスワードあってません')
    user_info_obj = UserInfo.objects.filter(user=user_obj.id).first()
    token = generate_jwt(user_obj)

    user_info = {
      'id': user_obj.pk,
      'mail_address': user_obj.mail_address,
      'company_id': user_obj.company_id,
      'auth': user_obj.authority,
      'first_name': user_info_obj.first_name,
      'last_name': user_info_obj.last_name,
    }

    return ('jwt ' + token, user_info)

  def authenticate_header(self, request):
    pass

# ドキュメント: https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=exp
def generate_jwt(user):

  # 有効期間を1時間に設定
  timestamp = int(time.time()) + 60 * 60
  return jwt.encode(
    {
      "user_id": user.pk,
      "company_id": user.company_id,
      "authority": user.authority,
      "exp": timestamp,
    },
    SECRET_KEY).decode("utf-8")

class JWTAuthentication(BaseAuthentication):
  keyword = 'JWT'
  model = None

  def authenticate(self, request):
    # auth = rest_framework.authentication.get_authorization_header(request).split()
    req_jwt = request.COOKIES.get('jwt')
    auth = None
    # cookieが取得できた場合、splitしてJWTを取り出す
    if req_jwt:
      auth = req_jwt.split()

    # 認証情報取得失敗 or プレフィックス不一致
    if auth is None or auth[0].lower() != self.keyword.lower():
      msg = "認証情報取得失敗"
      raise exceptions.AuthenticationFailed(msg)

    if len(auth) == 1 or len(auth) > 2:
      msg = "認証情報不正"
      raise exceptions.AuthenticationFailed(msg)

    try:
      jwt_token = auth[1]
      # decode時に有効期間が自動検証されるので自前検証不要
      jwt_info = jwt.decode(jwt_token, SECRET_KEY)

      user_id = jwt_info.get("user_id")
      try:
        user = UserInfo.objects.get(user=user_id)
        user.is_authenticated = True

        # 権限チェック
        user.is_admin = True if user.user.authority == 0 else False

        return (user, jwt_token)
      except:
        msg = "認証失敗"
        raise exceptions.AuthenticationFailed(msg)
    except jwt.ExpiredSignatureError:
      msg = "有効期間超過"
      raise exceptions.AuthenticationFailed(msg)

  def authenticate_header(self, request):
    pass
