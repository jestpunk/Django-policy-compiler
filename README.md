
# Django policy compiler

## What is it

Application which automatically checks whether user of some system has permission to change, view, delete etc. some object. I'm using ChRelBAC model of access in order to deploy this repo to [https://istina.msu.ru](https://istina.msu.ru) in the future

## How to use it

So far it's just a regular Django project, so it uses the basic Django syntax

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```