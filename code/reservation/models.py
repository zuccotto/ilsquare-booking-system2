# reservation/models.py
# 予約システム関連のモデル定義

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

# カスタムユーザーモデルを使用
User = get_user_model()


class Space(models.Model):
    """
    スペース（半個室・完全個室）のモデル
    """
    
    # スペース種別の選択肢
    SPACE_TYPE_CHOICES = [
        ('SEMI_PRIVATE', '半個室'),
        ('PRIVATE', '完全個室'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name='スペース名',
        help_text='例: 半個室A、完全個室B'
    )
    
    space_type = models.CharField(
        max_length=20,
        choices=SPACE_TYPE_CHOICES,
        verbose_name='スペース種別'
    )
    
    capacity = models.IntegerField(
        default=1,
        verbose_name='収容人数',
        help_text='通常は1人用'
    )
    
    equipment = models.TextField(
        verbose_name='設備',
        help_text='ノートPC、外付けモニター、ヘッドセットなど'
    )
    
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='時間単価（円）',
        help_text='半個室: 500円、完全個室: 1000円（設備は共通）'
    )
    
    description = models.TextField(
        verbose_name='説明',
        blank=True,
        help_text='スペースの特徴や利用シーンなど'
    )
    
    is_available = models.BooleanField(
        default=True,
        verbose_name='利用可能',
        help_text='メンテナンス時などはFalse'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='作成日時'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新日時'
    )
    
    class Meta:
        verbose_name = 'スペース'
        verbose_name_plural = 'スペース'
        ordering = ['space_type', 'name']  # 種別、名前順でソート
    
    def __str__(self):
        return f"{self.name} ({self.get_space_type_display()})"


class Reservation(models.Model):
    """
    予約情報のモデル
    """
    
    # 予約状態の選択肢
    STATUS_CHOICES = [
        ('CONFIRMED', '確定'),
        ('CANCELLED', 'キャンセル'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='ユーザー',
        related_name='reservations'
    )
    
    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        verbose_name='スペース',
        related_name='reservations'
    )
    
    reservation_date = models.DateField(
        verbose_name='予約日'
    )
    
    start_time = models.TimeField(
        verbose_name='開始時間'
    )
    
    end_time = models.TimeField(
        verbose_name='終了時間'
    )
    
    purpose = models.TextField(
        verbose_name='利用目的',
        blank=True,
        help_text='会議、作業、学習など'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='CONFIRMED',
        verbose_name='予約状態'
    )
    
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='利用料金総額（円）'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='予約作成日時'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='予約更新日時'
    )
    
    class Meta:
        verbose_name = '予約'
        verbose_name_plural = '予約'
        ordering = ['-reservation_date', '-start_time']  # 日付、時間の降順
        
        # 同じスペース・日付・時間の重複予約を防ぐ制約
        constraints = [
            models.UniqueConstraint(
                fields=['space', 'reservation_date', 'start_time', 'end_time'],
                condition=models.Q(status='CONFIRMED'),
                name='unique_confirmed_reservation'
            )
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.space.name} ({self.reservation_date} {self.start_time}-{self.end_time})"
    
    def get_duration_hours(self):
        """利用時間数を計算（Decimalで返す）"""
        from datetime import datetime
        from decimal import Decimal
        
        # 時間を計算するために datetime オブジェクトに変換
        start = datetime.combine(self.reservation_date, self.start_time)
        end = datetime.combine(self.reservation_date, self.end_time)
        
        # 時間差を計算
        duration = end - start
        
        # 時間数をDecimalで返す
        hours = duration.total_seconds() / 3600
        return Decimal(str(hours))


class Payment(models.Model):
    """
    支払い情報のモデル
    """
    
    # 支払い方法の選択肢
    PAYMENT_METHOD_CHOICES = [
        ('CASH', '現金'),
        ('PAYPAY', 'PayPay'),
        ('CREDIT', 'クレジットカード'),
        ('QR', 'QR決済'),
        ('INVOICE', '請求書'),
    ]
    
    # 支払い状態の選択肢
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', '支払い待ち'),
        ('COMPLETED', '支払い完了'),
        ('FAILED', '支払い失敗'),
        ('CANCELLED', 'キャンセル'),
    ]
    
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        verbose_name='予約',
        related_name='payment'
    )
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='支払い金額（円）'
    )
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='支払い方法'
    )
    
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING',
        verbose_name='支払い状態'
    )
    
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='取引ID',
        help_text='決済システムから返される取引ID'
    )
    
    paid_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='支払い完了日時'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='作成日時'
    )
    
    class Meta:
        verbose_name = '支払い'
        verbose_name_plural = '支払い'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reservation.user.username} - ¥{self.amount} ({self.get_payment_status_display()})"