from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
# from langchain.docstore.document import Document
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup as bs
import requests
import os

# SKT 한국어 임베딩 및 QA 모델 설정
hf_embeddings = HuggingFaceEmbeddings(
    model_name='jhgan/ko-sroberta-nli',
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

os.environ["HUGGINGFACEHUB_API_TOKEN"] = ""

os.environ.get("HUGGINGFACEHUB_API_TOKEN")


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
    text = "\n".join(paragraphs)
    documents = [Document(page_content=text, metadata={"source": url})]
    
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
        embedding = hf_embeddings.embed_query(split.page_content)
        
        # 임베딩이 올바르게 생성되었는지 길이와 형태 출력
        if embedding and len(embedding) > 0:
            print(f"Embedding created for split {i+1}, length: {len(embedding)}")
            valid_splits.append(split)
        else:
            print(f"Empty embedding for split {i+1}")

    if valid_splits:
        vectorstore = Chroma.from_documents(documents=valid_splits, embedding=hf_embeddings)
        return vectorstore
    else:
        raise ValueError("No valid documents with embeddings to add to vector store.")
from langchain_community.vectorstores import Chroma

# 사용 예시
topic = '화이트데이'
splits = load_Korean_game(topic)
if splits:
    vectorstore = create_vectorstore(splits)
else:
    print("No content to create vector store.")
from transformers import pipeline

# KoAlpaca 모델 로드
qa_pipeline = pipeline(
    "text2text-generation",
    model="beomi/KoAlpaca-Polyglot-5.8B",
    tokenizer="beomi/KoAlpaca-Polyglot-5.8B"
)
# context 구성
context = " ".join([split.page_content for split in splits])

# 질문 설정
question = "화이트데이 스토리 알려줘"

# context와 question을 하나의 문자열로 합쳐서 전달
input_text = f"{context}\n\n질문: {question}"
result = qa_pipeline(input_text, max_new_tokens=100)

# 질문과 답변만 출력
print("질문:", question)
print("답변:", result[0]['generated_text'])