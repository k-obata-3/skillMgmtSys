import os
from time import time
import traceback
from typing import List
from django.views import View
from rest_framework import status
from rest_framework import exceptions
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from django.db import transaction
from django.db.models import Q

from .module.itemKeyName import Const
from .utils.excelReportWithOpenpyxl import ExcelReportWithOpenpyxl
from .utils.auth import NormalAuthentication, JWTAuthentication
from .utils.jsonEncoder import JsonEncoder
from .utils.utils import Utils

from .models import CareerInfoItem, Project, User, Company, Department, DepartmentRelation, UserInfo, CareerInfo
from .renderers import JSONRenderer
from .serializers import CareerInfoItemSerializer, CareerInfoSerializer, DepartmentRelationSerializer, UserInfoSerializer, UserSerializer
import urllib.parse

"""[ログイン]
    ログイン処理
Returns:
    [Response]: [リクエストのレスポンス]
"""
class Login(APIView):
  authentication_classes = [NormalAuthentication,]
  def post(self, request, *args, **kwargs):
    response = Response()
    # クッキーの残存期間は1日としておく
    response.set_cookie('jwt', request.user, max_age=60 * 60 * 24, httponly=True)
    # response.data = {'token': request.user, 'user': request.auth}
    response.data = {'user': request.auth}
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

    company_id = self.request.GET.get('company_id')
    limit = self.request.GET.get('limit')
    ofset = self.request.GET.get('offset')

    if is_admin is True:
      # 管理者：すべてのユーザを取得
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

    company_id = self.request.GET.get('company_id')
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
          'authority': '管理者' if item.user.authority == 0 else '',
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

"""[経歴情報Dictionary取得]
    ユーザIDで経歴情報をDictionaryで取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class CareerInfoDicRetrieveAPIView(RetrieveAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    user_id = self.request.GET.get('user_id')

    try:
      career_info = CareerInfo.objects.filter(user = user_id)

      result = {
        'career_info_dic': ViewUtil.getCareerInfoDic(career_info)
      }

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '経歴情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[部署情報一覧取得]
    会社IDで部署情報を一覧取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class DepartmentListAPIView(ListAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    company_id = self.request.GET.get('company_id')

    try:
      department = Department.objects.filter(company = company_id).all()
      department_result = []
      for item in department:
        department_result.append({
          'id': item.id,
          'name': item.name,
          'selected': False,
        })
      result = {
        'department': department_result,
      }

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '部署情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[経歴情報一覧取得]
    ユーザIDで経歴情報を一覧取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class CareerInfoListAPIView(ListAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    user_id = self.request.GET.get('user_id')
    limit = self.request.GET.get('limit')
    ofset = self.request.GET.get('offset')

    try:
      total_count = career_info = CareerInfo.objects.filter(user = user_id).count()
      career_info = CareerInfo.objects.filter(user = user_id).all().order_by("start_date")[int(ofset):(int(ofset) + int(limit))]

      result = {
        'careerInfo': career_info,
        'totalCount': total_count
      };

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '経歴情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[経歴情報取得]
    経歴情報IDで経歴情報を取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class CareerInfoRetrieveAPIView(RetrieveAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    career_id = self.request.GET.get('id')

    try:
      career_info = CareerInfo.objects.get(id = career_id)
      key_list = Const.KEY_LIST
      dic = {}
      for key_name in key_list:
        dic[key_name] = CareerInfoItem.objects.filter(key=key_name, career_info_id=career_id).values_list('value', flat=True)

      result = {
        'career_info': career_info,
        'model': dic['model'],
        'os': dic['os'],
        'data_base': dic['data_base'],
        'language': dic['language'],
        'framework': dic['framework'],
        'tool': dic['tool'],
        'incharge': dic['incharge'],
        'role': dic['role'],
        'other': dic['other'][0] if any(dic['other']) else None,
      }

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '経歴情報の取得に失敗しました'
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

    # 管理者ではない場合は認証エラー
    if is_admin is not True:
      msg = "Authorization 無効"
      raise exceptions.AuthenticationFailed(msg)

    try:
      with transaction.atomic():
        user_serializer = UserSerializer(data=request.data)
        user_info_serializer = UserInfoSerializer(data=request.data)
        department_relation_serializer = DepartmentRelationSerializer(data=request.data['department'])
        new_user = None
        if user_serializer.is_valid():
          new_user = user_serializer.save(request.data, login_user)
        else:
          print('【ERROR】:' + user_serializer.error_messages['invalid'])
          raise exceptions

        if user_info_serializer.is_valid():
          user_info_serializer.save(request.data, new_user, login_user)
        else:
          print('【ERROR】:' + user_info_serializer.error_messages['invalid'])
          raise exceptions

        for d in request.data['department']:
          reqData = {
            'user': new_user,
            'depertment': Department.objects.get(id = d),
          }
          department_relation_serializer.save(reqData, login_user)

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
    user_id = self.request.GET.get('user_id')

    # ログインユーザ自身ではないユーザを更新する場合は、管理者権限チェック
    # 管理者ではない場合は認証エラー
    if str(login_user_id) != user_id:
      if is_admin is not True:
        msg = "Authorization 無効"
        raise exceptions.AuthenticationFailed(msg)

    try:
      with transaction.atomic():
        user = User.objects.get(pk = user_id)
        user_info = UserInfo.objects.get(user = user_id)
        department_relation = DepartmentRelation.objects.filter(user = user_id)

        user_info_serializer = UserInfoSerializer(user_info, data=request.data)
        department_relation_serializer = DepartmentRelationSerializer(user_info, data=request.data['department'])

        if user_info_serializer.is_valid():
          user_info_serializer.update(user_info, request.data, login_user)
        else:
          print('【ERROR】:' + user_info_serializer.error_messages['invalid'])
          raise exceptions

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
          raise exceptions

        # 本来は差分データのみを更新するべき
        # 部署リレーション情報は頻繁に更新されることはない想定のため、あらかじめdeleteしてしまう
        department_relation.delete()

        for d in request.data['department']:
          reqData = {
            'user': user_info.user,
            'depertment': Department.objects.get(id = d),
          }
          department_relation_serializer.save(reqData, login_user)

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'ユーザ情報の更新に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[経歴情報登録]
    経歴情報を新規登録
Returns:
    [Response]: [リクエストのレスポンス]
"""
class CareerInfoCreateAPIView(CreateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = CareerInfoSerializer

  def create(self, request):
    try:
      with transaction.atomic():
        serializer = CareerInfoSerializer(data=request.data)
        if serializer.is_valid():
          new_career_info = serializer.save(request.data)
        else:
          print('【ERROR】:' + serializer.error_messages['invalid'])
          raise exceptions

        key_list = Const.KEY_LIST
        for item in key_list:
          if request.data[item] is None:
            continue

          for val in request.data[item].split(','):
            req = {
              'key': item,
              'value': val,
              'user': request.data['user'],
            }
            careerInfoItemSerializer = CareerInfoItemSerializer(data=req)
            if serializer.is_valid():
              careerInfoItemSerializer.save(req, new_career_info)
            else:
              print('【ERROR】:' + serializer.error_messages['invalid'])
              raise exceptions
    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '経歴情報の登録に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[経歴情報更新]
    経歴情報IDで経歴情報を更新
Returns:
    [Response]: [リクエストのレスポンス]
"""
class CareerInfoUpdateAPIView(UpdateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = CareerInfoSerializer

  def update(self, request):
    
    career_id = self.request.GET.get('id')

    try:
      with transaction.atomic():
        career_info = CareerInfo.objects.get(id = career_id)

        serializer = CareerInfoSerializer(career_info, data=request.data)
        if serializer.is_valid():
          serializer.update(career_info, request.data)
        else:
          print('【ERROR】:' + serializer.error_messages['invalid'])
          raise exceptions

        key_list = Const.KEY_LIST
        for item_key in key_list:
          # DBに存在している値
          item_value = CareerInfoItem.objects.filter(career_info_id=career_id, key=item_key).values_list('value', flat=True)
          # リクエストデータの値
          if request.data[item_key] is None:
            req_value = []
          else:
            req_value = request.data[item_key].split(',')

          # リクエストデータの値 - DBに存在している値 = 新規追加データ
          add_value = list(set(req_value) - set(list(item_value)))
          # DBに存在している値 - リクエストデータの値 = 削除対象データ
          del_value = list(set(list(item_value)) - set(req_value))

          # 追加
          for val in add_value:
            req = {
              'key': item_key,
              'value': val,
              'user': request.data['user'],
            }
            careerInfoItemSerializer = CareerInfoItemSerializer(data=req)
            if careerInfoItemSerializer.is_valid():
              careerInfoItemSerializer.save(req, career_info)
            else:
              print('【ERROR】:' + careerInfoItemSerializer.error_messages['invalid'])
              raise exceptions

          # 削除
          for val in del_value:
            del_data = CareerInfoItem.objects.filter(career_info_id=career_id, key=item_key, value=val)
            del_data.delete()
    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '経歴情報の更新に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[経歴情報削除取得]
    経歴情報IDで経歴情報を物理削除
Returns:
    [Response]: [リクエストのレスポンス]
"""
class CareerInfoDestroyAPIView(DestroyAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = CareerInfoSerializer

  def destroy(self, request):
    career_id = self.request.GET.get('id');

    try:
      career_info = CareerInfo.objects.get(id = career_id);
      career_info.delete()

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '経歴情報の削除に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[案件情報取得]
    会社IDで案件情報を取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class ProjectListAPIView(ListAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    company_id = self.request.GET.get('company_id')
    limit = self.request.GET.get('limit')
    ofset = self.request.GET.get('offset')

    try:
      total_count = Project.objects.filter(company = company_id).count()
      project = Project.objects.filter(company = company_id).all().order_by("start_date")[int(ofset):(int(ofset) + int(limit))]

      result = {
        'project': project,
        'totalCount': total_count
      };

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '案件情報の取得に失敗しました'
      return response
    
    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[案件情報取得]
    案件IDで案件情報を取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class ProjectRetrieveAPIView(RetrieveAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    project_id = self.request.GET.get('project_id')

    try:
      project = Project.objects.get(pk = project_id)

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '案件情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(project, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[経歴情報出力処理]
    ユーザの経歴情報をエクセル出力
Returns:
    [Response]: [リクエストのレスポンス]
"""
class CareerInfoOutputAPIView(APIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  def get(self, request):
    user_id = self.request.GET.get('user_id')

    try:
      career_info = CareerInfo.objects.filter(user = user_id).all().order_by("start_date")
      user_info = UserInfo.objects.get(user = user_id)

      career_info_item_dic = {}
      key_list = Const.KEY_LIST
      for info in career_info:
        dic = {}
        for key_name in key_list:
          values = list(CareerInfoItem.objects.filter(key=key_name, career_info_id=info.id).values_list('value', flat=True))
          # カンマ区切りで結合
          dic[key_name] = ','.join(values)
        career_info_item_dic[str(info.id)] = dic

      temp_dir_path = 'temp'
      # os.makedirs(temp_dir_path, exist_ok=True)
      file_name = ExcelReportWithOpenpyxl.write(career_info, career_info_item_dic, user_info, temp_dir_path)
      quoted_filename = urllib.parse.quote(file_name)
      file = open('{0}/{1}'.format(temp_dir_path, file_name), 'rb')

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '経歴情報の取得に失敗しました'
      return response

    response = FileResponse(file)
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(quoted_filename)
    response['Access-Control-Expose-Headers'] = 'content-disposition'
    response.status_code = status.HTTP_200_OK

    return response

"""[経歴情報一覧取得]
    会社IDで経歴情報を一覧取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class CareerInfoAllListAPIView(ListAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    company_id = self.request.GET.get('company_id')

    try:
      career_info = CareerInfo.objects.filter(user__company = company_id, user__state = 1).all()

      db_dic = {}
      lang_dic = {}
      framework_dic = {}
      for info in career_info:
        if(info.start_date is not None and info.end_date is not None):
          period_days = abs(info.start_date - info.end_date)
          db_dic = ViewUtil.getCareerInfoItemDic(Const.KEY_DATA_BASE, db_dic, info, period_days)
          lang_dic = ViewUtil.getCareerInfoItemDic(Const.KEY_LANGUAGE, lang_dic, info, period_days)
          framework_dic = ViewUtil.getCareerInfoItemDic(Const.KEY_FRAMEWORK, framework_dic, info, period_days)

      for key, value in db_dic.items():
        db_dic[key] = value.days

      for key, value in lang_dic.items():
        lang_dic[key] = value.days

      for key, value in framework_dic.items():
        framework_dic[key] = value.days

      # 期間（日）で降順ソート
      db_list = sorted(db_dic.items(), key = lambda item: item[1], reverse = True)
      db_dic.clear()
      db_dic.update(db_list)

      lang_list = sorted(lang_dic.items(), key = lambda item: item[1], reverse = True)
      lang_dic.clear()
      lang_dic.update(lang_list)

      framework_list = sorted(framework_dic.items(), key = lambda item: item[1], reverse = True)
      framework_dic.clear()
      framework_dic.update(framework_list)

      result = {
          'career_info_db': str(db_dic),
          'career_info_lang': str(lang_dic),
          'career_info_framework': str(framework_dic),
      }

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '経歴情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[ViewUtility]
    viewクラス汎用処理
"""
class ViewUtil():

  def getCareerInfoItem(key_name, id):
    if id is None:
      return CareerInfoItem.objects.filter(key = key_name).all()
    else:
      return CareerInfoItem.objects.filter(career_info = id, key = key_name).all()

  def getCareerInfoItemDic(key_name, dic, info, days):
    item = ViewUtil.getCareerInfoItem(key_name, info.id)
    for db in item:
      db_dic_key = db.value.lower()
      if db_dic_key in dic.keys():
        dic[db_dic_key] = dic[db_dic_key] + days
      else:
        dic[db_dic_key] = days
    return dic

  def getCareerInfoDic(career_info):
    db_dic = {}
    lang_dic = {}
    framework_dic = {}
    for info in career_info:
      if(info.start_date is None or info.end_date is None):
        continue
      period_days = abs(info.start_date - info.end_date)
      db_dic = ViewUtil.getCareerInfoItemDic(Const.KEY_DATA_BASE, db_dic, info, period_days)
      lang_dic = ViewUtil.getCareerInfoItemDic(Const.KEY_LANGUAGE, lang_dic, info, period_days)
      framework_dic = ViewUtil.getCareerInfoItemDic(Const.KEY_FRAMEWORK, framework_dic, info, period_days)

    for key, value in db_dic.items():
      db_dic[key] = value.days

    for key, value in lang_dic.items():
      lang_dic[key] = value.days

    for key, value in framework_dic.items():
      framework_dic[key] = value.days

    # 期間（日）で降順ソート
    db_list = sorted(db_dic.items(), key = lambda item: item[1], reverse = True)
    db_dic.clear()
    db_dic.update(db_list)

    lang_list = sorted(lang_dic.items(), key = lambda item: item[1], reverse = True)
    lang_dic.clear()
    lang_dic.update(lang_list)

    framework_list = sorted(framework_dic.items(), key = lambda item: item[1], reverse = True)
    framework_dic.clear()
    framework_dic.update(framework_list)

    return {
      'career_info_db': str(db_dic),
      'career_info_lang': str(lang_dic),
      'career_info_framework': str(framework_dic),
    }
