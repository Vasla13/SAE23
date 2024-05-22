from django.contrib import admin
from .models import Ressource, UE, RessourceUE

class RessourceUEInline(admin.TabularInline):
    model = RessourceUE
    extra = 1

class RessourceAdmin(admin.ModelAdmin):
    inlines = (RessourceUEInline,)

admin.site.register(Ressource, RessourceAdmin)
admin.site.register(UE)
