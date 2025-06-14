# reservation/forms.py
# 予約システム関連のフォーム定義

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, time, datetime, timedelta
from .models import Reservation, Space


class ReservationForm(forms.ModelForm):
    """
    予約申込フォーム
    
    スペース・日時・利用目的を入力
    """
    
    # 時間選択肢（1時間単位）- 文字列で定義
    TIME_CHOICES = [
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
    ]
    
    # 時間フィールドを選択リストに変更
    start_time = forms.ChoiceField(
        choices=TIME_CHOICES[:-1],  # 18:00は開始時間から除外
        label='開始時間',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    end_time = forms.ChoiceField(
        choices=TIME_CHOICES[1:],  # 09:00は終了時間から除外
        label='終了時間',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Reservation
        fields = ['space', 'reservation_date', 'start_time', 'end_time', 'purpose']
        widgets = {
            'space': forms.Select(attrs={
                'class': 'form-control'
            }),
            'reservation_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '会議、学習、作業など（任意）'
            })
        }
        labels = {
            'space': 'スペース',
            'reservation_date': '利用日',
            'start_time': '開始時間',
            'end_time': '終了時間',
            'purpose': '利用目的（任意）'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 利用可能なスペースのみ表示
        self.fields['space'].queryset = Space.objects.filter(is_available=True)
        
        # 必須項目にマーク
        self.fields['space'].required = True
        self.fields['reservation_date'].required = True
        self.fields['start_time'].required = True
        self.fields['end_time'].required = True
        self.fields['purpose'].required = False
    
    def clean_reservation_date(self):
        """予約日のバリデーション"""
        reservation_date = self.cleaned_data['reservation_date']
        today = date.today()
        
        # 過去の日付は不可
        if reservation_date < today:
            raise ValidationError('過去の日付は選択できません。')
        
        # 6日後までの制限
        max_date = today + timedelta(days=6)
        if reservation_date > max_date:
            raise ValidationError('予約は6日後までしか選択できません。')
        
        # 平日のみ（月曜=0, 日曜=6）
        if reservation_date.weekday() >= 5:  # 土曜=5, 日曜=6
            raise ValidationError('平日（月〜金）のみ予約可能です。')
        
        return reservation_date
    
    def clean_start_time(self):
        """開始時間のバリデーション"""
        start_time_str = self.cleaned_data['start_time']
        
        # 文字列からtime objectに変換
        try:
            hour, minute = map(int, start_time_str.split(':'))
            start_time = time(hour, minute)
        except (ValueError, AttributeError):
            raise ValidationError('正しい時間形式で選択してください。')
        
        return start_time
    
    def clean_end_time(self):
        """終了時間のバリデーション"""
        end_time_str = self.cleaned_data['end_time']
        
        # 文字列からtime objectに変換
        try:
            hour, minute = map(int, end_time_str.split(':'))
            end_time = time(hour, minute)
        except (ValueError, AttributeError):
            raise ValidationError('正しい時間形式で選択してください。')
        
        return end_time
    
    def clean(self):
        """フォーム全体のバリデーション"""
        cleaned_data = super().clean()
        space = cleaned_data.get('space')
        reservation_date = cleaned_data.get('reservation_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if not all([space, reservation_date, start_time, end_time]):
            return cleaned_data
        
        # 開始時間 < 終了時間
        if start_time >= end_time:
            raise ValidationError('終了時間は開始時間より後に設定してください。')
        
        # 最低1時間の利用
        start_datetime = datetime.combine(reservation_date, start_time)
        end_datetime = datetime.combine(reservation_date, end_time)
        duration = end_datetime - start_datetime
        
        if duration.total_seconds() < 3600:  # 1時間 = 3600秒
            raise ValidationError('最低1時間からご利用いただけます。')
        
        # 重複予約チェック
        existing_reservations = Reservation.objects.filter(
            space=space,
            reservation_date=reservation_date,
            status='CONFIRMED'
        ).exclude(pk=self.instance.pk if self.instance else None)
        
        for reservation in existing_reservations:
            # 時間の重複をチェック
            if (start_time < reservation.end_time and end_time > reservation.start_time):
                raise ValidationError(
                    f'選択した時間帯は既に予約されています。'
                    f'（{reservation.start_time.strftime("%H:%M")}〜{reservation.end_time.strftime("%H:%M")}）'
                )
        
        return cleaned_data


class SpaceSearchForm(forms.Form):
    """
    スペース検索フォーム
    
    日付・スペース種別での検索
    """
    
    SPACE_TYPE_CHOICES = [
        ('', 'すべて'),
        ('SEMI_PRIVATE', '半個室'),
        ('PRIVATE', '完全個室'),
    ]
    
    search_date = forms.DateField(
        label='検索日',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    space_type = forms.ChoiceField(
        label='スペース種別',
        choices=SPACE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    def clean_search_date(self):
        """検索日のバリデーション"""
        search_date = self.cleaned_data.get('search_date')
        
        if search_date:
            today = date.today()
            if search_date < today:
                raise ValidationError('過去の日付は検索できません。')
            
            # 6日後までの制限
            max_date = today + timedelta(days=6)
            if search_date > max_date:
                raise ValidationError('6日後までの日付で検索してください。')
        
        return search_date