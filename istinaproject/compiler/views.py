from django.http import HttpResponse


def hello_view(request):
    return HttpResponse("This should be compiler visualization")