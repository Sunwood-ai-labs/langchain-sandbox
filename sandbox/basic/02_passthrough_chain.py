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
from logger_setup import setup_logger

# ロガーのセットアップ
logger = setup_logger()

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
        return {
            "text": f"{input_dict['input_text']}（{input_dict['additional_info']}）"
        }

    # プロンプトテンプレートの定義
    prompt = ChatPromptTemplate.from_template(
        "以下のトピックについて簡単に説明してください：{text}"
    )
    
    # チェーンの組み立て
    chain = (
        RunnableLambda(add_context)  # 入力テキストの加工
        | prompt                     # プロンプトの生成
        | ChatOpenAI()              # ChatGPTでの処理
        | StrOutputParser()         # 文字列への変換
    )
    
    return chain

def main():
    """
    モジュールのメイン関数
    RunnablePassthroughを使用したチェーンの基本的な使用例を実演します。
    """
    # 環境変数の読み込み
    load_dotenv()
    
    logger.info("RunnablePassthroughを使用したチェーンの使用例を実演します")
    
    # チェーンの作成
    chain = create_chain_with_passthrough()
    
    # テスト用の入力データ
    test_input = {
        "input_text": "Python",
        "additional_info": "プログラミング言語"
    }
    
    # 実行と結果の表示
    result = chain.invoke(test_input)
    logger.success(f"生成結果:\n{result}")

if __name__ == "__main__":
    main()
