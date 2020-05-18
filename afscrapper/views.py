from django.shortcuts import render


# Create your views here.
def homepage(request):
    return render(request, 'afscrapper/index.html')


def new_search(request):
    return render(request, 'afscrapper/new_search.html')
