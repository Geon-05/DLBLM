import os
import google.generativeai as genai
import json
import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup as bs
import requests
from langchain_community.vectorstores import Chroma

# 데이터베이스 파일 경로
db_path = "path_to_chroma_db"  # 실제 데이터베이스 경로로 변경

# 기존 데이터베이스 파일 삭제
try:
    if os.path.exists(db_path):
        os.remove(db_path)
        print("데이터베이스 초기화됨")
except PermissionError:
    print("데이터베이스 파일에 접근 권한이 없습니다. 관리자 권한으로 실행하거나 파일을 수동으로 삭제해 주세요.")
# 파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
target_file_path = os.path.join(current_dir, 'D:/important/APIkey.json')

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


# 모델 생성부 -----------------------------------------
# Streamlit 세션에서 모델을 한 번만 로드하도록 설정
if "model" not in st.session_state:
    with st.spinner("모델로딩중"):
        st.session_state.model = load_model()

# SKT 한국어 임베딩 및 QA 모델 설정
if "embedding" not in st.session_state:
    with st.spinner("임베딩 로딩중"):
        hf_embeddings = HuggingFaceEmbeddings(
            model_name='jhgan/ko-sroberta-nli',
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    st.session_state.embedding = hf_embeddings
# -----------------------------------------------------

# 검색부
def load_Korean_game(gametitle, display=5, pageno=1):
    url = f'https://www.grac.or.kr/WebService/GameSearchSvc.asmx/game?display={display}&pageno={pageno}&gametitle={gametitle}'
    
    response = requests.get(url)
    response.raise_for_status()  # 오류 발생 시 예외 처리

    # HTML 파싱 및 본문 내용 추출
    soup = bs(response.text, 'html.parser')
    content = soup.find_all('item')  # item 태그들 추출
    
    paragraphs = []
    for idx, i in enumerate(content):
        if i:
            paragraphs.append(i.text)
    
    # 텍스트 변환 및 Document 객체로 변환    
    documents = [Document(page_content=doc, metadata={"source": f"doc{i+1}"}) for i, doc in enumerate(paragraphs)]
    
    # 텍스트 스플릿
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    return splits

# vectorstore 생성 함수
def create_vectorstore(splits):
    # 세션에 vectorstore가 이미 존재하는 경우 재사용
    if "vectorstore" in st.session_state:
        return st.session_state.vectorstore
    
    valid_splits = []
    for i, split in enumerate(splits):
        embedding = st.session_state.embedding.embed_query(split.page_content)
        
        if embedding and len(embedding) > 0:
            print(f"Embedding created for split {i+1}, length: {len(embedding)}")
            valid_splits.append(split)
        else:
            print(f"Empty embedding for split {i+1}")

    if valid_splits:
        # 새로운 vectorstore 생성 및 세션에 저장
        vectorstore = Chroma.from_documents(
        documents=valid_splits,
        embedding=st.session_state.embedding,
        persist_directory="path_to_chroma_db",  # 데이터베이스 경로 지정
        collection_name="my_collection"
    )

        # 생성된 vectorstore를 세션 상태에 저장하여 재사용
        st.session_state.vectorstore = vectorstore
        return vectorstore
    else:
        raise ValueError("No valid documents with embeddings to add to vector store.")

# 세션의 대화 히스토리 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 사용자 입력과 버튼 처리
topic = st.text_input('게임명을 입력하세요.d')
question = st.text_input('질문을 입력하세요.')
if st.button('질문') and question:
    # 사용자 입력부
    splits = load_Korean_game(topic)
    
    if splits:
        st.session_state.vectorstore = create_vectorstore(splits)
    else:
        print("No content to create vector store.")
        
    context_doc = st.session_state.vectorstore.similarity_search(question, k=4)
    prompt = f"Context: {context_doc}\nQuestion: {question}\nAnswer in a complete sentence:"
    response = st.session_state.model.generate_content(prompt)
    answer = response.candidates[0].content.parts[0].text

    # 질문과 답변 출력
    st.text(f"질문: {question}")
    st.success(f"답변: {answer}")
    st.success(f"참고문서: {context_doc}")
    
    
    # 사용자의 질문을 히스토리에 추가
    st.session_state.chat_history.append(f"[사용자]: {question}\n")
    st.session_state.chat_history.append(f"[답변]: {answer}")
    
    # 전체 히스토리 출력
    st.text('--------------------------------------------')
    st.info("\n".join(st.session_state.chat_history))

