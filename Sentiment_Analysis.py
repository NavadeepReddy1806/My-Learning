from transformers import pipeline
import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Sentiment Analysis",layout="centered")
st.markdown("Upload a file (.csv,.xlsx,.json,.txt,.tsv)")

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis",model="distilbert-base-uncased-finetuned-sst-2-english")
analyzer=load_model()

uploaded_file=st.file_uploader("Upload file: ",type=['csv','txt','tsv','xlsx','json'])
def load_file(file):
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)
        elif file.name.endswith('.tsv'):
            return pd.read_csv(file,sep='\t')
        elif file.name.endswith('.txt'):
            lines=file.read().decode('utf-8').splitlines()
            return pd.DataFrame({'text':lines})
        elif file.name.endswith('.json'):
            data=json.load(file)
            if isinstance(data,list):
                return pd.DataFrame(data)
            elif isinstance(data,dict):
                return pd.DataFrame.from_dict(data)
    except Exception as e:
        st.error(f"Falied to load the file: {e}")
        return None
if uploaded_file:
    df=load_file(uploaded_file)
    if df is not None:
        if "text" not in df.columns:
            st.warning("No column named text!")
        else:
            st.write(df.head())
            st.subheader("Sentiment Analysis")
            with st.spinner("Analyzing....."):
                results=analyzer(df['text'].astype(str).tolist(),truncation=True)
                df['Sentiment']=[r["label"] for r in results]
                df['Confidence']=[round(r['score'],3) for r in results]
            st.success("Done")
            st.write(df.head(10))
            st.download_button("Download",data=df.to_csv(index=False),file_name="Sentiment Analysis",mime='text/csv')
text_input=st.text_area("Write something.......")
if st.button("Analyze Sentiment"):
    if text_input.strip():
        result=analyzer(text_input)[0]
        st.markdown(f"**Sentiment**: {result['label']} &nbsp;&nbsp;&nbsp; **Confidence**: {round(result['score'],3)}")
    else:
        st.warning("Please enter text!")
