---
title: langchain-sandbox
emoji: 🔗
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: mit
---


<p align="center">
  <img src="docs/langchain-sandbox.png" width="100%">
  <h1 align="center">🔗 langchain-sandbox</h1>
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/langchain-sandbox">
    <img alt="GitHub Repo" src="https://img.shields.io/badge/github-langchain--sandbox-blue?logo=github">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/langchain-sandbox/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/langchain-sandbox?color=green">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/langchain-sandbox/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/langchain-sandbox?style=social">
  </a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.8%2B-blue">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/LangChain-2F4F4F?style=for-the-badge&logo=chainlink" alt="LangChain">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai" alt="OpenAI">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
</p>

## 🎯 Project Overview

langchain-sandbox is a sandbox project providing implementation examples of various LangChain features, particularly AI processing systems utilizing Runnables. This repository serves as an educational resource for learning practical development patterns and best practices using LangChain.

## 🌟 Objectives

- 📚 Provide practical usage examples of LangChain's Runnable system.
- 🔄 Introduce implementation patterns with gradually increasing complexity.
- 🎓 Establish the foundation for practical AI application development.

## 📂 Project Structure

```plaintext
├─ sandbox/
│  ├─ runnable/                  # Langchain Runnable implementations
│  │  ├─ advanced/              # Advanced usage examples
│  │  │  ├─ 01_basic_parallel.py    # Basic parallel processing
│  │  │  ├─ 02_transform_chain.py   # Transform chain
│  │  │  ├─ 03_complex_parallel.py  # Complex parallel processing
│  │  ├─ basic/                 # Basic usage examples
│  │  │  ├─ 01_simple_transform.py  # Simple transformation
│  │  │  ├─ 02_passthrough_chain.py # Passthrough chain
│  │  │  ├─ 03_combined_chain.py    # Combined chain
│  │  │  ├─ 04_nested_chain.py      # Nested chain
│  │  │  ├─ logger_setup.py         # Logging configuration
├─ app.py                        # Streamlit application
├─ requirements.txt              # Dependencies
```

## ⚡ Implemented Features

### 🔰 Basic Runnable Features:
   - Simple transformation (`01_simple_transform.py`)
   - Passthrough chain (`02_passthrough_chain.py`)
   - Combined chain (`03_combined_chain.py`)
   - Nested chain (`04_nested_chain.py`)

### 🚀 Advanced Runnable Features:
   - Basic parallel processing (`01_basic_parallel.py`)
   - Transform chain (`02_transform_chain.py`)
   - Complex parallel processing (`03_complex_parallel.py`)

### 🛠️ Auxiliary Features:
   - Detailed logging system
   - Streamlit-based demo interface

## 🔧 Setup and Execution

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Sunwood-ai-labs/langchain-sandbox.git
   cd langchain-sandbox
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate    # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Execution

#### Running Basic Examples:
```bash
# Simple transformation example
python sandbox/runnable/basic/01_simple_transform.py

# Passthrough chain example
python sandbox/runnable/basic/02_passthrough_chain.py
```

#### Running Advanced Examples:
```bash
# Parallel processing example
python sandbox/runnable/advanced/01_basic_parallel.py

# Complex parallel processing example
python sandbox/runnable/advanced/03_complex_parallel.py
```

## 🔄 Example Processing Flow

```mermaid

graph TB
    Input[Input Text] --> Basic[Basic Runnable Processing]
    
    subgraph "Basic Runnable Processing"
        Transform[Text Transformation<br/>RunnableLambda]
        Passthrough[Passthrough Processing<br/>RunnablePassthrough]
        Transform --> Passthrough
    end
    
    Basic --> Advanced[Advanced Runnable Processing]
    
    subgraph "Advanced Runnable Processing"
        Parallel[Parallel Processing<br/>RunnableParallel]
        Chain[Chain Processing<br/>Combined Chain]
        Nested[Nested Processing<br/>Nested Chain]
        
        Parallel --> Chain
        Chain --> Nested
    end
    
    Advanced --> Output[Processing Result]
    
    style Input fill:#f9f,stroke:#333,stroke-width:2px
    style Output fill:#9ff,stroke:#333,stroke-width:2px
    style Transform fill:#ff9,stroke:#333,stroke-width:2px
    style Passthrough fill:#ff9,stroke:#333,stroke-width:2px
    style Parallel fill:#f9f,stroke:#333,stroke-width:2px
    style Chain fill:#f9f,stroke:#333,stroke-width:2px
    style Nested fill:#f9f,stroke:#333,stroke-width:2px
```

## 📚 Learning Resources

Each implementation example includes detailed documentation and comments, allowing you to learn about the following concepts:

- Basic usage of RunnableLambda
- Building and combining chains
- Implementing parallel processing
- Error handling and logging
- Design patterns for complex chains

## 🤝 Contributions

Pull requests and issue reports are welcome! You can contribute by following these steps:

1. Fork this repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push the branch (`git push origin feature/amazing-feature`)
5. Create a pull request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ using <a href="https://github.com/langchain-ai/langchain">LangChain</a>
</p>