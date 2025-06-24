from django.urls import path
from . import views

urlpatterns = [
    path('records/', views.record_list, name='record_list'),
    path('import/', views.import_data, name='import_data'),
    path('export/', views.export_data, name='export_data'),
]
