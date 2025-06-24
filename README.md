# 学生学习行为分析与成绩预测系统

本项目基于Django框架，集成了用户认证、学生数据管理、机器学习成绩预测等功能，旨在为教育管理者和教师提供学生学习行为分析与成绩预测的高效工具。

## 目录
- [项目简介](#项目简介)
- [主要功能模块](#主要功能模块)
- [环境依赖](#环境依赖)
- [安装与部署](#安装与部署)
- [使用说明](#使用说明)
- [常见问题与解决方案](#常见问题与解决方案)
- [项目结构说明](#项目结构说明)
- [联系方式](#联系方式)

---

## 项目简介
本系统通过对学生学习行为数据的管理与分析，结合机器学习模型，实现对学生成绩的预测。系统支持数据的导入导出、用户积分管理、后台管理等功能，适用于高校、培训机构等场景。

## 主要功能模块
- **用户认证与管理**：注册、登录、积分、权限分配
- **学生数据管理**：学生行为与成绩数据的增删改查、CSV/Excel批量导入导出
- **成绩预测与分析**：集成机器学习模型，对学生成绩进行预测，支持积分消耗兑换预测服务
- **后台管理**：基于Django Admin的可视化管理界面

## 环境依赖
- Python 3.8+
- Django 4.x
- pandas
- scikit-learn
- openpyxl

## 安装与部署
1. **克隆项目**
   ```bash
   git clone <你的GitHub仓库地址>
   cd 考试系统333
   ```
2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   # 或手动安装
   pip install django pandas scikit-learn openpyxl
   ```
3. **数据库迁移**
   ```bash
   python manage.py migrate
   ```
4. **创建超级用户（管理员）**
   ```bash
   python manage.py createsuperuser
   ```
5. **启动开发服务器**
   ```bash
   python manage.py runserver
   ```

## 使用说明
- 访问主页及功能页面：`http://127.0.0.1:8000/`
- 访问管理后台：`http://127.0.0.1:8000/admin/`
- 用户可注册、登录、查看积分、兑换预测服务等
- 管理员可在后台管理学生数据、导入导出数据、管理用户等
- 成绩预测功能位于“成绩预测”页面，需消耗积分

## 项目结构说明
```
├── data_manage/      # 学生数据管理模块
├── ml_model/         # 机器学习模型与预测模块
├── users/            # 用户认证与积分管理模块
├── templates/        # 前端模板页面
├── static/           # 静态资源
├── manage.py         # Django管理脚本
├── requirements.txt  # 依赖包列表
└── ...
```

## 常见问题与解决方案
1. **虚拟环境被加入Git版本控制**
   - 问题：`venv/`等虚拟环境文件夹被提交到Git，导致仓库臃肿。
   - 解决：在项目根目录下添加`.gitignore`文件，内容如下：
     ```
     venv/
     *.pyc
     __pycache__/
     db.sqlite3
     staticfiles/
     ```
   - 然后执行：
     ```bash
     git rm -r --cached venv
     git add .
     git commit -m "移除虚拟环境文件夹并添加.gitignore"
     ```

2. **依赖安装失败或版本不兼容**
   - 问题：部分依赖包安装失败或版本冲突。
   - 解决：
     - 检查Python版本是否为3.8及以上。
     - 使用`pip install -r requirements.txt`统一安装。
     - 如遇到权限问题，尝试加上`--user`参数。

3. **数据库迁移报错**
   - 问题：`python manage.py migrate`时报错。
   - 解决：
     - 检查`settings.py`数据库配置。
     - 删除`db.sqlite3`和`migrations/`下的`__pycache__`，重新迁移。

4. **静态文件无法加载**
   - 问题：页面样式丢失或图片无法显示。
   - 解决：
     - 执行`python manage.py collectstatic`收集静态文件。
     - 检查`settings.py`中的`STATIC_URL`和`STATICFILES_DIRS`配置。

5. **模型预测功能不可用**
   - 问题：成绩预测页面报错或无响应。
   - 解决：
     - 检查`ml_model/model.pkl`是否存在。
     - 确认`train_model.py`已正确训练并生成模型文件。

## 联系方式
如需技术支持或功能定制，请联系：
- 邮箱：your_email@example.com
- GitHub Issues

---
如需详细开发说明或功能扩展，请查阅源码注释或联系作者。
