import traceback
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
import json
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework import exceptions

from ..utils.auth import JWTAuthentication
from ..utils.jsonEncoder import JsonEncoder
from ..models import Department
from ..renderers import JSONRenderer
from ..serializers import DepartmentSerializer

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
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    company_id = login_user.user.company_id

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

"""[部署情報登録]
    部署情報を新規登録
Returns:
    [Response]: [リクエストのレスポンス]
"""
class DepartmentCreateAPIView(CreateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = DepartmentSerializer

  def create(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    company_id = login_user.user.company_id
    is_admin = login_user.is_admin

    # 管理者ではない場合は認証エラー
    if is_admin is not True:
      msg = "Authorization 無効"
      raise exceptions.AuthenticationFailed(msg)

    itemReqData = {
      'id': request.data['id'],
      'name': request.data['name'],
      'company_id': company_id,
    }

    try:
      with transaction.atomic():

        if request.data['id'] is None:
          # 新規
          serializer = DepartmentSerializer(data=itemReqData)
          if serializer.is_valid():
            serializer.save(itemReqData, login_user)
          else:
            print('【ERROR】:' + serializer.error_messages['invalid'])
            raise exceptions.ValidationError("部署情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
          # 更新
          department = Department.objects.get(company = company_id, id = request.data['id'])
          serializer = DepartmentSerializer(department, data=itemReqData)
          if serializer.is_valid():
            serializer.update(department, itemReqData, login_user)
          else:
            print('【ERROR】:' + serializer.error_messages['invalid'])
            raise exceptions.ValidationError("部署情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

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
        response.data = '登録済みの部署情報です'
      else:
        response.data = '部署情報の登録に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[部署情報削除]
    部署IDで部署情報を物理削除
Returns:
    [Response]: [リクエストのレスポンス]
"""
class DepartmentDestroyAPIView(DestroyAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = DepartmentSerializer

  def destroy(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    company_id = login_user.user.company_id
    is_admin = login_user.is_admin

    # 管理者ではない場合は認証エラー
    if is_admin is not True:
      msg = "Authorization 無効"
      raise exceptions.AuthenticationFailed(msg)

    id = self.request.GET.get('id');

    try:
      department = Department.objects.filter(id = id, company = company_id);
      department.delete()

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '部署情報の削除に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response
