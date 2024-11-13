"""
RunnableLambdaの基本的な使用方法を示すモジュール

このモジュールでは、通常のPython関数をRunnableとして扱う方法を説明します。
RunnableLambdaを使用することで、関数をLangchainのパイプラインに組み込むことができます。
"""

from typing import Dict, Any
from langchain_core.runnables import RunnableLambda

def create_simple_transform() -> RunnableLambda:
    """
    テキスト分析を行うRunnableLambdaを作成します。

    RunnableLambdaの特徴:
    1. 通常のPython関数をRunnableとして扱えるようにラップする
    2. 入力と出力の型を明確に定義できる
    3. チェーンの中で他のRunnableと組み合わせられる

    Returns:
        RunnableLambda: テキスト分析を行うRunnable
    """
    def text_analyzer(text: str) -> Dict[str, Any]:
        """
        テキストの基本的な分析を行う内部関数

        Args:
            text (str): 分析対象のテキスト

        Returns:
            Dict[str, Any]: 分析結果を含む辞書
                - original_text: 元のテキスト
                - character_count: 文字数
                - word_count: 単語数
                - is_question: 疑問文かどうか
        """
        return {
            "original_text": text,          # 元のテキスト
            "character_count": len(text),   # 文字数
            "word_count": len(text.split()),# 単語数
            "is_question": "?" in text      # 疑問文かどうか
        }
    
    return RunnableLambda(text_analyzer)
