# accounts/admin.py
# 管理画面でのユーザー管理設定

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    カスタムユーザーモデル用の管理画面設定
    """
    
    # リスト画面で表示するフィールド
    list_display = ('username', 'last_name', 'first_name', 'phone_number', 'is_active', 'date_joined')
    
    # 検索可能フィールド
    search_fields = ('username', 'last_name', 'first_name', 'phone_number')
    
    # フィルター
    list_filter = ('is_active', 'is_staff', 'date_joined')
    
    # 詳細画面のフィールド設定
    fieldsets = UserAdmin.fieldsets + (
        ('追加情報', {'fields': ('phone_number',)}),
    )
    
    # 新規作成画面のフィールド設定
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('追加情報', {'fields': ('first_name', 'last_name', 'phone_number')}),
    )