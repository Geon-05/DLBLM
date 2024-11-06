from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from bs4 import BeautifulSoup
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# SKT 한국어 임베딩 및 QA 모델 설정
hf_embeddings = HuggingFaceEmbeddings(
    model_name='jhgan/ko-sroberta-nli',
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

def load_Korean_wiki_docs(topic):
    url = f"https://ko.wikipedia.org/wiki/{topic}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', id='bodyContent')  # 페이지의 본문을 나타내는 ID

    # 텍스트가 있는지 확인
    if content:
        paragraphs = content.find_all('p')
        text = "\n".join([p.get_text() for p in paragraphs])
        if not text.strip():
            print("No text found in main content.")
    else:
        print("Body content div not found.")
        text = ""

    # 텍스트 내용 출력 확인
    print(f"Extracted text: {text[:500]}...")  # 텍스트 첫 500자 확인
    
    documents = [Document(page_content=text, metadata={"source": url})]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    
    print(f"Number of splits: {len(splits)}")  # Split 개수 확인
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

# 사용 예시
topic = "정년이"
splits = load_Korean_wiki_docs(topic)
if splits:
    vectorstore = create_vectorstore(splits)
else:
    print("No content to create vector store.")