from dataclasses import dataclass
from enum import Enum
from collections import defaultdict as dd
from loguru import logger as log
import sys


class Rule_category(Enum):
    ALLOWED = 1
    PROHIBITED = 2


# rename to rule
@dataclass
class Rule:
    def __init__(self, category=None, labels=None, name=None, chain=None):
        """
        category: Rule_category — запрещаем или разрешаем правило
        chain: ('author', 'publishers_of_paper', 'department')
        """
        # ДОБАВИТЬ ПОДДЕРЖКУ ФИЛЬТРА (ДЛЯ ЭТОГО ПОСЛЕДНИЙ ОБЪЕКТ ДОЛЖЕН БЫТЬ КОРТЕЖОМ
        # (ОТНОШЕНИЕ, МЕТКА) ТИПА ('department_name', 'мехмат')
        # self.

        self.labels = labels  # список типов доступа, разрешенных этой цепочкой
        self.name = name
        self.category = category
        self.chain = chain

    def init_from_dict(self, d):
        ...

    def get_category(self):
        return self.category

    def get_name(self):
        return self.name

    def get_labels(self):
        return self.labels

    def get_chain(self):
        return self.chain

    def __str__(self):
        return self.name


# rename to Policy
class Policy:
    def __init__(self):
        # dict for faster looking for names in future
        self.allowed_rules = dict()
        self.prohibited_rules = dict()

    # пока не поддерживает алиасы
    def add_rule(self, rule):
        if rule.get_category() == Rule_category.ALLOWED:
            self.allowed_rules[rule.get_name()] = rule
        else:
            self.prohibited_rules[rule.get_name()] = rule

    def get_allowed_rules(self):
        # в будущем можно возвращать сразу итератор
        return self.allowed_rules.values()

    def get_prohibited_rules(self):
        return self.prohibited_rules.values()


def is_chain_exist(rule, source_manager, source, dest):
    complex_field_for_query = ""
    chain = rule.get_chain()

    for i, field in enumerate(chain):
        complex_field_for_query += field
        if i != len(chain) - 1:
            complex_field_for_query += "__"

    # СЮДА МОЖНО ДОБАВИТЬ БОЛЕЕ СЛОЖНЫЕ УСЛОВИЯ
    complex_field_for_query += "__id"

    d = {complex_field_for_query: dest.id}

    # Не буду обрабатывать исключение, лучше добавить прогонку тестов для него в CICD
    result_object = source_manager.filter(**d).filter(id=source.id)

    return result_object.exists()


def compiler_function(source, label, dest, policy):
    #:log.remove(0)
    logging_format = "<green>[{level}]</green> {message}"
    log.add(sys.stderr, level="TRACE", format=logging_format)

    source_manager = type(source).objects
    dest_manager = type(dest).objects

    allowed_rules = policy.get_allowed_rules()
    prohibited_rules = policy.get_prohibited_rules()

    log.trace("Started prohibited policies")
    for r in prohibited_rules:
        if label not in r.get_labels():
            continue

        if is_chain_exist(r, source_manager, source, dest):
            return False

    log.trace("Started allowed policies")
    for r in allowed_rules:
        if label not in r.get_labels():
            continue

        if is_chain_exist(r, source_manager, source, dest):
            return True

    # didn't find any good policy
    return False


# ADDONS
# - по пользователю и типу получить все доступные объекты
# - по объекту получить всех пользователей
