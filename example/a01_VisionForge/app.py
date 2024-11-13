"""
Gradioを使用した画像分析アプリケーション
"""

import gradio as gr
from module.logger import logger
from module.utils import load_image, format_json
from module.chains.llm_chain import LLMChain
import os
from dotenv import load_dotenv
import traceback


def initialize_app():
    """
    アプリケーションの初期化
    - 環境変数の読み込み
    - 必要なディレクトリの作成
    - モデルファイルのダウンロード
    """
    try:
        logger.info("アプリケーションの初期化を開始")
        
        # 環境変数の読み込み
        load_dotenv()
        
        # 必要なディレクトリの作成
        os.makedirs("demo", exist_ok=True)
        
        logger.info("アプリケーションの初期化が完了")
        
    except Exception as e:
        logger.error(f"初期化中にエラーが発生: {str(e)}")
        raise
    
def create_analysis_interface():
    """
    Gradioインターフェースの作成
    
    Returns:
        gr.Blocks: Gradioインターフェース
    """
    logger.info("Gradioインターフェースの作成を開始")
    
    # LLMChainのインスタンスを作成
    chain = LLMChain()
    integrated_chain = chain.create_integrated_chain()
    
    def process_image(image, progress=gr.Progress()):
        """
        画像処理関数
        
        Args:
            image: 入力画像
            progress: Gradioのプログレスバー
        
        Returns:
            tuple: (総合分析, 技術評価, 推奨事項, 注意点, 将来展望, エラーメッセージ)
        """
        try:
            if image is None:
                raise ValueError("画像が選択されていません")
            
            logger.info("画像処理を開始")
            
            # 進捗状況の更新関数
            def update_progress(message):
                progress(0, desc=message)
                logger.info(f"進捗状況: {message}")
            
            # 画像の読み込みと処理
            update_progress("画像を読み込んでいます...")
            img = load_image(image)
            
            # 画像分析の実行
            update_progress("AIによる総合分析を実行中...")
            result = integrated_chain.invoke(img)
            
            logger.info("画像処理が完了")
            return (
                result.get("総合分析", ""),
                result.get("技術評価", ""),
                result.get("推奨事項", ""),
                result.get("注意点", ""),
                result.get("将来展望", ""),
                None  # エラーなし
            )
            
        except Exception as e:
            error_message = f"エラーが発生しました:\n{str(e)}\n\n{traceback.format_exc()}"
            logger.error(error_message)
            return (None, None, None, None, None, error_message)
    
    # インターフェースの作成
    with gr.Blocks(title="🔍 Image Analysis with LangChain") as interface:
        gr.Markdown("""
        # 🔍 Image Analysis with LangChain
        
        このアプリケーションは、画像を分析し、AIによる詳細な分析と推奨事項を提供します。
        
        ## 🌟 主な機能
        
        1. 📊 画像の詳細分析
           - 物体検出と認識
           - テキスト検出
           - 色彩分析
           - シーン理解
        
        2. 🤖 AIによる多段階分析
           - 視覚的特徴の分析
           - 技術的評価
           - 実用的な推奨事項
           - 将来展望の提示
        
        3. 🔍 総合的な結果提供
           - 分かりやすい要約
           - 具体的な改善提案
           - 実践的なアドバイス
        
        ## 💡 使用方法
        
        1. 画像をアップロードまたはドラッグ＆ドロップ
        2. 「画像を分析」ボタンをクリック
        3. 各タブで異なる視点からの分析結果を確認
        """)
        
        # エラーメッセージ表示用
        error_box = gr.Textbox(
            label="エラー",
            visible=False,
            container=False
        )
        
        with gr.Row():
            # 入力部分
            with gr.Column(scale=1):
                input_image = gr.Image(
                    label="分析する画像をアップロード",
                    type="numpy",
                    height=400
                )
                analyze_btn = gr.Button("画像を分析", variant="primary")
            
            # 出力部分
            with gr.Column(scale=2):
                with gr.Tabs():
                    with gr.TabItem("📝 総合分析"):
                        general_output = gr.Textbox(
                            label="総合分析結果",
                            lines=10,
                            show_copy_button=True
                        )
                    
                    with gr.TabItem("⚙️ 技術評価"):
                        technical_output = gr.Textbox(
                            label="技術的な評価",
                            lines=8,
                            show_copy_button=True
                        )
                    
                    with gr.TabItem("💡 推奨事項"):
                        recommendations_output = gr.Textbox(
                            label="推奨事項",
                            lines=6,
                            show_copy_button=True
                        )
                    
                    with gr.TabItem("⚠️ 注意点"):
                        cautions_output = gr.Textbox(
                            label="注意点",
                            lines=4,
                            show_copy_button=True
                        )
                    
                    with gr.TabItem("🔮 将来展望"):
                        future_output = gr.Textbox(
                            label="将来展望",
                            lines=6,
                            show_copy_button=True
                        )
                
        # ボタンクリック時の処理
        analyze_btn.click(
            fn=process_image,
            inputs=input_image,
            outputs=[
                general_output,
                technical_output,
                recommendations_output,
                cautions_output,
                future_output,
                error_box
            ],
            api_name="analyze"
        )
        
        # エラーハンドリング
        def update_error_visibility(error):
            return gr.update(visible=error is not None, value=error)
        
        error_box.change(
            fn=update_error_visibility,
            inputs=[error_box],
            outputs=[error_box]
        )
    
    logger.info("Gradioインターフェースの作成が完了")
    return interface

def main():
    """
    メイン関数
    アプリケーションの初期化と起動を行う
    """
    try:
        logger.info("アプリケーションを起動します")
        
        # アプリケーションの初期化
        initialize_app()
        
        # インターフェースの作成と起動
        interface = create_analysis_interface()
        interface.launch(
            server_name="0.0.0.0",
            server_port=7865,
            share=True
        )
        
    except Exception as e:
        logger.error(f"アプリケーションの起動中にエラーが発生: {str(e)}")
        raise

if __name__ == "__main__":
    main()
