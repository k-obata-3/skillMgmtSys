from rest_framework import serializers
from .models import CareerInfoItem, Company, Department, DepartmentRelation, MasterItem, Project, User, UserInfo, CareerInfo

class UserSerializer(serializers.ModelSerializer):
  # 会社ID
  company = serializers.IntegerField()
  # メールアドレス
  mail_address = serializers.CharField()
  # パスワード
  password = serializers.CharField()
  # 権限
  authority = serializers.IntegerField()
  # 状態
  state = serializers.IntegerField()
  # 最終ログイン
  lastLogin = serializers.DateTimeField(required=False, allow_null=True)

  class Meta:
    model = User
    fields = ('company', 'mail_address', 'password', 'authority', 'state', 'lastLogin')

  def update(self, instance, validated_data, login_user):
    instance.authority = validated_data.get('authority', instance.authority)
    instance.state = validated_data.get('state', instance.state)
    instance.version = instance.version + 1
    instance.ud_user = login_user.id
    instance.save()

    return instance

  def save(self, validated_data, login_user, company_id):
    return User.objects.create(
      company = Company.objects.get(pk = company_id),
      mail_address = validated_data.get('mail_address'),
      password = validated_data.get('password'),
      authority = validated_data.get('authority'),
      state = validated_data.get('state'),
      add_user = login_user.id,
      ud_user = login_user.id
    )
  
  def updateLoginDateTime(self, instance, dateTimeNow):
    instance.version = instance.version + 1
    instance.ud_user = instance.id
    instance.last_login = dateTimeNow
    instance.save()

    return instance

  def passwordUpdate(self, instance, password, login_user):
    instance.password = password
    instance.version = instance.version + 1
    instance.ud_user = login_user.id
    instance.save()

    return instance

class UserInfoSerializer(serializers.ModelSerializer):
  # 姓カナ
  first_name_kana = serializers.CharField()
  # 名カナ
  last_name_kana = serializers.CharField()
  # 姓
  first_name = serializers.CharField()
  # 名
  last_name = serializers.CharField()
  # 生年月日
  birthday = serializers.DateField()
  # 役職
  position = serializers.CharField(required=False, allow_null=True)

  class Meta:
    model = UserInfo
    fields = ('first_name_kana', 'last_name_kana', 'first_name', 'last_name', 'birthday', 'position')

  def update(self, instance, validated_data, login_user):
    instance.first_name_kana = validated_data.get('first_name_kana', instance.first_name_kana)
    instance.last_name_kana = validated_data.get('last_name_kana', instance.last_name_kana)
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    instance.birthday = validated_data.get('birthday', instance.birthday)
    instance.position = validated_data.get('position', instance.position)
    instance.ud_user = login_user.id
    instance.version = instance.version + 1
    instance.save()

    return instance;

  def save(self, validated_data, user, login_user):
    userInfo = UserInfo(
      user = user,
      first_name_kana = validated_data.get('first_name_kana'),
      last_name_kana = validated_data.get('last_name_kana'),
      first_name = validated_data.get('first_name'),
      last_name = validated_data.get('last_name'),
      birthday = validated_data.get('birthday'),
      position = validated_data.get('position'),
      add_user = login_user.id,
      ud_user = login_user.id,
    )
    userInfo.save()

class CareerInfoSerializer(serializers.ModelSerializer):
  # ユーザID
  user_id = User.id
  # 案件名
  project_name = serializers.CharField()
  # 概要
  overview = serializers.CharField(required=False, allow_null=True)
  # 開始年月日
  start_date = serializers.DateField(required=False, allow_null=True)
  # 終了年月日
  end_date = serializers.DateField(required=False, allow_null=True)

  class Meta:
    model = CareerInfo
    fields = ('user_id', 'project_name', 'overview', 'start_date', 'end_date')

  def update(self, instance, validated_data):
    careerInfo = CareerInfo(
      id = instance.id,
      project_name = validated_data.get('project_name', instance.project_name),
      overview = validated_data.get('overview', instance.overview),
      start_date = validated_data.get('start_date', instance.start_date),
      end_date = validated_data.get('end_date', instance.end_date),
      version = instance.version + 1,
      add_user = instance.add_user,
      add_date = instance.add_date,
      ud_user = validated_data.get('user'),
      user_id = instance.user_id,
    )

    instance = careerInfo
    instance.save();

    return instance;

  def save(self, validated_data):
    return CareerInfo.objects.create(
      user_id = validated_data.get('user'),
      project_name = validated_data.get('project_name'),
      overview = validated_data.get('overview'),
      start_date = validated_data.get('start_date'),
      end_date = validated_data.get('end_date'), 
      add_user = validated_data.get('user'),
      ud_user = validated_data.get('user'),
    )

    # careerInfo = CareerInfo(
    #   user_id = validated_data.get('user'),
    #   project_name = validated_data.get('project_name'),
    #   overview = validated_data.get('overview'),
    #   # model = validated_data.get('model'),
    #   # os = validated_data.get('os'),
    #   # data_base = validated_data.get('data_base'),
    #   # language = validated_data.get('language'),
    #   # framework = validated_data.get('framework'),
    #   # incharge = validated_data.get('incharge'),
    #   # role = validated_data.get('role'),
    #   # other = validated_data.get('other'),
    #   start_date = validated_data.get('start_date'),
    #   end_date = validated_data.get('end_date'), 
    #   add_user = validated_data.get('user'),
    #   ud_user = validated_data.get('user'),
    # )
    # careerInfo.save()

class CareerInfoItemSerializer(serializers.ModelSerializer):
  # 経歴情報ID
  career_info_id = CareerInfo.id
  # キー
  key = serializers.CharField()
  # 値
  value = serializers.CharField()

  class Meta:
    model = CareerInfoItem
    fields = ('career_info_id', 'key', 'value')

  def update(self, instance, validated_data):
    careerInfoItem = CareerInfoItem(
      career_info_id = instance.id,
      key = validated_data.get('key', instance.key),
      value = validated_data.get('value', instance.value),
      version = instance.version + 1,
      add_user = instance.add_user,
      add_date = instance.add_date,
      ud_user = validated_data.get('user'),
      # user_id = instance.user_id,
    )

    instance = careerInfoItem
    instance.save();

    return instance;

  def save(self, validated_data, new_career_info):
    careerInfoItem = CareerInfoItem(
      career_info_id = new_career_info.id,
      key = validated_data.get('key'),
      value = validated_data.get('value'),
      add_user = validated_data.get('user'),
      ud_user = validated_data.get('user'),
    )
    careerInfoItem.save()

class DepartmentSerializer(serializers.ModelSerializer):
  # 会社ID
  company_id = serializers.IntegerField()
  # 部署名
  name = serializers.CharField()

  class Meta:
    model = MasterItem
    fields = ('company_id', 'name')

  def update(self, instance, validated_data, login_user):
    department = Department(
      id = instance.id,
      company_id = instance.company_id,
      name = validated_data.get('name', instance.name),
      version = instance.version + 1,
      add_user = instance.add_user,
      add_date = instance.add_date,
      ud_user = login_user.id,
    )

    instance = department
    instance.save();

    return instance;

  def save(self, validated_data, login_user):
    department = Department(
      company_id = validated_data.get('company_id'),
      name = validated_data.get('name'),
      add_user = login_user.id,
      ud_user = login_user.id,
    )
    department.save()


class DepartmentRelationSerializer(serializers.ModelSerializer):
  # 部署ID
  department = serializers.IntegerField()
  # ユーザID
  user = serializers.IntegerField()

  class Meta:
    model = DepartmentRelation
    fields = ('department', 'user')

  def save(self, validated_data, login_user):
    departmentRelation = DepartmentRelation(
      user = validated_data.get('user'),
      department = validated_data.get('depertment'),
      add_user = login_user.id,
      ud_user = login_user.id,
    )
    departmentRelation.save()

class ProjectSerializer(serializers.ModelSerializer):
  # 会社ID
  company_id = serializers.IntegerField()
  # 案件名
  name = serializers.CharField()
  # 概要
  overview = serializers.CharField(required=False, allow_null=True)
  # 開始年月日
  start_date = serializers.DateField(required=False, allow_null=True)
  # 終了年月日
  end_date = serializers.DateField(required=False, allow_null=True)

  class Meta:
    model = Project
    fields = ('company_id', 'name', 'overview', 'start_date', 'end_date')

  def update(self, instance, validated_data, login_user):
    project = Project(
      id = instance.id,
      company_id = instance.company_id,
      name = validated_data.get('name', instance.name),
      overview = validated_data.get('overview', instance.overview),
      start_date = validated_data.get('start_date', instance.start_date),
      end_date = validated_data.get('end_date', instance.end_date),
      version = instance.version + 1,
      add_user = instance.add_user,
      add_date = instance.add_date,
      ud_user = login_user.id,
    )

    instance = project
    instance.save();

    return instance;

  def save(self, validated_data, login_user):
    return Project.objects.create(
      company_id = validated_data.get('company_id'),
      name = validated_data.get('name'),
      overview = validated_data.get('overview'),
      start_date = validated_data.get('start_date'),
      end_date = validated_data.get('end_date'), 
      add_user = login_user.id,
      ud_user = login_user.id,
    )

class MasterItemSerializer(serializers.ModelSerializer):
  # 会社ID
  company_id = serializers.IntegerField()
  # キー
  key = serializers.CharField()
  # 値
  value = serializers.CharField()

  class Meta:
    model = MasterItem
    fields = ('company_id', 'key', 'value')

  def update(self, instance, validated_data, login_user):
    masterItem = MasterItem(
      id = instance.id,
      company_id = instance.company_id,
      key = validated_data.get('key', instance.key),
      value = validated_data.get('value', instance.value),
      version = instance.version + 1,
      add_user = instance.add_user,
      add_date = instance.add_date,
      ud_user = login_user.id,
    )

    instance = masterItem
    instance.save();

    return instance;

  def save(self, validated_data, login_user):
    masterItem = MasterItem(
      company_id = validated_data.get('company_id'),
      key = validated_data.get('key'),
      value = validated_data.get('value'),
      add_user = login_user.id,
      ud_user = login_user.id,
    )
    masterItem.save()