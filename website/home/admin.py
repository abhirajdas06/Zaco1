from django.contrib import admin
from .models import Contact, Subscribers


# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone','timeStamp')
    search_fields = ['name', 'email']

admin.site.register(Contact, ContactAdmin)


admin.site.register(Subscribers)
