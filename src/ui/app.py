"""
Streamlit UI - Chat interface for the agent.
Run: streamlit run src/ui/app.py
"""
import streamlit as st
import requests
import os 

# Backend API URL
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_URL = f"{BASE_URL}/chat"

# Page config
st.set_page_config(
    page_title="Personal Assistant Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Personal Assistant Agent")
st.caption("Powered by GPT-4 + Tools (Weather, Calculator, Web Search)")


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **Available Tools:**
    - 🌤️ Weather (any city)
    - 🧮 Calculator
    - 🔍 Web Search
    """)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
        # Show tool calls if any
        if "tool_calls" in msg and msg["tool_calls"]:
            with st.expander("🔧 Tools Used"):
                for tc in msg["tool_calls"]:
                    st.json(tc)


# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"query": prompt},
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()
                
                answer = data["answer"]
                tool_calls = data["tool_calls_made"]
                
                st.write(answer)
                
                # Show transparency
                if tool_calls:
                    with st.expander(f"🔧 Tools Used ({len(tool_calls)})"):
                        for tc in tool_calls:
                            st.json(tc)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "tool_calls": tool_calls
                })
            
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Backend error: {e}")
            except Exception as e:
                st.error(f"❌ Error: {e}")