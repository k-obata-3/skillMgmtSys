import datetime

""" [Uilis]
    共通汎用処理
Returns:

"""
class Utils():
  # DIFF_JST_FROM_UTC = -9
  # t_delta = datetime.timedelta(hours=9)  # 9時間
  # JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差の「JST」タイムゾーン
  # output_date = datetime.datetime.now(JST)  # タイムゾーン付きでローカルな日付と時刻を取得
  # output_date = datetime.datetime.now()

  def default(self, obj):
    return

  def getNow():
    return datetime.datetime.now()

  def getAge(birthday):
    now = Utils.getNow()
    this_birthday = datetime.datetime(now.year, birthday.month, birthday.day)
    age = now.year - birthday.year
    if(now < this_birthday):
      return str(age -1)

    return str(age)