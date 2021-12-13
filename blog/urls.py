from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('create_post/', views.create_post, name='create_post'),
    path('post_detail/<int:id>/', views.post_detail, name='post_detail'),
    path('edit_post/<int:id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),

    path('edit_comment/<int:id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:id>', views.delete_comment, name='delete_comment'),
]
