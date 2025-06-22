import streamlit as st
import openai
import os
import re

st.set_page_config(page_title="My Chatbot",layout="centered")
st.title("Chatbot")

openai.api_key="tgp_v1_uKwK548I_W6IvZ2P0_TFsaX6ZcV3E6aSr-qEn4hfj2s"
openai.api_base="https://api.together.xyz/v1"

rules={
    "hello": "Hi there! How can I help you?",
    "hi": "Hello! Ask me anything.",
    "thanks": "You're welcome!",
    "bye": "Goodbye! Have a great day.",
    "who are you": "I am a chatbot.",
    "how are you": "I am fine, what about you?"
}

def rule_based_response(user_input:str):
    user_input=user_input.lower()
    for pattern,msg in rules.items():
        if re.search(rf"\b{re.escape(pattern)}\b",user_input):
            return msg
    return None

def llama_response(user_input:str):
    user_input=user_input.lower()
    try:
        response=openai.ChatCompletion.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{'role':'user','content':user_input}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Llama Model error: {str(e)}"

if "history" not in st.session_state:
    st.session_state.history=[]

with st.form(key="chat_form"):
    user_input=st.text_input("You: ",placeholder="Ask me anything....")
    submitted=st.form_submit_button("Send")

if submitted and user_input:
    rule_response=rule_based_response(user_input)
    if rule_response:
        reply=rule_response
    else:
        reply=llama_response(user_input)
    st.session_state.history.append(("You",user_input))
    st.session_state.history.append(("Bot",reply))

for speaker,message in st.session_state.history:
    st.markdown(f"**{speaker}:** {message}")

with st.sidebar:
    st.header("Chats")
    user_inputs=[message for speaker,message in st.session_state.history if speaker=="You"]
    if user_inputs:
        for idx,msgs in enumerate(user_inputs,1):
            st.markdown(f"**{idx}:** {msgs}")
        if st.button("Clear History"):
            st.session_state.history=[]
            st.rerun()
    else:
        st.info("No chat history yet.")