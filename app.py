import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables
load_dotenv()

# 2. Get the API key
# Even though the variable is named GROK_API_KEY, it's actually a Groq key. 
api_key = os.getenv("GROK_API_KEY")
if not api_key:
    st.error("Error: API Key not found. Please check your .env file.")
    st.stop()

# 3. Initialize the client using Groq's base URL
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1", # Changed to Groq's URL
)

# 4. Set up the Streamlit web page
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🤖 Groq Chatbot")

# 5. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful and concise AI assistant."}
    ]

# 6. Display chat messages from history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. React to user input
if prompt := st.chat_input("What's on your mind?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Send request to Groq API using a valid Groq model
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant", # Updated model name
                messages=st.session_state.messages,
            )
            
            bot_reply = response.choices[0].message.content
            message_placeholder.markdown(bot_reply)
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")