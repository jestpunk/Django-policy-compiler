from django.shortcuts import render
from django.http import HttpResponse

def compiler_view(request):
    return HttpResponse("compiler view")
    #return render(request, '')