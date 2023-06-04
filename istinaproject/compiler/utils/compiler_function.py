from dataclasses import dataclass
from enum import Enum
from collections import defaultdict as dd
from loguru import logger as log
import sys


class Rule_category(Enum):
    """
    Категория для правила,согласно модели ChRelBAC
    Может быть разрашающей или запрещающей
    """

    ALLOWED = 1
    PROHIBITED = 2


@dataclass
class Rule:
    def __init__(self, category=None, labels=None, name=None, chain=None):
        """
        — category: Rule_category
            НАПРИМЕР: Rule_сategory.ALLOWED

        — labels: Cписок из типов доступа, разрешаемых / запрещаемых этим правилом
            НАПРИМЕР: ['edit', 'create']

        — name: Строковое неформальное название правила
            НАПРИМЕР: "Изменение статьи её автором"

        — chain: Список из полей, последовательно соединяемых цепочкой
            ВАЖНО: Может быть как обратным отношением (согласно Django callout),
                   так и фильтром с условием. Для этого последний элемент цепочки
                   должен быть кортежем, у которого первый элемент — тип фильтра
                   (так же согласно callouts, например "gte" для >=), а второй
                   элемент — значение для фильтра. Если фильтр не применён,
                   по умолчанию цепочка заканчивается на фильтре для id конечной
                   модели, равному id переданного объекта dest
            НАПРИМЕР: ('papers_created_by_user', 'department_representative_of_paper',
                      'department_id', ('lte', 12))

        """

        self.labels = labels
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


class Policy:
    def __init__(self):
        """
        — allowed_rules: словарь, состоящий из пар название правила: правило
                         для разрешенных правил

        — prohibited_rules: то же, но для запрещенных правил
        """
        self.allowed_rules = dict()
        self.prohibited_rules = dict()

    def add_rule(self, rule):
        if rule.get_category() == Rule_category.ALLOWED:
            self.allowed_rules[rule.get_name()] = rule
        else:
            self.prohibited_rules[rule.get_name()] = rule

    def get_allowed_rules(self):
        return self.allowed_rules.values()

    def get_prohibited_rules(self):
        return self.prohibited_rules.values()


def is_chain_exist(rule, source_manager, source, dest):
    """
    Функция, проверяющая, проходит ли цепочка от source к
    dest по заданному правилу rule
    """
    complex_field_for_query = ""
    chain = rule.get_chain()

    value_of_last_field = dest.id

    for i, field in enumerate(chain):
        if i != len(chain) - 1:
            complex_field_for_query += field
            complex_field_for_query += "__"
        else:
            if isinstance(field, tuple):
                complex_field_for_query += field[0]
                value_of_last_field = field[1]
            else:
                complex_field_for_query += "id"

    log.debug(f"Complex_field = {complex_field_for_query}")
    log.debug(f"Last value = {value_of_last_field}")
    d = {complex_field_for_query: value_of_last_field}

    result_object = source_manager.filter(**d).filter(id=source.id)
    return result_object.exists()


def compiler_function(source, label, dest, policy):
    #:log.remove(0)
    logging_format = "<blue>[{level}]</blue> {message}"
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
# - поддержка псевдонимов для правил
# — использование правил внутри других правил
