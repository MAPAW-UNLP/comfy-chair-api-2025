from django.contrib import admin

from chairs.models import Bidding, AssignmentReview, Review

# Registramos los modelos para que aparezca en el admin
admin.site.register(Bidding)
admin.site.register(AssignmentReview)
admin.site.register(Review)   