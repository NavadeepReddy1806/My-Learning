import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Question Answering Bot",layout="centered")
st.title('Question Answering with SQuAD2')

st.markdown(
    '''<style>
            textarea, .stTextInput > div > input{
            font-size=16px !important;}
        </style>
''',unsafe_allow_html=True
)

@st.cache_resource
def load_pipeline():
    return pipeline('question-answering',model='deepset/roberta-base-squad2')

qa_pipeline=load_pipeline()

context=st.text_area("Context",height=250,placeholder="Enter the context......")
question=st.text_input("Question",placeholder='Enter the question......')

if st.button("Get Answer"):
    if context.strip()=="" or question.strip()=="":
        st.warning("Enter something in the fileds!")
    else:
        with st.spinner("Thinking......"):
            result=qa_pipeline({"context":context,"question":question})
            answer=result['answer']
            score=result['score']
        if answer.strip()=="":
            st.error("Sorry, I couldn't find an answer")
        else:
            st.success(f"**Answer:** {answer}")
            st.markdown(f"**Confidence:** {score:.2f}")