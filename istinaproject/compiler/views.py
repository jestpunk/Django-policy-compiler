from django.shortcuts import render
from django.http import HttpResponse
from . import models
from .utils.compiler_function import compiler_function, Policy_category, Policy, Policy_manager
#from .utils import compiler_function
#import .utils.compiler_function


def compiler_view(request):
    source = models.User.objects.get(id=2)
    dest = models.Paper.objects.get(id=3)

    # ДОРАБОТАТЬ ИНИЦИАЛИЗАЦИЮ ПОЛИТИК ДОСТУПА
    p = Policy(Policy_category.ALLOWED, 'edit', 
              (('papers_of_user', 'paper')))

    pm = Policy_manager()
    pm.add_policy(p)

    result = compiler_function(source, "edit", dest, pm)
    print(result)
    
    return HttpResponse('COMPILER')
    #return render(request, '')
