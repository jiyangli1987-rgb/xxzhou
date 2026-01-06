import streamlit as st

st.title("聊天机器人")

with st.chat_message("user"):
    st.markdown("你好")

with st.chat_message("AI"):
    st.markdown("你好，有什么可以帮你的吗？")

st.chat_input("请输入您的问题……")