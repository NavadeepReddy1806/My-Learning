import streamlit as st
st.set_page_config(page_title="Text Summarizer", layout="centered")
from transformers import T5Tokenizer,T5ForConditionalGeneration

@st.cache_resource
def load_model():
    model_name='t5-small'
    tokenizer=T5Tokenizer.from_pretrained(model_name)
    model=T5ForConditionalGeneration.from_pretrained(model_name)
    return model,tokenizer

model,tokenizer=load_model()

st.title("Abstractive Text Summarizer")
st.markdown("Paste any article or text and get a summary!")

input_text=st.text_area("Enter text to summarize.",height=300)
if st.button("Summarize"):
    if input_text.strip()=="":
        st.warning("Please enter some text!")
    else:
        text=tokenizer.encode("summarize: "+input_text,return_tensors='pt',max_length=512,truncation=True)
        summarize=model.generate(text,max_length=350,min_length=40,length_penalty=0.8,num_beams=4,early_stopping=True)
        output=tokenizer.decode(summarize[0],skip_special_tokens=True)

        st.subheader("Summary: ")
        st.success(output)
