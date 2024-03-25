__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import openai
import streamlit as st
import pandas as pd
import random

# OpenAI API 키 로드
openai.api_key = os.getenv('OPENAI_API_KEY')

st.title("Chat with Data File via ChatGPT")
st.write("---")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])
st.write("---")

def load_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
            df = pd.read_excel(uploaded_file)
        return df

def generate_sentence_with_word(word):
    # OpenAI의 ChatGPT API를 사용하여 주어진 단어를 포함한 문장 생성
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # 수정된 엔진 명칭
        prompt=f"Create a sentence using the word '{word}':",
        max_tokens=60,
        temperature=0.7
    )
    return response.choices[0].text.strip()

if uploaded_file is not None:
    if 'words_list' not in st.session_state or 'index' not in st.session_state:
        st.session_state['words_list'] = []
        st.session_state['index'] = 0
    
    df = load_file(uploaded_file)
    words_column = 'words'
    if words_column in df.columns and not st.session_state['words_list']:
        st.session_state['words_list'] = df[words_column].dropna().tolist()
        random.shuffle(st.session_state['words_list'])  # 단어 리스트를 랜덤으로 섞음
    
    if st.button("다음 단어"):
        st.session_state['index'] = (st.session_state['index'] + 1) % len(st.session_state['words_list'])
    
    if st.session_state['words_list']:
        word = st.session_state['words_list'][st.session_state['index']]
        sentence = generate_sentence_with_word(word)
        st.write(sentence)
    else:
        st.write("업로드된 파일에 'words' 열이 포함되어 있지 않습니다.")
