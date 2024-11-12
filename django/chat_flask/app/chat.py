import requests
from bs4 import BeautifulSoup as bs
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def subject_chk(gametitle, display=5, pageno=1):
    url = f'https://www.grac.or.kr/WebService/GameSearchSvc.asmx/game?display={display}&pageno={pageno}&gametitle={gametitle}'
    
    response = requests.get(url)
    response.raise_for_status()  # 오류 발생 시 예외 처리

    # HTML 파싱 및 본문 내용 추출
    soup = bs(response.text, 'xml') 
    content = soup.find_all('item')  # item 태그들 추출
    
    documents = [Document(page_content=i.text, metadata={"source": f"doc{idx+1}", "주제": gametitle }) for idx, i in enumerate(content)]
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    
    return splits