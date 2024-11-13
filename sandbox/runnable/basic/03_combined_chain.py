"""
複数のRunnableを組み合わせたチェーン作成モジュール

このモジュールでは、複数のRunnableを組み合わせて
より複雑な処理を実現する方法を説明します。
"""

from typing import Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from logger_setup import setup_logger, print_tutorial_header
import os

# ロガーのセットアップ
logger = setup_logger()

def create_combined_chain():
    """
    複数のRunnableを組み合わせたチェーンを作成します。

    複数Runnable組み合わせの利点:
    1. 複雑な処理を小さな機能単位に分割できる
    2. 各処理の役割が明確になる
    3. 再利用性が高まる

    チェーンの処理フロー:
    1. トピックにプレフィックスを追加
    2. 要件を追加
    3. プロンプトの作成
    4. ChatGPTでの生成
    5. 文字列への変換

    Returns:
        Runnable: 複数の処理を組み合わせたチェーン
    """
    def add_prefix(text: str) -> Dict[str, str]:
        """トピックにプレフィックスを追加する関数"""
        result = {"topic": f"最新の{text}について"}
        logger.info(f"🔄 プレフィックス追加: {result['topic']}")
        return result

    def add_requirements(data: Dict) -> Dict[str, str]:
        """要件を追加する関数"""
        result = {
            "topic": data["topic"],
            "requirements": "具体例を2つ含めてください。"
        }
        logger.info(f"📝 要件追加: {result['requirements']}")
        return result

    def log_prompt_creation(data: Dict) -> Dict:
        """プロンプト作成をログ出力する関数"""
        logger.info("🔨 プロンプト作成中...")
        return data

    def log_generation(data: str) -> str:
        """生成処理をログ出力する関数"""
        logger.info("🤖 ChatGPTによる生成中...")
        return data

    # プロンプトテンプレートの定義
    prompt = ChatPromptTemplate.from_template(
        "{topic}\n{requirements}"
    )

    # チェーンの組み立て
    chain = (
        RunnableLambda(add_prefix)         # Step 1: プレフィックスの追加
        | RunnableLambda(add_requirements) # Step 2: 要件の追加
        | RunnableLambda(log_prompt_creation)  # Step 3: プロンプト作成ログ
        | prompt                           # Step 3: プロンプトの作成
        | RunnableLambda(log_generation)   # Step 4: 生成ログ
        | ChatOpenAI()                     # Step 4: ChatGPTでの生成
        | StrOutputParser()                # Step 5: 文字列への変換
    )

    return chain

def main():
    """
    モジュールのメイン関数
    複数のRunnableを組み合わせたチェーンの使用例を実演します。
    """
    # ファイル名を表示
    print_tutorial_header(os.path.basename(__file__))
    
    # 環境変数の読み込み
    load_dotenv()
    
    logger.info("🚀 複数のRunnableを組み合わせたチェーンの実行を開始します")
    
    # チェーンの作成
    chain = create_combined_chain()
    
    # テスト用の入力
    test_input = "AI技術"
    logger.info(f"📥 入力: {test_input}")
    
    # 実行と結果の表示
    logger.info("⚙️ チェーンの処理を開始します...")
    result = chain.invoke(test_input)
    
    # 結果の表示
    logger.info("✨ チェーンの処理が完了しました")
    logger.success("📤 生成結果:")
    print(f"\n{result}\n")

if __name__ == "__main__":
    main()
