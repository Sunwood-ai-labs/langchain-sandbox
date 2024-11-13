# 🔗 langchain-sandbox

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

langchain-sandboxは、LangChainの様々な機能、特にRunnableを活用したAI処理システムの実装例を提供するサンドボックスプロジェクトです。基本的な使用例から高度な実装まで、段階的に学習できる教育リソースとして機能します。  バージョン: v0.2.0

## ✨ 主な機能

- LangChain Runnableを用いた段階的なチュートリアル
- 基本的なRunnableから高度な並列処理、カスタム変換機能まで網羅
- Mermaid.jsを用いた視覚的な処理フロー図
- 詳細なコード解説とコメント
- ログ出力機能による処理の可視化とデバッグ支援
- 実装例として、`sandbox/runnable/basic`と`sandbox/runnable/advanced`に複数のPythonファイルを提供


## 🔧 使用方法

1. **環境セットアップ:**
   ```bash
   git clone https://github.com/Sunwood-ai-labs/langchain-sandbox.git
   cd langchain-sandbox
   # uvを使用する場合:
   uv venv
   .venv\Scripts\activate    # Windows
   source .venv/bin/activate  # Linux/macOS
   # pythonを使用する場合:
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   source .venv/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   ```
2. **サンプルコードの実行:**
   - 基本的なRunnable例:  `python sandbox/runnable/basic/01_simple_transform.py`  など
   - 高度なRunnable例: `python sandbox/runnable/advanced/01_basic_parallel.py` など


## 📦 インストール手順

`pip install -U langchain-sandbox` を実行してください。 既存のコードとの互換性については、変更履歴を参照してください。


## 🆕 最新情報 (v0.2.0)

- LangChain高度なRunnableチュートリアルの追加: 基本的な並列処理から、複雑な並列チェーン、結果の選択的利用、複雑なチェーン構造の管理までを網羅。各例には、処理フローを説明するMermaid図を含んでいます。
- カスタム変換機能の実装とLangchainチェーンへの統合: テキストを大文字変換、文字数、単語数を取得するカスタム変換機能を実装し、LangchainのRunnableチェーンに統合。
- README.mdの全面的な更新とプロジェクト構造の改良: プロジェクトの概要をより明確に記述し、プロジェクト構造の説明を改善。


## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

---

<p align="center">
  Built with ❤️ using <a href="https://github.com/langchain-ai/langchain">LangChain</a>
</p>