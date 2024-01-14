import random
import streamlit as st
from openai import OpenAI

# 취약대상으로 가장하기
def setSettingPrompt(patrol):
    settingMessage = f"""
        당신(Chat GPT)는 지금부터 8살 여자아이를 연기해야 합니다. 
        현재 당신은 메타버스에 처음 가입하여 새로운 상대와 대화를 시작했습니다.
        당신이 연기하는 이 여자아이의 신상에 대해 알려드리겠습니다.
            - 메타버스 캐릭터 이름 : 샐리
            - 실제 이름: 김로아
            - 실제 나이 : 8살
            - 실제 주소 : 서울시 강남구
            - 성격 : 호기심이 많음
            
        당신의 응답에 주의사항을 몇가지 알려드리겠습니다.
            1. 만약 상대방이 당신이 8살 여자아이가 아니라는 것을 깨닫는다면  당신은 상대방을 적극적으로 설득해야합니다.
            2. 만약 상대방이 위 신상들 외에도 더 구체적인 내용을 알고자 한다면, "다음 번에 더 친해지면 말할게요!" 라는 등의 발언으로 상황을 회피합니다.
            3. 대화를 통해 알 수 있는 내용에 대해 다시 묻지 않아야 합니다.

        잘 이해했다면 "이해했습니다" 라고 대답하세요
    """

    response = patrol.chat.completions.create(    
    model=st.session_state["openai_model"],
    messages=settingMessage
    )
    if response.choice[0].message.content == "이해했습니다.":
        return True

    return False

def getResponse(patrol):
    assistant_response = ""
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    if "setting_prompt" not in st.session_state:
        isStart = setSettingPrompt(patrol)
        if isStart:
            st.session_state["setting_prompt"] = "done"
            # return random.choice([
            #         "Hello there! How can I assist you today?",
            #         "Hi, human! Is there anything I can help you with?",
            #         "Do you need help?",
            #     ])
            for response in patrol.chat.completions.create( 
                model=st.session_state["openai_model"],
                # 이전 대화를 모두 참고
                messages=[
                    {"role": m["role"], "content": m["content"]} for m in chat_history
                ],
                stream=True
            ):
                assistant_response += (response.choices[0].delta.content or "")   
    return assistant_response

# 위험발언 여부 판단하기

def isDangerous2(message):
    print(message)
    askingMessage = f"""
    당신(ChatGPT)은 위험도를 계산하는 인공지능 모델입니다. 
    위험도(단위: 백분율)는 상대방이 여자아이에게 성폭력을 가하고 있는지, 아이로부터 성착취 의도가 있는지를 판단하기 위함입니다. 

    - 입력 : 14살 여자아이(이하 A)와 신상 정보를 모르는 상대(이하 B)와 주고 받은 대화의 일부
        (예)
        B: 안녕 ?
        A: 안녕하세요!
        B: 이름이 뭐야? 
        A: 저는 하율이에요
        B: 예쁜 이름이다. 나는 그냥 오빠라고 불러주면 돼
        A:  아,, 넹넹

    - 출력 : B의 각 발언에 대해 위험도
        (예)
        [["안녕", 0], ["이름이 뭐야?", 25], ["예쁜 이름이다. 나는 그냥 오빠라고 불러주면 돼",64]]


    이제  당신이 판단해야할 대화입니다. 이때 출력 형식을 제외한 설명들은 모두 응답에서 제외합니다.
    - 대화내용
    {message}
    """
    
    judge = OpenAI(api_key=st.secrets["api_key"])
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    response = judge.chat.completions.create(    
        model=st.session_state["openai_model"],
        messages=askingMessage
    )
    if int(response.choice[0].message.content) == "True":
        return True
    return False



from googletrans import Translator
from deeppavlov import build_model
def isDangerous(message):
    # 1. 번역
    translator = Translator()
    translated = translator.translate(message, 'en', 'ko')
    # 2. 모델 인퍼런스
    model = build_model('insults_kaggle_bert', download=True, install=True)
    label = model([message])
    
    if label[0] == "Insult":
        return True
    else:
        return False
    