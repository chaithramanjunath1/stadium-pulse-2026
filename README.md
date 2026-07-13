# 🏟️ StadiumPulse 2026 — FIFA World Cup AI Assistant

An advanced, GenAI-powered dual-agent operational support and fan accessibility platform built for the **FIFA World Cup 2026**. Designed to enhance stadium operations, streamline incident management for staff, and provide real-time multilingual navigation and accessibility support for global fans.

---

## 🎯 Chosen Vertical
**[Challenge 4] Smart Stadiums & Tournament Operations** Focusing on: Real-time decision support, multilingual assistance, stadium navigation, crowd management, and inclusive accessibility routing.

---

## 🧠 Approach & Logic Architecture

StadiumPulse 2026 uses a dynamic context-aware routing architecture powered by **Google's Gemini 2.5 Flash** engine. Instead of relying on static conversational flows, the system adapts dynamically based on user persona and real-time telemetry inputs.

### ⚙️ Core Logic Flow:
1. **Dynamic Persona Routing:** The assistant switches between two highly specialized system instructions (`Fan Assist` vs. `Ops Commander`) based on the interface state, preventing context bleeding.
2. **Contextual Telemetry Injection:** Every user interaction dynamically embeds live structural venue tracking data (gate congestion matrix, medical service coordinates, stall statuses) into the processing layer.
3. **Deterministic Constraints:** Low temperature configuration ($0.3$) is explicitly enforced to eliminate hallucinations, ensuring emergency responses and navigation steps remain completely reliable and factually bound to the telemetry data.

---

## 🛠️ Tech Stack & Resource Efficiency

Adhering strictly to the **< 10 MB repository limit**, the application is engineered to be exceptionally lightweight by eliminating heavy local dependencies:
* **Interface & Presentation:** Streamlit (Native accessibility support, high-speed UI state handling).
* **GenAI Engine:** Official Google GenAI SDK (`google-genai`).
* **LLM Core:** `gemini-2.5-flash` (Optimized for low-latency, real-time response generation).

---

## 🔒 Security & Responsible AI Implementation
* **Zero Hardcoded Secrets:** Strict environment variable compliance via `os.environ.get("GEMINI_API_KEY")`.
* **Repository Safety:** Active `.gitignore` configurations implemented to systematically block caching anomalies and local environment leaks from entering the public domain.

---

## 🚀 How the Solution Works (Setup Summary)
1. Clone the repository:
   ```bash
   git clone [https://github.com/chaithramanunath1/stadium-pulse-2026.git](https://github.com/chaithramanunath1/stadium-pulse-2026.git)

1. Clone the repository:
   ```bash
   git clone [https://github.com/chaithramanunath1/stadium-pulse-2026.git](https://github.com/chaithramanunath1/stadium-pulse-2026.git)
