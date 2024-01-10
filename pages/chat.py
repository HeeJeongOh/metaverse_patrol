import random
import streamlit as st
from openai import OpenAI
from tinydb import TinyDB, Query

st.title("Chat Page Prototype")
st.button("종료하기")
patrol = OpenAI(api_key=st.secrets["api_key"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history from previous sessions
user_id = st.session_state.id
print(user_id)

db = TinyDB(f'./database/{user_id}.json')

chat_history = db.all()

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# 이전 대화 기록이 존재한다면 다시 나타내기 (세션)
print(chat_history)
for message in chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# := : 표현식의 결과를 할당하고 반환
# 유저 인풋 
if prompt := st.chat_input("대화를 시작하세요"):
    # 채팅 기록에 추가
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)
    db.insert(user_message) 
    
    # 화면에 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # 봇의 응답
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        assistant_response = ""
        assistant_response = random.choice([
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ])
        
        ######## GPT 통신 ########
        # for response in patrol.chat.completions.create( 
        #     model=st.session_state["openai_model"],
        #     messages=[
        #         {"role": m["role"], "content": m["content"]} for m in chat_history
        #     ],
        #     stream=True
        # ):
        #     assistant_response += (response.choices[0].delta.content or "")
        #     message_placeholder.markdown("▌")
            
        message_placeholder.markdown(assistant_response)
    
        assistant_message = {"role": "assistant", "content": assistant_response}
        chat_history.append(assistant_message)
        db.insert(assistant_message)