"""
分析チェーンの実装 (シンプルなデモ用)
"""

from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any
from ..logger import logger
from .base_chain import BaseChain

class AnalysisChain(BaseChain):
    """分析チェーンクラス (シンプル版)"""
    
    def __init__(self):
        """初期化"""
        super().__init__()
        logger.info("AnalysisChainの初期化を開始")
        
        # シンプルな分析プロンプト
        self.analysis_prompt = ChatPromptTemplate.from_template("""
        以下の画像分析結果に基づいて、実用的な分析を行ってください：

        【基本分析】
        {object_analysis}

        【シーン分析】
        {scene_analysis}

        以下の形式で出力してください：

        【総合評価】
        {評価内容を記述}

        【推奨事項】
        - {具体的な改善点を3つ程度}

        【注意点】
        - {実施時の注意点を2つ程度}
        """)
        
        logger.info("AnalysisChainの初期化が完了")
    
    def create_analysis_chain(self) -> RunnableLambda:
        """シンプルな分析チェーンを作成"""
        chain = self.create_chain(self.analysis_prompt)
        return RunnableLambda(lambda x: chain.invoke(x))
