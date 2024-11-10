from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup as bs
from langchain_community.vectorstores import Chroma
import os
import google.generativeai as genai
import json
import requests
from django.conf import settings

# 데이터베이스 파일 초기화
db_path = settings.DB_PATH  # settings.py에 정의
api_key_path = settings.API_KEY_PATH
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("데이터베이스 초기화됨")
    except PermissionError:
        print("데이터베이스 접근 권한 오류")

# API 키 및 모델 설정
def load_api_key():
    try:
        with open(api_key_path, 'r') as file:
            data = json.load(file)
            print("API 키 로딩이 완료되었습니다.")
            return data.get('Gemini')
    except FileNotFoundError:
        print("API 키 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        print("API 키 파일의 JSON 형식이 올바르지 않습니다.")
        return None
    
# 모델 생성부 -----------------------------------------
api_key = load_api_key()
if api_key:
    # Gemini모델 생성
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Gemini 로딩이 완료되었습니다.")
    
    # sroberta모델 생성
    embedding = HuggingFaceEmbeddings(
        model_name='jhgan/ko-sroberta-nli',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("sroberta 로딩이 완료되었습니다.")
# -----------------------------------------------------

# 검색부
def load_Korean_game(gametitle, display=5, pageno=1):
    url = f'https://www.grac.or.kr/WebService/GameSearchSvc.asmx/game?display={display}&pageno={pageno}&gametitle={gametitle}'
    
    response = requests.get(url)
    response.raise_for_status()  # 오류 발생 시 예외 처리

    # HTML 파싱 및 본문 내용 추출
    soup = bs(response.text, 'xml') 
    content = soup.find_all('item')  # item 태그들 추출
    
    documents = [Document(page_content=i.text, metadata={"source": f"doc{idx+1}"}) for idx, i in enumerate(content)]
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    
    return splits

# Vectorstore 생성
def create_vectorstore(splits):
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding,  # `embedding` 인스턴스를 직접 전달
        persist_directory=db_path,
        collection_name="my_collection"
    )
    return vectorstore

vectorstore = None

@api_view(['GET'])
def send_subject(request):
    user_subject = request.query_params.get('subject')
    print(f"검색요청 : {user_subject}")
    splits = load_Korean_game(user_subject)
    global vectorstore
    if splits:
        vectorstore = create_vectorstore(splits)
        print(vectorstore)
    else:
        print("No content to create vector store.")
    
    return Response({"response": user_subject or "No subject provided"})


@api_view(['POST'])
def send_message(request):
    global vectorstore, model
    user_message = request.data.get('message')
    
    if vectorstore:
        context_doc = vectorstore.similarity_search(user_message, k=4)
        print(context_doc)
        prompt = f"Context: {context_doc}\nQuestion: {user_message}\nAnswer in a complete sentence:"
        
        response = model.generate_content(prompt)
        answer = response.candidates[0].content.parts[0].text
        
        return Response({"response": answer})
    else:
        return Response({"response": "Vector store not initialized. Please initialize with a subject first."})


def studyvue(request):
    query = request.GET.get("query")
    results = []
    if query:
        results = ["검색 결과 예시 1", "검색 결과 예시 2", "검색 결과 예시 3"]
    
    context = {
        "query": query,
        "results": results,
        'star_range': range(1, 16),
    }
    return render(request, "studyvue/test.html", context)