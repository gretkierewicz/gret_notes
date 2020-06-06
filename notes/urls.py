from django.urls import path

from . import views


app_name = 'notes'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('<int:note_id>/edit/', views.edit, name='edit'),
    path('<int:note_id>/del/', views.delete, name='delete'),
]
