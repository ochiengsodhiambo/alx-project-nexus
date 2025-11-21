from django.contrib import admin

# Register your models here.
from .models import User, Buyer, Seller

admin.site.register(User)
admin.site.register(Buyer)
admin.site.register(Seller)
