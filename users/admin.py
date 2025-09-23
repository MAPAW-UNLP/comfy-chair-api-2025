from django.contrib import admin

from users.models import User

# Registramos los modelos para que aparezca en el admin
admin.site.register(User)