from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    response = "Hello, world! The new HvZ server will be here soon. <br>" + \
               '<a href ="/LongGame/">Long Games</a>'
    return HttpResponse(response)

