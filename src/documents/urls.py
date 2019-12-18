from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('documents', views.documents, name='documents'),
    path('mydocuments', views.personal_documents, name='personal_documents'),
    path('new_document', views.new_document, name='new_document'),
]

#if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)