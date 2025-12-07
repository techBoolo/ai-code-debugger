import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# 1. Configuration & Setup
st.set_page_config(
    page_title="DevAssist AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

# Custom CSS for Premium Look
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #ffffff;
    }
    
    /* Chat Input Styling */
    .stChatInput textarea {
        background-color: #1f242c;
        border: 1px solid #30363d;
        color: #e0e0e0;
        border-radius: 12px;
    }
    
    .stChatInput textarea:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 1px #58a6ff;
    }
    
    /* Bot Message Style */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: transparent; 
    }
    
    div[data-testid="chatAvatarIcon-user"] {
        background-color: #238636;
    }
    
    div[data-testid="chatAvatarIcon-assistant"] {
        background-color: #1f6feb;
    }
    
    /* Button Styling */
    .stButton button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background-color: #2ea043;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Configuration
with st.sidebar:
    st.title("🛠️ Configuration")
    
    with st.expander("🤖 Model Settings", expanded=True):
        model_name = st.text_input(
            "Model Name", 
            value=os.getenv("LLM_MODEL", "llama3"),
            help="Ensure you have this model pulled in Ollama (e.g., 'ollama pull llama3')"
        )
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

    with st.expander("🎭 System Persona", expanded=True):
        default_system_prompt = (
            "You are a Senior Software Engineer and Expert Debugger.\n"
            "Your goal is to help the user fix their code.\n"
            "Follow this structure in your response:\n"
            "1. **Analysis**: Concisely explain the root cause.\n"
            "2. **Fix**: Provide the corrected code block.\n"
            "3. **Prevention**: One short tip to avoid this in the future.\n"
            "Use Markdown filtering for code blocks."
        )
        system_prompt = st.text_area(
            "System Instructions", 
            value=default_system_prompt,
            height=200
        )

    st.markdown("---")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Status")
    st.info("Ready to debug")

# 3. Main Chat Interface
st.title("DevAssist AI Debugger")
st.markdown("Paste your code or error below. I'll analyze it for you.")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# Handle user input
if prompt := st.chat_input("Analyze this code..."):
    
    # 1. Display User Message
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate and Display AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Initialize LLM
            llm = ChatOllama(
                model=model_name,
                temperature=temperature
            )
            
            # Construct message history with System Prompt
            messages_to_send = [SystemMessage(content=system_prompt)] + st.session_state.messages
            
            # Stream response
            for chunk in llm.stream(messages_to_send):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")
            
            # Final update without cursor
            message_placeholder.markdown(full_response)
            
            # Save to history
            st.session_state.messages.append(AIMessage(content=full_response))
            
        except Exception as e:
            st.error(f"Error connecting to Ollama: {str(e)}")
            st.info("Make sure Ollama is running (`ollama serve`) and the model is pulled.")
