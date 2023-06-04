# Практическая реализация 

Фрагменттировать, добавить не всё отсюда

```Python  
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
  
	def get_category(self):
		return self.category
	  
	def get_name(self):
		return self.name
	

class Policy_manager:
	def __init__(self):
		self.allowed_policies = dict()
		self.prohibited_policies = dict()

	def add_policy(self, policy):
		if policy.get_category() == Policy_category.ALLOWED:
			self.allowed_policies[policy.get_name()] = policy
		else:
			self.prohibited_policies[policy.get_name()] = policy
	
	def get_allowed_policies(self):
		return self.allowed_policies.items()
	
	def get_prohibited_policies(self):
		return self.prohibited_policies.items()


def cool_str(name, obj, full=False):
	return f'[>>>] {name} ({(str(type(obj))[:40] + "...") 
						   if not full 
						   else str(type(obj))}):\n\t\t{(str(obj)[:40] + "...") 
								    if not full 
								    else obj}\n\n'


def compiler_function(source, label, dest, policies, user_model):
ret = ""

user_manager = source.objects
paper_manager = dest.objects

allowed_policies = policies.get_allowed_policies()
prohibited_policies = policies.get_prohibited_policies()

user_manager = user_model.objects
print(cool_str('Результат работы', user_object.objects.filter(papers_of_user__paper_name='Алгебра')))

for p in prohibited_policies:
# если в итоговом объединении есть элемент source -> dest, return False
	...

success = True
for p in allowed_policies:
# если сломалось, success = False
	...

return success
```

ellipsis