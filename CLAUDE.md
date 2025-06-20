# CLAUDE.md

このファイルはClaude Code (claude.ai/code) がこのリポジトリで作業する際のガイダンスを提供します。

## プロジェクト概要

これはiLスクエア予約システムを作成するDjangoチーム開発研修プロジェクトです。定義フェーズと実施フェーズを含む構造化されたアプローチで、アジャイル/スクラム手法を使用します。

**現在のステータス**: 教育資料、テンプレート、完全実装済みDjangoプロジェクト、および実装完了版ドキュメントが完備されています。`code/`に実装済み手本コード、`総合演習/成果物_結果/`に実装完了版お手本ドキュメントが作成済みです。

## プロジェクト構造

プロジェクトは以下の構造でチーム開発用に組織されています：

### 教育資料
- `総合演習/` - プロジェクト仕様、フェーズ定義、テンプレートを含む
- `00_演習概要.txt` - プロジェクト概要と要件
- `01_定義フェーズ.txt` - 定義フェーズのガイドライン
- `02_実施フェーズ.txt` - 実施フェーズ（スプリント1-3）のガイドライン
- `事例研究_配布用/` - iLスクエア予約システムの詳細仕様書
- `成果物_ひな型/` - 成果物のテンプレート（Excel、Word、PowerPoint）
- `成果物_結果/` - 実装完了版ドキュメント（Markdown形式）

### 完全実装済みDjangoプロジェクト
- `code/` - 実装完了版手本プロジェクト（3ステップ予約フロー）
  - `ilsquare_project/` - Django設定ファイル
  - `accounts/` - ユーザー管理アプリ（メール必須登録）
  - `reservation/` - 予約機能アプリ（3ステップフロー）
  - `templates/` - HTMLテンプレート（レスポンシブ対応）
  - `static/` - 静的ファイル（統合CSS）

### チーム開発用プロジェクト構造
チームは以下の名前でプロジェクトを作成します：
- `team1_project/` (Aチーム)
- `team2_project/` (Bチーム)
- `team3_project/` (Cチーム)
- `team4_project/` (Dチーム)

各チームプロジェクトは`code/`を参考に作成します。

## 開発プロセス

### フェーズ構造
1. **定義フェーズ** (3日間): 要件収集、システム設計、ドキュメント作成
2. **実施フェーズ** (3スプリント): Djangoアプリケーション開発
3. **最終発表**: デモとプロジェクトレビュー

### スプリント手法
- **スプリントプランニング**: 実装するプロダクトバックログアイテム（PBI）を選択
- **デイリースクラム**: 朝夕の進捗更新
- **スプリントレビュー**: プロダクトのデモンストレーションとフィードバック
- **レトロスペクティブ**: KPT分析を使用したチームプロセス改善

## 主要成果物

### 定義フェーズ
- プロジェクト憲章
- ユーザストーリーマップ
- プロダクトバックログ
- 画面遷移図
- モデル構成図
- テストデータ仕様
- ファイル構成計画

### 実施フェーズ
- スプリントバックログ
- モデル定義書
- フォーム定義書
- ビュー定義書
- 画面定義書（詳細）
- システムテスト実施記録
- 動作するDjangoアプリケーション

## 開発ガイドライン

### ドキュメント要件
- すべての成果物は提出時にPDFに変換する必要があります
- すべての変更について変更管理ログを維持
- バグ管理シートでバグと解決策を追跡
- スプリントバックログを毎日更新

### チーム組織
- 各チームには指定された役割と責任があります
- メイン講師への定期的な進捗報告
- 顧客役：メイン講師（馬場様）
- 上司役：講師陣（高田部長）

### 実装済み対象システム機能
- iLスクエア施設のWebベース予約システム（完全実装済み）
- ユーザー登録と認証（メールアドレス必須）
- 個人学習室（半個室・完全個室）の予約管理（3ステップフロー）
- 現金・PayPay支払い対応
- レスポンシブデザイン（マルチデバイス対応）
- 重複予約防止・エラーハンドリング

## ファイル命名規則

### 進捗報告
- 形式: `MMDD_[ファイル名]` (例: `0616_sprint1_backlog.pdf`)
- `00_進捗報告`フォルダに提出

### チームプロジェクト
- 指定されたチームフォルダ名を使用（`team1_project`、`team2_project`など）
- `empty_project`テンプレートを基に新しいプロジェクトを作成

## 品質保証

### テスト要件
- スプリントリリース前にシステムテストを完了する必要があります
- テストシナリオを文書化し実行
- 提出前にアプリケーションが期待通りに動作することを確認

### 提出プロセス
- Djangoアプリケーション: ZIPファイルとして提出
- ドキュメント: PDF形式に変換
- スプリント終了日までに指定フォルダに提出

## スケジュール (2024年)
- 06/11-06/13: 定義フェーズ
- 06/16-06/20: スプリント1
- 06/23-06/27: スプリント2
- 06/30-07/02: スプリント3
- 07/03: 最終発表

## 開発環境

### 必要なツール
- Python 3.11+
- uv (Pythonパッケージマネージャー)
- pandoc（ドキュメント変換）
- openpyxl（Excelファイル読み込み）

### 実装済みプロジェクトの起動
```bash
cd code
uv sync                                    # 依存関係のインストール
uv run python manage.py migrate           # データベース初期化
uv run python manage.py create_sample_data # サンプルデータ作成
uv run python manage.py runserver         # 開発サーバー起動
```

### 開発・管理コマンド
```bash
# 新しいアプリの作成
uv run python manage.py startapp app_name

# マイグレーション
uv run python manage.py makemigrations
uv run python manage.py migrate

# 管理者ユーザー作成
uv run python manage.py createsuperuser

# サンプルデータ作成（実装済み）
uv run python manage.py create_sample_data

# テスト実行
uv run python manage.py test
```

## 実装完了プロジェクト詳細

### 実装済みプロジェクト（`code/`）
- **Django 5.2.3** を使用した完全実装版
- **日本語・東京タイムゾーン** 設定済み
- **accounts（ユーザー管理）** - メールアドレス必須登録、ログイン、プロフィール管理
- **reservation（予約機能）** - 3ステップ予約フロー完全実装
- **レスポンシブデザイン** - モバイル・タブレット・デスクトップ対応
- **支払い機能** - 現金・PayPay対応、整数表示統一
- **エラーハンドリング** - 重複予約防止、バリデーション、例外処理
- **サンプルデータ** - 自動生成コマンド実装済み

### 実装済み機能一覧
1. **3ステップ予約フロー**
   - ステップ1: 日付選択（平日のみ、カレンダー表示）
   - ステップ2: スペース・開始時刻選択（動的UI）
   - ステップ2.5: 終了時刻選択・料金計算（整数表示）
   - ステップ3: 予約確認・利用目的入力
   - 完了: 予約完了・マイページ連携

2. **ユーザー管理機能**
   - 新規登録（メールアドレス必須）
   - ログイン・ログアウト
   - マイページ（予約一覧・管理）
   - プロフィール管理

3. **予約管理機能**
   - 予約作成・確認・キャンセル
   - 予約履歴表示
   - 重複予約防止
   - 営業時間・平日制限

4. **システム機能**
   - セッション管理（マルチステップ対応）
   - データベース設計（User, Space, Reservation, Payment）
   - 管理画面（Django Admin）
   - 静的ファイル管理（CSS統合）

### チームプロジェクト開発時の参考事項
- **完全実装版の活用**: `code/`は動作する完成品として参考可能
- **段階的実装**: 3ステップフローを参考に段階的な開発手法を学習
- **ドキュメント作成**: `総合演習/成果物_結果/`フォルダの実装完了版ドキュメントを参考
- **テスト手法**: システムテスト実施記録を参考にテスト計画作成
- **品質管理**: エラーハンドリングとユーザビリティの実装例を参考
- **プロジェクト管理**: 実装記録とKPT分析の手法を参考

### 技術スタック・ツール
- **Backend**: Django 5.2.3, Python 3.11
- **Frontend**: HTML5, CSS3, JavaScript（レスポンシブデザイン）
- **Database**: SQLite（開発用）
- **Package Manager**: uv
- **Version Control**: Git
- **Documentation**: Markdown（実装完了版）