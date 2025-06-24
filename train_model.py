"""
train_model.py
用于训练学生成绩预测模型，并保存为ml_model/model.pkl。
字段已与实际数据集完全对应。
"""
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# 1. 读取数据
DATA_PATH = os.path.join('data', 'student_habits_performance.csv')
df = pd.read_csv(DATA_PATH)

# 2. 特征与标签（字段名与实际一致）
X = df[['study_hours_per_day', 'attendance_percentage', 'exercise_frequency']]
y = df['exam_score']

# 3. 训练模型
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. 保存模型
os.makedirs('ml_model', exist_ok=True)
joblib.dump(model, os.path.join('ml_model', 'model.pkl'))

print('模型训练完成，已保存为 ml_model/model.pkl')
