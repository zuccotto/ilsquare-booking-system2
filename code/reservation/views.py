# reservation/views.py
# 予約システム関連のビュー（画面表示・処理）

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import date, datetime, timedelta, time
from .models import Space, Reservation, Payment
from .forms import ReservationForm


def top_view(request):
    """
    トップページ
    
    サービス概要とスペース紹介を表示
    """
    # 利用可能なスペースを取得
    spaces = Space.objects.filter(is_available=True).order_by('space_type', 'name')
    
    # スペース種別ごとに分ける
    semi_private_spaces = spaces.filter(space_type='SEMI_PRIVATE')
    private_spaces = spaces.filter(space_type='PRIVATE')
    
    context = {
        'semi_private_spaces': semi_private_spaces,
        'private_spaces': private_spaces,
    }
    
    return render(request, 'reservation/top.html', context)




@login_required
def reserve_step1_view(request):
    """
    予約ステップ1: 利用可能日付選択画面（ログイン必須）
    
    6日前までの平日リストから利用日を選択
    """
    # 今日から6日後までの平日を生成
    today = date.today()
    available_dates = []
    
    for i in range(6):
        target_date = today + timedelta(days=i)
        # 平日のみ（土曜日=5, 日曜日=6を除く）
        if target_date.weekday() < 5:
            available_dates.append({
                'date': target_date,
                'date_string': target_date.strftime('%Y-%m-%d'),
                'display_string': target_date.strftime('%m月%d日（%a）'),
                'full_display': target_date.strftime('%Y年%m月%d日（%a）')
            })
    
    context = {
        'available_dates': available_dates,
    }
    
    return render(request, 'reservation/reserve_step1.html', context)


@login_required
def reserve_step2_view(request, date_string):
    """
    予約ステップ2: スペース選択・時間選択画面（ログイン必須）
    
    選択した日付でのスペース選択と時間帯選択
    """
    try:
        reservation_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, '無効な日付です。')
        return redirect('reserve_step1')
    
    # 日付の妥当性チェック
    today = date.today()
    if reservation_date < today or reservation_date > today + timedelta(days=6):
        messages.error(request, '選択できない日付です。')
        return redirect('reserve_step1')
    
    if reservation_date.weekday() >= 5:
        messages.error(request, '平日のみ予約可能です。')
        return redirect('reserve_step1')
    
    # 利用可能なスペースを取得
    spaces = Space.objects.filter(is_available=True).order_by('space_type', 'name')
    
    # その日の既存予約を取得
    existing_reservations = Reservation.objects.filter(
        reservation_date=reservation_date,
        status='CONFIRMED'
    ).select_related('space')
    
    # 各スペースの時間帯別予約状況を準備
    spaces_with_availability = []
    for space in spaces:
        time_slots = []
        for hour in range(9, 18):  # 9:00-18:00
            start_time = time(hour, 0)
            end_time = time(hour + 1, 0)
            
            # この時間帯にこのスペースの予約があるかチェック
            is_available = not existing_reservations.filter(
                space=space,
                start_time__lte=start_time,
                end_time__gt=start_time
            ).exists()
            
            time_slots.append({
                'start_time': start_time,
                'end_time': end_time,
                'start_time_str': f"{hour:02d}:00",
                'end_time_str': f"{hour+1:02d}:00",
                'is_available': is_available,
                'slot_id': f"{hour:02d}_{space.id}"
            })
        
        spaces_with_availability.append({
            'space': space,
            'time_slots': time_slots,
            'available_slots_count': sum(1 for slot in time_slots if slot['is_available'])
        })
    
    context = {
        'reservation_date': reservation_date,
        'date_string': date_string,
        'date_display': reservation_date.strftime('%Y年%m月%d日（%a）'),
        'spaces_with_availability': spaces_with_availability,
    }
    
    return render(request, 'reservation/reserve_step2.html', context)


@login_required
def reserve_step2_5_view(request, date_string, space_id, start_time):
    """
    予約ステップ2.5: 終了時刻選択画面（ログイン必須）
    
    選択されたスペースと開始時刻に基づいて終了時刻を選択
    """
    try:
        reservation_date = datetime.strptime(date_string, '%Y-%m-%d').date()
        start_time_obj = datetime.strptime(start_time, '%H:%M').time()
        space = Space.objects.get(id=space_id, is_available=True)
    except (ValueError, Space.DoesNotExist):
        messages.error(request, '無効なパラメータです。')
        return redirect('reserve_step1')
    
    # 日付の妥当性チェック
    today = date.today()
    if reservation_date < today or reservation_date > today + timedelta(days=6):
        messages.error(request, '選択できない日付です。')
        return redirect('reserve_step1')
    
    if reservation_date.weekday() >= 5:
        messages.error(request, '平日のみ予約可能です。')
        return redirect('reserve_step1')
    
    # その日の既存予約を取得
    existing_reservations = Reservation.objects.filter(
        space=space,
        reservation_date=reservation_date,
        status='CONFIRMED'
    )
    
    # 開始時刻から選択可能な終了時刻を計算
    available_end_times = []
    start_hour = start_time_obj.hour
    
    for hour in range(start_hour + 1, 19):  # 開始時刻の次の時間から18:00まで
        end_time_obj = time(hour, 0)
        
        # この時間帯に予約が重複していないかチェック
        conflict = existing_reservations.filter(
            start_time__lt=end_time_obj,
            end_time__gt=start_time_obj
        ).exists()
        
        if not conflict:
            duration = hour - start_hour
            amount = int(space.hourly_rate * duration)
            available_end_times.append({
                'time': end_time_obj,
                'time_str': f"{hour:02d}:00",
                'duration': duration,
                'amount': amount
            })
        else:
            # 予約が重複している場合は、それ以降の時間は選択不可
            break
    
    context = {
        'reservation_date': reservation_date,
        'date_string': date_string,
        'date_display': reservation_date.strftime('%Y年%m月%d日（%a）'),
        'space': space,
        'start_time': start_time_obj,
        'start_time_str': start_time,
        'available_end_times': available_end_times,
    }
    
    return render(request, 'reservation/reserve_step2_5.html', context)


@login_required
def reserve_step3_view(request):
    """
    予約ステップ3: 予約確認画面（ログイン必須）
    
    選択内容の確認と最終予約処理
    """
    if request.method != 'POST':
        messages.error(request, '無効なアクセスです。')
        return redirect('reserve_step1')
    
    # POSTデータから選択内容を取得
    date_string = request.POST.get('date')
    space_id = request.POST.get('space_id')
    start_time_str = request.POST.get('start_time')
    end_time_str = request.POST.get('end_time')
    
    if not all([date_string, space_id, start_time_str, end_time_str]):
        messages.error(request, '必要な情報が不足しています。')
        return redirect('reserve_step1')
    
    try:
        reservation_date = datetime.strptime(date_string, '%Y-%m-%d').date()
        start_time_obj = datetime.strptime(start_time_str, '%H:%M').time()
        end_time_obj = datetime.strptime(end_time_str, '%H:%M').time()
        space = Space.objects.get(id=space_id, is_available=True)
    except (ValueError, Space.DoesNotExist):
        messages.error(request, '無効な選択内容です。')
        return redirect('reserve_step1')
    
    # 利用時間数と料金を計算
    start_datetime = datetime.combine(reservation_date, start_time_obj)
    end_datetime = datetime.combine(reservation_date, end_time_obj)
    duration_seconds = (end_datetime - start_datetime).total_seconds()
    duration_hours = int(duration_seconds / 3600)
    total_amount = int(space.hourly_rate * duration_hours)
    
    # 予約データを作成
    reservation_data = {
        'space': space,
        'start_time': start_time_obj,
        'end_time': end_time_obj,
        'duration': duration_hours,
        'amount': total_amount
    }
    
    context = {
        'reservation_date': reservation_date,
        'date_string': date_string,
        'date_display': reservation_date.strftime('%Y年%m月%d日（%a）'),
        'reservation_data': reservation_data,
        'total_amount': total_amount,
        'space_id': space_id,
        'start_time_str': start_time_str,
        'end_time_str': end_time_str,
    }
    
    return render(request, 'reservation/reserve_step3.html', context)


@login_required
def reserve_complete_view(request):
    """
    予約ステップ4: 予約完了処理（ログイン必須）
    
    最終的な予約作成と完了画面表示
    """
    if request.method != 'POST':
        messages.error(request, '無効なアクセスです。')
        return redirect('reserve_step1')
    
    # POSTデータから選択内容を取得
    date_string = request.POST.get('date')
    space_id = request.POST.get('space_id')
    start_time_str = request.POST.get('start_time')
    end_time_str = request.POST.get('end_time')
    
    if not all([date_string, space_id, start_time_str, end_time_str]):
        messages.error(request, '予約内容が正しくありません。')
        return redirect('reserve_step1')
    
    try:
        reservation_date = datetime.strptime(date_string, '%Y-%m-%d').date()
        start_time_obj = datetime.strptime(start_time_str, '%H:%M').time()
        end_time_obj = datetime.strptime(end_time_str, '%H:%M').time()
        space = Space.objects.get(id=space_id, is_available=True)
    except (ValueError, Space.DoesNotExist):
        messages.error(request, '無効な選択内容です。')
        return redirect('reserve_step1')
    
    # 利用時間数と料金を計算
    start_datetime = datetime.combine(reservation_date, start_time_obj)
    end_datetime = datetime.combine(reservation_date, end_time_obj)
    duration_seconds = (end_datetime - start_datetime).total_seconds()
    duration_hours = int(duration_seconds / 3600)
    total_amount = int(space.hourly_rate * duration_hours)
    
    try:
        # 重複チェック
        existing = Reservation.objects.filter(
            space=space,
            reservation_date=reservation_date,
            start_time__lt=end_time_obj,
            end_time__gt=start_time_obj,
            status='CONFIRMED'
        ).exists()
        
        if existing:
            raise Exception(f'{space.name}の{start_time_str}-{end_time_str}は既に予約されています。')
        
        # 予約作成
        reservation = Reservation.objects.create(
            user=request.user,
            space=space,
            reservation_date=reservation_date,
            start_time=start_time_obj,
            end_time=end_time_obj,
            total_amount=total_amount,
            status='CONFIRMED'
        )
        
        # 支払い情報を作成
        Payment.objects.create(
            reservation=reservation,
            amount=total_amount,
            payment_method='CASH',
            payment_status='PENDING'
        )
        
        messages.success(request, '予約が完了しました！')
        
        context = {
            'reservations': [reservation],
            'reservation_date': reservation_date,
            'date_display': reservation_date.strftime('%Y年%m月%d日（%a）'),
            'total_amount': total_amount,
        }
        
        return render(request, 'reservation/reserve_complete.html', context)
        
    except Exception as e:
        messages.error(request, f'予約処理中にエラーが発生しました: {str(e)}')
        return redirect('reserve_step1')


@login_required
def reserve_view(request):
    """
    旧予約申込画面（互換性のため残す）
    
    新しい予約フローへリダイレクト
    """
    return redirect('reserve_step1')


@login_required
def reservation_detail_view(request, reservation_id):
    """
    予約詳細確認画面（ログイン必須）
    
    予約内容と支払い状況を表示
    """
    reservation = get_object_or_404(
        Reservation, 
        id=reservation_id, 
        user=request.user
    )
    
    context = {
        'reservation': reservation,
    }
    
    return render(request, 'reservation/reservation_detail.html', context)


@login_required
def reservations_view(request):
    """
    予約一覧画面（ログイン必須）
    
    ユーザーの予約履歴を表示
    """
    # 現在の予約（今日以降）
    current_reservations = Reservation.objects.filter(
        user=request.user,
        reservation_date__gte=timezone.now().date()
    ).order_by('reservation_date', 'start_time')
    
    # 過去の予約
    past_reservations = Reservation.objects.filter(
        user=request.user,
        reservation_date__lt=timezone.now().date()
    ).order_by('-reservation_date', '-start_time')[:10]  # 最新10件
    
    context = {
        'current_reservations': current_reservations,
        'past_reservations': past_reservations,
    }
    
    return render(request, 'reservation/reservations.html', context)


@login_required
def cancel_reservation_view(request, reservation_id):
    """
    予約キャンセル処理（ログイン必須）
    
    前日まで予約をキャンセル可能
    """
    reservation = get_object_or_404(
        Reservation, 
        id=reservation_id, 
        user=request.user,
        status='CONFIRMED'
    )
    
    # 前日までキャンセル可能
    today = timezone.now().date()
    if reservation.reservation_date <= today:
        messages.error(request, '前日までの予約のみキャンセル可能です。')
        return redirect('reservations')
    
    if request.method == 'POST':
        # キャンセル処理
        reservation.status = 'CANCELLED'
        reservation.save()
        
        # 支払い情報も更新
        if hasattr(reservation, 'payment'):
            payment = reservation.payment
            payment.payment_status = 'CANCELLED'
            payment.amount = 0
            payment.save()
        
        messages.success(request, '予約をキャンセルしました。')
        return redirect('reservations')
    
    context = {
        'reservation': reservation,
    }
    
    return render(request, 'reservation/cancel_reservation.html', context)