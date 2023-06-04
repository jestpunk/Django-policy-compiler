from django.shortcuts import render
from django.http import HttpResponse
from . import models
from .utils.compiler_function import compiler_function, Policy_category, Policy, Policy_manager
#from .utils import compiler_function
#import .utils.compiler_function


def compiler_view(request):
    source = models.User.objects.get(user_name='Марат')
    dest = models.Department.objects.get(department_name='Мехмат')

    # ДОРАБОТАТЬ ИНИЦИАЛИЗАЦИЮ ПОЛИТИК ДОСТУПА
    p = Policy(Policy_category.ALLOWED, ['edit', 'create'], 
            'person to department, which represntative for his paper', 
            (('papers_of_user', 'Paper_for_representative_department')))

    pm = Policy_manager()
    pm.add_policy(p)
    
    result = compiler_function(source, "edit", dest, pm) 
    print(result) 
#    print(result)
    
    return HttpResponse('COMPILER')
    #return render(request, '')
