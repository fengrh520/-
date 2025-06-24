from django.contrib import admin
from .models import StudentRecord

@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'study_hours', 'homework_done', 'interaction_count', 'test_score')
    search_fields = ('user__username',)
    list_filter = ('date', 'homework_done')
