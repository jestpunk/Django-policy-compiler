from django.shortcuts import render
from django.http import HttpResponse

def homepage_view(request):
    #return HttpResponse("homepage view")
    return render(request, 'homepage/homepage.html')