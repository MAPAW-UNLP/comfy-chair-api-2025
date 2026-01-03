
# Inicialización y Reinicialización de la Base de Datos

Este documento explica cómo **borrar la base de datos**, **eliminar migraciones**, y **cargar datos desde un archivo JSON** para inicializar correctamente tu entorno Django.

---

## 🗑️ 1. Cómo borrar la base de datos

Si estás usando **SQLite (db.sqlite3)**:

```bash
rm db.sqlite3
```

---

## 🧹 2. Cómo borrar todas las migraciones

Ejecutá estos comandos dentro del proyecto:

```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
```

Esto elimina todos los archivos de migración excepto los `__init__.py`.

---

## 🔄 3. Cómo volver a crear las migraciones y aplicar cambios

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📥 4. Cómo cargar datos desde un archivo JSON (fixtures)

El `initial_data.json` se encunetra en la carpeta fixture, podés cargarlo así:

Verificar estar ubicado en: MAPAW/comfy-chair-api-2025 

```bash
python manage.py loaddata fixtures/initial_data.json
```

Esto poblará la base de datos con los datos definidos en el JSON.



## 📌 Nota importante

Asegurate de que tu JSON esté ubicado en una carpeta accesible para Django (generalmente dentro de `fixtures/` o en la misma carpeta donde ejecutás el comando).

---

¡Listo! Con esto vas a poder reiniciar tu base de datos y cargar datos sin problemas.
