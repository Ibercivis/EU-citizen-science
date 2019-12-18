from django.contrib import admin
from .models import Project, Category, Member

# Register your models here.

class ProjectA(admin.ModelAdmin):
    list_filter = ('creator',)

admin.site.register(Project, ProjectA)
admin.site.register(Category)
admin.site.register(Member)