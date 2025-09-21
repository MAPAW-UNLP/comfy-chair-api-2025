from django.contrib import admin

from chairs.models import Bidding, AsignacionRevisor, Revision

# Registramos los modelos para que aparezca en el admin
admin.site.register(Bidding)
admin.site.register(AsignacionRevisor)
admin.site.register(Revision)   