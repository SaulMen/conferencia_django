### **CONFERENCIA**

____

## **Pasos para la instalación**

[Django Instalación](https://docs.djangoproject.com/en/5.2/topics/install/#installing-official-release)

```cmd
py -m pip install Django
```

Revisar que se haya instalado Django

```cmd
python -m django --version
```

ó por medio de python

```cmd
import django

print(django.get_version())
```

Pasos para crear un proyecto de Django

1. Crear una carpeta donde estará nuestro proyecto
```cmd
mkdir proyecto-django
```

2. Crear el proyecto
```cmd
django-admin startproject ProyectoDjango ../conferencia
```

3. Corremos el server
```cmd
python manage.py runserver
```
