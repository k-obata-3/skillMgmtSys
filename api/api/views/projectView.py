import traceback
from rest_framework import status
from rest_framework import exceptions
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
import json
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from api.serializers import ProjectSerializer

from ..utils.auth import JWTAuthentication
from ..utils.jsonEncoder import JsonEncoder
from ..models import Project
from ..renderers import JSONRenderer

"""[案件情報一覧取得]
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

"""[案件情報登録]
    案件情報を新規登録
Returns:
    [Response]: [リクエストのレスポンス]
"""
class ProjectCreateAPIView(CreateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = ProjectSerializer

  def create(self, request):
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    projectReqData = {
      'company_id': login_user.user.company.id,
      'name': request.data['name'],
      'overview': request.data['overview'],
      'start_date': request.data['start_date'],
      'end_date': request.data['end_date'],
    }

    try:
      with transaction.atomic():
        serializer = ProjectSerializer(data=projectReqData)
        if serializer.is_valid():
          new_project = serializer.save(projectReqData, login_user)
        else:
          print('【ERROR】:' + serializer.error_messages['invalid'])
          raise exceptions.ValidationError("案件情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

    except exceptions.ValidationError as e:
      response = Response()
      response.status_code = e.args[1]
      response.data = e.args[0]
      return response

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '案件情報の登録に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[案件情報更新]
    案件情報IDで案件情報を更新
Returns:
    [Response]: [リクエストのレスポンス]
"""
class ProjectUpdateAPIView(UpdateAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = ProjectSerializer

  def update(self, request):
    project_id = self.request.GET.get('id')
    # 認証情報からユーザと権限を取得
    login_user = self.request.user
    projectReqData = {
      'company_id': login_user.user.company.id,
      'name': request.data['name'],
      'overview': request.data['overview'],
      'start_date': request.data['start_date'],
      'end_date': request.data['end_date'],
    }

    try:
      with transaction.atomic():
        project = Project.objects.get(id = project_id)

        serializer = ProjectSerializer(project, data=projectReqData)
        if serializer.is_valid():
          serializer.update(project, projectReqData, login_user)
        else:
          print('【ERROR】:' + serializer.error_messages['invalid'])
          raise exceptions.ValidationError("案件情報の入力内容が不正です", status.HTTP_422_UNPROCESSABLE_ENTITY)

    except exceptions.ValidationError as e:
      response = Response()
      response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
      response.data = e.args[0]
      return response

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '案件情報の更新に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response

"""[案件情報削除]
    案件情報IDで案件情報を物理削除
Returns:
    [Response]: [リクエストのレスポンス]
"""
class ProjectDestroyAPIView(DestroyAPIView):
  authentication_classes = [JWTAuthentication, ]
  permission_classes = [IsAuthenticated, ]

  renderer_classes = (JSONRenderer, )
  serializer_class = ProjectSerializer

  def destroy(self, request):
    project_id = self.request.GET.get('id');

    try:
      project = Project.objects.get(id = project_id);
      project.delete()

    except Exception as e:
      print('【ERROR】:' + traceback.format_exc())
      response = Response()
      response.status_code = status.HTTP_400_BAD_REQUEST
      response.data = '案件情報の削除に失敗しました'
      return response

    response = Response()
    response.status_code = status.HTTP_200_OK
    return response
