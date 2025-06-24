# 用户相关表单定义
# 包含注册、登录、头像上传等表单

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    """
    用户注册表单，继承自Django自带UserCreationForm。
    """
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class LoginForm(AuthenticationForm):
    """
    用户登录表单，继承自Django自带AuthenticationForm。
    """
    class Meta:
        model = User
        fields = ("username", "password")

class AvatarUploadForm(forms.ModelForm):
    """
    用户头像上传与预设头像选择表单
    """
    class Meta:
        model = User
        fields = ['avatar', 'avatar_choice']
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 1024 * 1024:
                raise forms.ValidationError('头像文件不能超过1MB')
            if not avatar.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError('仅支持jpg、jpeg、png格式图片')
        return avatar
