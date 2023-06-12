
# 👉 Django policy compiler

### What is it

Application which automatically checks whether user of some system has permission to change, view, delete etc. some object. I'm using ChRelBAC model of access in order to deploy this code to [https://istina.msu.ru](https://istina.msu.ru) repository in the future

### How to use it

First of all it's a Django project with Poetry, so start it with

```bash
poetry install
poetry python manage.py makemigrations
poetry python manage.py migrate
poetry python manage.py runserver
```

Then, you can test it with supported pytest

```bash
poetry run pytest /path/to/compiler/utils/compiler_function_test.py
```

And check your code style with

```bash
poetry run black .
```

&nbsp;

# 🎯 Coursework navigation (RU)

Раздел | Ссылка
------------- | -------------
**Введение**  | [ссылка](coursework_text/1_introduction.md)
**Модель доступа ChRelBAC**  | [ссылка](coursework_text/2_model.md)
**Компилятор разграничения доступа**  | [ссылка](coursework_text/3_compiler_theory.md)
**Практическая реализация** | [ссылка](coursework_text/4_compiler_practice.md)
**Тестирование и архитектура** | [ссылка](coursework_text/5_test_architecture.md)
**Заключение** | [ссылка](6_conclusion.md)
**Список литературы** | [ссылка](7_literature.md)
📁 **Папка со всеми файлами** | [ссылка](coursework_text)
