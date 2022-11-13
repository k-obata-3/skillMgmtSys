import traceback
import json
import glob
import os
from rest_framework import status
from rest_framework import exceptions
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from django.db import transaction

from ..module.itemKeyName import Const
from ..utils.excelReportWithOpenpyxl import ExcelReportWithOpenpyxl
from ..utils.auth import JWTAuthentication
from ..utils.jsonEncoder import JsonEncoder

from ..models import CareerInfoItem, UserInfo, CareerInfo
from ..renderers import JSONRenderer
from ..serializers import CareerInfoItemSerializer, CareerInfoSerializer
import urllib.parse

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
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    company_id = login_user.user.company_id

    user_id = self.request.GET.get('user_id')

    try:
      career_info = CareerInfo.objects.filter(user = user_id, user__company = company_id)
      career_info_item = CareerInfoItem.objects.filter(career_info__user = user_id).all()

      result = {
        'career_info_dic': ViewUtil.getCareerInfoDic(career_info, career_info_item)
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
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    login_user_id = login_user.user.id
    company_id = login_user.user.company_id
    user_id = self.request.GET.get('user_id')

    # ログインユーザ自身ではない場合は認証エラー
    if str(login_user_id) != user_id:
      msg = "Authorization 無効"
      raise exceptions.AuthenticationFailed(msg)

    limit = self.request.GET.get('limit')
    ofset = self.request.GET.get('offset')

    try:
      total_count = career_info = CareerInfo.objects.filter(user = user_id, user__company = company_id).count()
      career_info = CareerInfo.objects.filter(user = user_id, user__company = company_id).all().order_by("start_date")[int(ofset):(int(ofset) + int(limit))]

      result = {
        'careerInfo': career_info,
        'totalCount': total_count
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
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    company_id = login_user.user.company_id
    login_user_id = login_user.user.id

    career_id = self.request.GET.get('id')

    try:
      career_info = CareerInfo.objects.filter(id = career_id, user = login_user_id, user__company = company_id).first()

      key_list = Const.KEY_LIST
      dic = {}
      for key_name in key_list:
        dic[key_name] = CareerInfoItem.objects.filter(key=key_name, career_info_id=career_id).values_list('value', flat=True)

      result = {
        'career_info': career_info,
        Const.KEY_MODEL: dic[Const.KEY_MODEL],
        Const.KEY_OS: dic[Const.KEY_OS],
        Const.KEY_DATA_BASE: dic[Const.KEY_DATA_BASE],
        Const.KEY_LANGUAGE: dic[Const.KEY_LANGUAGE],
        Const.KEY_FRAMEWORK: dic[Const.KEY_FRAMEWORK],
        Const.KEY_TOOL: dic[Const.KEY_TOOL],
        Const.KEY_INCHARGE: dic[Const.KEY_INCHARGE],
        Const.KEY_ROLE: dic[Const.KEY_ROLE],
        Const.KEY_OTHER: dic[Const.KEY_OTHER][0] if any(dic[Const.KEY_OTHER]) else None,
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
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    login_user_id = login_user.user.id
    user_id = request.data['user']

    # ログインユーザ自身ではない場合は認証エラー
    if str(login_user_id) != user_id:
      msg = "Authorization 無効"
      raise exceptions.AuthenticationFailed(msg)

    try:
      with transaction.atomic():
        serializer = CareerInfoSerializer(data=request.data)
        if serializer.is_valid():
          new_career_info = serializer.save(request.data)
        else:
          print('【ERROR】:' + serializer.error_messages['invalid'])
          raise exceptions.ValidationError("経歴情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

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
              raise exceptions.ValidationError("経歴詳細情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

    except exceptions.ValidationError as e:
      response = Response()
      response.status_code = e.args[1]
      response.data = e.args[0]
      return response

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
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    login_user_id = login_user.user.id
    user_id = request.data['user']

    # ログインユーザ自身ではない場合は認証エラー
    if str(login_user_id) != user_id:
      msg = "Authorization 無効"
      raise exceptions.AuthenticationFailed(msg)

    try:
      with transaction.atomic():
        career_id = request.data['careerId']
        career_info = CareerInfo.objects.get(id = career_id)

        serializer = CareerInfoSerializer(career_info, data=request.data)
        if serializer.is_valid():
          serializer.update(career_info, request.data)
        else:
          print('【ERROR】:' + serializer.error_messages['invalid'])
          raise exceptions.ValidationError("経歴情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

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
              raise exceptions.ValidationError("経歴詳細情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

          # 削除
          for val in del_value:
            del_data = CareerInfoItem.objects.filter(career_info_id=career_id, key=item_key, value=val)
            del_data.delete()

    except exceptions.ValidationError as e:
      response = Response()
      response.status_code = e.args[1]
      response.data = e.args[0]
      return response

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '経歴情報の更新に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[経歴情報削除]
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
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    login_user_id = login_user.user.id

    career_id = self.request.GET.get('id')

    try:
      career_info = CareerInfo.objects.get(id = career_id)

      # ログインユーザ自身ではない場合は認証エラー
      if login_user_id != career_info.user.id:
        msg = "Authorization 無効"
        raise exceptions.AuthenticationFailed(msg)

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

"""[経歴情報出力処理]
    ユーザの経歴情報をエクセル出力
Returns:
    [Response]: [リクエストのレスポンス]
"""
class CareerInfoOutputAPIView(APIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  def get(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    is_admin = login_user.is_admin
    login_user_id = login_user.user.id
    company_id = login_user.user.company_id
    user_id = self.request.GET.get('user_id')

    # ログインユーザ自身ではないユーザの経歴情報を出力する場合は、管理者権限チェック
    # 管理者ではない場合は認証エラー
    if str(login_user_id) != user_id:
      if is_admin is not True:
        msg = "Authorization 無効"
        raise exceptions.AuthenticationFailed(msg)

    try:
      career_info = CareerInfo.objects.filter(user = user_id, user__company = company_id).all().order_by("start_date")
      user_info = UserInfo.objects.get(user = user_id, user__company = company_id)

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
      # 前方一致で前回作成したファイルを削除
      for file in glob.glob(os.getcwd() + '/' + temp_dir_path + '/スキル表_' + user_info.last_name + user_info.first_name + '*'):
        os.remove(file)

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
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    company_id = login_user.user.company_id

    try:
      career_info = CareerInfo.objects.filter(user__company = company_id, user__state = 1).all()
      career_info_item = CareerInfoItem.objects.filter(career_info__user__company = company_id, career_info__user__state = 1).all()

      db_dic = {}
      lang_dic = {}
      framework_dic = {}
      for info in career_info:
        if(info.start_date is not None and info.end_date is not None):
          period_days = abs(info.start_date - info.end_date)
          db_dic = ViewUtil.getCareerInfoItemPointDic(Const.KEY_DATA_BASE, db_dic, info, career_info_item, period_days)
          lang_dic = ViewUtil.getCareerInfoItemPointDic(Const.KEY_LANGUAGE, lang_dic, info, career_info_item, period_days)
          framework_dic = ViewUtil.getCareerInfoItemPointDic(Const.KEY_FRAMEWORK, framework_dic, info, career_info_item, period_days)

      for key, value in db_dic.items():
        db_dic[key] = value

      for key, value in lang_dic.items():
        lang_dic[key] = value

      for key, value in framework_dic.items():
        framework_dic[key] = value

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

  # def getCareerInfoItem(key_name, id):
  #   if id is None:
  #     return CareerInfoItem.objects.filter(key = key_name).all()
  #   else:
  #     return CareerInfoItem.objects.filter(career_info = id, key = key_name).all()

  # def getCareerInfoItemDic(key_name, dic, info, days):
  #   item = ViewUtil.getCareerInfoItem(key_name, info.id)
  #   for db in item:
  #     db_dic_key = db.value
  #     if db_dic_key in dic.keys():
  #       dic[db_dic_key] = dic[db_dic_key] + days
  #     else:
  #       dic[db_dic_key] = days
  #   return dic

  def getCareerInfoItemPointDic(key_name, dic, info, career_info_item, days):
    item = filter(lambda item: item.career_info.id == info.id and item.key == key_name, career_info_item)
    for i in item:
      db_dic_key = i.value
      dayInt = days.days
      point = 0
      if dayInt < 180:
        # 半年未満
        point = 1
      elif dayInt < 365:
        # 1年未満
        point = 2
      elif dayInt < 365 * 3:
        # 3年未満
        point = 3
      elif dayInt < 365 * 5:
        # 5年未満
        point = 4
      elif dayInt < 365 * 10:
        # 10年未満
        point = 5
      elif dayInt < 365 * 20:
        # 20年未満
        point = 6
      else:
        point = 7

      if db_dic_key in dic.keys():
        dic[db_dic_key] = dic[db_dic_key] + point
      else:
        dic[db_dic_key] = point
    return dic

  def getCareerInfoItemDic(key_name, dic, info, career_info_item, days):
    item = filter(lambda item: item.career_info.id == info.id and item.key == key_name, career_info_item)
    for i in item:
      db_dic_key = i.value
      if db_dic_key in dic.keys():
        dic[db_dic_key] = dic[db_dic_key] + days
      else:
        dic[db_dic_key] = days
    return dic


  def getCareerInfoDic(career_info, career_info_item):
    db_dic = {}
    lang_dic = {}
    framework_dic = {}
    for info in career_info:
      if(info.start_date is None or info.end_date is None):
        continue
      period_days = abs(info.start_date - info.end_date)
      db_dic = ViewUtil.getCareerInfoItemDic(Const.KEY_DATA_BASE, db_dic, info, career_info_item, period_days)
      lang_dic = ViewUtil.getCareerInfoItemDic(Const.KEY_LANGUAGE, lang_dic, info, career_info_item, period_days)
      framework_dic = ViewUtil.getCareerInfoItemDic(Const.KEY_FRAMEWORK, framework_dic, info, career_info_item, period_days)

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
