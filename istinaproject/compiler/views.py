from django.shortcuts import render
from django.http import HttpResponse
from . import models
from .utils.compiler_function import compiler_function, Rule_category, Policy, Rule


def compiler_view(request):
    source = models.User.objects.get(user_name="Марат")
    dest = models.Department.objects.get(department_name="Мехмат")

    r = Rule(
        Rule_category.ALLOWED,
        ["edit", "create"],
        "person to department, which represntative for his paper",
        (("papers_of_user", "Paper_for_representative_department")),
    )

    p = Policy()
    p.add_rule(r)

    result = compiler_function(source, "edit", dest, p)
    print(result)

    return HttpResponse("COMPILER")
