from django.urls import path

from . import views


app_name = 'tags'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:tag_id>/edit/', views.edit, name='edit'),
    path('<int:tag_id>/del/', views.delete, name='delete'),
]
