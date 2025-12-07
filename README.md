# VerbaView
Engineered a fault-tolerant "Text-to-UI" generation pipeline using Python, Streamlit, and Ollama (Llama 3.2) with &lt;5s local inference latency.
# 🎨 VerbaView Studio: Generative UI Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Llama 3](https://img.shields.io/badge/Model-Llama%203.2-orange)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **VerbaView** is a local, agentic AI workflow that converts natural language instructions into production-grade Frontend code (HTML/Tailwind & React). It runs **100% locally** using Ollama, featuring a self-healing pipeline that guarantees valid rendering.

---

## ⚡ Key Features

* **🗣️ Natural Language to UI:** Generate responsive interfaces using simple English prompts (e.g., *"Create a dark mode dashboard for a fintech app"*).
* **🛡️ Self-Healing Middleware:** A custom Python layer that intercepts LLM output, detects syntax errors (like broken tags or hallucinations), and automatically sanitizes code before rendering.
* **🔄 Context-Aware Refinement:** Maintains a stateful conversation loop, allowing users to iteratively tweak designs (e.g., *"Make the button blue"*) without losing the existing layout.
* **⚛️ React Export Engine:** Includes a transpiler that converts the generated HTML/Tailwind prototype into clean, functional **React (JSX)** components.
* **🎨 Custom CSS Support:** Supports both utility-first (Tailwind) and custom CSS animations.

---

## 🚀 Demo

![VerbaView Dashboard Screenshot](assets/demo_preview.png)
*(Note: Please verify the path to your screenshot)*

---

## 🏗️ Engineering Architecture

VerbaView is designed to solve the "Black Box" problem of generative UI by implementing a robust engineering pipeline rather than just wrapping an API.

```mermaid
graph LR
    A[User Prompt] --> B(Streamlit Frontend)
    B --> C{State Manager}
    C --> D[Prompt Engineering Layer]
    D --> E[Ollama / Llama 3.2 Local]
    E --> F[Raw Output]
    F --> G{Sanitization Middleware}
    G -- Fixes Tags/Scripts --> H[Valid HTML]
    H --> I[IFrame Renderer]
    H --> J[React Transpiler]
