from django.conf.urls import url
from api.views import loginView, userInfoView, careerInfoView, departmentView, projectView, masterItemView

app_name = 'api'
urlpatterns = [
  # ログイン
  url(r'login/$', loginView.Login.as_view()),

  # 部署情報一覧取得
  url(r'^departmentList/$', departmentView.DepartmentListAPIView.as_view()),
  # 部署情報登録
  url(r'^departmentCreate', departmentView.DepartmentCreateAPIView.as_view()),
  # 部署情報削除
  url(r'^departmentDestroy/$', departmentView.DepartmentDestroyAPIView.as_view()),

  # ログインユーザ情報取得
  url(r'^selfUserInfoRetrieve/$', userInfoView.SelfUserInfoRetrieveAPIView.as_view()),
  # ログインユーザ情報更新
  url(r'^selfUserInfoUpdate/$', userInfoView.SelfUserInfoUpdateAPIView.as_view()),
  # ユーザ情報一覧取得
  url(r'^userInfoList/$', userInfoView.UserInfoListAPIView.as_view()),
  # ユーザ情報（自身を除く）一覧取得
  url(r'^userInfoExcludeSelfList/$', userInfoView.UserInfoExcludeSelfListAPIView.as_view()),
  # ユーザ情報取得
  url(r'^userInfoRetrieve/$', userInfoView.UserInfoRetrieveAPIView.as_view()),
  # ユーザ情報登録
  url(r'^userCreate', userInfoView.UserCreateAPIView.as_view()),
  # ユーザ情報更新
  url(r'^userInfoUpdate/$', userInfoView.UserInfoUpdateAPIView.as_view()),
  # パスワード初期化
  url(r'^passwordReset/$', userInfoView.PasswordResetAPIView.as_view()),
  # ログインユーザパスワード更新
  url(r'^passwordUpdate/$', userInfoView.PasswordUpdateAPIView.as_view()),

  # 経歴情報Dictionary取得
  url(r'^careerInfoDicRetrieve/$', careerInfoView.CareerInfoDicRetrieveAPIView.as_view()),
  # 経歴情報一覧取得
  url(r'^careerInfoList/$', careerInfoView.CareerInfoListAPIView.as_view()),
  # 経歴情報一覧取得
  url(r'^careerInfoAllList/$', careerInfoView.CareerInfoAllListAPIView.as_view()),
  # 経歴情報取得
  url(r'^careerInfoRetrieve/$', careerInfoView.CareerInfoRetrieveAPIView.as_view()),
  # 経歴情報登録
  url(r'^careerInfoCreate', careerInfoView.CareerInfoCreateAPIView.as_view()),
  # 経歴情報更新
  url(r'^careerInfoUpdate/$', careerInfoView.CareerInfoUpdateAPIView.as_view()),
  # 経歴情報削除
  url(r'^careerInfoDestroy/$', careerInfoView.CareerInfoDestroyAPIView.as_view()),
  # 経歴情報出力処理
  url(r'^careerInfoOutput/$', careerInfoView.CareerInfoOutputAPIView.as_view()),

  # 案件情報一覧取得
  url(r'^projectList/$', projectView.ProjectListAPIView.as_view()),
  # 案件情報取得
  url(r'^projectRetrieve/$', projectView.ProjectRetrieveAPIView.as_view()),
  # 案件情報登録
  url(r'^projectCreate', projectView.ProjectCreateAPIView.as_view()),
  # 案件情報更新
  url(r'^projectUpdate/$', projectView.ProjectUpdateAPIView.as_view()),
  # 案件情報削除
  url(r'^projectDestroy/$', projectView.ProjectDestroyAPIView.as_view()),

  # マスタ項目情報一覧取得
  url(r'^masterItemList/$', masterItemView.MasterItemListAPIView.as_view()),
  # マスタ項目情報一覧取得
  url(r'^masterItemAllList/$', masterItemView.MasterItemAllListAPIView.as_view()),
  # マスタ項目情報登録
  url(r'^masterItemCreate', masterItemView.MasterItemCreateAPIView.as_view()),
  # マスタ項目情報削除
  url(r'^masterItemDestroy/$', masterItemView.MasterItemDestroyAPIView.as_view()),
]

