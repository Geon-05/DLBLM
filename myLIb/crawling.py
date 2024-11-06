from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import requests
from langchain.schema import Document
from bs4 import BeautifulSoup

# 검색부
def load_Korean_game(gametitle, display=5, pageno=1):
    # display : 한번에 출력하는 게임물 건 수 (최대:1000) // 필수
    # pageno : 검색 페이지 번호. 검색결과 페이지 당 display건의 데이터가 전송되며 display건 이상의 데이터가 존재할 경우 해당 페이지 번호를 전송해야 함. 없을 경우에는 1로 전송함 // 필수
    # gametitle : 검색하고자 하는 게임물명 // 선택
    url = f'https://www.grac.or.kr/WebService/GameSearchSvc.asmx/game?display={display}&pageno={pageno}&gametitle={gametitle}'
    
    response = requests.get(url)
    response.raise_for_status()  # raise Exception when error occurs

    # HTML parsing and extract body contents
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.findAll('item')  # 페이지의 본문을 나타내는 ID
    
    print(content)
    
    # Extract contents
    paragraphs = content.find_all('p')
    text = "\n".join([p.get_text() for p in paragraphs])  # concat all context in <p> tags 
 
    # convert to Document object (required for LangChain)
    documents = [Document(page_content=text, metadata={"source": url})]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    return splits

load_Korean_game('화이트데이')



display = 1000 # 한번에 출력하는 게임물 건 수 (최대:1000) // 필수
pageno = 1 # 검색 페이지 번호. 검색결과 페이지 당 display건의 데이터가 전송되며 display건 이상의 데이터가 존재할 경우 해당 페이지 번호를 전송해야 함. 없을 경우에는 1로 전송함 // 필수
gametitle = '화이트데이' # 검색하고자 하는 게임물명 // 선택

url = f'https://www.grac.or.kr/WebService/GameSearchSvc.asmx/game?display={display}&pageno={pageno}&gametitle={gametitle}'


# 임배딩
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

persist_directory = "./new_chroma_db"

vectorstore = Chroma.from_documents(docs, embedding=embedding_model, persist_directory="./chroma_db")