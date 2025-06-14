# iLスクエア予約システム

Django初心者向けのチーム開発演習プロジェクトです。

## プロジェクト概要

iLスクエア（学習スペース）の予約システムを開発します。
ユーザーは半個室や完全個室を時間単位で予約できます。

### 主な機能

- **ユーザー登録・ログイン**: ID・氏名・メールアドレス・電話番号でのシンプルな登録
- **予約申込**: 日付選択→スペース選択→時刻選択の3ステップ予約フロー
- **予約管理**: 予約履歴・キャンセル（前日まで）
- **プロフィール管理**: 登録情報の確認・変更
- **支払い**: 現金またはPayPay決済

### 予約の流れ

1. **日付選択**: 利用したい日付を平日カレンダーから選択
2. **スペース選択**: 用途に合わせて半個室または完全個室を選択
3. **時刻選択**: 9:00-18:00の間で開始・終了時刻を指定

### スペース種別

- **個人スペース（半個室）**: 500円/時間 - デスクが広めで演習に適したスペース
- **個人スペース（完全個室）**: 1,000円/時間 - 防音・吸音仕様の完全個室

## 開発環境セットアップ

### 1. 仮想環境の確認
```bash
# uvが正しく設定されているか確認
uv --version
```

### 2. データベースのマイグレーション
```bash
# プロジェクトディレクトリに移動
cd /Users/miyauchi/src/claude-code/ilearning/code

# マイグレーションファイルを作成
uv run python manage.py makemigrations

# データベースに適用
uv run python manage.py migrate
```

### 3. 管理者ユーザーの作成
```bash
# スーパーユーザーを作成
uv run python manage.py createsuperuser
```

### 4. サンプルデータの投入
```bash
# スペース・ユーザー・予約のサンプルデータを作成
uv run python manage.py create_sample_data
```

### 5. 開発サーバーの起動
```bash
# サーバーを起動
uv run python manage.py runserver
```

ブラウザで http://127.0.0.1:8000/ にアクセスしてください。

## サンプルユーザー

サンプルデータ投入後、以下のユーザーでログインできます：

| ユーザーID | パスワード | 氏名 |
|------------|------------|------|
| tanaka01 | password123 | 田中一郎 |
| sato02 | password123 | 佐藤花子 |
| yamada03 | password123 | 山田太郎 |
| suzuki04 | password123 | 鈴木美咲 |
| takahashi05 | password123 | 高橋健太 |

## プロジェクト構成

```
ilsquare_project/
├── accounts/              # ユーザー管理アプリ
│   ├── models.py         # カスタムユーザーモデル
│   ├── views.py          # ログイン・登録・マイページ・プロフィール
│   ├── forms.py          # ユーザー登録・ログインフォーム
│   └── urls.py           # アカウント関連URL
├── reservation/           # 予約システムアプリ
│   ├── models.py         # Space, Reservation, Payment
│   ├── views.py          # 予約（4ステップ）・予約履歴
│   ├── forms.py          # 予約フォーム
│   └── urls.py           # 予約関連URL
├── templates/             # HTMLテンプレート
│   ├── base.html         # ベーステンプレート（ヘッダー・フッター）
│   ├── accounts/         # アカウント関連テンプレート
│   └── reservation/      # 予約関連テンプレート
├── static/
│   └── css/
│       └── style.css     # メインスタイルシート
└── manage.py
```

## 主要なファイル説明

### モデル (reservation/models.py)

- **User**: カスタムユーザーモデル（電話番号・メールアドレス追加）
- **Space**: スペース情報（半個室・完全個室）
- **Reservation**: 予約情報
- **Payment**: 支払い情報（現金・PayPay対応）

### ビュー (accounts/views.py, reservation/views.py)

- **top_view**: トップページ
- **register_view**: ユーザー登録
- **login_view**: ログイン
- **mypage_view**: マイページ
- **profile_view**: プロフィール確認・編集
- **reserve_step1_view**: 予約ステップ1（日付選択）
- **reserve_step2_view**: 予約ステップ2（スペース選択）
- **reserve_step2_5_view**: 予約ステップ2.5（終了時刻選択）
- **reserve_step3_view**: 予約ステップ3（予約確認）
- **reserve_complete_view**: 予約ステップ4（完了）
- **reservations_view**: 予約履歴

### フォーム (accounts/forms.py, reservation/forms.py)

- **CustomUserCreationForm**: ユーザー登録フォーム（メールアドレス必須）
- **CustomAuthenticationForm**: ログインフォーム  
- **ReservationForm**: 予約申込フォーム

## 画面構成

### ログイン前
- **トップページ**: サービス紹介・予約の流れ
- **ユーザー登録**: ID・氏名・メールアドレス・電話番号・パスワード
- **ログイン**: ユーザーID・パスワード

### ログイン後
- **マイページ**: 新規予約・予約履歴・プロフィールへのアクセス
- **予約フロー**: 
  1. 日付選択
  2. スペース選択
  3. 時刻選択  
  4. 予約確認
  5. 完了
- **予約履歴**: 現在の予約・過去の予約
- **プロフィール**: 登録情報の確認・変更

## 開発のポイント

### 1. Django初心者向けの設計

- シンプルなモデル構成
- わかりやすいビュー関数
- 丁寧なコメント
- 基本的なバリデーション

### 2. ユーザビリティ重視

- 直感的な3ステップ予約フロー
- 進行状況の可視化
- 分かりやすいエラーメッセージ
- レスポンシブデザイン

### 3. 日本語対応

- settings.py で日本語・東京タイムゾーン設定
- 日本語のラベル・メッセージ
- 日本の電話番号形式対応

### 4. セキュリティ

- CSRF保護
- ログイン必須画面の設定
- 入力値のバリデーション

## 拡張可能な機能

受講者のレベルに応じて以下の機能を追加できます：

- **管理者機能**: ユーザー・スペースのCRUD操作
- **予約検索**: 日付・スペース種別での検索
- **通知機能**: メール・SMS通知
- **決済機能**: 本格的な決済システム連携
- **API機能**: REST APIの実装
- **レポート機能**: 利用統計・売上レポート

## トラブルシューティング

### マイグレーションエラー
```bash
# マイグレーションをリセット
uv run python manage.py migrate --run-syncdb
```

### 静的ファイルが読み込まれない
```bash
# 静的ファイルを収集
uv run python manage.py collectstatic
```

### サンプルデータを再作成
```bash
# 既存データを削除してから再実行
uv run python manage.py create_sample_data
```

## 学習リソース

- [Django公式ドキュメント](https://docs.djangoproject.com/ja/5.2/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/ja/)
- [プロジェクト仕様書](../総合演習/成果物_結果/)

---

**作成者**: Aチーム  
**更新日**: 2025年6月14日