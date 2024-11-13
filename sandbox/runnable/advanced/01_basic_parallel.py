"""
基本的な並列処理を示すモジュール

このモジュールでは、RunnableParallelを使用して
複数の処理を並列に実行する方法を説明します。
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

def create_basic_parallel():
    """
    基本的な並列チェーンを作成します。

    並列処理の特徴:
    1. 複数の処理を同時に実行できる
    2. 各処理の結果を個別に取得できる
    3. 処理時間を短縮できる

    Returns:
        RunnableParallel: 並列処理を行うチェーン
    """
    logger.info("基本的な並列チェーンを作成中")
    
    description_prompt = ChatPromptTemplate.from_template(
        "{animal}について1文で説明してください。"
    )
    fact_prompt = ChatPromptTemplate.from_template(
        "{animal}についての面白い豆知識を1つ教えてください。"
    )
    
    model = ChatOpenAI(temperature=0.7)
    parser = StrOutputParser()
    
    return RunnableParallel(
        description=description_prompt | model | parser,
        fun_fact=fact_prompt | model | parser
    )

def main():
    """
    モジュールのメイン関数
    基本的な並列処理の使用例を実演します。
    """
    # ファイル名を表示
    print_tutorial_header(os.path.basename(__file__))
    
    # 環境変数の読み込み
    load_dotenv()
    
    logger.info("基本的な並列処理の実演を開始します")
    
    # 並列チェーンの作成と実行
    parallel_chain = create_basic_parallel()
    result = parallel_chain.invoke({"animal": "象"})
    
    # 結果の表示
    logger.success("並列処理の結果:")
    logger.success(f"説明: {result['description']}")
    logger.success(f"豆知識: {result['fun_fact']}")

if __name__ == "__main__":
    main()
