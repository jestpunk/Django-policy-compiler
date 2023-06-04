import pytest

from .compiler_function import compiler_function, Rule, Policy, Rule_category

from django.core.exceptions import FieldError
from ..models import User, Paper, Department
from .conftest import django_db_setup


@pytest.fixture
def good_policy():
    r = Rule(
        Rule_category.ALLOWED,
        ["edit", "create"],
        "person to department, which is representative for his paper",
        ("papers_of_user", "paper_for_representative_department"),
    )

    p = Policy()
    p.add_rule(r)
    return p


@pytest.fixture
def bad_policy():
    r = Rule(
        Rule_category.ALLOWED,
        ["edit", "create"],
        "it shouldn't work",
        ("BLABLABLA", "BLABLABLABLABLABLA", "BLABLA"),
    )

    p = Policy()
    p.add_rule(r)
    return p


@pytest.mark.django_db
def test_empty_source(django_db_setup, good_policy):
    source = User.objects.get(user_name="Пустой")
    dest = Department.objects.get(department_name="Мехмат")

    result = True
    result = compiler_function(source, "edit", dest, good_policy)

    assert result == False


@pytest.mark.django_db
def test_full_source(django_db_setup, good_policy):
    source = User.objects.get(user_name="Полный")
    dest = Department.objects.get(department_name="Мехмат")

    result = True
    result = compiler_function(source, "edit", dest, good_policy)

    assert result == True


@pytest.mark.django_db
def test_wrong_field(django_db_setup, bad_policy):
    source = User.objects.get(user_name="Полный")
    dest = Department.objects.get(department_name="Мехмат")

    result = True
    with pytest.raises(FieldError):
        result = compiler_function(source, "edit", dest, bad_policy)
