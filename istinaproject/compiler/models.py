from django.db import models


class User(models.Model):
    user_name = models.CharField('Имя пользователя', 
                                 max_length=50)
    departments_employee =       models.ManyToManyField('Department', 
                                                        related_name='employee_of_department', 
                                                        #hidden=False,
                                                        blank=True)
    departments_representative = models.ManyToManyField('Department', 
                                                        related_name='representatives_of_department', 
                                                        #hidden=False,
                                                        blank=True)
    is_superuser = models.BooleanField('Является админом?', 
                                       default=False)
    papers_of_user = models.ManyToManyField('Paper', 
                                            related_name='users_of_paper',
                                            #hidden=False,
                                            blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return (f'[USER]' + ('[SU]' if self.is_superuser else '') + 
                f' {self.user_name}')


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