# 用户相关数据模型
# 包含自定义用户、抽奖历史、兑换历史、积分日志等

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.conf.urls.static import static
#这段代码实现了一个完整的用户积分系统
# ，包括用户管理、头像设置、积分记录和操作日志，支持积分增减、抽奖、兑换等业务场景，并提供了管理后台配置。
class User(AbstractUser):
    """
    用户模型，继承自Django自带用户，增加积分和角色字段。
    role: 0-普通用户，1-管理员
    points: 用户积分
    avatar: 头像图片
    avatar_choice: 预设头像选择
    """
    ROLE_CHOICES = (
        (0, '普通用户'),
        (1, '管理员'),
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=0, verbose_name='角色')
    points = models.IntegerField(default=5, verbose_name='积分')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    AVATAR_CHOICES = [
        ('1.png', '预设头像1'),
        ('2.png', '预设头像2'),
        ('3.png', '预设头像3'),
        ('4.png', '预设头像4'),
        ('5.png', '预设头像5'),
    ]
    avatar_choice = models.CharField(max_length=32, blank=True, null=True, choices=AVATAR_CHOICES, verbose_name='预设头像')

    def __str__(self):
        return self.username

class LotteryHistory(models.Model):
    """
    用户积分抽奖历史记录
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prize = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} 抽奖 {self.prize}分 @ {self.time.strftime('%Y-%m-%d %H:%M')}"

class ExchangeHistory(models.Model):
    """
    用户兑换学习宝典历史记录
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tip = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} 兑换宝典 @ {self.time.strftime('%Y-%m-%d %H:%M')}"

class PointLog(models.Model):
    """
    用户积分变动明细日志
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    change = models.IntegerField()
    reason = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} {self.change:+}分 {self.reason} @ {self.time.strftime('%Y-%m-%d %H:%M')}"

urlpatterns = [
    # ...你的其它url...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
