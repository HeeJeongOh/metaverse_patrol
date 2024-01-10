import streamlit as st
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore
import random

uid = st.session_state["id"]
st.title("Chat Page Prototype")
st.button("종료하기")

patrol = OpenAI(api_key=st.secrets["api_key"])
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

cred = credentials.Certificate('.streamlit/metaverse-patrol-firebase-adminsdk-uyg9e-7ccf8ecea3.json')
try:
    default_app = firebase_admin.get_app()
except ValueError:
    # If the app doesn't exist, initialize Firebase
    firebase_admin.initialize_app(cred)
    
main_collection = firestore.client().collection('database')

# get user document
db = [doc.to_dict() for doc in main_collection.stream()]
get_user_query = main_collection.where('uid', '==', uid)
user_data = [doc.to_dict() for doc in get_user_query.stream()]
# st.write("user",user_data)

# set new user
if user_data == []:
    new_user = {
        "uid": uid,
        "cnt": 0,
        "chat": []
    }
    main_collection.add(new_user)
    
user_data = [doc for doc in get_user_query.stream()]
user = user_data[0]
st.write("user",user.to_dict())

# # get chat documents
document_id = user_data[0].id
sub_collection = main_collection.document(document_id).collection('chat')
# Iterate over the results and extract the data
chat_history = [doc.to_dict() for doc in sub_collection.stream()]
# st.write("chat_history", chat_history)

for message in chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        

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
    # if isDanger():
    print(user.to_dict())
    cnt = user.to_dict()["cnt"]
    main_collection.document(user.id).update({"cnt": cnt+1})
    print(user.to_dict)
    
    # 2. 대화에 응답하기
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        assistant_response = ""
        assistant_response = random.choice([
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ])
        
        ######## GPT 통신 ########
   
        ### 2. 대화에 응답하기
        # for response in patrol.chat.completions.create( 
        #     model=st.session_state["openai_model"],
        #     messages=[
        #         {"role": m["role"], "content": m["content"]} for m in chat_history
        #     ],
        #     stream=True
        # ):
        #     assistant_response += (response.choices[0].delta.content or "")
        #     message_placeholder.markdown("▌")
        
        ### 
        message_placeholder.markdown(assistant_response)
    
        assistant_message = {"role": "assistant", "content": assistant_response}
        chat_history.append(assistant_message)
        sub_collection.add(assistant_message)

