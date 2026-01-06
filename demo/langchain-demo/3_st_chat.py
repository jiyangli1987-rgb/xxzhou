import streamlit as st
st.title("聊天机器人")

prompt = st.chat_input("请输入您的问题……")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("AI"):
        st.markdown("你好，有什么可以帮你的吗？")