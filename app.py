import streamlit as st
from main import ask


st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Agent")
st.caption("Ask me questions and I'll do my best to answer them!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
prompt = st.chat_input("Ask me something...")

if prompt:
    # Store and display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = ask(prompt)
                st.markdown(response)

            except Exception as e:
                response = f"Error: {str(e)}"
                st.error(response)

    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )