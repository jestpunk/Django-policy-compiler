from django.db import models


class User(models.Model):
    user_name = models.CharField('Имя пользователя', max_length=50)
    user_department = models.ForeignKey('Department', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'[USER] {self.user_name} (dep: {self.user_department})'


class Paper(models.Model):
    paper_name = models.CharField('Название статьи', max_length=50)
    paper_text = models.TextField('Текст статьи')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'[PAPER]: {self.paper_name}'

class Department(models.Model):
    department_name = models.CharField('Название отдела', max_length=50)


    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return f'[DEPARTMENT] {self.department_name}'