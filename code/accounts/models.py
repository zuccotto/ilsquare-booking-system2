# accounts/models.py
# ユーザー関連のモデル定義

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    カスタムユーザーモデル
    Django標準のUserモデルを拡張して電話番号を追加
    """
    
    # 電話番号フィールドを追加
    phone_number = models.CharField(
        max_length=20,
        verbose_name='電話番号',
        help_text='例: 090-1234-5678'
    )
    
    # メール認証は使わないのでメールフィールドを空にできるように変更
    email = models.EmailField(
        verbose_name='メールアドレス',
        blank=True,  # 空白OK
        null=True    # NULL値OK
    )
    
    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'
    
    def __str__(self):
        """管理画面などで表示される文字列"""
        return f"{self.last_name} {self.first_name} ({self.username})"