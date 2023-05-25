# compiler_function(some_user, "delete", some_paper, policy)

#policy = ['users', 'representative', 'paper', ['delete', 'edit', 'create']]

from dataclasses import dataclass
from enum import Enum
from collections import defaultdict as dd


class Policy_category(Enum):
    ALLOWED = 1
    PROHIBITED = 2


@dataclass
class Policy:
    def __init__(self, category=None, 
                       name=None, 
                       chain=None):
        '''
            category: Policy_category — запрещаем или разрешаем политику
            chain: (('author', 'paper'), ('topic', 'Algebra'))
        '''
        self.name = name
        self.category = category
        self.chain = chain

    def init_from_dict(self, d):
        ...

    def get_category(self):
        return self.category

    def get_name(self):
        return self.name



class Policy_manager:
    def __init__(self):
        self.allowed_policies = dict()
        self.prohibited_policies = dict()

    # пока не поддерживает алиасы
    def add_policy(self, policy):
        if policy.get_category() == Policy_category.ALLOWED:
            self.allowed_policies[policy.get_name()] = policy
        else:
            self.prohibited_policies[policy.get_name()] = policy
   

    def get_allowed_policies(self):
        # в будущем можно возвращать сразу итератор
        return self.allowed_policies.items()
        

    def get_prohibited_policies(self):
        return self.prohibited_policies.items()


def cool_str(name, obj, full=False):
    return f'[>>>] {name} ({(str(type(obj))[:40] + "...") if not full else str(type(obj))}):\n\t\t{(str(obj)[:40] + "...") if not full else obj}\n\n'


def compiler_function(source, label, dest, policies):
    ret = ""

#    user_manager = source.objects
#    eugen = user_manager.get(id=2)
    
#    paper_manager = dest.objects
#    algebra = paper_manager.get(id=3)

    # all users, created this paper
    # нам требуется объект модели, название отношения, необходимый фильтр на это отношение
    #ret += cool_str('paper', source.objects.filter(papers_of_user__paper_name='Алгебра') , True)

    allowed_policies = policies.get_allowed_policies()
    prohibited_policies = policies.get_prohibited_policies()

    for p in prohibited_policies:
        # если в итоговом объединении есть элемент source -> dest, return False
        ...

    success = True
    for p in allowed_policies:
        # если сломалось, success = False
        ...

    return success








