import os
import google.generativeai as genai
import json
import streamlit as st
# DeprecationWarning에 따라 langchain_community 및 langchain_huggingface로 임포트 경로 수정
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup as bs
import requests
from transformers import pipeline

# 파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
target_file_path = os.path.join(current_dir, '../data/APIkey.json')

# 파일 읽기
with open(target_file_path, 'r') as file:
    data = json.load(file)  # JSON 파일을 파이썬 딕셔너리로 로드

# API 키 설정
api_key = data['Gemini']
genai.configure(api_key=api_key)

os.environ["HUGGINGFACEHUB_API_TOKEN"] = data['Huggingface']
os.environ.get("HUGGINGFACEHUB_API_TOKEN")


# 모델 로드 함수
def load_model():
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Model loaded...")
    return model


# Streamlit 세션에서 모델을 한 번만 로드하도록 설정
if "model" not in st.session_state:
    with st.spinner("모델로딩중"):
        st.session_state.model = load_model()
    

# DB 및 모델 추가 부분 😤 --------------------------------------------------
# 모델 생성부
# SKT 한국어 임베딩 및 QA 모델 설정
if "embedding" not in st.session_state:
    with st.spinner("임베딩 로딩중"):
        hf_embeddings = HuggingFaceEmbeddings(
            model_name='jhgan/ko-sroberta-nli',
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    st.session_state.embedding = hf_embeddings

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
        # print(f'idx : {idx}')
        # print('-'*50)
        # print(f'content : {i}')
        # title = i.find('gametitle')  # gametitle 태그 추출
        if i:
            # print(f'gametitle : {i.text}')
            paragraphs.append(i.text)
    
    # 텍스트 변환 및 Document 객체로 변환    
    documents = [Document(page_content=doc, metadata={"source": f"doc{i+1}"}) for i, doc in enumerate(paragraphs)]
    # text = "\n".join(paragraphs)    
    # documents = [Document(page_content=text, metadata={"source": url})]
    
    # 텍스트 스플릿
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    return splits

def create_vectorstore(splits):
    valid_splits = []
    for i, split in enumerate(splits):
        print(f"Processing split {i+1}/{len(splits)}: {split.page_content[:30]}...")  # 첫 30자 출력
        
        # 임베딩 생성 과정 확인
        embedding = st.session_state.embedding.embed_query(split.page_content)
        
        # 임베딩이 올바르게 생성되었는지 길이와 형태 출력
        if embedding and len(embedding) > 0:
            print(f"Embedding created for split {i+1}, length: {len(embedding)}")
            valid_splits.append(split)
        else:
            print(f"Empty embedding for split {i+1}")

    if valid_splits:
        vectorstore = Chroma.from_documents(documents=valid_splits, embedding=st.session_state.embedding )
        return vectorstore
    else:
        raise ValueError("No valid documents with embeddings to add to vector store.")
from langchain_community.vectorstores import Chroma

# KoAlpaca 모델 로드
# qa_pipeline = pipeline(
#     "text2text-generation",
#     model="beomi/KoAlpaca-Polyglot-5.8B",
#     tokenizer="beomi/KoAlpaca-Polyglot-5.8B"
# )
# qa_pipeline = pipeline(
#     "text-generation",
#     model="beomi/KoAlpaca-Polyglot-5.8B",
#     tokenizer="beomi/KoAlpaca-Polyglot-5.8B"
# )
# qa_pipeline = pipeline(
#     "text-generation",  # 또는 "text2text-generation" 태스크
#     model="t5-small",
#     tokenizer="t5-small"
# )

# T5 기반 모델 사용 예시
if "qa_pipeline" not in st.session_state:    
    qa_pipeline = pipeline(
        "text2text-generation",
        model="t5-small",
        tokenizer="t5-small"
    )
    st.session_state.qa_pipeline = qa_pipeline
    
# ---------------------------모델생성부종료---------------------------

# 세션의 대화 히스토리 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 사용자 입력과 버튼 처리
topic = st.text_input('게임명을 입력하세요.')
question = st.text_input('질문을 입력하세요.')
if st.button('질문') and question:
    # 사용자 입력부
    splits = load_Korean_game(topic)
    # 사용자의 질문을 히스토리에 추가
    st.session_state.chat_history.append(f"[사용자]: {question}")
    st.text(f'[사용자]\n{question}')
    
    if splits:
        st.session_state.vectorstore = create_vectorstore(splits)
    else:
        print("No content to create vector store.")
        
        
    from transformers import pipeline
    
    # context 구성
    # context = " ".join([split.page_content for split in splits])
    
    
    context_doc = st.session_state.vectorstore.similarity_search(question, k=4)
    # context = context_doc[0].page_content if context_doc else "정보를 찾을 수 없습니다."
    # context = ' '.join([doc.page_conent for doc in context_docs])
    
    prompt = f"Context: {context_doc}\nQuestion: {question}\nAnswer in a complete sentence:"
    # response = gemini_model(prompt)
    
    response = st.session_state.model.generate_content(prompt)
    answer = response.candidates[0].content.parts[0].text
    
    # # 모델 응답 생성
    # response = st.session_state.model.generate_content(user_querie)
    # model_response = response.candidates[0].content.parts[0].text
    # st.text(f'[모델]\n{model_response}')
    
    # # 모델 응답을 히스토리에 추가 😤 히스토리 내용을 기억하지 못함
    # st.session_state.chat_history.append(f"[모델]: {model_response}")
    
    # context와 question을 하나의 문자열로 합쳐서 전달
    # input_text = f"{context}\n\n질문: {question}"
    # result = st.session_state.qa_pipeline(input_text, max_new_tokens=100)

    # 질문과 답변만 출력
    st.text(f"질문: {question}")
    st.text(f"답변: {answer}")
    # st.text(f"답변: {result[0]['generated_text']}")
    
    # 전체 히스토리 출력
    st.text('--------------------------------------------')
    st.text("\n".join(st.session_state.chat_history))
