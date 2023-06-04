import pytest

from .compiler_function import compiler_function, Rule, Policy, Rule_category

from django.core.exceptions import FieldError
from ..models import User, Paper, Department
from .conftest import django_db_setup


@pytest.mark.django_db
def test_empty_source(django_db_setup):
    source = User.objects.get(user_name="Пустой")
    dest = Department.objects.get(department_name="Мехмат")

    r = Rule(
        Rule_category.ALLOWED,
        ["edit", "create"],
        "person to department, which is representative for his paper",
        ("papers_of_user", "Paper_for_representative_department"),
    )

    p = Policy()
    p.add_rule(r)

    result = True
    result = compiler_function(source, "edit", dest, p)
    # print(result)

    assert result == False


@pytest.mark.django_db
def test_full_source(django_db_setup):
    source = User.objects.get(user_name="Полный")
    dest = Department.objects.get(department_name="Мехмат")

    r = Rule(
        Rule_category.ALLOWED,
        ["edit", "create"],
        "person to department, which is representative for his paper",
        ("papers_of_user", "Paper_for_representative_department"),
    )

    p = Policy()
    p.add_rule(r)

    result = True
    result = compiler_function(source, "edit", dest, p)
    # print(result)

    assert result == True


@pytest.mark.django_db
def test_wrong_field(django_db_setup):
    source = User.objects.get(user_name="Полный")
    dest = Department.objects.get(department_name="Мехмат")
    
    r = Rule(
        Rule_category.ALLOWED,
        ["edit", "create"],
        "person to department, which is representative for his paper",
        ("BLABLABLA", "BLABLABLA"),
    )

    p = Policy()
    p.add_rule(r)

    result = True
    with pytest.raises(FieldError):
        result = compiler_function(source, "edit", dest, p)
    # print(result)

  # assert result == True


