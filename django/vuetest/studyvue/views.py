from django.shortcuts import render

# chat/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def send_message(request):
    user_message = request.data.get('message')
    bot_response = f"챗봇 응답: {user_message}"
    return Response({"response": bot_response})

@api_view(['GET'])
def send_subject(request):
    user_subject = request.query_params.get('subject')  # GET 요청에서 매개변수 받기
    return Response({"response": user_subject})


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