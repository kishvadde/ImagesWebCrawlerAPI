from bs4 import BeautifulSoup as BS
import requests
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_400_BAD_REQUEST)

images = {}
pending = []
visited = {}


def get_domain_name(url):

    domain = None
    protocal = 'http://'
    arr = url.split(protocal)
    if not len(arr) > 1:
        protocal = 'https://'
        arr = url.split(protocal)
    if len(arr) > 1:
        domain = protocal + arr[1].split('/')[0]

    return domain


def is_includes_domain_name(url):

    if 'http' in url or 'https' in url:
        return True
    return False




def crawl(pending,visited,images):

    error = None

    try:
        while pending:
            url,depth = pending.pop(0)
            visited[url] = True
            img_tags = []
            url_tags = []
            domain_name = get_domain_name(url)
            try:
                response = requests.get(url)
                if response.status_code == HTTP_200_OK:
                    soup = BS(response.content, 'html.parser')
                    img_tags = soup.findAll('img')
                    url_tags = soup.findAll('a', href=True)
            except Exception as e:
                print(e)

            if img_tags:
                images[url] = []
                for img in img_tags:
                    src = img.get('src')
                    if src:
                        if not is_includes_domain_name(src):
                            src = domain_name + src
                        images[url].append(src)

            if depth > 0 and url_tags:
                for url_tg in url_tags:
                    href = url_tg.get('href')
                    if href and not '#' in href:
                        if not is_includes_domain_name(href):
                            href = domain_name + href
                        if not visited.get(href):
                            pending.append((href,depth-1))
    except Exception as e:
        error = e.__str__()

    return error


def process_crawl(url,depth):
    visited = {}
    images = {}
    pending = [(url,depth)]
    status = HTTP_200_OK
    error = crawl(pending,visited,images)
    if not images:
        status = HTTP_404_NOT_FOUND
    if error:
        status = HTTP_400_BAD_REQUEST

    return images,status



