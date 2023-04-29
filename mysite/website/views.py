import os
from django.shortcuts import render
from django.http import FileResponse
from pathlib import Path

from asgiref.sync import sync_to_async
from django_q.tasks import async_task, result

from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from scraperra.spiders.artistspider import PostsSpider
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

def index(request):

    THIS_FOLDER = Path(__file__).parent.parent.resolve()
    print(THIS_FOLDER)

    if request.method == "POST":
        artist = request.POST.get("artist")
        print(artist)
        try:

            ### optie 2
            configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

            crawler = CrawlerRunner(get_project_settings())
            crawler.crawl(PostsSpider, artist=artist).addBoth(lambda _: reactor.stop())

            # async_task(reactor.run())
            sync_to_async(reactor.run(), thread_sensitive=True)

            # download the XLSX file
            file_path = os.path.join(THIS_FOLDER, 'output.xlsx')
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{artist}.xlsx')

            return response
        except Exception as e:
                print('Error', str(e))


    return render(request, 'index.html')