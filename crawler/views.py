from rest_framework.views import APIView
from rest_framework.response import Response
from .crawlers import process_crawl


# Create your views here.


class CrawlerAPI(APIView):

    def post(self,request,*args,**kwargs):
        url = request.data.get('url')
        depth = request.data.get('depth')
        if not depth:
            depth = 0
        response,status = process_crawl(url,int(depth))
        return Response(data=response,status=status)

