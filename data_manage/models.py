from django.db import models
from users.models import User

class StudentRecord(models.Model):
    """
    学生学习行为与成绩数据模型。
    记录学生每日学习时长、作业完成情况、课堂互动次数、测试成绩等。
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='学生')
    study_hours = models.FloatField(verbose_name='每日学习时长')
    homework_done = models.BooleanField(verbose_name='作业完成情况')
    interaction_count = models.IntegerField(verbose_name='课堂互动次数')
    test_score = models.FloatField(verbose_name='测试成绩')
    date = models.DateField(verbose_name='日期')

    def __str__(self):
        return f"{self.user.username} {self.date}"
