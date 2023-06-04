from dataclasses import dataclass
from enum import Enum
from collections import defaultdict as dd


class Policy_category(Enum):
    ALLOWED = 1
    PROHIBITED = 2


# rename to rule
@dataclass
class Policy:
    def __init__(self, category=None, 
                       labels=None,
                       name=None,
                       chain=None):
        '''
            category: Policy_category — запрещаем или разрешаем политику
            chain: ('author', 'publishers_of_paper', 'department')
        '''
        # ДОБАВИТЬ ПОДДЕРЖКУ ФИЛЬТРА (ДЛЯ ЭТОГО ПОСЛЕДНИЙ ОБЪЕКТ ДОЛЖЕН БЫТЬ КОРТЕЖОМ
        # (ОТНОШЕНИЕ, МЕТКА) ТИПА ('department_name', 'мехмат')
        #self.
       
        self.labels = labels # список типов доступа, разрешенных этой цепочкой
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
class Policy_manager:
    def __init__(self):
        self.allowed_policies = dict()
        self.prohibited_policies = dict()

    # пока не поддерживает алиасы
    def add_policy(self, policy):
        if policy.get_category() == Policy_category.ALLOWED:
            self.allowed_policies[policy.get_name()] = policy
        else:            self.prohibited_policies[policy.get_name()] = policy
   

    def get_allowed_policies(self):
        # в будущем можно возвращать сразу итератор
        return self.allowed_policies.values()
        

    def get_prohibited_policies(self):
        return self.prohibited_policies.values()


def is_chain_exist(policy, source_manager, source, dest):
    complex_field_for_query = ""
    chain = policy.get_chain() 

    for i, field in enumerate(chain):
        complex_field_for_query += field
        if i != len(chain) - 1:
            complex_field_for_query += '__'
    
    # СЮДА МОЖНО ДОБАВИТЬ БОЛЕЕ СЛОЖНЫЕ УСЛОВИЯ
    complex_field_for_query += '__id' 

    d = {complex_field_for_query: dest.id}
    
    # Не буду обрабатывать исключение, лучше добавить прогонку тестов для него в CICD
    result_object = source_manager.filter(**d).filter(id=source.id)

    return result_object.exists()


def compiler_function(source, label, dest, policies):
    
    source_manager = type(source).objects
    dest_manager = type(dest).objects

    allowed_policies = policies.get_allowed_policies()
    prohibited_policies = policies.get_prohibited_policies()

    for p in prohibited_policies:
        #print('[i] Started prohibited policies')
        if label not in p.get_labels():
            continue
        
        if is_chain_exist(p, source_manager, source, dest):
            return False

    for p in allowed_policies:
        #print("[i] Started allowed policies")
        
        if label not in p.get_labels():
            continue

        if is_chain_exist(p, source_manager, source, dest):
            return True
        
    # didn't find any good policy
    return False


# ADDONS
# - по пользователю и типу получить все доступные объекты
# - по объекту получить всех пользователей
