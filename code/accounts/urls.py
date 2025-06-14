# accounts/urls.py
# アカウント関連のURL設定

from django.urls import path
from . import views

urlpatterns = [
    # ユーザー登録
    path('register/', views.register_view, name='register'),
    
    # ログイン
    path('login/', views.login_view, name='login'),
    
    # ログアウト
    path('logout/', views.logout_view, name='logout'),
    
    # マイページ
    path('mypage/', views.mypage_view, name='mypage'),
    
    # プロフィール
    path('profile/', views.profile_view, name='profile'),
]