# Компилятор разграничения доступа

Существенным недостатком текущей реализации модели ChRelBAC в репозитории портала ИСТИНА является сложность проверки политик прав доступа. Для этого каждая политика переводится в набор строковых SQL-запросов, и для каждой политики этот запрос хранится отдельно в репозитории. Вместо этого предлагается сделать один программный модуль, отвечающий за проверку прав доступа и не хранящий в себе никакой дополнительной информации.

Таким образом перед нами встаёт задача проверки политик с помощью всего одной булевой функции `check_permission`, без преобразований класса `policy` в какие-либо промежуточные форматы. Эта функция должна быть ёмкой, тестируемой и изменяемой. При этом компилятор политик должен каким-то образом поддерживать проверку всевозможных отношений между объектами (прямых и обратных), их фильтрацию и применение логических операций.

Всё это становится возможно благодаря `ORM` (Object Related Model) модели внутри фреймворка Django. Она предоставляет программную прослойку между базой данных проекта и исполняемым кодом. Так, например, имея следующие модели


```Python
class User(models.Model):
	user_name = models.CharField('Имя пользователя', max_length=50)
	departments_employee = models.ManyToManyField('Department', 
						   related_name='employee_of_department', 
						   blank=True)
	departments_representative = models.ManyToManyField('Department',
	                       related_name='representatives_of_department',
						   blank=True)
	is_superuser = models.BooleanField('Является админом?',
						   default=False)
	papers_of_user = models.ManyToManyField('Paper',
						   related_name='users_of_paper',
						   blank=True)


class Paper(models.Model):
	paper_name = models.CharField('Название статьи', max_length=50)
	paper_text = models.TextField('Текст статьи')
  

class Department(models.Model):
	department_name = models.CharField('Название отдела', max_length=50)
```

мы способны обращаться к базе данных проекта, чтобы производить операции `select`, `join` и другие над объектами и, например, получать записи обо всех пользователях, которые являются авторами статьи с названием "ChRelBAC":


```Python
User.objects.filter(papers_of_user__paper_name='ChRelBAC'))
```

Для доступа к подобного рода манипуляциям у каждой модели имеется свой собственный менеджер `objects`, у которого и вызываются все манипуляции с базой данных.

Получается, что для проверки наличия прав доступа между объектами `source` и `dest` нам необходимо пройтись по множеству политик доступа и для каждой из них рассмотреть цепочку зависимостей, фильтров и условий, описанных в политике. Если данная цепочка обнаружена (итоговый `join` двух таблиц содержит `source`), то `source` имеет по отношению к `dest` вид доступа, описанный в политике.

Заметим одно важное преимущество такого подхода — он очень легко расширяем на запрещающие политики. Нет никакой сложности внедрить в описание политики её вид (разрешающая или запрещающая) и блокировать доступ при удовлетворении запрещающей цепочке.

Также для удобства дальнейшей разработки будет не лишним интегрировать в проект версионирование, контроль пакетов, систему тестов и форматтер кода для поддержания стандартного стиля написания.

Теперь, когда описано общее представление об этой функции, давайте посмотрим на непосредственно реализацию компилятора и сопровождающих его модулей

