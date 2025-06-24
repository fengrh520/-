from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User
from .models import PredictionRecord
from django.contrib import messages
import joblib
import os

# 加载预训练模型（假设已保存为ml_model/model.pkl）
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

@login_required
def predict_view(request):
    user = request.user
    from .models import PredictionRecord
    last_record = PredictionRecord.objects.filter(user=user).first()
    if not hasattr(user, 'points'):
        user.points = 10  # 超级用户等无积分字段时自动补全
        user.save()
    if user.points <= 0:
        messages.error(request, '积分不足，无法进行预测！')
        return render(request, 'ml_model/predict.html', {'last': last_record})
    if request.method == 'POST':
        def safe_float(val):
            try:
                return float(val)
            except (TypeError, ValueError):
                return None
        def safe_int(val):
            try:
                return int(val)
            except (TypeError, ValueError):
                return None
        data = {
            'student_id': request.POST.get('student_id') or None,
            'age': safe_int(request.POST.get('age')),
            'gender': request.POST.get('gender') or None,
            'study_hours_per_day': safe_float(request.POST.get('study_hours_per_day')),
            'social_media_hours': safe_float(request.POST.get('social_media_hours')),
            'netflix_hours': safe_float(request.POST.get('netflix_hours')),
            'part_time_job': request.POST.get('part_time_job') if request.POST.get('part_time_job') in ['0', '1'] else None,
            'attendance_percentage': safe_float(request.POST.get('attendance_percentage')),
            'sleep_hours': safe_float(request.POST.get('sleep_hours')),
            'diet_quality': request.POST.get('diet_quality') or None,
            'exercise_frequency': safe_int(request.POST.get('exercise_frequency')),
            'parental_education_level': request.POST.get('parental_education_level') or None,
            'internet_quality': request.POST.get('internet_quality') or None,
            'mental_health_rating': safe_int(request.POST.get('mental_health_rating')),
            'extracurricular_participation': request.POST.get('extracurricular_participation') if request.POST.get('extracurricular_participation') in ['0', '1'] else None,
            'exam_score': safe_float(request.POST.get('exam_score')),
        }
        # 只取模型需要的3个特征
        X = [[
            data['study_hours_per_day'] or 0,
            data['homework_done'] if 'homework_done' in data else 0,
            data['interaction_count'] if 'interaction_count' in data else 0
        ]]
        from django.conf import settings
        import joblib, os
        MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
        model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
        if model:
            pred = model.predict(X)[0]
            PredictionRecord.objects.create(
                user=user,
                predict_result=pred,
                **data
            )
            user.points -= 1
            user.save()
            history = PredictionRecord.objects.filter(user=user)[:10]
            return render(request, 'ml_model/predict.html', {'result': pred, 'last': data, 'history': history})
        else:
            messages.error(request, '模型未部署，无法预测。')
    history = PredictionRecord.objects.filter(user=user)[:10]
    return render(request, 'ml_model/predict.html', {'last': last_record, 'history': history})
