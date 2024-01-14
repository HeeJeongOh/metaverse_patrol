import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.title("대화가 종료되었습니다.")

uid = st.session_state["id"]

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

document_id = user_data[0].id

sub_collection = main_collection.document(document_id).collection('chat')
chat_history = [doc.to_dict() for doc in sub_collection.stream()]
st.markdown(chat_history)
