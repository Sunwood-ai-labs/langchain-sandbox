"""
RunnablePassthroughを使用したチェーン作成モジュール

このモジュールでは、RunnablePassthroughを使用して、
入力データを後続の処理に渡す方法を説明します。
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

def display_progress(step: str, data: any) -> any:
    """
    処理の進捗状況を表示する関数

    Args:
        step (str): 現在の処理ステップ
        data (any): 処理中のデータ

    Returns:
        any: 入力データをそのまま返す
    """
    logger.info(f"🔄 ステップ: {step}")
    logger.info(f"📝 データ: {data}")
    return data

def create_chain_with_passthrough():
    """
    RunnablePassthroughを使用したチェーンを作成します。

    RunnablePassthroughの利点:
    1. 入力データを変更せずに次の処理に渡せる
    2. 複数の処理で同じ入力データを参照できる
    3. データの流れを制御しやすい

    チェーンの処理フロー:
    1. 入力テキストに追加情報を組み合わせる
    2. プロンプトテンプレートに渡す
    3. ChatGPTで生成
    4. 文字列として出力

    Returns:
        Runnable: 入力テキストを加工して説明を生成するチェーン
    """
    def add_context(input_dict: Dict) -> Dict:
        """
        入力テキストに追加情報を組み合わせる関数

        Args:
            input_dict (Dict): 入力辞書
                - input_text: 入力テキスト
                - additional_info: 追加情報

        Returns:
            Dict: 組み合わせたテキストを含む辞書
        """
        combined_text = f"{input_dict['input_text']}（{input_dict['additional_info']}）"
        result = {"text": combined_text}
        return display_progress("テキストの組み合わせ", result)

    # プロンプトテンプレートの定義
    prompt = ChatPromptTemplate.from_template(
        "以下のトピックについて簡単に説明してください：{text}"
    )
    
    # チェーンの組み立て
    chain = (
        RunnableLambda(add_context)                                           # 入力テキストの加工
        | RunnableLambda(lambda x: display_progress("プロンプト生成前", x))  # 進捗表示
        | prompt                                                              # プロンプトの生成
        | RunnableLambda(lambda x: display_progress("ChatGPT入力前", x))     # 進捗表示
        | ChatOpenAI()                                                        # ChatGPTでの処理
        | RunnableLambda(lambda x: display_progress("出力パース前", x))      # 進捗表示
        | StrOutputParser()                                                   # 文字列への変換
    )
    
    return chain

def display_chain_info():
    """チェーンの処理フローを視覚的に表示する関数"""
    flow = """
    📊 処理フロー:
    
    1️⃣ 入力データ
       ↓
    2️⃣ テキスト組み合わせ
       ↓
    3️⃣ プロンプト生成
       ↓
    4️⃣ ChatGPT処理
       ↓
    5️⃣ 文字列変換
       ↓
    6️⃣ 最終出力
    """
    logger.info(flow)

def main():
    """
    モジュールのメイン関数
    RunnablePassthroughを使用したチェーンの基本的な使用例を実演します。
    """
    # ファイル名を表示
    print_tutorial_header(os.path.basename(__file__))
    
    # 環境変数の読み込み
    load_dotenv()
    
    logger.info("🚀 RunnablePassthroughを使用したチェーンの使用例を実演します")
    
    # 処理フローの表示
    display_chain_info()
    
    # チェーンの作成
    chain = create_chain_with_passthrough()
    
    # テスト用の入力データ
    test_input = {
        "input_text": "Python",
        "additional_info": "プログラミング言語"
    }
    
    logger.info("📥 入力データ:")
    logger.info(test_input)
    
    # 実行と結果の表示
    result = chain.invoke(test_input)
    logger.success(f"✨ 生成結果:\n{result}")

if __name__ == "__main__":
    main()
