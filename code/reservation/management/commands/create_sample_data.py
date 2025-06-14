# reservation/management/commands/create_sample_data.py
# 初期データ（サンプルスペース）を作成するコマンド

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reservation.models import Space, Reservation, Payment
from decimal import Decimal
from datetime import date, time, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'サンプルデータ（スペース・ユーザー・予約）を作成します'

    def handle(self, *args, **options):
        self.stdout.write('サンプルデータを作成しています...')

        # 既存データの削除
        Space.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('既存のサンプルデータを削除しました')

        # スペースデータの作成
        spaces_data = [
            # 半個室（4ブース）
            {
                'name': '半個室A',
                'space_type': 'SEMI_PRIVATE',
                'capacity': 1,
                'equipment': 'ノートPC、外付けモニター、ヘッドセット',
                'hourly_rate': Decimal('500.00'),
                'description': 'デスクが広めで演習に適したスペース',
                'is_available': True
            },
            {
                'name': '半個室B',
                'space_type': 'SEMI_PRIVATE',
                'capacity': 1,
                'equipment': 'ノートPC、外付けモニター、ヘッドセット',
                'hourly_rate': Decimal('500.00'),
                'description': 'デスクが広めで演習に適したスペース',
                'is_available': True
            },
            {
                'name': '半個室C',
                'space_type': 'SEMI_PRIVATE',
                'capacity': 1,
                'equipment': 'ノートPC、外付けモニター、ヘッドセット',
                'hourly_rate': Decimal('500.00'),
                'description': 'デスクが広めで演習に適したスペース',
                'is_available': True
            },
            {
                'name': '半個室D',
                'space_type': 'SEMI_PRIVATE',
                'capacity': 1,
                'equipment': 'ノートPC、外付けモニター、ヘッドセット',
                'hourly_rate': Decimal('500.00'),
                'description': 'デスクが広めで演習に適したスペース',
                'is_available': True
            },
            
            # 完全個室（6ブース）
            {
                'name': '完全個室A',
                'space_type': 'PRIVATE',
                'capacity': 1,
                'equipment': 'ノートPC、外付けモニター、ヘッドセット',
                'hourly_rate': Decimal('1000.00'),
                'description': '防音・吸音仕様の完全個室',
                'is_available': True
            },
            {
                'name': '完全個室B',
                'space_type': 'PRIVATE',
                'capacity': 1,
                'equipment': 'ノートPC、外付けモニター、ヘッドセット',
                'hourly_rate': Decimal('1000.00'),
                'description': '防音・吸音仕様の完全個室',
                'is_available': True
            },
            {
                'name': '完全個室C',
                'space_type': 'PRIVATE',
                'capacity': 1,
                'equipment': 'ノートPC、外付けモニター、ヘッドセット',
                'hourly_rate': Decimal('1000.00'),
                'description': '防音・吸音仕様の完全個室',
                'is_available': True
            },
            {
                'name': '完全個室D',
                'space_type': 'PRIVATE',
                'capacity': 1,
                'equipment': 'ノートPC、外付けモニター、ヘッドセット',
                'hourly_rate': Decimal('1000.00'),
                'description': '防音・吸音仕様の完全個室',
                'is_available': True
            },
            {
                'name': '完全個室E',
                'space_type': 'PRIVATE',
                'capacity': 1,
                'equipment': 'ノートPC、外付けモニター、ヘッドセット',
                'hourly_rate': Decimal('1000.00'),
                'description': '防音・吸音仕様の完全個室',
                'is_available': True
            },
            {
                'name': '完全個室F',
                'space_type': 'PRIVATE',
                'capacity': 1,
                'equipment': 'ノートPC、外付けモニター、ヘッドセット',
                'hourly_rate': Decimal('1000.00'),
                'description': '防音・吸音仕様の完全個室',
                'is_available': False  # メンテナンス中
            }
        ]

        for space_data in spaces_data:
            space = Space.objects.create(**space_data)
            self.stdout.write(f'スペース "{space.name}" を作成しました')

        # サンプルユーザーの作成
        users_data = [
            {
                'username': 'tanaka01',
                'first_name': '一郎',
                'last_name': '田中',
                'phone_number': '090-1234-5678',
                'password': 'password123'
            },
            {
                'username': 'sato02',
                'first_name': '花子',
                'last_name': '佐藤',
                'phone_number': '080-2345-6789',
                'password': 'password123'
            },
            {
                'username': 'yamada03',
                'first_name': '太郎',
                'last_name': '山田',
                'phone_number': '070-3456-7890',
                'password': 'password123'
            },
            {
                'username': 'suzuki04',
                'first_name': '美咲',
                'last_name': '鈴木',
                'phone_number': '090-4567-8901',
                'password': 'password123'
            },
            {
                'username': 'takahashi05',
                'first_name': '健太',
                'last_name': '高橋',
                'phone_number': '080-5678-9012',
                'password': 'password123'
            }
        ]

        for user_data in users_data:
            user = User.objects.create_user(**user_data)
            self.stdout.write(f'ユーザー "{user.username}" を作成しました')

        # サンプル予約の作成（今日から数日後）
        today = date.today()
        spaces = list(Space.objects.filter(is_available=True))
        users = list(User.objects.filter(is_superuser=False))

        reservations_data = [
            {
                'user': users[0],
                'space': spaces[0],  # 半個室A
                'reservation_date': today + timedelta(days=2),
                'start_time': time(9, 0),
                'end_time': time(11, 0),
                'purpose': 'プレゼン資料作成',
                'status': 'CONFIRMED',
                'total_amount': Decimal('1000.00')  # 2時間 × 500円
            },
            {
                'user': users[1],
                'space': spaces[4],  # 完全個室A
                'reservation_date': today + timedelta(days=2),
                'start_time': time(13, 0),
                'end_time': time(15, 0),
                'purpose': 'オンライン会議',
                'status': 'CONFIRMED',
                'total_amount': Decimal('2000.00')  # 2時間 × 1000円
            },
            {
                'user': users[2],
                'space': spaces[1],  # 半個室B
                'reservation_date': today + timedelta(days=3),
                'start_time': time(10, 0),
                'end_time': time(12, 0),
                'purpose': 'システム開発作業',
                'status': 'CONFIRMED',
                'total_amount': Decimal('1000.00')  # 2時間 × 500円
            }
        ]

        for reservation_data in reservations_data:
            # 予約日が平日かチェック
            if reservation_data['reservation_date'].weekday() < 5:
                reservation = Reservation.objects.create(**reservation_data)
                
                # 支払い情報も作成
                Payment.objects.create(
                    reservation=reservation,
                    amount=reservation.total_amount,
                    payment_method='CREDIT',
                    payment_status='COMPLETED',
                    transaction_id=f'TXN_{reservation.id:08d}'
                )
                
                self.stdout.write(
                    f'予約 "{reservation.user.username} - {reservation.space.name}" を作成しました'
                )

        self.stdout.write(
            self.style.SUCCESS('サンプルデータの作成が完了しました！')
        )
        self.stdout.write('')
        self.stdout.write('作成されたデータ:')
        self.stdout.write(f'- スペース: {Space.objects.count()}件')
        self.stdout.write(f'- ユーザー: {User.objects.filter(is_superuser=False).count()}件')
        self.stdout.write(f'- 予約: {Reservation.objects.count()}件')
        self.stdout.write('')
        self.stdout.write('テストユーザーのログイン情報:')
        for user_data in users_data:
            self.stdout.write(f'- ID: {user_data["username"]}, パスワード: {user_data["password"]}')