import traceback
from rest_framework import status
from rest_framework import exceptions
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
import json
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from ..utils.auth import JWTAuthentication
from ..utils.jsonEncoder import JsonEncoder
from ..module.itemKeyName import Const

from ..models import MasterItem
from ..renderers import JSONRenderer
from ..serializers import MasterItemSerializer

"""[マスタ項目情報一覧取得]
    会社IDでマスタ項目情報を一覧取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class MasterItemListAPIView(ListAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    company_id = self.request.GET.get('company_id')
    key = self.request.GET.get('key')

    try:
      master = MasterItem.objects.filter(company = company_id, key = key).all()
      master_result = []
      for item in master:
        master_result.append({
          'id': item.id,
          'key': item.key,
          'name': item.value,
        })

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'マスタ情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(master_result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[マスタ項目情報一覧取得]
    会社IDでマスタ項目情報を一覧取得
Returns:
    [Response]: [リクエストのレスポンス]
"""
class MasterItemAllListAPIView(ListAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )

  def get(self, request):
    company_id = self.request.GET.get('company_id')

    try:
      key_list = Const.KEY_LIST
      dic = {}
      for key_name in key_list:
        dic[key_name] = MasterItem.objects.filter(company = company_id, key = key_name).values_list('value', flat=True)

      result = {
        Const.KEY_MODEL: dic[Const.KEY_MODEL],
        Const.KEY_OS: dic[Const.KEY_OS],
        Const.KEY_TOOL: dic[Const.KEY_TOOL],
        Const.KEY_DATA_BASE: dic[Const.KEY_DATA_BASE],
        Const.KEY_LANGUAGE: dic[Const.KEY_LANGUAGE],
        Const.KEY_FRAMEWORK: dic[Const.KEY_FRAMEWORK],
      }

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'マスタ情報の取得に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    response.data = json.dumps(result, ensure_ascii = False, cls = JsonEncoder)
    return response

"""[マスタ項目情報登録]
    マスタ項目情報を新規登録
Returns:
    [Response]: [リクエストのレスポンス]
"""
class MasterItemCreateAPIView(CreateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = MasterItemSerializer

  def create(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    itemReqData = {
      'id': request.data['id'],
      'key': request.data['key'],
      'value': request.data['name'],
      'company_id': login_user.user.company.id,
    }

    try:
      with transaction.atomic():

        if request.data['id'] is None:
          # 新規
          serializer = MasterItemSerializer(data=itemReqData)
          if serializer.is_valid():
            serializer.save(itemReqData, login_user)
          else:
            print('【ERROR】:' + serializer.error_messages['invalid'])
            raise exceptions.ValidationError("マスタ項目情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
          # 更新
          master_item = MasterItem.objects.get(company = login_user.user.company.id, id = request.data['id'])
          serializer = MasterItemSerializer(master_item, data=itemReqData)
          if serializer.is_valid():
            serializer.update(master_item, itemReqData, login_user)
          else:
            print('【ERROR】:' + serializer.error_messages['invalid'])
            raise exceptions.ValidationError("マスタ項目情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

    except exceptions.ValidationError as e:
      response = Response()
      response.status_code = e.args[1]
      response.data = e.args[0]
      return response

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      if(e.args[0] == 1062):
        response.data = '登録済みのマスタ項目情報です'
      else:
        response.data = 'マスタ項目情報の登録に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[マスタ項目情報削除]
    マスタ項目情報IDでマスタ項目情報を物理削除
Returns:
    [Response]: [リクエストのレスポンス]
"""
class MasterItemDestroyAPIView(DestroyAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = MasterItemSerializer

  def destroy(self, request):
    master_id = self.request.GET.get('id');

    try:
      masterItem = MasterItem.objects.get(id = master_id);
      masterItem.delete()

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = 'マスタ項目情報の削除に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response