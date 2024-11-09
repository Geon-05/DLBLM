from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import google.generativeai as genai
import json
from django.conf import settings

# 데이터베이스 파일 초기화
db_path = settings.DB_PATH  # settings.py에 정의
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("데이터베이스 초기화됨")
    except PermissionError:
        print("데이터베이스 접근 권한 오류")

# API 키 및 모델 설정
def load_api_key():
    api_key_path = settings.API_KEY_PATH
    try:
        with open(api_key_path, 'r') as file:
            data = json.load(file)
            return data.get('Gemini')
    except FileNotFoundError:
        print("API 키 파일을 찾을 수 없습니다.")
        return None

api_key = load_api_key()
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')


@api_view(['POST'])
def send_message(request):
    user_message = request.data.get('message')
    # 챗봇 응답 생성 로직 추가
    if user_message and model:
        bot_response = model.generate_text(user_message)
        return Response({"response": bot_response})
    return Response({"response": "응답 생성 오류 발생"})


@api_view(['GET'])
def send_subject(request):
    user_subject = request.query_params.get('subject')
    return Response({"response": user_subject or "No subject provided"})


def studyvue(request):
    query = request.GET.get("query")

    results = []
    if query:
        results = ["검색 결과 예시 1", "검색 결과 예시 2", "검색 결과 예시 3"]

    context = {
        "query": query,
        "results": results,
        'star_range': range(1, 16),  # 1부터 15까지의 범위를 템플릿에 전달
    }
    return render(request, "studyvue/test.html", context)