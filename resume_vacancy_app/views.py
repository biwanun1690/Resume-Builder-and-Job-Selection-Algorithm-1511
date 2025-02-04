import datetime

from django.contrib.auth import logout
from django.shortcuts import render, redirect

#from resume_vacancy_app.forms import
#from resume_vacancy_app.models import

from django.contrib.auth.decorators import login_required


def index_page(request):
    context = {
        "text": "В процессе разработки :)"
    }
    return render(request, "index.html", context)

