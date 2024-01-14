"""
1. Setting
    1.1 데이터베이스 연동 및 읽어오기
    1.2 유저 설정
        1.2.1 새로운 유저 -> 계정 등록 맟 초기화
        1.2.2 기존 유저 -> 계정 설정 및 채팅 기록 불러오기
2. Chat
    2.1 대화 응답
    2.2 위험상황 감지
        1.2.1 유저 경고 수 증가
    2.3 위험상황 횟수 초과 
        2.3.1 사용자 IP / 아이디 / 비밀번호 
        2.3.2 현재까지의 대화 모음
        2.3.3 신고(?) / 강제 종료되기
"""
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore

from prompt import getResponse, isDangerous

uid = st.session_state["id"]
st.title("Chat Page Prototype")


##### Setting #####
patrol = OpenAI(api_key=st.secrets["api_key"])
# 1.1 데이터베이스 연동 및 읽어오기
cred = credentials.Certificate('.streamlit/metaverse-patrol-firebase-adminsdk-uyg9e-7ccf8ecea3.json')
try:
    default_app = firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)

# 1.2 데이터베이스 읽어오기
main_collection = firestore.client().collection('database')
db = [doc.to_dict() for doc in main_collection.stream()]

# 로그인한 유저 불러오기
get_user_query = main_collection.where('uid', '==', uid)
user_data = [doc for doc in get_user_query.stream()]
# st.write("user",user_data)

# 1.2.1 새로운 유저인 경우, 계정 생성하기
if user_data == []:
    new_user = {
        "uid": uid,
        "cnt": 0,
        "chat": []
    }
    main_collection.add(new_user)
    user = new_user
# 1.2.2 기존 유저인 경우, 채팅 기록 불러오기
else:        
    # 유저 세팅
    user = user_data[0]

    # # get chat documents
    document_id = user_data[0].id
    sub_collection = main_collection.document(document_id).collection('chat')
    chat_history = [doc.to_dict() for doc in sub_collection.stream()]
    # st.write("chat_history", chat_history)

    for message in chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
print(user)
print(chat_history)
    
   
##### Chat #####
# 유저 인풋 
if prompt := st.chat_input("대화를 시작하세요"):
    # 채팅 기록에 추가
    user_message = {"role": "user", "content": prompt}
    chat_history.append(user_message)
    sub_collection.add(user_message) 
    
    # 화면에 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 1. user_message의 위험도 확인하기
    print(chat_history[-1:-3])
    if isDangerous(user_message):
        cnt = user.to_dict()["cnt"]
        main_collection.document(user.id).update({"cnt": cnt+1})

        print(user.to_dict()["cnt"])
        if cnt >= 3:
            print("caught")
            switch_page("end")


    # 2. 대화에 응답하기
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        assistant_response = ""
        assistant_response = getResponse(patrol)
        message_placeholder.markdown(assistant_response)
    
        assistant_message = {"role": "assistant", "content": assistant_response}
        chat_history.append(assistant_message)
        sub_collection.add(assistant_message)

