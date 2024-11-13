# 🔗 langchain-sandbox

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

## 🚀 Project Overview

langchain-sandbox is a sandbox project providing implementation examples of various LangChain features, particularly those utilizing Runnables for AI processing systems.  It serves as an educational resource, offering a step-by-step learning path from basic usage to advanced implementations. Version: v0.2.0

## ✨ Main Features

- Step-by-step tutorials using LangChain Runnables
- Covers basic Runnables to advanced parallel processing and custom transformation functions
- Visual process flow diagrams using Mermaid.js
- Detailed code explanations and comments
- Logging functionality for process visualization and debugging support
- Multiple Python files provided as implementation examples in `sandbox/runnable/basic` and `sandbox/runnable/advanced`


## 🔧 How to Use

1. **Environment Setup:**
   ```bash
   git clone https://github.com/Sunwood-ai-labs/langchain-sandbox.git
   cd langchain-sandbox
   # If using uv:
   uv venv
   .venv\Scripts\activate    # Windows
   source .venv/bin/activate  # Linux/macOS
   # If using python:
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   source .venv/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   ```
2. **Running Sample Code:**
   - Basic Runnable examples: `python sandbox/runnable/basic/01_simple_transform.py` etc.
   - Advanced Runnable examples: `python sandbox/runnable/advanced/01_basic_parallel.py` etc.


## 📦 Installation

Run `pip install -U langchain-sandbox`. For compatibility with existing code, please refer to the changelog.


## 🆕 What's New (v0.2.0)

- Added advanced LangChain Runnable tutorials: Covering basic parallel processing, complex parallel chains, selective result utilization, and managing complex chain structures. Each example includes a Mermaid diagram explaining the processing flow.
- Implemented and integrated custom transformation functions into Langchain chains:  Implemented custom transformation functions for converting text to uppercase, getting character counts, and word counts, and integrated them into Langchain's Runnable chains.
- Completely updated README.md and improved project structure:  The project overview is now clearer, and the project structure explanation has been improved.


## 📄 License

This project is licensed under the MIT License.  See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ using <a href="https://github.com/langchain-ai/langchain">LangChain</a>
</p>