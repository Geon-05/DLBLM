import os
import google.generativeai as genai
import json
import streamlit as st

# 파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
target_file_path = os.path.join(current_dir, '../data/APIkey.json')

# 파일 읽기
with open(target_file_path, 'r') as file:
    data = json.load(file)  # JSON 파일을 파이썬 딕셔너리로 로드

# API 키 설정
api_key = data['Gemini']
genai.configure(api_key=api_key)

# 모델 로드 함수
def load_model():
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Model loaded...")
    return model



# Streamlit 세션에서 모델을 한 번만 로드하도록 설정
if "model" not in st.session_state:
    st.session_state.model = load_model()
    

# DB 및 모델 추가 부분 😤


# 세션의 대화 히스토리 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 사용자 입력과 버튼 처리
user_querie = st.text_input('질문을 입력하세요.')
if st.button('질문') and user_querie:
    # 사용자의 질문을 히스토리에 추가
    st.session_state.chat_history.append(f"[사용자]: {user_querie}")
    st.text(f'[사용자]\n{user_querie}')
    
    # 모델 응답 생성
    response = st.session_state.model.generate_content(user_querie)
    model_response = response.candidates[0].content.parts[0].text
    st.text(f'[모델]\n{model_response}')
    
    # 모델 응답을 히스토리에 추가 😤 히스토리 내용을 기억하지 못함
    st.session_state.chat_history.append(f"[모델]: {model_response}")
    
    # 전체 히스토리 출력
    st.text('--------------------------------------------')
    st.text("\n".join(st.session_state.chat_history))
