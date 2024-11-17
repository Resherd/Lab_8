from django.contrib import admin
from .models import Medicine, Supplier, Deliveries

admin.site.register(Medicine)
admin.site.register(Supplier)
admin.site.register(Deliveries)
