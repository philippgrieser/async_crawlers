from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('files/', views.files, name='files'),
    path('last/', views.last_file, name='last'),
    path('updated-at/', views.last_updated_at, name='updated-at'),
    path('perform-update', views.perform_update, name='perform-update')
]
