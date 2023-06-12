# Тестирование, логирование, архитектура проекта

### Общая структура

Данный проект, как было неоднократно описано выше, написан на Django. Токен подключается к проекту с помощью переменной окружения для повышения безопасности. Внутри Django проекта реализовано два приложения — `compiler` и `homepage`. Приложение `homepage` несёт тривиальный и служебный характер — обслуживание стартовой страницы, по которой осуществляется навигация между приложением администратора и приложением компилятора (внутри которого вызывается функция `compiler_function`).

```
homepage
├── __init__.py
├── __pycache__
├── admin.py
├── apps.py
├── models.py
├── templates
│   └── homepage
│       └── homepage.html
├── tests.py
├── urls.py
└── views.py
```
*структура приложения `homepage`*

Всё наукоёмкое содержание, относящееся непосредственно к компилятору политик, сосредоточено в приложении `compiler`. А именно папка `utils`, внутри которой находятся два достойных упоминания — `compiler_function.py` и `compiler_function_test.py`.

Во втором находятся фикстуры и тесты, написанные с помощью библиотеки pytest. В первом файле содержатся все функции и структуры, описанные в главе "Практическая реализация". Вызывается функция при переходе на подстраницу `/compiler` проекта, то есть вызов функции `compiler_function` реализована внутри файла `views.py` приложения

```
compiler
├── __init__.py
├── __pycache__
├── admin.py
├── apps.py
├── models.py
├── templates
│   └── compiler
├── tests.py
├── urls.py
├── utils
│   ├── __init__.py
│   ├── __pycache__
│   ├── compiler_function.py
│   ├── compiler_function_test.py
│   └── conftest.py
└── views.py
```
*структура приложения `compiler_function`*

&nbsp;

### Тестирование

Система тестирования проекта реализована с помощью библиотеки `pytest`. Внутри содержатся "happy path" тесты, крайние случаи в виде попытки доступа к несуществующим полям базы проекта. 

```Python
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
```
*фикстура корректной политики*

&nbsp;

### Логирование

Масштабируемость проекта должна быть обеспечена не только тестами. Также довольно важную роль в расширяемости проекта занимают логи. Среди великого разнообразия средств логирования мой выбор пал на `loguru`. Эта система обладает невероятно простым интерфейсом взаимодействия, что кажется важным для системы логирования — код остаётся читаемый и функциональным.

```Python
allowed_rules = policy.get_allowed_rules()
prohibited_rules = policy.get_prohibited_rules()

log.trace("Started prohibited policies") #logging
for r in prohibited_rules:
	if label not in r.get_labels():
		continue
```

*фрагмент функции `compiler_function`, использующий логирование*