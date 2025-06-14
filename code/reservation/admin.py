# reservation/admin.py
# 管理画面での予約システム管理設定

from django.contrib import admin
from .models import Space, Reservation, Payment


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    """
    スペース管理画面の設定
    """
    
    list_display = ('name', 'space_type', 'hourly_rate', 'is_available', 'created_at')
    list_filter = ('space_type', 'is_available', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本情報', {
            'fields': ('name', 'space_type', 'capacity', 'is_available')
        }),
        ('詳細情報', {
            'fields': ('equipment', 'description', 'hourly_rate')
        }),
        ('システム情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    予約管理画面の設定
    """
    
    list_display = ('user', 'space', 'reservation_date', 'start_time', 'end_time', 'status', 'total_amount')
    list_filter = ('status', 'reservation_date', 'space__space_type', 'created_at')
    search_fields = ('user__username', 'user__last_name', 'space__name', 'purpose')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('予約情報', {
            'fields': ('user', 'space', 'reservation_date', 'start_time', 'end_time')
        }),
        ('詳細情報', {
            'fields': ('purpose', 'status', 'total_amount')
        }),
        ('システム情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    date_hierarchy = 'reservation_date'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    支払い管理画面の設定
    """
    
    list_display = ('reservation', 'amount', 'payment_method', 'payment_status', 'paid_at')
    list_filter = ('payment_method', 'payment_status', 'created_at')
    search_fields = ('reservation__user__username', 'transaction_id')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('支払い情報', {
            'fields': ('reservation', 'amount', 'payment_method', 'payment_status')
        }),
        ('取引詳細', {
            'fields': ('transaction_id', 'paid_at')
        }),
        ('システム情報', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )