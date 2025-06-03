import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Let's Get Coffee", page_icon="☕", layout="wide")

# Inject custom styles
st.markdown("""
<style>
/* Chat input container */
[data-testid="stChatInput"] {
    background-color: #CCD5AE;
    border: 2px solid #6C584C;
    border-radius: 12px;
    padding: 6px;
}

/* Input field */
[data-testid="stChatInput"] input {
    background: transparent;
    color: #3E3E3E;
    font-weight: 600;
    border: none;
    outline: none;
}

/* Placeholder text */
[data-testid="stChatInput"] input::placeholder {
    color: #6C584C;
}

/* Chat message (assistant side) */
.chat-message .stMarkdown {
    color: #3E3E3E;
}

/* Chat message (user side) */
.chat-message.user {
    background-color: #DDE5B6;
    color: #3E3E3E;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #CCD5AE;
    color: #3E3E3E;
}
</style>
""", unsafe_allow_html=True)


# Sidebar navigation
st.sidebar.title("☕ Let's Get Coffee")
page = st.sidebar.radio("Menu", ["Welcome", "Coffee Shop Map", "Chatbot"])

# Coffee Shop Map Page
if page == "Welcome":
    st.title(" 👋 Welcome to Let's Get Coffee!")
    st.subheader("Our Story")
    st.write(
    "Los Angeles is an exciting place to live. Of course, there are beaches, museums, parks, and more. "
    "But when you're a student, the only place you truly have outside of campus is... well, you guessed it — coffee shops. "
    "With LA being LA, navigating all the different spots to study solo, hang out with a friend, or dive into a book can be overwhelming. "
    "That’s where *Let's Get Coffee* comes in!"
    )

    st.subheader("Overview of the Site")
    st.write(
    "This website has two main features. First, a map of some coffee shops in LA, so you can visualize where they’re located. "
    "Second — and this is the fun part — our Coffee ChatBot! You can tell it what you’re looking for in a coffee shop, and it’ll try to recommend the perfect place for you."
)


elif page == "Coffee Shop Map":
    st.title("📍 Coffee Shop Map")
    st.write("Use the Map to learn about some available coffee shops in LA! Hover over the location of your liking and use the Chatbot for specific questions!")
    
    df = pd.read_csv("updated_coffee_shops.csv")
    try:
        fig = px.scatter_mapbox(
            df,
            lat='Latitude',
            lon='Longitude',
            hover_name='Name',
            hover_data=['Address', 'Rating'],
            zoom=11,
            height=650
        )
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0, "t":0, "l":0, "b":0}
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating map: {str(e)}")
        st.write("Columns:", list(df.columns))
        st.write(df.head())

# Chatbot Page
elif page == "Chatbot":
    st.title("💬 Coffee Shop Chatbot")
    st.write("Ask me anything about coffee shops in LA!")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    user_input = st.chat_input("Where can I find good matcha?")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        "https://letsgetcoffee-image-508717259631.us-central1.run.app/ask",
                        json={"question": user_input},
                        timeout=10
                    )
                    if response.status_code == 200:
                        result = response.json()
                        answer = result.get("answer", "⚠️ No response found.")
                    else:
                        answer = f"❌ Server error: {response.status_code}"
                except Exception as e:
                    answer = f"❌ Failed to reach model: {e}"

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
#old 
