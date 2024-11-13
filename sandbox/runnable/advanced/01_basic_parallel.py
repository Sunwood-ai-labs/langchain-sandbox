"""
基本的な並列処理を示すモジュール

このモジュールでは、RunnableParallelを使用して
複数の処理を並列に実行する方法を説明します。
デバッグ用の中間出力を追加しています。
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
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
    辞書を見やすく整形する
    
    Args:
        d: 整形する辞書
        indent: インデントスペース数
    Returns:
        str: 整形された文字列
    """
    return json.dumps(d, ensure_ascii=False, indent=indent)

class DebugCallbackHandler(BaseCallbackHandler):
    """
    デバッグ用のコールバックハンドラー
    """
    def _format_message(self, message) -> Dict[str, Any]:
        """メッセージの情報を整形"""
        return {
            "content": message.content,
            "type": message.__class__.__name__
        }

    def _format_generation(self, generation) -> Dict[str, Any]:
        """生成結果の情報を整形"""
        return {
            "text": generation.text,
            "message": self._format_message(generation.message),
            "generation_info": generation.generation_info
        }

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        """LLMの開始時に呼ばれる"""
        formatted_prompts = {
            "prompts": prompts,
            "serialized": {
                "name": serialized.get("name", "unknown"),
                "type": serialized.get("type", "unknown")
            }
        }
        logger.debug(f"[Debug] LLM開始:\n{format_dict(formatted_prompts)}")

    def on_llm_end(self, response, **kwargs) -> None:
        """LLMの終了時に呼ばれる"""
        formatted_response = {
            "generations": [
                [self._format_generation(gen) for gen in gens]
                for gens in response.generations
            ],
            "token_usage": response.llm_output.get("token_usage", {}),
            "model_name": response.llm_output.get("model_name", "unknown")
        }
        logger.debug(f"[Debug] LLM終了:\n{format_dict(formatted_response)}")

    def on_llm_error(self, error: Exception, **kwargs) -> None:
        """LLMでエラーが発生した時に呼ばれる"""
        error_info = {
            "error_type": error.__class__.__name__,
            "error_message": str(error)
        }
        logger.error(f"[Debug] LLMエラー:\n{format_dict(error_info)}")

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        """チェーンの開始時に呼ばれる"""
        chain_info = {
            "chain_type": serialized.get("name", "unknown"),
            "inputs": inputs
        }
        logger.debug(f"[Debug] チェーン開始:\n{format_dict(chain_info)}")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        """チェーンの終了時に呼ばれる"""
        logger.debug(f"[Debug] チェーン終了:\n{format_dict(outputs)}")

    def on_chain_error(self, error: Exception, **kwargs) -> None:
        """チェーンでエラーが発生した時に呼ばれる"""
        error_info = {
            "error_type": error.__class__.__name__,
            "error_message": str(error)
        }
        logger.error(f"[Debug] チェーンエラー:\n{format_dict(error_info)}")

def create_basic_parallel():
    """
    基本的な並列チェーンを作成します。

    Returns:
        RunnableParallel: 並列処理を行うチェーン
    """
    logger.info("基本的な並列チェーンを作成中")
    
    # プロンプトの作成
    description_prompt = ChatPromptTemplate.from_messages([
        ("human", "{animal}について1文で説明してください。")
    ])
    prompt_info = {
        "messages": str(description_prompt.messages),
        "input_variables": description_prompt.input_variables
    }
    logger.debug(f"[Debug] 説明用プロンプトを作成:\n{format_dict(prompt_info)}")
    
    fact_prompt = ChatPromptTemplate.from_messages([
        ("human", "{animal}についての面白い豆知識を1つ教えてください。")
    ])
    prompt_info = {
        "messages": str(fact_prompt.messages),
        "input_variables": fact_prompt.input_variables
    }
    logger.debug(f"[Debug] 豆知識用プロンプトを作成:\n{format_dict(prompt_info)}")
    
    # モデルとパーサーの初期化
    model = ChatOpenAI(
        temperature=0.7,
        callbacks=[DebugCallbackHandler()]
    )
    logger.debug("[Debug] ChatOpenAIモデルを初期化")
    
    parser = StrOutputParser()
    logger.debug("[Debug] 文字列パーサーを初期化")
    
    # チェーンの作成
    chain = RunnableParallel(
        description=description_prompt | model | parser,
        fun_fact=fact_prompt | model | parser
    )
    logger.debug("[Debug] 並列チェーンを作成完了")
    
    return chain

def measure_execution_time(func):
    """実行時間を計測するデコレータ"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"[Performance] 実行時間: {execution_time:.2f}秒")
        return result
    return wrapper

@measure_execution_time
def execute_parallel_chain(chain, input_data):
    """
    並列チェーンを実行し、実行時間を計測します。
    
    Args:
        chain (RunnableParallel): 実行する並列チェーン
        input_data (dict): 入力データ
    Returns:
        dict: 実行結果
    """
    logger.debug(f"[Debug] 入力データ:\n{format_dict(input_data)}")
    result = chain.invoke(input_data)
    logger.debug(f"[Debug] 実行結果:\n{format_dict(result)}")
    return result

def main():
    """
    モジュールのメイン関数
    基本的な並列処理の使用例を実演します。
    """
    print_tutorial_header(os.path.basename(__file__))
    
    load_dotenv()
    logger.debug("[Debug] 環境変数を読み込み完了")
    
    logger.info("基本的な並列処理の実演を開始します")
    
    try:
        parallel_chain = create_basic_parallel()
        input_data = {"animal": "象"}
        result = execute_parallel_chain(parallel_chain, input_data)
        
        logger.success("並列処理の結果:")
        logger.success(f"説明: {result['description']}")
        logger.success(f"豆知識: {result['fun_fact']}")
        
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        raise

if __name__ == "__main__":
    main()
