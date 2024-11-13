"""
カスタム変換機能を示すモジュール

このモジュールでは、RunnableLambdaを使用して
カスタム変換処理を実装する方法を説明します。
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from logger_setup import setup_logger, print_tutorial_header
import os

# ロガーのセットアップ
logger = setup_logger()

def transform_text(text: str) -> dict:
    """
    テキストを変換する関数

    Args:
        text (str): 変換対象のテキスト

    Returns:
        dict: 変換結果を含む辞書
            - original: 元のテキスト
            - uppercase: 大文字変換したテキスト
            - length: 文字数
            - words: 単語数
    """
    logger.info("テキスト変換を実行中")
    return {
        "original": text,
        "uppercase": text.upper(),
        "length": len(text),
        "words": len(text.split())
    }

def create_chain_with_transform():
    """
    変換機能を含むチェーンを作成します。

    変換チェーンの特徴:
    1. カスタム変換処理を組み込める
    2. 変換結果を後続の処理で活用できる
    3. 柔軟な処理フローを構築できる

    Returns:
        Runnable: テキスト変換と分析を行うチェーン
    """
    logger.info("変換チェーンを作成中")
    transform = RunnableLambda(transform_text)
    
    prompt = ChatPromptTemplate.from_template("""
    以下のテキストデータを分析してください:
    原文: {original}
    大文字: {uppercase}
    文字数: {length}
    単語数: {words}
    
    簡単な分析結果を提供してください。
    """)
    
    model = ChatOpenAI(temperature=0.7)
    
    return transform | prompt | model | StrOutputParser()

def main():
    """
    モジュールのメイン関数
    カスタム変換機能の使用例を実演します。
    """
    # ファイル名を表示
    print_tutorial_header(os.path.basename(__file__))
    
    # 環境変数の読み込み
    load_dotenv()
    
    logger.info("カスタム変換機能の実演を開始します")
    
    # 変換チェーンの作成と実行
    chain_with_transform = create_chain_with_transform()
    result = chain_with_transform.invoke("こんにちは、世界！")
    
    # 結果の表示
    logger.success(f"変換結果: {result}")

if __name__ == "__main__":
    main()
