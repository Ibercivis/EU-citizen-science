from django.urls import path, include

from . import views

urlpatterns = [
    path('new_project', views.new_project, name='new_project'),
    path('projects', views.projects, name='projects'),
    path('project/<int:pk>', views.project, name='project'),
    path('editProject/<int:pk>', views.editProject, name='editProject'),
    path('deleteProject/<int:pk>', views.deleteProject, name='deleteProject'),
    path('overview', views.overview, name='overview'),
    path('testing', views.testing, name='testing'),
    path('text_autocomplete/', views.text_autocomplete, name='text_autocomplete'),
    path('select2/', include('django_select2.urls')),
    path('myprojects', views.personal_projects, name='personal_projects'),
    path('dashboard', views.dashboard, name='dashboard'),

]