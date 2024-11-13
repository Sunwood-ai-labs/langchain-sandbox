"""
LangChainの高度な並列処理と連鎖的実行を示すモジュール

このモジュールでは以下の機能を実装しています：
1. 複数のLLMチェーンの並列実行
2. チェーン結果の選択的利用（pick機能）
3. 結果の組み合わせによる新規タスクの実行
4. デバッグ情報の構造化出力
5. パフォーマンス計測

使用例:
    python 02_enhanced_parallel_chains.py
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.callbacks import BaseCallbackHandler
from logger_setup import setup_logger, print_tutorial_header
import os
import time
import json
from typing import Any, Dict, List

# ロガーのセットアップ
logger = setup_logger()

def format_dict(d: Dict[str, Any], indent: int = 2) -> str:
    """
    デバッグ出力用の辞書整形関数
    
    Args:
        d: 整形する辞書オブジェクト
        indent: インデントのスペース数
    
    Returns:
        str: 整形されたJSON文字列
    """
    return json.dumps(d, ensure_ascii=False, indent=indent)

def measure_execution_time(func):
    """
    関数の実行時間を計測するデコレータ
    
    Args:
        func: 計測対象の関数
    
    Returns:
        wrapper: 計測機能を追加したラッパー関数
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"[Performance] 実行時間: {execution_time:.2f}秒")
        return result
    return wrapper

class DebugCallbackHandler(BaseCallbackHandler):
    """
    LangChainの実行過程をデバッグ出力するためのコールバックハンドラー
    
    実装されているコールバック:
    - on_llm_start: LLM実行開始時
    - on_llm_end: LLM実行完了時
    """
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        """
        LLM実行開始時のコールバック
        プロンプトの内容とLLMの設定を出力
        """
        formatted_prompts = {
            "prompts": prompts,
            "serialized": {
                "name": serialized.get("name", "unknown"),
                "type": serialized.get("type", "unknown")
            }
        }
        logger.debug(f"[Debug] LLM開始:\n{format_dict(formatted_prompts)}")

    def on_llm_end(self, response, **kwargs) -> None:
        """
        LLM実行完了時のコールバック
        生成された結果とトークン使用量を出力
        """
        formatted_response = {
            "generations": [[{
                "text": gen.text,
                "message_type": gen.message.__class__.__name__
            } for gen in gens] for gens in response.generations],
            "token_usage": response.llm_output.get("token_usage", {})
        }
        logger.debug(f"[Debug] LLM終了:\n{format_dict(formatted_response)}")

def create_multi_chain():
    """
    複数のチェーンを組み合わせた処理を作成
    
    実装される処理フロー:
    1. 基本的な情報を3つの異なるプロンプトで並列取得
       - 動物の基本説明
       - 興味深い豆知識
       - 生息地情報
    2. 取得した情報の一部を使用して要約を生成
       - 基本説明と豆知識を入力として使用
    
    チェーンの特徴:
    - 並列実行による効率化
    - pick機能による必要な情報の選択的利用
    - RunnablePassthroughによる入力の受け渡し
    
    Returns:
        RunnableParallel: 構築された複合チェーン
    """
    logger.info("複数チェーンの作成を開始")
    
    # 基本的なモデルとパーサーの設定
    # temperature=0.7で適度なランダム性を持たせる
    model = ChatOpenAI(temperature=0.7, callbacks=[DebugCallbackHandler()])
    parser = StrOutputParser()
    
    # 各種プロンプトの作成
    # 異なる視点からの情報を取得するための3つのプロンプト
    description_prompt = ChatPromptTemplate.from_messages([
        ("human", "{animal}について1文で説明してください。")
    ])
    
    fact_prompt = ChatPromptTemplate.from_messages([
        ("human", "{animal}についての面白い豆知識を1つ教えてください。")
    ])
    
    habitat_prompt = ChatPromptTemplate.from_messages([
        ("human", "{animal}の主な生息地について教えてください。")
    ])
    
    # 要約用プロンプト
    # 前段で取得した情報を組み合わせて新しい視点の情報を生成
    summary_prompt = ChatPromptTemplate.from_messages([
        ("human", """
        以下の情報を元に、{animal}についての簡潔な要約を作成してください：
        
        基本情報: {description}
        豆知識: {fun_fact}
        """)
    ])
    
    # Step 1: 基本的な並列チェーンの構築
    # 3つのプロンプトを同時に実行
    base_chain = RunnableParallel(
        description=description_prompt | model | parser,
        fun_fact=fact_prompt | model | parser,
        habitat=habitat_prompt | model | parser
    )
    
    # Step 2: 要約チェーンの作成
    summary_chain = summary_prompt | model | parser
    
    # Step 3: 全体のチェーンを組み立て
    # まず、summaryチェーン用の入力を準備するチェーンを作成
    summary_input_chain = RunnableParallel(
        {
            "description": base_chain.pick("description"),
            "fun_fact": base_chain.pick("fun_fact"),
            "animal": RunnablePassthrough()
        }
    )
    
    # 最終的なチェーンを構築
    final_chain = RunnableParallel(
        {
            "description": base_chain.pick("description"),
            "fun_fact": base_chain.pick("fun_fact"),
            "habitat": base_chain.pick("habitat"),
            "summary": summary_input_chain | summary_chain,
            "animal": RunnablePassthrough()
        }
    )
    
    logger.debug("[Debug] 複数チェーンの作成完了")
    return final_chain

@measure_execution_time
def execute_chain(chain, input_data):
    """
    チェーンを実行し、実行時間を計測
    
    Args:
        chain: 実行するチェーン
        input_data: 入力データ
        
    Returns:
        dict: チェーンの実行結果
    """
    logger.debug(f"[Debug] 入力データ:\n{format_dict(input_data)}")
    result = chain.invoke(input_data)
    logger.debug(f"[Debug] 実行結果:\n{format_dict(result)}")
    return result

def main():
    """
    メイン実行関数
    
    処理の流れ:
    1. 環境設定の読み込み
    2. マルチチェーンの作成
    3. チェーンの実行
    4. 結果の出力
    """
    print_tutorial_header(os.path.basename(__file__))
    load_dotenv()
    
    logger.info("複数チェーンを組み合わせた処理の実演を開始します")
    
    try:
        # チェーンの作成と実行
        chain = create_multi_chain()
        input_data = {"animal": "象"}
        result = execute_chain(chain, input_data)
        
        # 結果の出力
        logger.success("処理結果:")
        logger.success(f"基本説明: {result['description']}")
        logger.success(f"豆知識: {result['fun_fact']}")
        logger.success(f"生息地: {result['habitat']}")
        logger.success(f"要約: {result['summary']}")
        
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        raise

if __name__ == "__main__":
    main()
