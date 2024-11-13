---
title: langchain-sandbox
emoji: 🔗
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: mit
---


<p align="center">
  <img src="docs/langchain-sandbox.png" width="100%">
  <h1 align="center">🔗 langchain-sandbox</h1>
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/langchain-sandbox">
    <img alt="GitHub Repo" src="https://img.shields.io/badge/github-langchain--sandbox-blue?logo=github">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/langchain-sandbox/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/langchain-sandbox?color=green">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/langchain-sandbox/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/langchain-sandbox?style=social">
  </a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.8%2B-blue">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/LangChain-2F4F4F?style=for-the-badge&logo=chainlink" alt="LangChain">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai" alt="OpenAI">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
</p>

## 🚀 プロジェクト概要

langchain-sandboxは、LangChainの様々な機能、特にRunnableを活用したAI処理システムの実装例を提供するサンドボックスプロジェクトです。このリポジトリは、LangChainを使用した実践的な開発パターンとベストプラクティスを学ぶための教育リソースとして機能します。

## 🎯 目的

- LangChainのRunnableシステムの実践的な使用例の提供
- 段階的に複雑さを増す実装パターンの紹介
- 実用的なAIアプリケーション開発の基礎の確立

## 📦 プロジェクト構造

```plaintext
├─ sandbox/
│  ├─ runnable/                  # Langchain Runnable実装
│  │  ├─ advanced/              # 高度な使用例
│  │  │  ├─ 01_basic_parallel.py    # 基本的な並列処理
│  │  │  ├─ 02_transform_chain.py   # 変換チェーン
│  │  │  ├─ 03_complex_parallel.py  # 複雑な並列処理
│  │  ├─ basic/                 # 基本的な使用例
│  │  │  ├─ 01_simple_transform.py  # シンプルな変換
│  │  │  ├─ 02_passthrough_chain.py # パススルーチェーン
│  │  │  ├─ 03_combined_chain.py    # 結合チェーン
│  │  │  ├─ 04_nested_chain.py      # ネストされたチェーン
│  │  │  ├─ logger_setup.py         # ロギング設定
├─ app.py                        # Streamlitアプリケーション
├─ requirements.txt              # 依存関係
```

## ✨ 実装された機能

1. **基本的なRunnable機能**:
   - シンプルな変換処理 (`01_simple_transform.py`)
   - パススルーチェーン (`02_passthrough_chain.py`)
   - 結合チェーン (`03_combined_chain.py`)
   - ネストされたチェーン (`04_nested_chain.py`)

2. **高度なRunnable機能**:
   - 基本的な並列処理 (`01_basic_parallel.py`)
   - 変換チェーン (`02_transform_chain.py`)
   - 複雑な並列処理 (`03_complex_parallel.py`)

3. **補助機能**:
   - 詳細なロギングシステム
   - Streamlitベースのデモインターフェース

## 🔧 セットアップと実行

### 環境のセットアップ

1. リポジトリのクローン:
   ```bash
   git clone https://github.com/Sunwood-ai-labs/langchain-sandbox.git
   cd langchain-sandbox
   ```

2. 仮想環境の作成と有効化:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate    # Windows
   ```

3. 依存関係のインストール:
   ```bash
   pip install -r requirements.txt
   ```

### 実行方法

#### 基本的な例の実行:
```bash
# シンプルな変換の例
python sandbox/runnable/basic/01_simple_transform.py

# パススルーチェーンの例
python sandbox/runnable/basic/02_passthrough_chain.py
```

#### 高度な例の実行:
```bash
# 並列処理の例
python sandbox/runnable/advanced/01_basic_parallel.py

# 複雑な並列処理の例
python sandbox/runnable/advanced/03_complex_parallel.py
```

## 🔄 処理フロー例

```mermaid
%%{init:{'theme':'base','themeVariables':{'primaryColor':'#024959','primaryTextColor':'#F2C335','primaryBorderColor':'#F2AE30','lineColor':'#A1A2A6','secondaryColor':'#593E25','tertiaryColor':'#F2C335'}}}%%

graph TB
    A[入力] --> B[基本処理]
    B --> C[チェーン処理]
    
    subgraph "基本処理"
    B1[テキスト変換] --> B2[データ加工]
    end
    
    subgraph "チェーン処理"
    C1[シーケンシャル実行] --> C2[並列実行]
    C2 --> C3[結果統合]
    end
    
    C --> D[出力]
```

## 📚 学習リソース

各実装例には詳細なドキュメントとコメントが含まれており、以下の概念を学ぶことができます：

- RunnableLambdaの基本的な使用方法
- チェーンの構築と組み合わせ
- 並列処理の実装
- エラーハンドリングとロギング
- 複雑なチェーンの設計パターン

## 🤝 コントリビューション

プルリクエストや課題の報告は大歓迎です。以下の手順で貢献できます：

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

---

<p align="center">
  Built with ❤️ using <a href="https://github.com/langchain-ai/langchain">LangChain</a>
</p>
