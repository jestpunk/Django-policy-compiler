from django.shortcuts import render
from django.http import HttpResponse
from . import models
from .utils.compiler_function import compiler_function, policy

def compiler_view(request):
    compiler_function(models.User, 2, models.Paper, policy)

    return HttpResponse("compiler view")
    #return render(request, '')