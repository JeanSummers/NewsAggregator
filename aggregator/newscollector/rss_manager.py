from django.http import HttpResponse


def getJSON(request):
    return HttpResponse("'data':None", content_type="application/json")
