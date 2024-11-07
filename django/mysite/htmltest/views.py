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
