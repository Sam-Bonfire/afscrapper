import requests
from requests.utils import requote_uri
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_URL_AMAZON = 'https://www.amazon.in/s?k='
BASE_URL_FLIPKART = 'https://www.flipkart.com/search?q='
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
           "Connection": "close", "Upgrade-Insecure-Requests": "1"
           }
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}


# Create your views here.
def homepage(request):
    return render(request, 'afscraper/index.html')


def new_search(request):
    search = request.POST.get("search-term")
    models.Search.objects.create(search=search)
    response_amazon = requests.get(BASE_URL_AMAZON + requote_uri(search), headers=headers)
    amazon_soup = BeautifulSoup(response_amazon.content, features='html.parser')
    final_posting = []
    for item in amazon_soup.findAll('div', attrs={
        'class': 'sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28'}):
        name = item.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
        image_link = None
        link = item.find('a', attrs={'class': 'a-link-normal a-text-normal'})
        price = item.find('span', attrs={'class': 'a-offscreen'})

        product = []
        if name is not None:  # product.0
            product.append(name.text)
            image_link = amazon_soup.find('img', {'alt': name.text})
        else:
            product.append("Unknown Product")

        if image_link is not None:  # product.1
            product.append(image_link['src'])
        else:
            product.append(
                'https://www.chillinoodle.co.uk/skin/frontend/chillinoodle/default/images/catalog/product/placeholder/image.jpg')

        if link is not None:  # product.2
            product.append('https://amazon.in/'+link['href'])
        else:
            product.append('amazon.in')

        if price is not None:  # product.3
            product.append(price.text)
        else:
            product.append('NA')
        final_posting.append(product)
    frontend_package = {'search_term': search, 'final_posting': final_posting[1:]}
    return render(request, 'afscraper/new_search.html', frontend_package)
