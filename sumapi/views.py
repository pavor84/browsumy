# -*- coding: utf8 -*-

from django.http import HttpResponse

from . import apis

def index(request):
    return HttpResponse("Hello, world. You're at the index.")

def sum(request):
    method = request.GET.get("method", "lsa")
    length = request.GET["length"]
    url = request.GET["url"]

    summary, language = apis.summarize(method, length, url)
    response = HttpResponse(summary, content_type="text/plain")
    response["Content-Language"] = language
    return response
