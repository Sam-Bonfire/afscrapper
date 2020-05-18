import requests
from django.shortcuts import render
from bs4 import BeautifulSoup


# Create your views here.
def homepage(request):
    return render(request, 'afscrapper/index.html')


def new_search(request):
    search = request.POST.get("search-term")
    search_term = {'search_term': search}
    return render(request, 'afscrapper/new_search.html', search_term)
