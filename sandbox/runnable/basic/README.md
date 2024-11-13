# 🔰 Langchain Basic Runnable Tutorial

## 📝 概要

このディレクトリには、Langchainの基本的なRunnableコンポーネントの使用例が含まれています。段階的に複雑さを増していく4つのサンプルを通じて、Runnableの基本的な概念と使い方を学ぶことができます。

## ⚡ 実装例と詳細ワークフロー

### 1. シンプルな変換処理 (01_simple_transform.py)
- 通常のPython関数をRunnableLambdaでラップ
- 基本的なテキスト分析の実装
- エラーハンドリングの基礎

#### ワークフロー図
```mermaid
graph TB
    Input[入力テキスト] --> Transform[RunnableLambda]
    
    subgraph "テキスト分析処理"
        Transform --> |text_analyzer| Analysis[分析結果]
        Analysis --> CharCount[文字数カウント]
        Analysis --> WordCount[単語数カウント]
        Analysis --> Question[疑問文判定]
    end
    
    Analysis --> Output[出力: 分析結果辞書]
    
    style Input fill:#f9f,stroke:#333,stroke-width:2px
    style Output fill:#9ff,stroke:#333,stroke-width:2px
    style Transform fill:#ff9,stroke:#333,stroke-width:2px
```

### 2. パススルーチェーン (02_passthrough_chain.py)
- RunnablePassthroughを使用したデータの受け渡し
- 複数の処理のチェーン化
- ログ出力による処理の可視化

#### ワークフロー図
```mermaid
graph TB
    Input[入力テキスト<br/>& 追加情報] --> AddContext[テキスト結合処理]
    
    subgraph "パススルーチェーン"
        AddContext --> Prompt[プロンプト生成]
        Prompt --> GPT[ChatGPT処理]
        GPT --> Parser[文字列パーサー]
    end
    
    Parser --> Output[出力: 生成テキスト]
    
    %% ログ出力ポイントの表示
    Log1[ログ: テキスト結合] -.-> AddContext
    Log2[ログ: プロンプト生成] -.-> Prompt
    Log3[ログ: ChatGPT入力] -.-> GPT
    Log4[ログ: 出力パース] -.-> Parser
    
    style Input fill:#f9f,stroke:#333,stroke-width:2px
    style Output fill:#9ff,stroke:#333,stroke-width:2px
    style AddContext fill:#ff9,stroke:#333,stroke-width:2px
    style Prompt fill:#ff9,stroke:#333,stroke-width:2px
    style GPT fill:#f9f,stroke:#333,stroke-width:2px
```

### 3. 結合チェーン (03_combined_chain.py)
- 複数のRunnableの組み合わせ
- 段階的な処理の実装
- 処理フローの制御

#### ワークフロー図
```mermaid
graph TB
    Input[入力テキスト] --> Prefix[プレフィックス追加]
    
    subgraph "結合チェーン"
        Prefix --> Requirements[要件追加]
        Requirements --> PromptLog[プロンプト作成ログ]
        PromptLog --> Prompt[プロンプト生成]
        Prompt --> GenLog[生成処理ログ]
        GenLog --> GPT[ChatGPT処理]
    end
    
    GPT --> Parser[文字列パーサー]
    Parser --> Output[出力: 生成テキスト]
    
    style Input fill:#f9f,stroke:#333,stroke-width:2px
    style Output fill:#9ff,stroke:#333,stroke-width:2px
    style Prefix fill:#ff9,stroke:#333,stroke-width:2px
    style Requirements fill:#ff9,stroke:#333,stroke-width:2px
    style GPT fill:#f9f,stroke:#333,stroke-width:2px
    style Prompt fill:#ddf,stroke:#333,stroke-width:2px
```

### 4. ネストされたチェーン (04_nested_chain.py)
- 入れ子構造を持つ複雑なチェーンの実装
- 中間結果の活用
- エラーハンドリングの応用

#### ワークフロー図
```mermaid
graph TB
    Input[入力データ] --> Format[入力整形]
    
    subgraph "内部チェーン"
        Format --> InnerPrompt[内部プロンプト生成]
        InnerPrompt --> ChatGPT1[ChatGPT処理1]
    end
    
    subgraph "外部チェーン"
        ChatGPT1 --> LogResult[中間結果ログ]
        LogResult --> OuterPrompt[外部プロンプト生成]
        OuterPrompt --> ChatGPT2[ChatGPT処理2]
    end
    
    ChatGPT2 --> Parser[文字列パーサー]
    Parser --> Output[最終出力]
    
    style Input fill:#f9f,stroke:#333,stroke-width:2px
    style Output fill:#9ff,stroke:#333,stroke-width:2px
    style Format fill:#ff9,stroke:#333,stroke-width:2px
    style InnerPrompt fill:#ddf,stroke:#333,stroke-width:2px
    style OuterPrompt fill:#ddf,stroke:#333,stroke-width:2px
    style ChatGPT1 fill:#f9f,stroke:#333,stroke-width:2px
    style ChatGPT2 fill:#f9f,stroke:#333,stroke-width:2px
    style LogResult fill:#ff9,stroke:#333,stroke-width:2px
```

## 🔄 全体の処理フロー

以下は、4つのコンポーネントがどのように連携するかを示す全体図です：

```mermaid
%%{init:{'theme':'base','themeVariables':{'primaryColor':'#024959','primaryTextColor':'#F2C335','primaryBorderColor':'#F2AE30','lineColor':'#A1A2A6','secondaryColor':'#593E25','tertiaryColor':'#F2C335'}}}%%

graph TB
    Input[入力データ] --> SimpleTransform[シンプルな変換処理<br/>RunnableLambda]
    SimpleTransform --> Passthrough[パススルーチェーン<br/>RunnablePassthrough]
    Passthrough --> Combined[結合チェーン<br/>Multiple Runnables]
    
    subgraph "ネストされたチェーン"
        Inner[内部チェーン]
        Outer[外部チェーン]
        Inner --> Outer
    end
    
    Combined --> Inner
    Outer --> Output[出力結果]
    
    style Input fill:#f9f,stroke:#333,stroke-width:2px
    style Output fill:#9ff,stroke:#333,stroke-width:2px
    style SimpleTransform fill:#ff9,stroke:#333,stroke-width:2px
    style Passthrough fill:#ff9,stroke:#333,stroke-width:2px
    style Combined fill:#f9f,stroke:#333,stroke-width:2px
    style Inner fill:#f9f,stroke:#333,stroke-width:2px
    style Outer fill:#f9f,stroke:#333,stroke-width:2px
```

## 💡 実装のポイント

### シンプルな変換処理
```python
def text_analyzer(text: str) -> Dict[str, Any]:
    return {
        "original_text": text,
        "character_count": len(text),
        "word_count": len(text.split()),
        "is_question": "?" in text
    }

transform = RunnableLambda(text_analyzer)
```

### パススルーチェーン
```python
chain = (
    RunnableLambda(add_context)
    | prompt
    | ChatOpenAI()
    | StrOutputParser()
)
```

### 結合チェーン
```python
chain = (
    RunnableLambda(add_prefix)
    | RunnableLambda(add_requirements)
    | prompt
    | ChatOpenAI()
    | StrOutputParser()
)
```

### ネストされたチェーン
```python
inner_chain = RunnableLambda(format_input) | inner_prompt
outer_chain = outer_prompt | ChatOpenAI()
```

## 📊 使用例

各モジュールは個別に実行可能です：

```bash
# シンプルな変換の例
python 01_simple_transform.py

# パススルーチェーンの例
python 02_passthrough_chain.py

# 結合チェーンの例
python 03_combined_chain.py

# ネストされたチェーンの例
python 04_nested_chain.py
```

## ✨ 特徴

- 段階的な学習が可能な構成
- 実践的なユースケースの実装
- 詳細なログ出力による処理の可視化
- エラーハンドリングのベストプラクティス
- 再利用可能なコンポーネント設計

## 🎨 色分けの説明

各ワークフロー図で使用されている色の意味：
- 🟣 入力/出力 (紫/青)
- 🟡 データ変換処理 (黄)
- 🔵 プロンプト関連 (青)
- 🟣 ChatGPT処理 (紫)

## 🔍 詳細説明

各実装例の詳細な説明とソースコードのコメントを参照してください：

- [シンプルな変換処理の説明](01_simple_transform.py)
- [パススルーチェーンの説明](02_passthrough_chain.py)
- [結合チェーンの説明](03_combined_chain.py)
- [ネストされたチェーンの説明](04_nested_chain.py)

---

<p align="center">
  このチュートリアルは<a href="https://github.com/langchain-ai/langchain">LangChain</a>のRunnableコンポーネントの基本的な使い方を学ぶために作成されました。
</p>
