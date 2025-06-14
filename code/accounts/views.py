# accounts/views.py
# アカウント関連のビュー（画面表示・処理）

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def register_view(request):
    """
    ユーザー登録画面
    
    GET: 登録フォームを表示
    POST: ユーザー登録処理
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # ユーザーを作成
            user = form.save()
            
            # 登録後は自動ログイン
            login(request, user)
            
            # 成功メッセージ
            messages.success(request, f'{user.username}さん、登録が完了しました！')
            
            # マイページにリダイレクト
            return redirect('mypage')
        else:
            # エラーメッセージ
            messages.error(request, '入力に不備があります。確認してください。')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    ログイン画面
    
    GET: ログインフォームを表示
    POST: ログイン処理
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 認証情報を取得
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # ユーザー認証
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # ログイン実行
                login(request, user)
                
                # 成功メッセージ
                messages.success(request, f'{user.username}さん、ログインしました！')
                
                # 次のページへリダイレクト（指定がなければマイページ）
                next_page = request.GET.get('next', 'mypage')
                return redirect(next_page)
        else:
            # エラーメッセージ
            messages.error(request, 'ユーザーIDまたはパスワードが正しくありません。')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(['POST'])
def logout_view(request):
    """
    ログアウト処理（POSTのみ）
    """
    logout(request)
    messages.success(request, 'ログアウトしました。')
    return redirect('top')


@login_required
def mypage_view(request):
    """
    マイページ画面（ログイン必須）
    
    ユーザーの予約状況やメニューを表示
    """
    # ユーザーの現在の予約を取得
    from reservation.models import Reservation
    from django.utils import timezone
    
    current_reservations = Reservation.objects.filter(
        user=request.user,
        status='CONFIRMED',
        reservation_date__gte=timezone.now().date()
    ).order_by('reservation_date', 'start_time')[:5]  # 最大5件
    
    context = {
        'user': request.user,
        'current_reservations': current_reservations,
    }
    
    return render(request, 'accounts/mypage.html', context)


@login_required
def profile_view(request):
    """
    プロフィール確認・編集画面（ログイン必須）
    """
    if request.method == 'POST':
        # プロフィール更新処理
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        
        if first_name and last_name and email and phone_number:
            # ユーザー情報を更新
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
            user.save()
            
            messages.success(request, 'プロフィールを更新しました。')
            return redirect('profile')
        else:
            messages.error(request, 'すべての項目を入力してください。')
    
    return render(request, 'accounts/profile.html', {'user': request.user})