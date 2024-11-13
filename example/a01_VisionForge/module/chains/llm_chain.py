"""
LLM統合チェーンの実装 (チェーン連結の練習用)
"""

from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any
from ..logger import logger
from .base_chain import BaseChain
from .vision_chain import VisionChain
from .analysis_chain import AnalysisChain

class LLMChain(BaseChain):
    """LLM統合チェーンクラス"""
    
    def __init__(self):
        """初期化"""
        super().__init__()
        logger.info("LLMChainの初期化を開始")
        
        # 各チェーンの初期化
        self.vision_chain = VisionChain()
        self.analysis_chain = AnalysisChain()
        
        # 最終的な結果を整形するためのプロンプト
        self.final_prompt = ChatPromptTemplate.from_template("""
        以下の分析結果を元に、最終的なレポートを作成してください：

        【視覚分析結果】
        {vision_result}

        【詳細分析結果】
        {analysis_result}

        以下の形式で出力してください：

        【総合分析】
        {ここに全体的な分析を記述}

        【技術評価】
        {ここに技術的な評価を記述}

        【推奨事項】
        {ここに推奨事項を箇条書きで記述}

        【注意点】
        {ここに注意点を箇条書きで記述}

        【将来展望】
        {ここに将来の可能性や展望を記述}
        """)
        
        logger.info("LLMChainの初期化が完了")
    
    def create_integrated_chain(self) -> RunnableParallel:
        """
        統合チェーンを作成
        - チェーンの連結を活用した実装
        """
        # 視覚チェーンを作成
        vision_chain = self.vision_chain.create_vision_chain()
        
        # 分析チェーンを作成
        analysis_chain = self.analysis_chain.create_analysis_chain()
        
        # 最終整形チェーンを作成
        final_chain = self.create_chain(self.final_prompt)
        
        # 並列処理を含むチェーンの連結
        return (
            # 入力を複製して各チェーンに渡す
            RunnablePassthrough() | {
                "vision_result": vision_chain,
                "analysis_result": RunnablePassthrough() | analysis_chain
            }
            # 最終的な整形チェーンに接続
            | final_chain
            # 出力を辞書形式に整形
            | RunnableLambda(self._format_output)
        )
    
    def _format_output(self, result: str) -> Dict[str, str]:
        """
        最終出力を整形
        """
        try:
            # 結果を行で分割
            sections = result.split("\n\n")
            
            # セクションごとに分類
            output = {}
            current_section = None
            
            for line in result.split("\n"):
                if line.startswith("【"):
                    # 新しいセクションの開始
                    current_section = line.strip("【】")
                    output[current_section] = ""
                elif current_section and line.strip():
                    # 既存のセクションに内容を追加
                    output[current_section] += line + "\n"
            
            # 末尾の改行を削除
            for key in output:
                output[key] = output[key].strip()
            
            return output
            
        except Exception as e:
            logger.error(f"出力の整形中にエラーが発生: {str(e)}")
            return {
                "総合分析": "結果の整形中にエラーが発生しました",
                "技術評価": str(e),
                "推奨事項": "",
                "注意点": "",
                "将来展望": ""
            }
