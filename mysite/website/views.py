import subprocess
from django.shortcuts import render
import os
from django.http import FileResponse
from pathlib import Path

def index(request):

    THIS_FOLDER = Path(__file__).parent.parent.resolve()
    print(THIS_FOLDER)

    if request.method == "POST":
        artist = request.POST.get("artist")
        print(artist)
        try:
            spider_name = 'posts'
            process = subprocess.Popen(['scrapy', 'crawl', spider_name, '-a', 'artist=%s' % artist])
            process.wait()

            # download the XLSX file
            file_path = os.path.join(THIS_FOLDER, 'output.xlsx')
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{artist}.xlsx')
            return response
        except Exception as e:
                print('Error', str(e))


    return render(request, 'index.html')