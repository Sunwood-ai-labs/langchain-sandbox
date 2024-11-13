"""
ロギング設定モジュール
"""

from loguru import logger
import sys

def setup_logger():
    """
    loguruロガーの設定を行う
    
    Returns:
        logger: 設定済みのloguruロガーインスタンス
    """
    # デフォルトのハンドラーを削除
    logger.remove()
    
    # カスタムフォーマットでロガーを追加
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>",
        level="DEBUG"
    )
    
    # ファイルにもログを出力
    logger.add(
        "app.log",
        rotation="500 MB",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
    )
    
    return logger

# グローバルなロガーインスタンスを作成
logger = setup_logger()
