"""
基本チェーンの実装
"""

from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any
from ..logger import logger

class BaseChain:
    """基本チェーンクラス"""
    
    def __init__(self):
        """初期化"""
        logger.info("BaseChainの初期化を開始")
        
        # 基本的なモデルの設定
        self.gpt4_model = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-4o"
        )
        
        self.gpt35_model = ChatOpenAI(
            temperature=0.5,
            model_name="gpt-4o-mini"
        )
        
        # 出力パーサー
        self.parser = StrOutputParser()
        
        logger.info("BaseChainの初期化が完了")
    
    def create_chain(self, prompt: ChatPromptTemplate, model: ChatOpenAI = None) -> RunnableLambda:
        """
        基本的なチェーンを作成
        
        Args:
            prompt (ChatPromptTemplate): プロンプトテンプレート
            model (ChatOpenAI, optional): 使用するモデル
        
        Returns:
            RunnableLambda: 作成されたチェーン
        """
        if model is None:
            model = self.gpt35_model
        
        return (
            prompt
            | model
            | self.parser
        )
    
    def create_parallel_chain(self, chains: Dict[str, RunnableLambda]) -> RunnableLambda:
        """
        並列チェーンを作成
        
        Args:
            chains (Dict[str, RunnableLambda]): チェーンの辞書
        
        Returns:
            RunnableLambda: 作成された並列チェーン
        """
        return RunnablePassthrough() | chains
    
    def format_output(self, result: Dict[str, Any]) -> Dict[str, str]:
        """
        出力結果をフォーマット
        
        Args:
            result (Dict[str, Any]): 処理結果
        
        Returns:
            Dict[str, str]: フォーマットされた結果
        """
        try:
            return {
                key: str(value) if value is not None else ""
                for key, value in result.items()
            }
        except Exception as e:
            logger.error(f"出力のフォーマット中にエラーが発生: {str(e)}")
            return {"error": str(e)}
