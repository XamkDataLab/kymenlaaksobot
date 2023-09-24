import openai
import streamlit as st
from prompts import *

st.title("Kysy Kaakkois-Suomen ammattikorkeakouusta")
openai.api_key = st.secrets["apikey"]

available_prompts = [
    ("Opas Tamperelaisille", system_prompt1),
    ("Opas Savolaisille", system_prompt2),
    ("Opas Helsinkiläisille", system_prompt3)
]

selected_prompt_name, selected_prompt_content = st.selectbox(
    "Valitse asiantuntija",
    options=available_prompts,
    format_func=lambda option: option[0]  #
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if prompt := st.chat_input("Kysy xamkista"):

    st.session_state.messages.append({"role": "system", "content": selected_prompt_content})
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

   
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("...asiantuntija kirjoittaa...▌")  

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

