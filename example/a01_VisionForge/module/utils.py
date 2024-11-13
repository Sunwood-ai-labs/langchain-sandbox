"""
ユーティリティ関数モジュール
"""

import cv2
import numpy as np
from PIL import Image
import io
from typing import Union
from .logger import logger

def load_image(image: Union[np.ndarray, Image.Image, bytes, str]) -> np.ndarray:
    """
    画像データを読み込み、OpenCV形式に変換する
    
    Args:
        image: 入力画像（numpy.ndarray, PIL.Image, bytes, または文字列のパス）
    
    Returns:
        np.ndarray: OpenCV形式の画像データ（BGR）
    """
    try:
        logger.debug("画像の読み込みを開始")
        
        if isinstance(image, np.ndarray):
            # すでにnumpy配列の場合
            img = image.copy()
        elif isinstance(image, Image.Image):
            # PIL Imageの場合
            img = np.array(image)
        elif isinstance(image, bytes):
            # バイトデータの場合
            img = np.array(Image.open(io.BytesIO(image)))
        elif isinstance(image, str):
            # ファイルパスの場合
            img = cv2.imread(image)
            if img is None:
                raise ValueError(f"画像の読み込みに失敗しました: {image}")
        else:
            raise ValueError(f"サポートされていない画像形式です: {type(image)}")
        
        # RGBからBGRに変換（OpenCV形式）
        if len(img.shape) == 3 and img.shape[2] == 3:
            if not isinstance(image, str):  # ファイルから直接読み込んだ場合は変換不要
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # 画像の正規化
        img = normalize_image(img)
        
        logger.debug(f"画像の読み込みが完了: shape={img.shape}")
        return img
        
    except Exception as e:
        logger.error(f"画像の読み込み中にエラーが発生: {str(e)}")
        raise

def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    画像を正規化する
    
    Args:
        image (np.ndarray): 入力画像
    
    Returns:
        np.ndarray: 正規化された画像
    """
    try:
        logger.debug("画像の正規化を開始")
        
        # サイズの正規化
        max_size = 800
        height, width = image.shape[:2]
        if height > max_size or width > max_size:
            scale = max_size / max(height, width)
            new_height = int(height * scale)
            new_width = int(width * scale)
            image = cv2.resize(image, (new_width, new_height))
            logger.debug(f"画像をリサイズ: {width}x{height} -> {new_width}x{new_height}")
        
        # ノイズ除去
        image = cv2.GaussianBlur(image, (3, 3), 0)
        
        # コントラスト正規化
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl,a,b))
        image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        
        logger.debug("画像の正規化が完了")
        return image
        
    except Exception as e:
        logger.error(f"画像の正規化中にエラーが発生: {str(e)}")
        raise

def format_json(data: dict) -> str:
    """
    辞書データを見やすい文字列に整形する
    
    Args:
        data (dict): 整形する辞書データ
    
    Returns:
        str: 整形された文字列
    """
    try:
        import json
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"JSONの整形中にエラーが発生: {str(e)}")
        return str(data)
