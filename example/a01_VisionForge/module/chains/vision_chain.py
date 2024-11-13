"""
画像認識チェーンの実装 (LLMのみを使用した疑似的な実装)
"""

from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any, List
import numpy as np
from ..logger import logger
from .base_chain import BaseChain

class VisionChain(BaseChain):
    """画像認識チェーンクラス (LLMベース)"""
    
    def __init__(self):
        """初期化"""
        super().__init__()
        logger.info("VisionChainの初期化を開始")
        
        # 画像基本情報解析用プロンプト
        self.image_info_prompt = ChatPromptTemplate.from_template("""
        画像の基本情報:
        - 縦サイズ: {height}px
        - 横サイズ: {width}px
        - チャンネル数: {channels}
        - コントラスト: {contrast:.2f}
        - 平均輝度: {brightness:.2f}

        この情報をもとに画像の基本的な特徴を簡潔に説明してください。
        """)
        
        # 画像認識用プロンプト
        self.vision_prompt = ChatPromptTemplate.from_template("""
        以下の画像基本情報と画像の説明をもとに、詳細な分析を行ってください：

        {image_info}

        画像の説明：
        {image_description}

        以下の要素について詳細に分析し、JSON形式で出力してください：

        1. 画像内の物体とその位置関係
        2. 検出可能なテキスト
        3. 画像の色彩や全体的な印象

        出力形式：
        {
            "検出物体": [
                {"物体": "...", "信頼度": 0.95, "位置": "画像中央"},
                ...
            ],
            "テキスト": ["テキスト1", "テキスト2", ...],
            "色情報": {
                "色相": {"平均": 180.0, "標準偏差": 45.0},
                "彩度": {"平均": 0.6, "標準偏差": 0.2},
                "明度": {"平均": 0.7, "標準偏差": 0.15},
                "主要な色": [
                    {"RGB": "(255, 255, 255)", "割合": 0.4},
                    ...
                ]
            }
        }
        """)
        
        # 物体認識用プロンプト
        self.object_analysis_prompt = ChatPromptTemplate.from_template("""
        以下の物体検出結果を分析し、画像内の物体の関係性や配置について詳細に説明してください。

        検出された物体:
        {objects}

        以下の点に注目して分析してください：
        1. 物体の配置と相互関係
        2. 主要な物体とその重要性
        3. 画像の意図や目的
        4. 特筆すべき特徴や異常
        """)
        
        # シーン理解用プロンプト
        self.scene_analysis_prompt = ChatPromptTemplate.from_template("""
        以下の画像解析データに基づいて、シーン全体の理解と解釈を提供してください。

        物体検出結果：
        {objects}

        テキスト検出結果：
        {texts}

        色彩分析：
        {colors}

        以下の観点から分析してください：
        1. シーンの全体的な状況
        2. 環境や雰囲気
        3. 想定される文脈や状況
        4. 重要な視覚的要素とその意味
        """)
        
        logger.info("VisionChainの初期化が完了")
    
    def create_vision_chain(self) -> RunnableLambda:
        """
        画像認識チェーンを作成
        
        Returns:
            RunnableLambda: 作成されたチェーン
        """
        # LLMによる画像解析チェーン
        analysis_chain = RunnableLambda(self._analyze_image)
        
        # 物体認識チェーン
        object_chain = self.create_chain(
            self.object_analysis_prompt,
            self.gpt4_model
        )
        
        # シーン理解チェーン
        scene_chain = self.create_chain(
            self.scene_analysis_prompt,
            self.gpt4_model
        )
        
        # 並列チェーンの作成
        parallel_chain = self.create_parallel_chain({
            "object_analysis": object_chain,
            "scene_analysis": scene_chain,
            "raw_data": RunnablePassthrough()
        })
        
        # 全体のチェーンを構築
        return (
            analysis_chain
            | parallel_chain
            | RunnableLambda(self.format_output)
        )
    
    def _analyze_image(self, image_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        LLMを使用して画像を解析
        
        Args:
            image_data (Dict[str, Any]): 画像データと説明
                {
                    "description": str,  # 画像の説明テキスト
                    "height": int,       # 画像の高さ
                    "width": int,        # 画像の幅
                    "channels": int,     # チャンネル数
                    "contrast": float,   # コントラスト
                    "brightness": float  # 平均輝度
                }
        
        Returns:
            Dict[str, Any]: 解析結果
        """
        try:
            logger.info("LLMによる画像解析を開始")
            
            # 画像基本情報の分析
            info_chain = self.create_chain(
                self.image_info_prompt,
                self.gpt4_model
            )
            
            image_info = info_chain.invoke({
                "height": image_data["height"],
                "width": image_data["width"],
                "channels": image_data["channels"],
                "contrast": image_data["contrast"],
                "brightness": image_data["brightness"]
            })
            
            # LLMによる詳細な画像解析の実行
            analysis_chain = self.create_chain(
                self.vision_prompt,
                self.gpt4_model
            )
            
            result = analysis_chain.invoke({
                "image_info": image_info,
                "image_description": image_data["description"]
            })
            
            # 結果を辞書形式に変換（JSON.loads()を使用）
            import json
            parsed_result = json.loads(result)
            
            # プロンプト用にデータを整形
            formatted_data = {
                "objects": self._format_objects(parsed_result["検出物体"]),
                "texts": self._format_texts(parsed_result["テキスト"]),
                "colors": self._format_colors(parsed_result["色情報"])
            }
            
            logger.info("LLMによる画像解析が完了")
            return formatted_data
            
        except Exception as e:
            logger.error(f"画像解析中にエラーが発生: {str(e)}")
            raise
    
    def _format_objects(self, objects: List[Dict[str, Any]]) -> str:
        """物体検出結果のフォーマット"""
        if not objects:
            return "検出された物体はありません。"
        
        formatted = ["検出された物体:"]
        for i, obj in enumerate(objects, 1):
            formatted.append(f"{i}. {obj['物体']} - 信頼度: {obj['信頼度']}, 位置: {obj['位置']}")
        return "\n".join(formatted)
    
    def _format_texts(self, texts: List[str]) -> str:
        """テキスト検出結果のフォーマット"""
        if not texts:
            return "検出されたテキストはありません。"
        
        formatted = ["検出されたテキスト:"]
        formatted.extend([f"- {text}" for text in texts])
        return "\n".join(formatted)
    
    def _format_colors(self, colors: Dict[str, Any]) -> str:
        """色情報のフォーマット"""
        formatted = ["色彩分析:"]
        
        # 基本的な色情報
        for key in ["色相", "彩度", "明度"]:
            info = colors[key]
            formatted.append(f"{key}:")
            formatted.append(f"  - 平均: {info['平均']:.1f}")
            formatted.append(f"  - 標準偏差: {info['標準偏差']:.1f}")
        
        # 主要な色
        formatted.append("\n主要な色:")
        for color in colors["主要な色"]:
            formatted.append(f"- RGB: {color['RGB']}, 割合: {color['割合']}")
        
        return "\n".join(formatted)
