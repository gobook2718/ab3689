from django.urls import path
from core import views

urlpatterns = [
    path('users', views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:pk>', views.UserDetail.as_view(), name=views.UserDetail.name),
    path('post-categories', views.PostCategoryList.as_view(), name=views.PostCategoryList.name),
    path('post-categories/<int:pk>', views.PostCategoryDetail.as_view(), name=views.PostCategoryDetail.name),
    path('posts', views.PostList.as_view(), name=views.PostList.name),
    path('posts/<int:pk>', views.PostDetail.as_view(), name=views.PostDetail.name),
    path('api/', views.APIRoot.as_view(), name=views.APIRoot.name),

    path('api/login', views.login),
]