# accounts/forms.py
# アカウント関連のフォーム定義

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    カスタムユーザー登録フォーム
    
    ID・氏名・電話番号のみのシンプルな登録フォーム
    """
    
    # フィールドの追加設定
    username = forms.CharField(
        label='ユーザーID',
        max_length=30,
        help_text='英数字30文字以内で入力してください',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'tanaka01'
        })
    )
    
    first_name = forms.CharField(
        label='名',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '一郎'
        })
    )
    
    last_name = forms.CharField(
        label='姓',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '田中'
        })
    )
    
    email = forms.EmailField(
        label='メールアドレス',
        required=True,
        help_text='連絡用のメールアドレスを入力してください',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'user@example.com'
        })
    )
    
    phone_number = forms.CharField(
        label='電話番号',
        max_length=20,
        help_text='ハイフンありなしどちらでも可（例: 090-1234-5678）',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '090-1234-5678'
        })
    )
    
    password1 = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'パスワードを入力'
        }),
        help_text='8文字以上で入力してください'
    )
    
    password2 = forms.CharField(
        label='パスワード（確認）',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'パスワードを再入力'
        }),
        help_text='確認のため同じパスワードを入力してください'
    )
    
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'phone_number', 'password1', 'password2')
    
    def clean_phone_number(self):
        """電話番号のバリデーション"""
        phone_number = self.cleaned_data['phone_number']
        
        # ハイフンを除去して数字のみにする
        phone_digits = ''.join(filter(str.isdigit, phone_number))
        
        # 11桁（携帯）または10桁（固定）をチェック
        if len(phone_digits) not in [10, 11]:
            raise forms.ValidationError('電話番号は10桁または11桁で入力してください')
        
        return phone_number
    
    def save(self, commit=True):
        """ユーザー作成時の処理"""
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    カスタムログインフォーム
    
    ユーザーIDとパスワードでのシンプルなログイン
    """
    
    username = forms.CharField(
        label='ユーザーID',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ユーザーIDを入力',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'パスワードを入力'
        })
    )
    
    error_messages = {
        'invalid_login': 'ユーザーIDまたはパスワードが正しくありません。',
        'inactive': 'このアカウントは無効です。',
    }