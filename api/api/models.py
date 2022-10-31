from django.db import models
from django.forms.models import model_to_dict

class BaseModel(models.Model):
  class Meta:
    # マイグレーション時にテーブルを作成しないModelは以下のオプションが必要
    abstract = True

  # バージョン
  version = models.BigIntegerField(default=1, blank=False, null=False)
  # 登録日時
  add_date = models.DateTimeField(auto_now_add=True, null=True)
  # 登録者
  add_user = models.BigIntegerField(blank=False, null=False)
  # 更新日時
  ud_date = models.DateTimeField(auto_now=True, null=True)
  # 更新者
  ud_user = models.BigIntegerField(blank=False, null=False)

  def to_dict(self):
    return model_to_dict(self)

""" 会社モデル """
class Company(BaseModel):
  class Meta:
    db_table = "company"

  # ID
  id = models.BigAutoField(primary_key=True)
  # 会社名
  name = models.CharField(blank=False, null=False, max_length=50)

""" ユーザモデル """
class User(BaseModel):
  class Meta:
    db_table = "user"

  # ID
  id = models.BigAutoField(primary_key=True)
  # 会社ID
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  # メールアドレス
  mail_address = models.CharField(blank=False, null=False, max_length=255)
  # パスワード
  password = models.CharField(blank=True, null=True, max_length=50)
  # 権限
  authority = models.BigIntegerField(blank=True, null=True, default=0)
  # 状態
  state = models.BigIntegerField(blank=True, null=True, default=1)
  # 最終ログイン
  last_login = models.DateTimeField(blank=True, null=True)

""" ユーザ情報モデル """
class UserInfo(BaseModel):
  class Meta:
    db_table = "user_info"

  # ID
  id = models.BigAutoField(primary_key=True)
  # ユーザID
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # 名カナ
  first_name_kana = models.CharField(blank=False, null=False, max_length=20)
  # 姓カナ
  last_name_kana = models.CharField(blank=False, null=False, max_length=20)
  # 名
  first_name = models.CharField(blank=False, null=False, max_length=10)
  # 姓
  last_name = models.CharField(blank=False, null=False, max_length=10)
  # 生年月日
  birthday = models.DateTimeField(blank=False, null=False)
  # 役職
  position = models.CharField(blank=True, null=True, max_length=50)

""" 経歴情報モデル """
class CareerInfo(BaseModel):
  class Meta:
    db_table = "career_info"

  # ID
  id = models.BigAutoField(primary_key=True)
  # ユーザID
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # 案件名
  project_name = models.CharField(blank=False, null=False, max_length=50)
  # 概要
  overview = models.CharField(blank=True, null=True, max_length=100)
  # 開始年月日
  start_date = models.DateTimeField(blank=True, null=True)
  # 終了年月日
  end_date = models.DateTimeField(blank=True, null=True)

""" 部署モデル """
class Department(BaseModel):
  class Meta:
    db_table = "department"
    constraints = [models.UniqueConstraint(fields=["company", "name"], name="department_unique")]

  # ID
  id = models.BigAutoField(primary_key=True)
  # 会社ID
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  # 部署名
  name = models.CharField(blank=False, null=False, max_length=50)

""" 部署リレーションモデル """
class DepartmentRelation(BaseModel):
  class Meta:
    db_table = "department_relation"

  # 部署ID
  department = models.ForeignKey(Department, on_delete=models.CASCADE)
  # ユーザID
  user = models.ForeignKey(User, on_delete=models.CASCADE)

""" 案件モデル """
class Project(BaseModel):
  class Meta:
    db_table = "project"

  # ID
  id = models.BigAutoField(primary_key=True)
  # 会社ID
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  # 案件名
  name = models.CharField(blank=False, null=False, max_length=50)
  # 概要
  overview = models.CharField(blank=True, null=True, max_length=100)
  # 開始年月日
  start_date = models.DateTimeField(blank=True, null=True)
  # 終了年月日
  end_date = models.DateTimeField(blank=True, null=True)

""" 案件リレーションモデル """
class ProjectRelation(BaseModel):
  class Meta:
    db_table = "project_relation"

  # 案件ID
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  # ユーザID
  user = models.ForeignKey(User, on_delete=models.CASCADE)

""" 経歴情報項目モデル """
class CareerInfoItem(BaseModel):
  class Meta:
    db_table = "career_info_item"

  # 経歴情報ID
  career_info = models.ForeignKey(CareerInfo, on_delete=models.CASCADE)
  # キー
  key = models.CharField(blank=False, null=False, max_length=50)
  # 値
  value = models.CharField(blank=False, null=False, max_length=100)

""" 案件情報項目モデル """
class ProjectInfoItem(BaseModel):
  class Meta:
    db_table = "project_info_item"

  # 案件情報ID
  project_info = models.ForeignKey(Project, on_delete=models.CASCADE)
  # キー
  key = models.CharField(blank=False, null=False, max_length=50)
  # 値
  value = models.CharField(blank=False, null=False, max_length=100)

""" マスタ項目モデル """
class MasterItem(BaseModel):
  class Meta:
    db_table = "master_item"
    constraints = [models.UniqueConstraint(fields=["company", "key", "value"], name="master_unique")]

  # 会社ID
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  # キー
  key = models.CharField(blank=False, null=False, max_length=50)
  # 値
  value = models.CharField(blank=False, null=False, max_length=100)