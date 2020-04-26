from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/tezina', views.post_list, name='post data and list all'),
    path('api/v1/tezina/<str:date>', views.get_delete_patch, name='get, patch i delete'),
    path('api/v1/users', views.log_in, name='login'),
    path('api/v1/users/<str:email>', views.change_pass, name='change pass'),
    path('api/v1/create_user', views.create_user, name='create and list users'),

    ]   