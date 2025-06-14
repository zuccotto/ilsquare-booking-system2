# reservation/urls.py
# 予約システム関連のURL設定

from django.urls import path
from . import views

urlpatterns = [
    # トップページ
    path('', views.top_view, name='top'),
    
    
    # 予約申込（新フロー）
    path('reserve/', views.reserve_view, name='reserve'),
    path('reserve/step1/', views.reserve_step1_view, name='reserve_step1'),
    path('reserve/step2/<str:date_string>/', views.reserve_step2_view, name='reserve_step2'),
    path('reserve/step2-5/<str:date_string>/<int:space_id>/<str:start_time>/', views.reserve_step2_5_view, name='reserve_step2_5'),
    path('reserve/step3/', views.reserve_step3_view, name='reserve_step3'),
    path('reserve/complete/', views.reserve_complete_view, name='reserve_complete'),
    
    # 予約詳細
    path('reservation/<int:reservation_id>/', views.reservation_detail_view, name='reservation_detail'),
    
    # 予約一覧
    path('reservations/', views.reservations_view, name='reservations'),
    
    # 予約キャンセル
    path('reservation/<int:reservation_id>/cancel/', views.cancel_reservation_view, name='cancel_reservation'),
]