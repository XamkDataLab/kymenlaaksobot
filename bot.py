import openai
import streamlit as st
from prompts import *

st.title("Ulkopolitiikkabot")

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize available system prompts list
# (You can add more prompts as per your requirements)
available_prompts = [
    ("System Prompt 1", system_prompt1),
    ("System Prompt 2", system_prompt2),
    # Add more prompts if needed
]

# Dropdown for the user to select a system prompt
selected_prompt_name, selected_prompt_content = st.selectbox(
    "Select a System Prompt",
    options=available_prompts,
    format_func=lambda option: option[0]  # This will display the name part only in the dropdown
)

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Keskustele ulkopolitiikasta"):
    # Add user message to chat history with the selected system prompt
    st.session_state.messages.append({"role": "system", "content": selected_prompt_content})
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            if response.choices[0].delta.get("role") != "system":
                full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

