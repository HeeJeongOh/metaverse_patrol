# from openai import OpenAI
# import streamlit as st
# from keys import *
# from database import *

# # st.title("Chat Page with Patrol")

# patrol = OpenAI(api_key=api_key)

# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# # 이전 대화가 존재했는지 확인하기
# # chat_history = database.
# # 
# # 대화 기록 초기화
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # 이전 대화 기록이 존재한다면 다시 나타내기 (세션)
# print(st.session_state.messages)
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # := : 표현식의 결과를 할당하고 반환
# # 유저 인풋 
# if prompt := st.chat_input("What is up?"):
#     # 채팅 기록에 추가
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     # 화면에 표시
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # 봇의 응답
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         for response in patrol.chat.completions.create( 
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True
#         ):
#             full_response += (response.choices[0].delta.content or "")
#             # message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
        
#     st.session_state.messages.append({"role": "assistant", "content": full_response})

# database[id] += st.session_state