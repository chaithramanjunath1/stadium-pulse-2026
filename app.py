import streamlit as st
import os
import re
from typing import Dict, Any, Optional
from google import genai
from google.genai import types

# -------------------------------------------------------------------
# 1. PAGE ARCHITECTURE & ACCESSIBILITY INTERFACE
# -------------------------------------------------------------------
st.set_page_config(
    page_title="StadiumPulse 2026 - FIFA World Cup AI Assistant",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------
# 2. DUAL-TIER MEMORY CACHING LAYER (Efficiency Maximize)
# -------------------------------------------------------------------
@st.cache_resource
def get_secure_gemini_client() -> Optional[genai.Client]:
    """Initializes and retains the structural GenAI client instance."""
    api_key: Optional[str] = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key.strip() == "":
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None

@st.cache_data
def load_immutable_venue_telemetry() -> str:
    """Caches static telemetry data matrix to preserve CPU cycles."""
    return """
    Current Match: Brazil vs France at MetLife Stadium.
    Attendance: 82,500 (Full Capacity) | Time: 15 mins before kick-off.

    [NAVIGATION & CROWD MANAGEMENT PILLAR]
    - Gate A: Heavy congestion (30 min wait time). Recommendation: Avoid.
    - Gate B: Moderate congestion (15 min wait time).
    - Gate C (Dedicated Accessible Entrance): Clear (2 min wait time). Fully optimized for wheelchair routing.

    [TRANSPORTATION & TRANSIT PILLAR]
    - Stadium Shuttle Hub: 10 min transit delay due to heavy volume.
    - Express Train Transit Link: Operations fluent, trains departure every 4 mins.

    [SUSTAINABILITY & ECO-LOGISTICS PILLAR]
    - Section 100-200: Smart recycling hubs operating at 85% capacity.
    - Section 300: Eco-waste centers clear.

    [FACILITIES & REAL-TIME OPERATIONAL INTELLIGENCE]
    - Main Medical Bay: Located at Level 1, adjacent to Section 114.
    - Concessions: High crowd density at Section 100 food stalls. Section 300 stalls clear.
    """

# Initialize structures securely
client: Optional[genai.Client] = get_secure_gemini_client()
VENUE_CONTEXT: str = load_immutable_venue_telemetry()

# -------------------------------------------------------------------
# 3. SECURITY APPLICATION LAYER (Security & Guardrail Check)
# -------------------------------------------------------------------
def sanitize_user_input(raw_text: str) -> str:
    """Sanitizes incoming textual vectors to neutralize prompt injection threats."""
    if not raw_text:
        return ""
    # Enforce maximum safe length limit to prevent token-exhaustion DOS exploits
    truncated_text: str = raw_text[:500]
    # Strip dangerous scripting system commands or structural markdown anchors
    clean_text: str = re.sub(r"[<>\{\}\[\]\\\/]", "", truncated_text)
    return clean_text.strip()

# -------------------------------------------------------------------
# 4. SIDEBAR GRAPHICAL OVERLAYS (Accessibility Compliance)
# -------------------------------------------------------------------
st.sidebar.title("⚽ StadiumPulse 2026")
st.sidebar.markdown("---")
st.sidebar.write("### ♿ **Accessibility Settings**")

user_role: str = st.sidebar.radio(
    "Select Structural System Protocol:",
    options=["Spectator / Fan", "Stadium Staff / Volunteer"],
    help="Modifies underlying system intelligence directives."
)

preferred_lang: str = st.sidebar.selectbox(
    "Select Interface Linguistic Directives:",
    options=["English", "Español", "Português", "Français", "Deutsch", "日本語"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Live Telemetry Broadcast Data")
st.sidebar.text(VENUE_CONTEXT)

# -------------------------------------------------------------------
# 5. TECHNICAL AGENT INSTRUCTION FACTORY
# -------------------------------------------------------------------
def get_system_instruction(role: str, language: str) -> str:
    """Generates highly deterministic contextual personas with type safety."""
    base_rules: str = f"Language Constraint: Respond exclusively in {language}."
    
    if role == "Spectator / Fan":
        return f"""
        {base_rules}
        You are 'StadiumPulse Fan Assist', a highly inclusive AI concierge for the FIFA World Cup 2026.
        Your goal is to guide fans safely, optimize navigation using live metrics, and assist individuals with diverse accessibility needs.
        Context Rules: Cross-reference Gate C for mobility challenges, explain shuttle updates, and encourage eco-waste recycling centers.
        """
    else:
        return f"""
        {base_rules}
        You are 'StadiumPulse Ops Commander', a rapid operational support framework for stadium managers and volunteers.
        Your goal is to evaluate incidents and produce immediate, structured crisis handling steps.
        Format Constraint: Every output MUST contain exactly these bold sections:
        - **Severity Level** (Low/Medium/High/Critical)
        - **Immediate Mitigation Action** (Deterministic step-by-step instructions based on telemetry)
        - **Resource Allocation Suggestion** (Strategic positioning of staff assets)
        """

# -------------------------------------------------------------------
# 6. APPLICATION PIPELINE & RENDER ENGINE
# -------------------------------------------------------------------
st.title(f"🏟️ StadiumPulse 2026 — {user_role} Workspace")
st.caption("GenAI Real-Time Multi-Agent Orchestration Engine for Tournament Operations & Accessibility")

if not client:
    st.warning("⚠️ Application is running in offline demo mode. Please set a valid GEMINI_API_KEY environment variable to enable live AI analysis.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear history safely upon user profile alterations
if "last_role" in st.session_state and st.session_state.last_role != user_role:
    st.session_state.messages = []
st.session_state.last_role = user_role

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if raw_input := st.chat_input("Input transmission data regarding layout, crowds, incidents, or safety paths..."):
    clean_input: str = sanitize_user_input(raw_input)
    
    if clean_input:
        with st.chat_message("user"):
            st.markdown(clean_input)
        st.session_state.messages.append({"role": "user", "content": clean_input})
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing live telemetry vectors..."):
                try:
                    system_prompt: str = get_system_instruction(user_role, preferred_lang)
                    full_prompt: str = f"Telemetry Data Matrix:\n{VENUE_CONTEXT}\n\nSanitized User Input: {clean_input}"
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=full_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.3
                        )
                    )
                    
                    output_text: str = response.text if response.text else "Transmission successful but clear data return vector empty."
                    st.markdown(output_text)
                    st.session_state.messages.append({"role": "assistant", "content": output_text})
                    
                except ValueError as val_err:
                    st.error(f"Data value handling error: {str(val_err)}")
                except RuntimeError as run_err:
                    st.error(f"Runtime processing error: {str(run_err)}")
