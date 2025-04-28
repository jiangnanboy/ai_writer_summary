import streamlit as st

from src import generate_article, summary_article
from src.init import deepseek_model

st.title('智能写作与总结')
option_task = st.sidebar.radio('目前支持以下功能', ('写作', '总结'))

col1, col2 = st.columns(2)

@st.cache_data(ttl=6*5, max_entries=10)
def generate(topic:str, word_count:int):
    print(f"生成文章主题是 '{topic}'，大概 {word_count} 字...\n")
    markdown_content = generate_article(topic, word_count, model=deepseek_model)
    return markdown_content

@st.cache_data(ttl=6*5, max_entries=10)
def summary(content:str):
    print(f"文章内容总结 ...\n")
    markdown_content = summary_article(content, model=deepseek_model)
    return markdown_content

if option_task == '写作':
    topic = st.text_input('输入要生成文章的主题', )
    word_count = st.slider('选择生成的文章字数', 100, 8000, 2000)
    if st.button('开始'):
        if topic is None or len(topic.strip()) == 0:
            st.write('主题不能为空!')
        else:
            content_summary = generate(topic, word_count)
            st.markdown(content_summary)

if option_task == '总结':
    content = st.text_area('输入需要总结观点的文章内容', height=500)
    if st.button('开始'):
        if content is None or len(content.strip()) == 0:
            st.write('内容不能为空!')
        else:
            summary_response = summary(content)
            st.markdown(summary_response)

