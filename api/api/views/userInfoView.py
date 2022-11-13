import traceback
import json
import re
from rest_framework import status
from rest_framework import exceptions
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from ..utils.auth import JWTAuthentication
from ..utils.jsonEncoder import JsonEncoder
from ..utils.utils import Utils
from ..models import User, Department, DepartmentRelation, UserInfo
from ..renderers import JSONRenderer
from ..serializers import DepartmentRelationSerializer, UserInfoSerializer, UserSerializer

"""[ログインユーザ情報取得]
    ログインユーザのユーザ情報を取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class SelfUserInfoRetrieveAPIView(RetrieveAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    login_user_id = login_user.user.id
    company_id = login_user.user.company_id

    try:
      user_info = UserInfo.objects.get(user = login_user_id)
      department = Department.objects.filter(company = company_id).all()
      department_relation = DepartmentRelation.objects.select_related('user').filter(user = login_user_id).all()

      department_result = []
      for item in department:
        department_result.append({
          'id': item.id,
          'name': item.name,
          'selected': [True for department in department_relation if department.department_id == item.id],
        })

      for department in department_result:
        if len(department['selected']) == 0:
          department['selected'] = False
        else:
          department['selected'] = department['selected'][0]

      result = {
        'id': user_info.user.id,
        'mail_address': user_info.user.mail_address,
        'password': user_info.user.password,
        'first_name_kana': user_info.first_name_kana,
        'last_name_kana': user_info.last_name_kana,
        'first_name': user_info.first_name,
        'last_name': user_info.last_name,
        'birthday': user_info.birthday,
        'position': user_info.position,
        'authority': user_info.user.authority,
        'state': user_info.user.state,
        'department': department_result,
      }

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'ユーザ情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[ログインユーザ情報更新]
    ログインユーザのユーザ情報を更新
Returns:
    [Response]: [リクエストのレスポンス]
"""
class SelfUserInfoUpdateAPIView(UpdateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = UserSerializer, UserInfoSerializer, DepartmentRelationSerializer

  def update(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    login_user_id = login_user.user.id
    company_id = login_user.user.company_id

    try:
      with transaction.atomic():
        user_info = UserInfo.objects.get(user = login_user_id)
        department_relation = DepartmentRelation.objects.filter(user = login_user_id)

        user_info_serializer = UserInfoSerializer(user_info, data=request.data)
        department_relation_serializer = DepartmentRelationSerializer(user_info, data=request.data['department'])

        if user_info_serializer.is_valid():
          user_info_serializer.update(user_info, request.data, login_user)
        else:
          print('【ERROR】:' + user_info_serializer.error_messages['invalid'])
          raise exceptions.ValidationError("入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 本来は差分データのみを更新するべき
        # 部署リレーション情報は頻繁に更新されることはない想定のため、あらかじめdeleteしてしまう
        department_relation.delete()

        for d in request.data['department']:
          reqData = {
            'user': user_info.user,
            'depertment': Department.objects.get(id = d),
          }
          department_relation_serializer.save(reqData, login_user)

    except exceptions.ValidationError as e:
      response = Response()
      response.status_code = e.args[1]
      response.data = e.args[0]
      return response

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'ユーザ情報の更新に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[ユーザ情報一覧取得]
    会社IDでユーザ情報を一覧取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class UserInfoListAPIView(ListAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    is_admin = login_user.is_admin
    company_id = login_user.user.company_id

    limit = self.request.GET.get('limit')
    ofset = self.request.GET.get('offset')

    if is_admin is True:
      # 管理者：すべてのユーザを取得
      # ログインユーザ自身を含む
      total_count = UserInfo.objects.filter(user__company = company_id).all().count()
      user_info = UserInfo.objects.filter(user__company = company_id).all()[int(ofset):(int(ofset) + int(limit))]
      department_relation = DepartmentRelation.objects.select_related('user').filter(user__company = company_id).all()
    else:
      # メンバー：有効なユーザのみを取得
      # ログインユーザ自身を含む
      total_count = UserInfo.objects.filter(user__company = company_id, user__state = 1).all().count()
      user_info = UserInfo.objects.filter(user__company = company_id, user__state = 1).all()[int(ofset):(int(ofset) + int(limit))]
      department_relation = DepartmentRelation.objects.select_related('user').filter(user__company = company_id, user__state = 1).all()

    department = Department.objects.filter(company = company_id).all()

    try:
      department_result = []
      for item in department_relation:
        department_result.append({
          'id': item.department.id,
          'user_id': item.user.id,
          'name': [department.name for department in department if department.id==item.department.id][0],
        })

      user_info_list = []
      for item in user_info:
        user_info_list.append({
          'id': item.user.id,
          'first_name_kana': item.first_name_kana,
          'first_name_kana': item.first_name_kana,
          'first_name': item.first_name,
          'last_name': item.last_name,
          'age': Utils.getAge(item.birthday),
          'birthday': item.birthday,
          'position': item.position,
          'department': [department for department in department_result if department['user_id'] == item.user.id],
          'authority': item.user.authority,
          'state': item.user.state,
        })

      result = {
        'userInfoList': user_info_list,
        'totalCount': total_count
      }

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'ユーザ情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[ユーザ情報一覧取得]
    会社IDで自身を除いたすべてのユーザ情報を一覧取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class UserInfoExcludeSelfListAPIView(ListAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    company_id = login_user.user.company_id

    limit = self.request.GET.get('limit')
    ofset = self.request.GET.get('offset')

    # ログインユーザ自身は除外
    total_count = UserInfo.objects.filter(user__company = company_id).exclude(id = login_user.id).all().count()
    user_info = UserInfo.objects.filter(user__company = company_id).exclude(id = login_user.id).all()[int(ofset):(int(ofset) + int(limit))]
    department_relation = DepartmentRelation.objects.select_related('user').filter(user__company = company_id).all()

    department = Department.objects.filter(company = company_id).all()

    try:
      department_result = []
      for item in department_relation:
        department_result.append({
          'id': item.department.id,
          'user_id': item.user.id,
          'name': [department.name for department in department if department.id==item.department.id][0],
        })

      user_info_list = []
      for item in user_info:
        user_info_list.append({
          'id': item.user.id,
          'first_name_kana': item.first_name_kana,
          'first_name_kana': item.first_name_kana,
          'first_name': item.first_name,
          'last_name': item.last_name,
          'age': Utils.getAge(item.birthday),
          'birthday': item.birthday,
          'position': item.position,
          'department': [department for department in department_result if department['user_id'] == item.user.id],
          'authority': item.user.authority,
          'state': item.user.state,
          'last_login': item.user.last_login,
        })

      result = {
        'userInfoList': user_info_list,
        'totalCount': total_count
      }

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'ユーザ情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[ユーザ情報取得]
    ユーザIDでユーザ情報を取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class UserInfoRetrieveAPIView(RetrieveAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    user_id = self.request.GET.get('user_id')

    try:
      user_info = UserInfo.objects.get(user = user_id)
      department = Department.objects.filter(company = user_info.user.company_id).all()
      department_relation = DepartmentRelation.objects.select_related('user').filter(user = user_id).all()

      department_result = []
      for item in department:
        department_result.append({
          'id': item.id,
          'name': item.name,
          'selected': [True for department in department_relation if department.department_id == item.id],
        })

      for department in department_result:
        if len(department['selected']) == 0:
          department['selected'] = False
        else:
          department['selected'] = department['selected'][0]

      result = {
        'id': user_info.user.id,
        'mail_address': user_info.user.mail_address,
        'password': user_info.user.password,
        'first_name_kana': user_info.first_name_kana,
        'last_name_kana': user_info.last_name_kana,
        'first_name': user_info.first_name,
        'last_name': user_info.last_name,
        'birthday': user_info.birthday,
        'position': user_info.position,
        'authority': user_info.user.authority,
        'state': user_info.user.state,
        'department': department_result,
      }

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'ユーザ情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[ユーザ情報登録]
    ユーザ情報を新規登録
Returns:
    [Response]: [リクエストのレスポンス]
"""
class UserCreateAPIView(CreateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = UserSerializer, UserInfoSerializer, DepartmentRelationSerializer

  def create(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    is_admin = login_user.is_admin
    company_id = login_user.user.company_id

    # 管理者ではない場合は認証エラー
    if is_admin is not True:
      msg = "Authorization 無効"
      raise exceptions.AuthenticationFailed(msg)

    try:
      with transaction.atomic():
        request.data['company'] = company_id
        # 初期パスワードをセット
        request.data['password'] = Utils.getInitialPasswordHash()

        user_serializer = UserSerializer(data=request.data)
        user_info_serializer = UserInfoSerializer(data=request.data)
        department_relation_serializer = DepartmentRelationSerializer(data=request.data['department'])
        new_user = None
        if user_serializer.is_valid():
          pattern = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
          if not re.match(pattern, request.data['mail_address']):
            raise exceptions.ValidationError("メールアドレスの形式が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

          new_user = user_serializer.save(request.data, login_user, company_id)
        else:
          print('【ERROR】:' + user_info_serializer.error_messages['invalid'])
          # validError = {}
          # for field in user_serializer.errors:
            # validError[field] = user_serializer.errors[field][0]
          raise exceptions.ValidationError("ユーザ情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

        if user_info_serializer.is_valid():
          user_info_serializer.save(request.data, new_user, login_user)
        else:
          print('【ERROR】:' + user_info_serializer.error_messages['invalid'])
          raise exceptions.ValidationError("ユーザ詳細情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

        for d in request.data['department']:
          reqData = {
            'user': new_user,
            'depertment': Department.objects.get(id = d),
          }
          department_relation_serializer.save(reqData, login_user)

    except exceptions.ValidationError as e:
      response = Response()
      response.status_code = e.args[1]
      response.data = e.args[0]
      return response

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'ユーザ情報の登録に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[ユーザ情報更新]
    ユーザIDでユーザ情報を更新
Returns:
    [Response]: [リクエストのレスポンス]
"""
class UserInfoUpdateAPIView(UpdateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = UserSerializer, UserInfoSerializer, DepartmentRelationSerializer

  def update(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    is_admin = login_user.is_admin
    login_user_id = login_user.user.id
    company_id = login_user.user.company_id
    user_id = self.request.GET.get('user_id')

    # ログインユーザ自身ではないユーザを更新する場合は、管理者権限チェック
    # 管理者ではない場合は認証エラー
    if str(login_user_id) != user_id:
      if is_admin is not True:
        msg = "Authorization 無効"
        raise exceptions.AuthenticationFailed(msg)

    try:
      with transaction.atomic():
        user = User.objects.filter(id = user_id, company = company_id).first()
        user_info = UserInfo.objects.get(user = user_id)
        department_relation = DepartmentRelation.objects.filter(user = user_id)

        user_info_serializer = UserInfoSerializer(user_info, data=request.data)
        department_relation_serializer = DepartmentRelationSerializer(user_info, data=request.data['department'])

        if user_info_serializer.is_valid():
          user_info_serializer.update(user_info, request.data, login_user)
        else:
          print('【ERROR】:' + user_info_serializer.error_messages['invalid'])
          raise exceptions.ValidationError("ユーザ情報詳細の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

        userReqData = {
          'company': user.company.id,
          'mail_address': user.mail_address,
          'password': user.password,
          'authority': request.data['authority'],
          'state': request.data['state'],
        }
        user_serializer = UserSerializer(user, data=userReqData)
        if user_serializer.is_valid():
          user_serializer.update(user, request.data, login_user)
        else:
          print('【ERROR】:' + user_serializer.error_messages['invalid'])
          raise exceptions.ValidationError("ユーザ情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 本来は差分データのみを更新するべき
        # 部署リレーション情報は頻繁に更新されることはない想定のため、あらかじめdeleteしてしまう
        department_relation.delete()

        for d in request.data['department']:
          reqData = {
            'user': user_info.user,
            'depertment': Department.objects.get(id = d),
          }
          department_relation_serializer.save(reqData, login_user)

    except exceptions.ValidationError as e:
      response = Response()
      response.status_code = e.args[1]
      response.data = e.args[0]
      return response

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'ユーザ情報の更新に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[パスワード初期化]
    パスワードを初期化
Returns:
    [Response]: [リクエストのレスポンス]
"""
class PasswordResetAPIView(UpdateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = UserSerializer, UserInfoSerializer, DepartmentRelationSerializer

  def update(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    is_admin = login_user.is_admin
    login_user_id = login_user.user.id
    company_id = login_user.user.company_id
    user_id = self.request.GET.get('user_id')

    # ログインユーザ自身ではないユーザを更新する場合は、管理者権限チェック
    # 管理者ではない場合は認証エラー
    if str(login_user_id) != user_id:
      if is_admin is not True:
        msg = "Authorization 無効"
        raise exceptions.AuthenticationFailed(msg)

    try:
      with transaction.atomic():
        user = User.objects.filter(id = user_id, company = company_id).first()
        hashPass = Utils.getInitialPasswordHash()
        user_serializer = UserSerializer(user)
        user_serializer.passwordUpdate(user, hashPass, login_user)

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'パスワードの初期化に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[ログインユーザパスワード更新]
    ログインユーザのパスワードを更新
Returns:
    [Response]: [リクエストのレスポンス]
"""
class PasswordUpdateAPIView(UpdateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = UserSerializer, UserInfoSerializer, DepartmentRelationSerializer

  def update(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    is_admin = login_user.is_admin
    login_user_id = login_user.user.id
    company_id = login_user.user.company_id

    try:
      with transaction.atomic():
        current_password = request.data['current_password']
        new_password = request.data['new_password']

        user = User.objects.filter(id = login_user_id, company = company_id).first()
        if user.password != Utils.getPasswordHash(current_password) or new_password is None:
          raise exceptions.ValidationError("入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

        hashPass = Utils.getPasswordHash(new_password)
        user_serializer = UserSerializer(user)
        user_serializer.passwordUpdate(user, hashPass, login_user)

    except exceptions.ValidationError as e:
      response = Response()
      response.status_code = e.args[1]
      response.data = e.args[0]
      return response

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'パスワードの変更に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response
