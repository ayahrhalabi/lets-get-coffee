import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Coffee ChainBot", page_icon="☕")
st.title("☕ Let's Get Coffee - Chatbot")
st.write("Ask me anything about coffee shops in LA!")

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
# User input
    user_input = st.chat_input("Where can I find good matcha?")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                # Send POST request to your Cloud Run RAG endpoint
                try:
                    response = requests.post(
                        "https://letsgetcoffee-image-508717259631.us-central1.run.app/ask",
                        json={"question": user_input},
                        timeout=10
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.markdown(result.get("answer", "No response field named 'answer'."))
                    else:
                        st.error(f"Server error: {response.status_code}")
                except Exception as e:
                    st.error(f"Failed to reach model: {e}")

