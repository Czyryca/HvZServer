from django.http import HttpResponse


def index(request):
    response = "Hello, world! This is the new Long Game page.<br>" + \
               '<a href ="/">Return</a>'
    return HttpResponse(response)
