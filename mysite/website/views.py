import subprocess
from django.shortcuts import render
import os
from django.http import FileResponse
from pathlib import Path

def index(request):

    THIS_FOLDER = Path(__file__).parent.resolve()

    if request.method == "POST":
        name = request.POST.get("name")
        print(name)

    return render(request, 'index.html')