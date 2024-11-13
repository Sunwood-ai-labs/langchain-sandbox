"""
複雑な並列処理を示すモジュール

このモジュールでは、RunnableParallelを使用して
より複雑な並列処理フローを実現する方法を説明します。
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from logger_setup import setup_logger, print_tutorial_header
import os

# ロガーのセットアップ
logger = setup_logger()

def create_complex_parallel():
    """
    より複雑な並列チェーンを作成します。

    複雑な並列処理の特徴:
    1. 複数の異なる視点からの分析が可能
    2. 結果を構造化された形で取得できる
    3. 処理の依存関係を管理できる

    Returns:
        RunnableParallel: 複雑な並列処理を行うチェーン
    """
    logger.info("複雑な並列チェーンを作成中")
    
    summary_prompt = ChatPromptTemplate.from_template(
        "{topic}について簡潔な概要を提供してください。"
    )
    pros_prompt = ChatPromptTemplate.from_template(
        "{topic}の主な利点を3つ挙げてください。"
    )
    cons_prompt = ChatPromptTemplate.from_template(
        "{topic}の主な課題や欠点を3つ挙げてください。"
    )
    
    model = ChatOpenAI(temperature=0.7)
    parser = StrOutputParser()
    
    return RunnableParallel(
        summary=summary_prompt | model | parser,
        pros=pros_prompt | model | parser,
        cons=cons_prompt | model | parser
    )

def main():
    """
    モジュールのメイン関数
    複雑な並列処理の使用例を実演します。
    """
    # ファイル名を表示
    print_tutorial_header(os.path.basename(__file__))
    
    # 環境変数の読み込み
    load_dotenv()
    
    logger.info("複雑な並列処理の実演を開始します")
    
    # 複雑な並列チェーンの作成と実行
    complex_chain = create_complex_parallel()
    result = complex_chain.invoke({"topic": "宇宙探査"})
    
    # 結果の表示
    logger.success("複雑な並列処理の結果:")
    logger.success(f"概要: {result['summary']}")
    logger.success(f"利点: {result['pros']}")
    logger.success(f"課題: {result['cons']}")

if __name__ == "__main__":
    main()
