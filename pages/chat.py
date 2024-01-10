# import random
# import streamlit as st
# from openai import OpenAI
# from tinydb import TinyDB, Query, where

# st.title("Chat Page Prototype")
# st.button("종료하기")
# patrol = OpenAI(api_key=st.secrets["api_key"])

# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# # Initialize chat history from previous sessions
# user_id = st.session_state.id
# print(user_id)
# database = TinyDB('./database/databse.json')

# user_table = database.table("user")
# warning_table = database.table("warn")
# user = Query()


# chat_history = user_table.search(where('user_id') == user_id)
# print(chat_history)

# if chat_history == []:
#     warning_table.insert({"user_id": user_id, "cnt": 0})

# # 이전 대화 기록이 존재한다면 다시 나타내기 (세션)
# for message in chat_history:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # := : 표현식의 결과를 할당하고 반환
# # 유저 인풋 
# if prompt := st.chat_input("대화를 시작하세요"):
#     # 채팅 기록에 추가
#     user_message = {"role": "user", "content": prompt}
#     chat_history.append(user_message)
#     user_table.insert(user_message) 
    
#     # 화면에 표시
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # 1. user_message의 위험도 확인
#     user_cnt = warning_table.search(where('user_id') ==user_id)
#     print(user_cnt)
#     # isDanger = isDangerResponse()
#     # if isDanger:
#             # warning_table.update({'cnt' : str()}, user.roll_number == 1 )

#     #     warning_table.update(increment("cnt"), Query().user_id == user_id)
#     #     if user.search[""]

#     # 봇의 응답
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         assistant_response = ""
#         assistant_response = random.choice([
#             "Hello there! How can I assist you today?",
#             "Hi, human! Is there anything I can help you with?",
#             "Do you need help?",
#         ])
        
#         ######## GPT 통신 ########
   
#         ### 2. 대화에 응답하기
#         # for response in patrol.chat.completions.create( 
#         #     model=st.session_state["openai_model"],
#         #     messages=[
#         #         {"role": m["role"], "content": m["content"]} for m in chat_history
#         #     ],
#         #     stream=True
#         # ):
#         #     assistant_response += (response.choices[0].delta.content or "")
#         #     message_placeholder.markdown("▌")
        
#         ### 
#         message_placeholder.markdown(assistant_response)
    
#         assistant_message = {"role": "assistant", "content": assistant_response}
#         chat_history.append(assistant_message)
#         user_table.insert(assistant_message)

