# 🤖 AI Research Multi Agent

[![CI](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/ci.yml)
[![Daily Report](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/daily-report.yml/badge.svg)](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/daily-report.yml)
[![Weekly Report](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/weekly-report.yml/badge.svg)](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/weekly-report.yml)
[![Monthly Report](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/monthly-report.yml/badge.svg)](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/monthly-report.yml)
[![Claude](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/claude.yml/badge.svg)](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/claude.yml)
[![Gemini CLI](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/gemini.yml/badge.svg)](https://github.com/Yagami360/ai-research-multi-agent/actions/workflows/gemini.yml)

複数 AI Agent のレポートを統合分析し、AIテクノロジードリブンによる個人のスキル成長とビジネス創出のための戦略的アクションプランのレポートを自動生成するマルチ AI Agent です。

- [📅 最新レポート](https://github.com/Yagami360/ai-research-multi-agent/issues?q=is%3Aissue%20label%3Areport)
<!--
- [📊 週次レポート](https://github.com/Yagami360/ai-research-multi-agent/issues?q=is%3Aissue%20label%3Aweekly-report)
- [📈 月次レポート](https://github.com/Yagami360/ai-research-multi-agent/issues?q=is%3Aissue%20label%3Amonthly-report)
-->

## 🎯 概要

このAI Agentは、複数の AI Agentが生成した GitHub Issue レポートを総合的に分析します。

**現在のソース AI Agent：**

1. **[ai-research-multi-agent](https://github.com/Yagami360/ai-research-multi-agent)**
   - AI技術ニュース、企業発表、製品動向
   - OSS/GitHub動向、市場トレンド
   
2. **[ai-paper-catchup-agent](https://github.com/Yagami360/ai-paper-catchup-agent)**
   - 最新AI研究論文、学術動向
   - 技術的ブレークスルー、研究トレンド

これらのソースを統合分析し、以下の観点から実践的なアクションプランを提案します：

### 📚 スキル成長支援
- 今学ぶべき技術・ツールの優先順位付け
- 深掘りすべき研究領域の特定
- 具体的な学習リソースと実装プロジェクト案
- 即実践可能なアクションアイテム

### 💼 ビジネス創出支援
- 注目すべき新規ビジネス機会の発見
- PoC/MVP開発アイデアの提案
- 市場トレンドとビジネスインサイト
- 技術スタックと収益化戦略

## 🚀 使用方法

### ☁️ GitHub Actions で動かす場合

1. **前提条件**: ソースとなる2つの AI Agent リポジトリが既に稼働していること
   - [ai-research-multi-agent](https://github.com/Yagami360/ai-research-multi-agent)
   - [ai-paper-catchup-agent](https://github.com/Yagami360/ai-paper-catchup-agent)

2. GitHub secrets and variables を設定する

    - **Variables**<br>
        - `MODEL_NAME`: 利用するモデル名（推奨: `claude-sonnet-4-20250514`）<br>
            ※ GitHub MCPサーバーを使用するため、Claudeモデルを推奨
        - `ENABLED_MCP_SERVERS`: **必須** - `github` を設定<br>
            GitHub Issueからレポートを取得するために必要

    - **Secrets**<br>
        - `ANTHROPIC_API_KEY`: Claude モデル使用のため**必須**<br>
        - `GITHUB_TOKEN`: 自動設定（ソースリポジトリのIssue取得に使用）<br>

3. 一定期間間隔でワークフローが自動実行され、GitHub Issue に統合分析レポートが自動作成されます

4. （オプション）手動実行したい場合は、ワークフローの `Run workflow` から実行できます

### 💻 ローカル環境で動かす場合

#### 1️⃣ 依存関係のインストール

```bash
# uvのインストール（まだの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# PATHの設定
source $HOME/.local/bin/env

# 依存関係のインストール
make install
```

#### 2️⃣ 環境設定

```bash
# 環境設定ファイルの作成
make setup

# .envファイルを編集してAPIキーと設定を行う
# ANTHROPIC_API_KEY=your_anthropic_api_key_here    # Claude API Key
# MODEL_NAME=claude-sonnet-4-20250514              # Claudeモデル推奨
# ENABLED_MCP_SERVERS=github                       # GitHub MCPサーバー必須
# GITHUB_TOKEN=your_github_token_here              # GitHub Personal Access Token
# GITHUB_REPOSITORY=your_username/your_repo           # 出力先リポジトリ
# MAX_TOKENS=20000                                    # トークン数（分析用に多めを推奨）
```

#### 3️⃣ GitHub CLI認証（GitHub MCPサーバー使用のため必須）

```bash
# GitHub CLIのインストール（まだの場合）
# macOS
brew install gh

# Linux
sudo apt install gh

# 認証
gh auth login
# または環境変数で設定
export GITHUB_TOKEN="your_github_token"
```

#### 4️⃣ 実行

```bash
# 📊 統合分析レポート作成
make run

# 動作確認（Issue作成なし）
make test
```

### 🤖 レポート内容の質疑応答する

作成された Issue レポートの内容について、AI モデルと質疑応答することもできます。

#### Claude と質疑応答する

Issue や PR のコメントで `@claude` とメンションすると、Claude が自動的に日本語で応答します。

**使用例：**
```
@claude この中で最も重要なニュースは何ですか?
@claude OpenAI の最新情報について詳しく教えてください
@claude このレポートの要点を3つにまとめてください
```

#### Gemini と質疑応答する

Issue や PR のコメントで `@gemini-cli` とメンションすると、Gemini が自動的に日本語で応答します。

**使用例：**
```
@gemini-cli Multi-Agent System の実装例を教えてください
@gemini-cli この技術のユースケースは何ですか?
@gemini-cli 今後のトレンドについて教えてください
```

> **Note**: 
> - Claude は `@claude` メンション、Gemini は `@gemini-cli` メンションで呼び出します
> - どちらも Issue コメントおよび PR コメントで利用可能です
> - レポート Issue の内容を理解した上で回答します

## 👨‍💻 開発者向け情報

### 📋 利用可能コマンド

| コマンド | 説明 |
|---------|------|
| `make install` | 📦 依存関係をインストール |
| `make setup` | ⚙️ 開発環境のセットアップ |
| `make run` | 📰 最新レポート作成 |
| `make run-weekly` | 📊 週次レポート生成 |
| `make run-monthly` | 📈 月次レポート生成 |
| `make test` | 🧪 テストを実行 |
| `make lint` | 🔍 コードのリンティング |
| `make format` | ✨ コードのフォーマット |

### 🔌 MCP サーバー統合

AI Research Multi Agent は MCP (Model Context Protocol) サーバーをサポートしており、Claude モデルを使用時に外部ツールやサービスと連携できます。

#### 利用可能な MCP サーバー

1. **GitHub MCP Server** ✅
   - GitHubリポジトリ、Issue、PRへの直接アクセス
   - GitHub Trending からトレンドプロジェクトの取得
   - Code Security アラートの確認

#### MCPサーバーの有効化

**環境変数で設定**:
```bash
# .env ファイルに追加
ENABLED_MCP_SERVERS=github,huggingface
```

**CLIで指定**:
```bash
# GitHub MCP サーバーを使用
uv run python -m src.main --mcp-servers github

# 複数のMCPサーバーを使用
uv run python -m src.main --mcp-servers github,huggingface
```

#### 事前準備

**GitHub MCP Server**:
1. GitHub CLI のインストール:
   ```bash
   # macOS
   brew install gh
   
   # Linux
   sudo apt install gh
   ```

2. 認証:
   ```bash
   gh auth login
   # または
   export GITHUB_TOKEN="your_github_token"
   ```

**Hugging Face MCP Server**:
1. Hugging Face トークンの取得:
   - [Hugging Face Settings](https://huggingface.co/settings/tokens) からアクセストークンを作成
   - トークンタイプは `read` で十分です

2. 環境変数の設定:
   ```bash
   export HF_TOKEN="your_huggingface_token"
   ```

   または `.env` ファイルに追加:
   ```
   HF_TOKEN=your_huggingface_token
   ```

> **Note**: ローカル環境では初回実行時に自動的にログインプロンプトが表示されますが、CI/CD環境では`HF_TOKEN`の設定が必須です

詳細は [`mcp/mcp_servers.yaml`](mcp/mcp_servers.yaml) を参照してください。
