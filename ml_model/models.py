from django.db import models
from django.conf import settings

# 机器学习模型本地无数据库表，仅用于集成预测逻辑。
# 相关预测逻辑将在views.py中实现。

class PredictionRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predictions')
    student_id = models.CharField(max_length=32, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=8, blank=True, null=True)
    study_hours_per_day = models.FloatField(blank=True, null=True)
    social_media_hours = models.FloatField(blank=True, null=True)
    netflix_hours = models.FloatField(blank=True, null=True)
    part_time_job = models.BooleanField(blank=True, null=True)
    attendance_percentage = models.FloatField(blank=True, null=True)
    sleep_hours = models.FloatField(blank=True, null=True)
    diet_quality = models.CharField(max_length=16, blank=True, null=True)
    exercise_frequency = models.IntegerField(blank=True, null=True)
    parental_education_level = models.CharField(max_length=32, blank=True, null=True)
    internet_quality = models.CharField(max_length=16, blank=True, null=True)
    mental_health_rating = models.IntegerField(blank=True, null=True)
    extracurricular_participation = models.BooleanField(blank=True, null=True)
    exam_score = models.FloatField(blank=True, null=True)
    predict_result = models.FloatField(blank=True, null=True)
    predict_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-predict_time']
        verbose_name = '成绩预测记录'
        verbose_name_plural = '成绩预测记录'
