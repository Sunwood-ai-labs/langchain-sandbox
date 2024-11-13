from loguru import logger
import sys
from art import text2art

def setup_logger():
    # ロガーの初期設定をクリア
    logger.remove()
    
    # カスタムフォーマットでロガーを追加
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>",
        level="INFO"
    )
    
    return logger

def print_tutorial_header(title):
    """チュートリアルのヘッダーをアートで表示"""
    ascii_art = text2art(title)
    print("\n" + "="*80)
    print(ascii_art)
    print("="*80 + "\n")
