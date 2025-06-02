import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Let's Get Coffee", page_icon="☕", layout="wide")

# Inject custom styles
st.markdown("""
<style>
[data-testid="stChatInput"] {
    border: 2px solid #6C584C;
    background-color: #FAEDCD;
    color: #3E3E3E;
    border-radius: 12px;
}
[data-testid="stChatInput"] input {
    color: #3E3E3E !important;
}
.chat-message .stMarkdown {
    color: #3E3E3E;
}
.chat-message.user {
    background-color: #f0e6d6;
    color: #333;
}
/* Sidebar background and text color */
[data-testid="stSidebar"] {
    background-color: #CCD5AE;
    color: #CCD5AE;
}

/* Sidebar widget text color */
[data-testid="stSidebar"] {
    color: #CCD5AE;
}

/* Sidebar title text */
[data-testid="stSidebar"] {
    color: #656D4A;
}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("☕ Let's Get Coffee")
page = st.sidebar.radio("Menu", ["Welcome", "Coffee Shop Map", "Chatbot"])

# Coffee Shop Map Page
if page == "Welcome":
    st.title("Welcome to Let's Get Coffee!")
    st.subheader("Our Story")
    st.write("Los Angeles is an exciting place to live in. While ofcourse you have the beaches, museuams, " \
    "parks etc... However when you are a student the only place you truly have other than campus is... well you guessed it... coffee shops. " \
    " With LA being LA, navigating through the different coffee shops to study alone, \"study\" with a friend, or read a book etc.. can be overwhelming." \
    "This is where Let's get coffee comes in!")
    st.subheader("Overview of Site")
    st.write(" There are 2 components for this website. The first, you have a map of some coffee shops in LA to provide a visualization on where some coffee shops are located. " \
    "The second (the fun part hehe) is our Coffee ChatBot where you can tell it what you are looking for in a specific coffee shop, and it will try to " \
    "recommend you a specific place. ")

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

    user_input = st.chat_input("Where can I find good matcha?")

    if user_input:
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
                        st.markdown(result.get("answer", "⚠️ No response found."))
                    else:
                        st.error(f"❌ Server error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Failed to reach model: {e}")

