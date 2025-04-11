from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
 

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'), # Login sahifasi
    path('post/', create_news, name='create_news'),
    path('category/', create_category, name='create_category'),
    path('category/<int:pk>/', category_news, name='category_news'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('videos/', video_news, name='video_news'),
    path('about/', about, name='about'),
    path('search/', search_news, name='search_news'),
    path('informations/', information_list, name='information_list'),
    path('edit-author/', edit_author, name='edit_author'),
    # path('logout/', logout_view, name='logout'),
]   