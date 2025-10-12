from django.contrib import admin

from chairs.models import Bid, ReviewAssignment, Review

# Registramos los modelos para que aparezca en el admin
admin.site.register(Bid)
admin.site.register(ReviewAssignment)
admin.site.register(Review)   