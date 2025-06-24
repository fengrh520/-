# 用户相关视图与功能模块
# 包含注册、登录、登出、主页、积分抽奖、积分兑换、积分中心等

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, AvatarUploadForm
from .models import User, LotteryHistory, ExchangeHistory, PointLog
from django.contrib import messages
from django.utils import timezone
from datetime import date
from ml_model.models import PredictionRecord
import random

# 用户注册视图
# 注册成功赠送5积分，普通用户默认role=0

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.points = 10  # 注册赠送积分
            user.role = 0    # 普通用户
            user.save()
            messages.success(request, '注册成功，请登录！')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

# 用户登录视图
# 登录成功当天首次登录赠送3积分

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # 登录成功
            today = date.today()
            if user.last_login is None or user.last_login.date() < today:
                user.points += 3
                user.save()
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# 用户登出视图

def logout_view(request):
    logout(request)
    return redirect('login')

# 主页视图（需登录）
# 展示个人信息、最近预测、头像上传/选择、积分抽奖/兑换入口、历史记录等
@login_required
def home_view(request):
    badge_color = '#36D399' if request.user.points > 0 else '#FF9F43'
    students = PredictionRecord.objects.filter(user=request.user).order_by('-predict_time')[:5]
    avatar_form = AvatarUploadForm(instance=request.user)
    lottery_result = None
    exchange_tip = None
    today = timezone.now().date()
    lottery_left = 5
    user = request.user
    if hasattr(user, 'lottery_count_date') and user.lottery_count_date == today:
        lottery_left = max(0, 5 - getattr(user, 'lottery_count', 0))
    else:
        lottery_left = 5
    # 查询历史
    lottery_history = LotteryHistory.objects.filter(user=user).order_by('-time')[:5]
    exchange_history = ExchangeHistory.objects.filter(user=user).order_by('-time')[:5]
    point_logs = PointLog.objects.filter(user=user).order_by('-time')[:10]
    if request.method == 'POST':
        if 'avatar_submit' in request.POST:
            avatar_form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, '头像已更新！')
                return redirect('home')
        elif 'lottery' in request.POST:
            if hasattr(user, 'lottery_count_date') and user.lottery_count_date == today:
                if user.lottery_count >= 5:
                    lottery_result = '今日抽奖次数已达上限！'
                else:
                    if user.points < 1:
                        lottery_result = '积分不足，无法抽奖！'
                    else:
                        prize = random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1])[0]
                        user.points = user.points - 1 + prize
                        user.lottery_count += 1
                        user.lottery_count_date = today
                        user.save()
                        lottery_result = prize
                        lottery_left = max(0, 5 - user.lottery_count)
                        LotteryHistory.objects.create(user=user, prize=prize)
                        PointLog.objects.create(user=user, change=-1, reason='抽奖消耗')
                        if prize > 0:
                            PointLog.objects.create(user=user, change=prize, reason='抽奖获得')
            else:
                user.lottery_count = 1
                user.lottery_count_date = today
                if user.points < 1:
                    lottery_result = '积分不足，无法抽奖！'
                else:
                    prize = random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1])[0]
                    user.points = user.points - 1 + prize
                    user.save()
                    lottery_result = prize
                    lottery_left = max(0, 5 - user.lottery_count)
                    LotteryHistory.objects.create(user=user, prize=prize)
                    PointLog.objects.create(user=user, change=-1, reason='抽奖消耗')
                    if prize > 0:
                        PointLog.objects.create(user=user, change=prize, reason='抽奖获得')
        elif 'exchange_tip' in request.POST:
            if user.points < 1:
                exchange_tip = '积分不足，无法兑换！'
            else:
                tip = random.choice(LEARNING_TIPS)
                user.points -= 1
                user.save()
                exchange_tip = tip
                ExchangeHistory.objects.create(user=user, tip=tip)
                PointLog.objects.create(user=user, change=-1, reason='兑换宝典')
    return render(request, 'users/home.html', {
        'badge_color': badge_color,
        'students': students,
        'avatar_form': avatar_form,
        'lottery_result': lottery_result,
        'exchange_tip': exchange_tip,
        'lottery_left': lottery_left,
        'lottery_history': lottery_history,
        'exchange_history': exchange_history,
        'point_logs': point_logs,
    })

# 学习葵花宝典内容
# 用于积分兑换时随机抽取
LEARNING_TIPS = [
    "营造安静环境：选择干扰少、专注度高的地方学习。",
    "设定明确小目标：分解任务，完成小目标获得成就感。",
    "主动提问思考：学习时不断问‘为什么’和‘如何应用’。",
    "定期复习回顾：学完新内容后，当天或隔天快速复习。",
    "尝试费曼技巧：用自己的话复述概念，假装教给别人。",
    "善用思维导图：用图形梳理知识结构和关联。",
    "交替学习科目：避免长时间死磕一门，切换保持新鲜感。",
    "利用碎片时间：通勤、排队时复习卡片或听音频。",
    "充足睡眠优先：保证休息，大脑才能有效巩固记忆。",
    "积极寻求反馈：完成练习后，主动请教他人或核对答案。",
    "理论联系实际：寻找所学知识在现实中的应用场景。",
    "组建学习小组：与同伴讨论、互相讲解、共同解决问题。",
    "专注当下任务：一次只做一件事，避免多任务分心。",
    "善用间隔重复：使用闪卡等工具，按遗忘曲线安排复习。",
    "整理学习笔记：课后及时梳理、精简、归纳课堂/阅读笔记。",
    "保持强烈好奇心：对学习内容真正感兴趣是最大动力。",
    "番茄工作法专注：25分钟高度集中学习+5分钟短休息。",
    "勇于输出实践：写作、解题、做项目是检验学习的最好方式。",
    "建立知识关联：将新知识与已有经验或知识网络连接。",
    "奖励学习成果：完成阶段性目标后，适当奖励自己。",
]

# 积分抽奖功能视图
# 每天最多抽奖5次，消耗1积分，奖品为0/1/2/3积分
@login_required
def lottery_view(request):
    user = request.user
    if request.method == 'POST':
        # 限制每天最多抽奖5次
        today = timezone.now().date()
        if hasattr(user, 'lottery_count_date') and user.lottery_count_date == today:
            if user.lottery_count >= 5:
                messages.error(request, '今日抽奖次数已达上限！')
                return redirect('home')
        else:
            user.lottery_count = 0
            user.lottery_count_date = today
        if user.points < 1:
            messages.error(request, '积分不足，无法抽奖！')
            return redirect('home')
        prize = random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1])[0]
        user.points = user.points - 1 + prize
        user.lottery_count += 1
        user.lottery_count_date = today
        user.save()
        messages.success(request, f'抽奖结果：获得{prize}积分！')
        return redirect('home')
    return redirect('home')

# 积分兑换学习宝典功能视图
# 消耗1积分，随机获得一条学习宝典
@login_required
def exchange_tip_view(request):
    user = request.user
    if request.method == 'POST':
        if user.points < 1:
            messages.error(request, '积分不足，无法兑换！')
            return redirect('home')
        tip = random.choice(LEARNING_TIPS)
        user.points -= 1
        user.save()
        messages.success(request, f'你获得了一条学习葵花宝典：{tip}')
        return redirect('home')
    return redirect('home')

# 积分中心页面视图
# 展示抽奖、兑换、历史记录、积分明细等
@login_required
def points_view(request):
    badge_color = '#36D399' if request.user.points > 0 else '#FF9F43'
    user = request.user
    today = timezone.now().date()
    lottery_left = 5
    if hasattr(user, 'lottery_count_date') and user.lottery_count_date == today:
        lottery_left = max(0, 5 - getattr(user, 'lottery_count', 0))
    else:
        lottery_left = 5
    lottery_result = None
    exchange_tip = None
    lottery_history = LotteryHistory.objects.filter(user=user).order_by('-time')[:5]
    exchange_history = ExchangeHistory.objects.filter(user=user).order_by('-time')[:5]
    point_logs = PointLog.objects.filter(user=user).order_by('-time')[:10]
    if request.method == 'POST':
        if 'lottery' in request.POST:
            if hasattr(user, 'lottery_count_date') and user.lottery_count_date == today:
                if user.lottery_count >= 5:
                    lottery_result = '今日抽奖次数已达上限！'
                else:
                    if user.points < 1:
                        lottery_result = '积分不足，无法抽奖！'
                    else:
                        prize = random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1])[0]
                        user.points = user.points - 1 + prize
                        user.lottery_count += 1
                        user.lottery_count_date = today
                        user.save()
                        lottery_result = prize
                        lottery_left = max(0, 5 - user.lottery_count)
                        LotteryHistory.objects.create(user=user, prize=prize)
                        PointLog.objects.create(user=user, change=-1, reason='抽奖消耗')
                        if prize > 0:
                            PointLog.objects.create(user=user, change=prize, reason='抽奖获得')
            else:
                user.lottery_count = 1
                user.lottery_count_date = today
                if user.points < 1:
                    lottery_result = '积分不足，无法抽奖！'
                else:
                    prize = random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1])[0]
                    user.points = user.points - 1 + prize
                    user.save()
                    lottery_result = prize
                    lottery_left = max(0, 5 - user.lottery_count)
                    LotteryHistory.objects.create(user=user, prize=prize)
                    PointLog.objects.create(user=user, change=-1, reason='抽奖消耗')
                    if prize > 0:
                        PointLog.objects.create(user=user, change=prize, reason='抽奖获得')
        elif 'exchange_tip' in request.POST:
            if user.points < 1:
                exchange_tip = '积分不足，无法兑换！'
            else:
                tip = random.choice(LEARNING_TIPS)
                user.points -= 1
                user.save()
                exchange_tip = tip
                ExchangeHistory.objects.create(user=user, tip=tip)
                PointLog.objects.create(user=user, change=-1, reason='兑换宝典')
    return render(request, 'users/points.html', {
        'badge_color': badge_color,
        'lottery_result': lottery_result,
        'exchange_tip': exchange_tip,
        'lottery_left': lottery_left,
        'lottery_history': lottery_history,
        'exchange_history': exchange_history,
        'point_logs': point_logs,
    })
