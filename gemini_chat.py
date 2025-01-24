import streamlit as st
import google.generativeai as genai

# Configure page
st.set_page_config(
    page_title="🌱 EcoChat Assistant",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .stButton>button {
        border-radius: 20px;
        padding: 0.5rem 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    .user-message {
        background-color: #e6f3ff;
    }
    .assistant-message {
        background-color: #f0f2f6;
    }
    .header-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Configure API key
GOOGLE_API_KEY = "AIzaSyCrSaDe5hduLgCxR4EcIlD94HgWtj9C5dM"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Header
st.markdown("""
    <div class="header-container">
        <h1>🌱 EcoChat Assistant</h1>
        <p>Your AI guide to sustainable living</p>
    </div>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Chat interface
    st.markdown("### Chat History")
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["text"])

with col2:
    # Quick suggestions
    st.markdown("### Quick Topics")
    if st.button("🚗 Transportation Tips"):
        prompt = "What are some eco-friendly transportation options?"
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.write(response.text)
            st.session_state.chat_history.append({"role": "assistant", "text": response.text})

    if st.button("🏠 Home Energy Savings"):
        prompt = "How can I reduce my home energy consumption?"
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.write(response.text)
            st.session_state.chat_history.append({"role": "assistant", "text": response.text})

    if st.button("♻️ Recycling Guide"):
        prompt = "What are the best practices for recycling at home?"
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.write(response.text)
            st.session_state.chat_history.append({"role": "assistant", "text": response.text})

# Chat input at the bottom
user_input = st.chat_input("Ask me anything about sustainable living...")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    # Get AI response
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(user_input)
        st.write(response.text)
    
    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "assistant", "text": response.text})

# Add a clear chat button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.chat = model.start_chat(history=[])
    st.experimental_rerun() 