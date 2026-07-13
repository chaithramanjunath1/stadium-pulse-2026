import streamlit as st
import os
from google import genai
from google.genai import types

# -------------------------------------------------------------------
# 1. PAGE CONFIGURATION & ACCESSIBILITY POLISH
# -------------------------------------------------------------------
st.set_page_config(
    page_title="StadiumPulse 2026 - FIFA World Cup AI Assistant",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------
# 2. INITIALIZE GEMINI CLIENT (Secure API Key Handling)
# -------------------------------------------------------------------
# Fetching from Environment variables for Security compliance
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 GEMINI_API_KEY not found in environment variables. Please configure it to continue.")
    st.stop()

client = genai.Client(api_key=api_key)

# -------------------------------------------------------------------
# 3. MOCK REAL-TIME CONTEXT DATA (Simulating Live Venue Telemetry)
# -------------------------------------------------------------------
VENUE_CONTEXT = """
Current Match: Brazil vs France at MetLife Stadium (New Jersey/New York).
Attendance: 82,500 (Full Capacity).
Current Status: 15 minutes before kick-off.
Gate Status: 
- Gate A: Heavy congestion (30 min wait time).
- Gate B: Moderate congestion (15 min wait time).
- Gate C (Accessible Entrance): Clear (2 min wait time).
Concessions: Section 100-200 food stalls are highly crowded. Section 300 is clear.
Emergency Services: Main medical bay located at Level 1, Near Section 114.
"""

# -------------------------------------------------------------------
# 4. SIDEBAR - PERSONA & LANGUAGE CONTROLS
# -------------------------------------------------------------------
st.sidebar.title("⚽ StadiumPulse 2026")
st.sidebar.markdown("---")

# Accessibility selection
user_role = st.sidebar.radio(
    "Select Your Profile:",
    options=["Spectator / Fan", "Stadium Staff / Volunteer"],
    help="Changes the AI agent's persona and logic to match your context."
)

preferred_lang = st.sidebar.selectbox(
    "Preferred Language:",
    options=["English", "Español", "Português", "Français", "Deutsch", "日本語"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Live Venue Telemetry")
st.sidebar.info(VENUE_CONTEXT)

# -------------------------------------------------------------------
# 5. CORE SYSTEM PROMPT & AGENT LOGIC
# -------------------------------------------------------------------
def get_system_instruction(role, language):
    if role == "Spectator / Fan":
        return f"""
        You are 'StadiumPulse Fan Assist', an elite multilingual AI concierge for the FIFA World Cup 2026. 
        Your goal is to help fans navigate the stadium safely, manage crowd stress, locate facilities, and provide excellent tournament experiences.
        
        CRITICAL RULES:
        1. Always respond in the user's selected language: {language}.
        2. Utilize the provided Live Venue Telemetry to give accurate advice. If a gate is crowded, recommend alternatives (e.g., Gate C for accessible needs).
        3. Be encouraging, polite, clear, and prioritize safety and inclusive accessibility.
        """
    else:
        return f"""
        You are 'StadiumPulse Ops Commander', a real-time operational support system for venue managers and volunteers.
        Your goal is to analyze operational issues (crowds, safety, infrastructure failures) and provide immediate triage steps.
        
        CRITICAL RULES:
        1. Always respond in the user's selected language: {language}.
        2. Format responses with: **Severity Level**, **Immediate Mitigation Action**, and **Resource Allocation Suggestion**.
        3. Maintain a calm, professional, and highly decisive operational tone.
        """

# -------------------------------------------------------------------
# 6. USER INTERFACE & CHAT LOGIC
# -------------------------------------------------------------------
st.title(f"🏟️ StadiumPulse 2026 — {user_role} Portal")
st.caption("Real-time GenAI Decision Support & Assistance for the FIFA World Cup 2026")

# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear history if role changes to avoid context leakage
if "last_role" in st.session_state and st.session_state.last_role != user_role:
    st.session_state.messages = []
st.session_state.last_role = user_role

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User prompt input
if user_input := st.chat_input("Ask about navigation, crowd updates, incidents, or emergency procedures..."):
    # Render user query
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate AI agent response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing live venue parameters..."):
            try:
                system_prompt = get_system_instruction(user_role, preferred_lang)
                
                # Combine telemetry data with the user input for complete situational awareness
                full_prompt = f"Live Venue Data:\n{VENUE_CONTEXT}\n\nUser Input: {user_input}"
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.3 # Low temperature for reliable, precise operational facts
                    )
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error(f"Error communicating with Gemini: {str(e)}")
