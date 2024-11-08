from django.shortcuts import render

def main(request):
    return render(request, "htmltest/main.html")

def testpage(request):
    query = request.GET.get("query")

    results = []
    if query:
        results = ["검색 결과 예시 1", "검색 결과 예시 2", "검색 결과 예시 3"]

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "htmltest/testpage.html", context)

from django.shortcuts import render

# 😎수정부분
@app.route("/myapp/hello")
def hello0(str: ):
    data = python function 호출
    
    return data
    
    
def testpage(request):
    context = {
        'star_range': range(1, 16)  # 1부터 15까지의 범위를 템플릿에 전달
    }
    return render(request, "htmltest/testpage.html", context)
