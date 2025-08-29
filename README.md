# Comfy Chair API

Este repositorio contiene el frontend del proyecto 2025 de la materia Métodos Ágiles para Aplicaciones Web (MAPAW) de la Facultad de Informatica, UNLP.

## Tecnologías
- [Python 3.12](https://www.python.org/) (Revisar otras versiones).
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## Instalación
1. Clonar el repositorio y entrar al directorio del proyecto.
2. Crear y activar un entorno virtual. Importante para tener un entorno de python aislado, sobre todo cuando se trabaja con múltiples versiones de python.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Aplicar las migraciones:
   ```bash
   python manage.py migrate
   ```
5. Ejecutar el servidor:
   ```bash
   python manage.py runserver
   ```
6. Probar endpoint de ejemplo en: [http://localhost:8000/dummy/test/](http://localhost:8000/dummy/test/)

## Base de datos
Por defecto Django utiliza [SQLite](https://www.sqlite.org/). Es muy útil para desarrollar ya que toda la base de datos se almacena en un solo archivo.  
