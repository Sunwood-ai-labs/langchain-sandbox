"""
Runnableの入れ子構造を使用したチェーン作成モジュール

このモジュールでは、Runnableの入れ子構造を使用して
より複雑な処理フローを実現する方法を説明します。
"""

from typing import Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from logger_setup import setup_logger, print_tutorial_header
import os

# ロガーのセットアップ
logger = setup_logger()

def format_input(input_dict: Dict) -> Dict:
    """
    入力を整形する関数

    Args:
        input_dict (Dict): 入力辞書
            - topic: トピック
            - style: 説明スタイル

    Returns:
        Dict: 整形された入力を含む辞書
    """
    logger.info(f"入力の整形を開始: {input_dict}")
    formatted = {
        "formatted_topic": f"{input_dict['topic']}について",
        "style": input_dict["style"]
    }
    logger.info(f"入力の整形が完了: {formatted}")
    return formatted

def log_intermediate_result(result: str) -> str:
    """中間結果をログに出力する関数"""
    logger.info("中間結果を生成:")
    logger.info("-" * 40)
    logger.info(result)
    logger.info("-" * 40)
    return result

def create_nested_chain():
    """
    Runnableの入れ子構造を使用したチェーンを作成します。

    入れ子構造の利点:
    1. 複雑な処理フローを段階的に実行できる
    2. 中間結果を次の処理に活用できる
    3. 処理の依存関係を明確に表現できる

    チェーンの処理フロー:
    1. 内部チェーン
        - 入力の整形
        - トピックの説明生成
    2. 外部チェーン
        - 説明文の箇条書き化
        - 最終的な文字列生成

    Returns:
        Runnable: 入れ子構造を持つ複雑なチェーン
    """
    logger.info("チェーンの作成を開始")

    # 内部チェーン: トピックの説明を生成
    inner_prompt = ChatPromptTemplate.from_template(
        "{formatted_topic}の説明を{style}書いてください。"
    )
    logger.info(f"内部プロンプトを作成: {inner_prompt}")
    inner_chain = RunnableLambda(format_input) | inner_prompt

    # 外部チェーン: 説明を箇条書きに変換
    outer_prompt = ChatPromptTemplate.from_template(
        "以下の説明文を箇条書きにしてください：\n{text}"
    )
    logger.info(f"外部プロンプトを作成: {outer_prompt}")
    
    # チェーンの組み立て
    chain = (
        inner_chain                        # 内部チェーンで説明を生成
        | ChatOpenAI()                    # ChatGPTで処理
        | StrOutputParser()               # 文字列に変換
        | RunnableLambda(log_intermediate_result)  # 中間結果のログ出力
        | {"text": RunnablePassthrough()} # 中間結果の保持
        | outer_prompt                    # 外部チェーンで箇条書きに変換
        | ChatOpenAI()                    # 再度ChatGPTで処理
        | StrOutputParser()               # 最終的な文字列に変換
    )

    logger.info("チェーンの作成が完了")
    return chain

def process_with_error_handling(chain, input_data: Dict) -> str:
    """
    エラーハンドリング付きでチェーンを実行する関数

    Args:
        chain: 実行するチェーン
        input_data (Dict): 入力データ

    Returns:
        str: 生成結果
    """
    try:
        logger.info(f"チェーンの実行を開始: 入力 = {input_data}")
        result = chain.invoke(input_data)
        logger.success("チェーンの実行が正常に完了")
        return result
    except Exception as e:
        logger.error(f"チェーンの実行中にエラーが発生: {str(e)}")
        raise

def main():
    """
    モジュールのメイン関数
    Runnableの入れ子構造を使用したチェーンの使用例を実演します。
    """
    # ファイル名を表示
    print_tutorial_header(os.path.basename(__file__))
    
    # 環境変数の読み込み
    load_dotenv()
    logger.info("環境変数の読み込みが完了")
    
    logger.info("=== Runnableの入れ子構造を使用したチェーンの実演を開始 ===")
    
    # チェーンの作成
    chain = create_nested_chain()
    
    # テスト用の入力
    test_input = {
        "topic": "機械学習",
        "style": "わかりやすく"
    }
    
    # 実行と結果の表示
    logger.info("テスト実行を開始")
    result = process_with_error_handling(chain, test_input)
    
    logger.info("最終結果:")
    logger.info("=" * 40)
    logger.success(result)
    logger.info("=" * 40)
    
    logger.info("=== デモンストレーションが正常に完了 ===")

if __name__ == "__main__":
    main()
